import AppContext
import GermanWiktionaryService
import SentenceUtils
import Utils
from AnkiCardEntity import AnkiCardEntity
from MultilingualAnkiService import MultilingualAnkiService
from OdtFilesService import OdtFilesService
from GermanSentenceTranscriber import GermanSentenceTranscriber
from View_enums import CurrentLanguageComboBoxEnum

adj_endings_ai_prompt = """
Тебе будет дан список греческих прилагательных в форме мужского рода. Поставь после каждого прилагательного
"|// ", продублируй форму мужского рода и укажи окончания для женского и среднего рода. Приведу тебе
несколько примеров как это должно выглядеть:
μεγάλος|// μεγάλος, -η, -ο
ωραίος|// ωραίος, -α, -ο
αυθάδης|// αυθάδης, -ης, -ες

А теперь сделай эту работу для следующих прилагательных:
{}
"""


class A020_TranscriptionsAndTranslationsLookUpper:

    def __init__(self):
        self.odtFilesService = None
        self.multilingualAnkiService = None
        self.germanSentenceTranscriber = GermanSentenceTranscriber()
        self.results_dict = {}

    def look_up(self, input_text):
        self.results_dict = {}  # очищаем словарь от предыдущих результатов
        self.odtFilesService = OdtFilesService()
        raw_lines = Utils.split_by(input_text, '\n')
        # В некоторых строках после леммы может стоять pipe (|), за которым будет следовать некоторая вспомогательная
        # техническая информация. Например, для ГРЕЧЕСКИХ прилагательных после PIPE будет стоять ADJ как напоминание
        # о том, что во Front_commnent к прилагательному нужно дописать его окончания в fem. и neut. формах.
        unpiped_lines = [raw_line.split('|')[0] for raw_line in raw_lines]
        processed_lines = self.process_lines(unpiped_lines)
        processed_lines_output = '\n'.join(processed_lines)

        if AppContext.is_language_ancient_greek() or AppContext.is_language_modern_greek():
            adj_lines = [raw_line.split('|')[0] for raw_line in raw_lines if raw_line.endswith('|ADJ')]
            adj_endings_output = adj_endings_ai_prompt.format('\n'.join(adj_lines))
            output = '\n\n'.join([out for out in [processed_lines_output, adj_endings_output] if out])
        else:
            output = processed_lines_output

        return output

    # Данный метод используется не только в текущем UC#2, но и может вызываться из UC#3
    def process_lines(self, lines):
        # for i, line in enumerate(lines):
        for line in lines:
            # Если line является ПРЕДЛОЖЕНИЕМ (а не словом), просто добавляем его в результаты!
            # TODO: выполнять if-ветку не только для ПРЕДЛОЖЕНИЙ, но и для ВЫРАЖЕНИЙ!
            if SentenceUtils.is_sentence(line):
                if AppContext.is_language_german():
                    # Стараемся по максимуму получить транскрипцию предложения (флаг установлен в True)
                    # sentence_unknown_words, sentence_transcription = self.germanTableCellTextTranscriber.transcribe(
                    #     line, True)

                    sentence_unknown_words, sentence_transcription = self.germanSentenceTranscriber.transcribe_sentence(
                        line, True)

                    result = f'{line}||{sentence_transcription}'
                else:
                    result = f'{line}||'
                self.results_dict[line] = result
            # если же столбец содержит не предложение (а слово), пробуем найти его среди настоящих Анки-карточек
            else:
                # Инициализируем сервис только тогда, когда он реально становится нужным, чтобы из-за ошибки
                # дизайна классов не было преждевременного обращения к Анки
                if self.multilingualAnkiService is None:
                    self.multilingualAnkiService = MultilingualAnkiService()

                # Поскольку line не является предложением, значит оно является словом
                self.search_recursively_in_anki(line)

        results = self.results_dict.values()
        return results

    def search_recursively_in_anki(self, word):
        # Ищем слово в Анки
        found_regular_card = self.multilingualAnkiService.search_among_main_regular_cards(word)
        if found_regular_card:
            front_stripes = found_regular_card.front
            # Если найденная карточка является однополосной, добавляем её в результат при условии, что она НЕ является
            # дубликатом по отношению к:
            # 1) содержимому словаря results_dict
            # 2) содержимому предыдущих [Vocab]-файлов.
            if len(front_stripes) == 1:
                front_stripe = front_stripes[0]
                front_stripe_ready_token = AnkiCardEntity.parse_front_stripe(front_stripe)

                # Ключами словаря results_dict являются слова, которые уже были обработаны, т. е. которые технически
                # будут расположены выше рассматриваемого слова в таблице будущего Vocab-файла. Поэтому проверка на
                # невхождение слова в множество ключей словаря это по сути проверка на то, что данное слово ещё
                # не встречалось в текущем Vocab-файле. Раньше для этой проверки я делал слайс lines[:i], но теперь
                # достаточно проверить наличие слова в словаре results_dict.
                is_not_in_results = front_stripe_ready_token not in self.results_dict
                should_add = self._should_stripe_be_added_above_as_a_separate_table_record(front_stripe_ready_token)
                if is_not_in_results and should_add:
                    # Преобразуем карточку в строковую форму
                    result = found_regular_card.to_str(format_type="front_transcription_back_with_comments")
                    # Добавляем карточку в результирующий набор
                    self.results_dict[front_stripe_ready_token] = result
            elif len(front_stripes) > 1:
                # Если карточка является многополосной, нужно определить нуждаются ли во вставке в таблицу
                # (выше текущего слова) её полосы (кроме последней) в качестве отдельных слов-строк.
                # Для каждой полосы (кроме последней) мультиполосной карточки проверить отсутствует ли она:
                # 1) среди строк входного текста, расположенных выше текущей строки
                # 2) во всех предыдущих [Vocab]-файлах
                # и если отсутствует, добавить её в результирующий набор перед сложным/составным словом.
                for j in range(0, len(front_stripes)):
                    front_stripe = front_stripes[j]
                    front_stripe_ready_token = AnkiCardEntity.parse_front_stripe(front_stripe)
                    if j < len(front_stripes) - 1:  # все полосы, кроме последней
                        # Рекурсивный вызов функции.
                        # Пока карточка является многополосной, для каждой полосы (кроме последней) будет производиться
                        # рекурсивный поиск в Анки этой полосы как самостоятельной карточки. Как только дошли в этой
                        # цепочке вызовов до однополосной карточки -> рекурсия прекращается.
                        self.search_recursively_in_anki(front_stripe_ready_token)
                    # логика для последней полосы многополосной карточки
                    elif j == len(front_stripes) - 1:  # последняя полоса
                        found_regular_card_str = found_regular_card.to_str(
                            format_type="front_transcription_back_with_comments")
                        self.results_dict[word] = found_regular_card_str
        else:
            # Если слово не найдено в Анки, попробовать заполнить хотя бы транскрипцию для него
            transcription = GermanWiktionaryService.get_word_transcription(word, True)
            result = f'{word}||{transcription}'
            self.results_dict[word] = result

    def _should_stripe_be_added_above_as_a_separate_table_record(self, front_stripe_ready_token):
        # Ищем Анки-полосу среди предыдущих [Vocab]-файлов
        if self.odtFilesService is None:
            self.odtFilesService = OdtFilesService()

        is_absent = self.odtFilesService.is_word_absent_from_vocabulary_of_all_files_but_last(front_stripe_ready_token)
        return is_absent  # should_be_added отвечает на тот же вопрос, что и is_absent


