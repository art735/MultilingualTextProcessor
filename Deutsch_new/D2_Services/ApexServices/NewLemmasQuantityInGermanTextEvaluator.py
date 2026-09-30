import re

import spacy

import FileContentsReader
from Tokenizer import Tokenizer
from A010_NewLemmasFinder import A010_NewLemmasFinder
from OdtFilesService import OdtFilesService


# Нужно различать две разные задачи:
# 1) выяснить общее кол-во лемм в любом тексте (модуль A010_NewLemmasFinder.py)
# 2) оценить количество только неизвестных лемм в тексте относительно известного корпуса текстов и предложений.

# Первая задача труднее для реализации в немецком и не всегда нужна, а вторая задача проще в реализации и часто
# нужна именно она! Нижеследующий модуль предназначен для решения именно второй задачи.

# Пример use case-а для оценки кол-ва новых лемм во всех предложениях уровня А2.
# 1) вычитываем из заранее подготовленного txt-файла список всех предложений уровня A2, токенизируем этот общий массив
# текста и формируем список уникальных токенов
# 2) вычитываем из [Vocab]-файлов все предложения уровня А1 и тоже формируем из них список уникальных токенов
# 3) в первом списке оставляем только те токены, которых нет во втором списке и дорабатываем их сначала с помощью
# модели "de_core_news_sm", а затем с помощью A010_NewLemmasFinder
class NewLemmasQuantityInGermanTextEvaluator:
    def __init__(self):
        # Должен инициализироваться в методе-обработчике, а не в конструкторе.
        # В данном классе это непринципиально (потому что он чисто консольный и не используется в gui),
        # но в целом в проекте правило для данного класса именно такое!
        self.odtFilesService = OdtFilesService()
        self.tokenizer = Tokenizer()

    def evaluate(self, filename):

        # Step 1.1 Извлекаем немецкие предложения из [Vocab]-файлов
        vocab_files_sentences = self.odtFilesService.get_sentences_from_all_vocab_files()

        # Для самопроверки алгоритма (или в будущем юнит-тестирования) хорошей техникой является брать в качестве
        # исходного текста и в качестве предложений из [Vocab]-файлов один и тот же текст. Если алгоритм не находит
        # ни одной новой леммы - это хороший признак того, что он работает правильно!
        # base_path = r'E:\Languages\[Git repo] MultilingualTextProcessor\resources\German'
        # vocab_files_sentences = FileContentsReader.get_file_text_as_lines(f'{base_path}\A2 sentences.txt')
        # vocab_files_sentences = FileContentsReader.get_file_text_as_lines(f'{base_path}\B1 sentences.txt')

        # Step 1.2 Ищем уникальные (неповторяющиеся) токены
        vocab_files_unique_tokens = self._find_unique_tokens(vocab_files_sentences)

        # Step 2.1 Извлекаем текст из txt-файла / srt-файла субтитров, игнорируя строки не содержащие ни одной буквы
        # (строки с тайм-кодами и т. д.)
        text_lines = self._extract_text_from_file(filename)

        # Step 2.2 Ищем в тексте уникальные (неповторяющиеся) токены
        input_text_unique_tokens_all = self._find_unique_tokens(text_lines)

        # Step 3. Берём в дальнейшую работу только те токены, которых нет в [Vocab]-файлах
        input_text_unique_tokens_remaining = []
        for input_text_unique_token in input_text_unique_tokens_all:
            # Проверяем содержится ли токен исследуемого текста в коллекции уже известных токенов (без учёта регистра)
            # Метод casefold() предпочтителен, если строки могут содержать символы из других языков (в частности нем.
            # яз.) или символы Unicode
            if not any(input_text_unique_token.casefold() == vfut.casefold() for vfut in vocab_files_unique_tokens):
                # print("Строка НЕ найдена в списке (без учета регистра)")
                input_text_unique_tokens_remaining.append(input_text_unique_token)

        # Step 4. Поиск лемм входного текста
        rough_new_lemmas, more_accurate_new_lemmas = self._find_lemmas(input_text_unique_tokens_remaining,
                                                                       vocab_files_unique_tokens)

        # Step 5. Print results
        print('--=ALREADY EXISTING DATA ([VOCAB]-DATA) STATISTICS=--')
        print(f'Unique tokens: {len(vocab_files_unique_tokens)}')
        vocabulary_capacity = len(self.odtFilesService.all_words_as_entities)
        print(f'Lemmas (vocabulary capacity): {vocabulary_capacity}')
        unique_tokens_to_lemmas_ratio = len(vocab_files_unique_tokens) / float(vocabulary_capacity)
        print(f'Unique tokens / lemmas ratio: {unique_tokens_to_lemmas_ratio:.2f}\n')

        print('--=INPUT (NEW) DATA STATISTICS=--')
        print(f'All unique tokens: {len(input_text_unique_tokens_all)}')
        print(f'Remaining unique tokens: {len(input_text_unique_tokens_remaining)}')
        print(f'Rough new lemmas: {len(rough_new_lemmas)}')
        print(f'!!! More accurate new lemmas: {len(more_accurate_new_lemmas)} !!!')
        remaining_unique_tokens_to_lemmas_ratio = len(input_text_unique_tokens_remaining) / float(
            len(more_accurate_new_lemmas))
        print(
            f'Remaining unique tokens / more accurate new lemmas ratio: {remaining_unique_tokens_to_lemmas_ratio:.2f}\n')

        # TODO интересно сравнивать два коэффициента между собой (unique_tokens_to_lemmas_ratio и
        #  remaining_unique_tokens_to_lemmas_ratio). На момент написания текста (январь 2025 года) он варьируется
        #  от 11% (на большей части материала А1) до 41% (на оценке материала А2) и 40% (на оценке материала A2+B1).
        #  Зная этот коэффициент, можно легко посчитать приблизительное кол-во новых лемм в тексте просто зная кол-во
        #  новых уникальных токенов в нём (разделить кол-во новых уникальных токенов на коэффициент).

        return more_accurate_new_lemmas

    def _extract_text_from_file(self, file_path):
        lines = FileContentsReader.get_file_text_as_lines(file_path)

        text_lines = []
        for line in lines:
            # Берём строку в дальнейшую работу, если она содержит хотя бы одну букву (а не состоит целиком из цифр и
            # других небуквенных символов, как например, строки с тайм-кодами или номерами эпизодов)
            if re.search(r'[a-zA-Z]', line):
                text_lines.append(line.strip())

        return text_lines

    # Метод принимает список строк (не важно вычитаны они из txt-/srt-файла или из Vocab-файлов) и возвращает список
    # уникальных токенов. Такой метод будет востребован минимум дважды.
    def _find_unique_tokens(self, text_lines):
        # Токенизируем строки текста
        all_tokens = []
        for line in text_lines:
            # print(line)
            tokens = self.tokenizer.tokenize(line, consider_number_as_token=False, strip_apostrophe=True)
            all_tokens.extend(tokens)

        # В немецком языке лучше оставить регистр слов "как есть", потому что существительные пишутся всегда с большой
        # буквы и их принудительное приведение к нижнему регистру может повлиять на точность лемматизации в spaCy (лучше
        # ошибиться только на 1-м слове предложения, написанном с большой буквы, чем на всех остальных существительных
        # предложения).
        # is_lang_de = filename.endswith('-de.srt') or filename.endswith('-de.txt')
        # if not is_lang_de:
        #     tokens = [t.lower() for t in tokens]

        # Формируем список УНИКАЛЬНЫХ токенов (т. е. игнорируем дубликаты), используя dict.fromkeys(...) для сохранения
        # естественного порядка следования слов в тексте
        unique_tokens = list(dict.fromkeys(all_tokens))

        return unique_tokens

    def _find_lemmas(self, input_text_unique_tokens_remaining, vocab_files_unique_tokens):
        # Step 1. Поиск лемм входного текста
        nlp = spacy.load("de_core_news_sm")
        # на файле с субтитрами к Nicos Weg MEDIUM MODEL и LARGE MODEL показали точно такие же результаты,
        # как и SMALL MODEL
        # nlp = spacy.load("de_core_news_md")
        # nlp = spacy.load("de_core_news_lg")
        rough_new_lemmas = []
        for input_text_unique_token in input_text_unique_tokens_remaining:
            # Ищем лемму токена, которого, как уже выяснили, нет в [Vocab]-файлах
            doc_object = nlp(input_text_unique_token)
            for item in doc_object:
                lemma = item.lemma_
                is_absent1 = self.odtFilesService.is_word_absent_from_vocabulary(lemma)
                is_absent2 = self.odtFilesService.is_word_absent_from_vocabulary(lemma.lower())
                is_absent_from_vocabulary = is_absent1 and is_absent2  # здесь именно AND, но не OR
                if is_absent_from_vocabulary and lemma not in rough_new_lemmas:
                    rough_new_lemmas.append(lemma)

        # Step 2. Пропускаем грубо оцененные новые леммы через A010_NewLemmasFinder
        more_accurate_new_lemmas = []
        if rough_new_lemmas:
            rough_new_lemmas_str = '\n'.join(rough_new_lemmas)

            a010_NewLemmasFinder = A010_NewLemmasFinder()
            more_accurate_new_lemmas_str = a010_NewLemmasFinder.find_new_lemmas(rough_new_lemmas_str, False,
                                                                                False,
                                                                                False,
                                                                                False)
            # .strip() удаляет символы [ \t\n\r\f\v] в начале и конце строки
            more_accurate_new_lemmas = more_accurate_new_lemmas_str.strip().split('\n')

        return rough_new_lemmas, more_accurate_new_lemmas


