import re

import GermanWiktionaryService
from T0_TranscriptionProcessorsController import T0_TranscriptionProcessorsController
from Tokenizer import Tokenizer
from GermanExcelWorkbooksDao import GermanExcelWorkbooksDao
from GermanTimeTranscribableMaker import GermanTimeTranscribableMaker

TRANSCRIPTION_NOT_FOUND = '???'


# Движок транскрибирования предложений.
# Данный класс занимается транскрибированием именно отдельного предложения, а значит такое предложение должно быть
# заранее выделено из какого-либо текста / диалога и передано сюда для транскрибирования.
# Если возникает необходимость транскрибирования сразу нескольких предложений или целого текста, нужно обращаться к
# другим специализированным классам-обёрткам (GermanPopovTextTranscriber, GermanTableCellTextTranscriber).
class GermanSentenceTranscriber:
    def __init__(self):
        self.germanExcelWorkbooksDao = GermanExcelWorkbooksDao()
        self.excel_word_transcription_dict = self.germanExcelWorkbooksDao.get_data_as_dict()
        self.germanTimeTranscribableMaker = GermanTimeTranscribableMaker()
        self.tokenizer = Tokenizer()
        self.t0_TranscriptionProcessorsController = T0_TranscriptionProcessorsController()

        # Глобальный список, который должен инициализироваться заново при каждом вызове метода для очистки результатов
        # предыдущего вызова метода.
        self.sentence_unknown_words = None

    # TODO: сделать работу с флагом более явной и в вызывающем коде, и на UI
    def transcribe_sentence(self, sentence, should_lookup_unknown_word_transcription_in_wiktionary=False):

        if '\n' in sentence:
            raise Exception('Sentence contains newline character.'
                            ' Consider other classes (e.g. GermanPopovTextTranscriber or GermanTableCellTextTranscriber)'
                            ' to transcribe this text.')

        self.sentence_unknown_words = []

        sentence = self._preprocess_before_transcribing(sentence)

        # Для транскрибации предложений 'So, das war’s!' / 'So, das wär’s!' важно, чтобы флаг strip_apostrophe=False
        if re.search(r"w[aä]r’s", sentence):
            strip_apostrophe = False
        else:
            strip_apostrophe = True
        words = self.tokenizer.tokenize(sentence, True, strip_apostrophe)

        # Не нужно слова немецкого предложения приводить к нижнему регистру! Среди них могут быть существительные,
        # которые, будучи написанными с маленькой буквы, не смогут быть найденными в Wiktionary.
        # Лучше пожертвовать самым первым словом предложения, которое будет написано с большой буквы (и поэтому его
        # транскрипция может быть не найдена или окажется неправильной), чем всеми остальными существительными
        # предложения.
        # words = [word.lower() for word in words]

        transcriptions = []
        for index, word in enumerate(words):
            # 1. Пробуем вычитать транскрипцию из Excel-файла
            # В Python можно использовать метод .get() для доступа к элементам словаря с возможностью указания
            # значения по умолчанию, которое будет возвращено, если ключ отсутствует.
            # В данном случае вместо стандартного None будет возвращаться указанная строка.
            transcription = self.excel_word_transcription_dict.get(word, TRANSCRIPTION_NOT_FOUND)
            is_transcription_found_in_excel = self._is_transcription_valid(transcription)
            if is_transcription_found_in_excel:
                transcriptions.append(transcription.strip()[1:-1])  # убираем квадратные скобки
            elif index == 0:
                # Транскрипция слова могла быть не найдена в Excel, потому что слово стоит в самом начале предложения
                # (а значит написано с большой буквы), и при этом оно не является существительным.
                # Такое слово нужно попробовать написать с маленькой буквы и повторить попытку вычитки его транскрипции.
                word = word.lower()
                # 2. Пробуем ещё раз вычитать транскрипцию из Excel-файла
                transcription = self.excel_word_transcription_dict.get(word, TRANSCRIPTION_NOT_FOUND)
                is_transcription_found_in_excel = self._is_transcription_valid(transcription)
                if is_transcription_found_in_excel:
                    transcriptions.append(transcription.strip()[1:-1])

            # Специально сделано в отдельном if-блоке на уровне вложенности с остальными if-else-блоками, чтобы избежать
            # дублирования кода в двух блоках else (если продолжать писать код на один уровень вложенности глубже).
            # Лучше не пытаться весь этот набор отдельных if-else-блоков в теле цикла объединять в один if-else-блок:
            # это чревато как минимум дублированием кода в разных else-ветках разных уровней вложенности + трудность
            # чтения и понимания такого громоздкого кода. Хотя текущий код и выглядит немного дисперсным, на самом деле
            # это самый простой и гарантированно правильный вариант работы алгоритма.
            if not is_transcription_found_in_excel:
                # Поскольку транскрипции слова не оказалось в Excel-файле, то оно считается "unknown"
                self.sentence_unknown_words.append(word)
                transcriptions.append(TRANSCRIPTION_NOT_FOUND)

                # Ветка для случая, когда в Excel-файле транскрипции не оказалось, и флаг разрешает попробовать
                # достать транскрипцию из Wiktionary.
                if should_lookup_unknown_word_transcription_in_wiktionary:
                    # 3. Пробуем вычитать транскрипцию из Wiktionary
                    transcription = GermanWiktionaryService.get_word_transcription(word, True)
                    if self._is_transcription_valid(transcription):
                        # Заменяем последний элемент списка (со значением TRANSCRIPTION_NOT_FOUND) на новое значение
                        transcriptions[-1] = transcription.strip()[1:-1]
                    elif index == 0:
                        # Транскрипция слова могла быть не найдена в Wiktionary, потому что слово стоит в самом начале
                        # предложения (а значит написано с большой буквы), и при этом оно не является
                        # существительным.
                        # Такое слово нужно написать с маленькой буквы и повторить попытку вычитки его транскрипции.
                        word = word.lower()  # делаем слово с маленькой буквы
                        # 4. Пробуем ещё раз вычитать транскрипцию из Wiktionary
                        transcription = GermanWiktionaryService.get_word_transcription(word, True)
                        if self._is_transcription_valid(transcription):
                            # Заменяем последний элемент списка (со значением TRANSCRIPTION_NOT_FOUND) на новое значение
                            transcriptions[-1] = transcription.strip()[1:-1]

        # Преобразовываем список неизвестных слов в множество (set) с сохранением порядка следования слов
        sentence_unknown_words_set = dict.fromkeys(self.sentence_unknown_words).keys()

        # Формируем строковое представление транскрипции
        sentence_transcription = f"[{' '.join([t.strip() for t in transcriptions])}]"

        # Выполняем пост-обработку транскрипции
        sentence_transcription = self._post_process_sentence_transcription(sentence, sentence_transcription)

        # Добавляем в транскрипцию доп. маркеры: гортанные смычки, аспирацию, ассимиляцию, подчёркивание альвеолярных
        # согласных и пр.
        sentence_transcription = self.t0_TranscriptionProcessorsController.process_single_transcription(
            sentence_transcription, 'deu')

        return sentence_unknown_words_set, sentence_transcription

    def _is_transcription_valid(self, transcription):
        is_valid = transcription not in [None, '', TRANSCRIPTION_NOT_FOUND, f'[{TRANSCRIPTION_NOT_FOUND}]']
        return is_valid

    def _preprocess_before_transcribing(self, sentence):
        sentence = self._preprocess_currency(sentence)
        sentence = self.germanTimeTranscribableMaker.make_time_transcribable(sentence)  # preprocess time
        sentence = self._preprocess_numbers(sentence)

        if 'Ankunft(-szeit)' in sentence:
            # 'Auf diesem Plan steht nur die Ankunft(-szeit) der Züge.'
            # \b обозначает границу слова и срабатывает в местах, где символ слова (\w: буквы, цифры, подчёркивание)
            # соседствует с не-словесным символом (\W: пробел, пунктуация, конец строки и т. д.).
            # С анкерами \b по краям замена не работает: метасимвол \b (граница слова) не работает с - и (, ),
            # так как они не считаются буквенно-цифровыми символами. Граница слова \b действует только между
            # буквенно-цифровыми (\w) и не-буквенно-цифровыми (\W) символами.
            # В случае Ankunft(-szeit), после Ankunft идёт (, который не является \w, поэтому \b здесь не действует,
            # и соответствие не находится.
            # sentence = re.sub(fr'{re.escape("Ankunft(-szeit)")}', 'Ankunftszeit', sentence)
            sentence = sentence.replace('Ankunft(-szeit)', 'Ankunftszeit')

        return sentence

    def _preprocess_currency(self, sentence):
        for raw_case in re.findall(r'DM\s[0-9,-]+', sentence):
            # Лесенка условий: от самого объёмного и конкретного - к самому простому
            if ',-' in raw_case:  # DM 10,-  --> DM 10 Mark
                nice_case = raw_case.replace(',-', ' Mark')
            elif ',' in raw_case:  # DM 10,50 --> DM 10 Mark 50
                nice_case = raw_case.replace(',', ' Mark ')
            else:  # DM 10 --> DM 10 Mark
                nice_case = raw_case + ' Mark'

            nice_case = nice_case.replace('DM ', '')  # удаляем название валюты DM
            sentence = sentence.replace(raw_case, nice_case)
        return sentence

    def _preprocess_numbers(self, sentence):
        # 'Der Mount Everest ist 8,848 Meter hoch.',
        pattern = r'\b8,848\b'
        if re.search(pattern, sentence):
            sentence = re.sub(pattern, 'achttausend achthundert achtundvierzig', sentence)

        # 'Hier ist 06131–553221, Pamela Linke.'
        pattern = r'\b06131–553221\b'
        if re.search(pattern, sentence):
            sentence = re.sub(pattern, '0 6 1 3 1 5 5 3 2 2 1', sentence)

        return sentence

    def _post_process_sentence_transcription(self, sentence, sentence_transcription):
        updated_sentence_transcription = sentence_transcription

        # Флаг, который показывает, что транскрипция предложения была изменена
        is_sentence_transcription_modified = False

        # Разбиваем предложение на отдельные слова
        sentence_words = sentence.split()
        # Убираем квадратные скобки и разбиваем транскрипцию на отдельные слова
        transcription_words = sentence_transcription[1:-1].split()

        for index, word in enumerate(sentence_words):
            # Используем метод startswith(), а не проверку на равенство ==, потому что к слову могут
            # приклеиться знаки пунктуации после разбивки по пробелу (не очень совершенный метод токенизации)
            if word.startswith("geht’s"):
                try:
                    # Используем блок try-except для перезаписи транскрипции, т. к. нет гарантии, что длина списка
                    # со словами равна длине списка с их транскрипциями, и выход индекса за пределы списка
                    # теоретически возможен
                    transcription_words[index] = "ɡeːt͡s"
                    is_sentence_transcription_modified = True
                except ValueError:
                    # Если почему-то слово не найдено в транскрипции, возвращаем её без изменений
                    pass
            # Формируем транскрипцию выражения "Pommes frites"
            elif self._is_multi_worded_expression("Pommes", "frites", sentence_words, index):
                # перезаписываем транскрипцию: вместо ˈpɔməs пишем ˈpɔmˌfʁɪt
                transcription_words[index] = "ˈpɔmˌfʁɪt"
                # удаляем транскрипцию слова "frites" (она там значится в виде трёх знаков вопроса)
                del transcription_words[index + 1]
                is_sentence_transcription_modified = True
            # Формируем транскрипцию выражения "Mount Everest"
            elif self._is_multi_worded_expression("Mount", "Everest", sentence_words, index):
                # перезаписываем транскрипцию 1-го слова
                transcription_words[index] = "maʊ̯nt ˈɛvəʁɛst"
                # удаляем транскрипцию 2-го слова
                del transcription_words[index + 1]
                is_sentence_transcription_modified = True
            # Формируем транскрипцию выражения "Starnberger See"
            elif self._is_multi_worded_expression("Starnberger", "See", sentence_words, index):
                # перезаписываем транскрипцию 1-го слова
                transcription_words[index] = "ˈʃtaʁnˌbɛʁɡɐ ˈzeː"
                # удаляем транскрипцию 2-го слова
                del transcription_words[index + 1]
                is_sentence_transcription_modified = True

            if is_sentence_transcription_modified:
                # Собираем обновлённую транскрипцию
                merged_transcription = ' '.join(transcription_words)
                updated_sentence_transcription = f'[{merged_transcription}]'

        return updated_sentence_transcription

    # Слова типа "Pommes frites", "Mount Everest" называются "noun phrases" или "multi-word expressions" (c) ChatGPT
    def _is_multi_worded_expression(self, piece1, piece2, sentence_words, index):
        is_cond1 = sentence_words[index] == piece1
        is_cond2 = index + 1 < len(sentence_words) and sentence_words[index + 1].startswith(piece2)
        is_multi_worded = is_cond1 and is_cond2
        # Если каждый из элементов multi-word expression попал в список незнакомых слов, удаляем их оттуда, т. к.
        # по отдельности эти элементы не являются в полном смысле "незнакомыми" словами
        if is_multi_worded:
            if piece1 in self.sentence_unknown_words:
                self.sentence_unknown_words.remove(piece1)
            if piece2 in self.sentence_unknown_words:
                self.sentence_unknown_words.remove(piece2)

        return is_multi_worded