###########################

test_input_str = 'abholen'

test_input_str = """
der Unterricht
gleich
Der Unterricht fängt gleich an.

der Anfang
Sie wohnt am Anfang der Straße.
"""

test_input_str = 'Wie geht’s?'

test_input_str = """
die Ehe
der Ehemann
die Ehefrau
"""

# test_input_str = 'die Donaudampfschifffahrtsgesellschaftskapitänsmütze'

# test_input_str = """
# die Donau
# der Dampf
# das Schiff
# die Fahrt
# """

test_input_str = 'die Bundesrepublik'

test_input_str = 'ανεγείρω'

test_input_str = """
είμαι
όλος
τέλειος|ADJ
(ΓΙΑΝΝΑΚΗΣ) Σήμερα ο μπαμπάς μου παντρεύεται και θέλει να είναι όλα τέλεια.
για
αυτός
ταραγμένος|ADJ
σπαστικός|ADJ
Γι’ αυτό είναι ταραγμένος και σπαστικός.
δεν
πρώτος|ADJ
η φορά
αλλά
"""

if __name__ == '__main__':
    # language = CurrentLanguageComboBoxEnum.GERMAN.value
    language = CurrentLanguageComboBoxEnum.MODERN_GREEK.value
    # language = CurrentLanguageComboBoxEnum.ANCIENT_GREEK.value
    AppContext.switch_language(language)

    a020_TranscriptionsAndTranslationsLookUpper = A020_TranscriptionsAndTranslationsLookUpper()
    res = a020_TranscriptionsAndTranslationsLookUpper.look_up(test_input_str)
    print(res)