######################

subtitle_filename = r'C:\Users\user\Desktop\Subtitles\Shrek 1 (2001)-de.srt'
subtitle_filename = r'C:\Users\user\Desktop\Subtitles\Groundhog Day-de.srt'
subtitle_filename = r'C:\Users\user\Desktop\Subtitles\The Terminal-de.srt'

subtitle_filename = r'E:\Languages\[Git repo] MultilingualTextProcessor\Deutsch_new\D2_Services\zConsoleUtils\NicosWeg\Nicos Weg (A1) subtitles-de.txt'  # 1690 слов

# # Goethe-Institut A1, A2, B1 sentences
german_folder = r'E:\Languages\[Git repo] MultilingualTextProcessor\resources\German'
subtitle_filename = fr'{german_folder}\A1 sentences.txt'
subtitle_filename = fr'{german_folder}\A2 sentences.txt'
# subtitle_filename = fr'{german_folder}\A2+B1 sentences.txt'
# subtitle_filename = fr'{german_folder}\B1 sentences.txt'

if __name__ == '__main__':
    newLemmasQuantityInGermanTextEvaluator = NewLemmasQuantityInGermanTextEvaluator()
    res = newLemmasQuantityInGermanTextEvaluator.evaluate(subtitle_filename)
    [print(r) for r in res]