###################################################################

sentence = 'Am nächsten Montag geht es leider nicht.'
sentence = 'Wo geht’s hier bitte zur Autobahn?'
sentence = 'zur'
sentence = 'Schnell, steig ein, der Zug fährt gleich.'
sentence = 'steig'
sentence = '48'
sentence = 'Dieses Auto kostet'
sentence = 'Ich bin kulturell interessiert. Ich gehe oft ins Museum.'
sentence = 'Ich wohne am Messeplatz 5.'
sentence = 'Pommes'
sentence = 'frites'
sentence = 'Pommes frites.'
sentence = 'Die Kinder essen Hähnchen mit Pommes frites.'
sentence = 'Wörter'
sentence = 'Das ist das aktuelle Kinoprogramm.'
sentence = 'aktuelle Kinoprogramm.'
sentence = 'Hier fängt die Bahnhofstraße an.'
sentence = 'Auf diesem Plan steht nur die Ankunft(-szeit) der Züge.'
sentence = 'Du brauchst den Schlüssel nicht. Die Wohnung ist auf.'
sentence = 'Das Spiel beginnt um 15.30 Uhr.'
sentence = 'Viele meiner Verwandten, z. B. meine beiden Brüder, arbeiten auch hier.'
sentence = 'Die Jacke kostet nur 10 Euro! Die ist aber billig!'
sentence = 'Bei „Familienstand“ musst du „ledig“ ankreuzen.'
sentence = 'Der Abflug ist um 11.20 Uhr.'
sentence = 'Jetzt muss ich (aber) leider gehen.'
sentence = 'Der Mount Everest ist 8,848 Meter hoch.'
sentence = 'Unser Deutschkurs ist international: Silvana kommt aus Italien, Conchi aus Spanien, Yin aus China...'
sentence = '– Sind Sie Herr Watanabe?\n– Ja.'
sentence = 'Jenny hat einen neuen Job bei der Post.'
sentence = 'Hier ist 06131–553221, Pamela Linke.'
sentence = 'Der Laden ist samstags bis 16.00 Uhr geöffnet.'
sentence = 'Von 12.00 bis 12.30 Uhr haben wir Mittagspause.'
sentence = 'Komm, wir fahren zum Starnberger See.'
# sentence = 'Das Licht ist an.\nVS.\nDas Licht ist aus.'
# sentence = 'So, das war’s!'
# sentence = 'acht'
# sentence = 'Ankunft(-szeit)'
# sentence = 'abend'
# sentence = 'Weißt du, wie er heißt?'

if __name__ == '__main__':
    germanSentenceTranscriber = GermanSentenceTranscriber()

    sentence_unknown_words, sentence_transcription = germanSentenceTranscriber.transcribe_sentence(
        sentence, False)

    print(sentence_unknown_words)
    print(sentence_transcription)
