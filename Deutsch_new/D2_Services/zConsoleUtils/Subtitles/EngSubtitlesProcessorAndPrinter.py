import spacy

import FileContentsReader
from FilenameUtils import FilenameUtils
from Tokenizer import Tokenizer
from DeuLemmaResolver import DeuLemmaResolver


class EngSubtitlesProcessorAndPrinter:
    def __init__(self):
        self.deuLemmaResolver = DeuLemmaResolver()
        self.tokenizer = Tokenizer()

    # Бизнес-метод №1. Создаёт печатную версию субтитров
    def make_printable_version(self, subtitle_filename):

        # Вычитываем текст файла субтитров
        file_text = FileContentsReader.get_file_text(subtitle_filename)

        # Извлекаем текст (как список текстовой информации по каждому блоку) из субтитров
        text_lines_by_blocks = self._extract_text_lines_by_blocks_from_subtitles(file_text)

        # Преобразовываем список строк в текстовую строку
        printable_version = '\n\n'.join(text_lines_by_blocks)

        return printable_version

    # Бизнес-метод №2. Определяет леммы текста субтитров, а также выводит статистику по токенам
    def find_tokens_and_lemmas(self, subtitle_filenames: list):

        all_text = ''
        for subtitle_filename in subtitle_filenames:
            # Вычитываем текст файла субтитров
            all_text += FileContentsReader.get_file_text(subtitle_filename)

        # Извлекаем текст (как список текстовой информации по каждому блоку) из субтитров, игнорируя строки
        # не содержащие ни одной буквы (строки с тайм-кодами и т. д.)
        text_lines_by_blocks = self._extract_text_lines_by_blocks_from_subtitles(all_text)

        # Преобразовываем список строк в текстовую строку
        text = '\n'.join(text_lines_by_blocks)

        # Токенизируем текст
        tokens = self.tokenizer.tokenize(text, consider_number_as_token=False, strip_apostrophe=True)

        # Приводим все токены к нижнему регистру
        tokens = [t.lower() for t in tokens]

        # Формируем список УНИКАЛЬНЫХ токенов (т. е. игнорируем дубликаты), используем dict.fromkeys(...) для сохранения
        # естественного порядка следования слов в тексте
        unique_tokens = list(dict.fromkeys(tokens))

        # Лемматизируем токены с помощью spaCy
        lemmas = self._lemmatize_tokens(unique_tokens)
        # lemmas = self._lemmatize_text(text)

        print(f'All tokens: {len(tokens)}')
        print(f'Unique tokens: {len(unique_tokens)}')
        print(f'Lemmas: {len(lemmas)}\n')

        return lemmas

    # Очень важно отбирать текстовые строки именно поблочно, поэтому не менять без серьёзной необходимости этот
    # алгоритм.
    def _extract_text_lines_by_blocks_from_subtitles(self, file_text):
        all_text_lines = []

        # 144
        # 00:06:39,950 --> 00:06:42,400
        # but he really hates college.

        # 145
        # 00:06:42,400 --> 00:06:45,200
        # Anyway, he's doing a TED
        # talks in Palo Alto tonight.

        # 146
        # 00:06:45,210 --> 00:06:47,900
        # - We should try to get in.
        # - I dropped out of college.

        # По-английски вышеуказанные фрагменты субтитров называются "subtitle blocks". Они обычно состоят из:
        # - номера (index),
        # - временного кода (timestamp / timecode),
        # - текста (text).
        blocks = file_text.split('\n\n')
        # for block in blocks:
        #     dirty_block_lines = block.split('\n')
        #     pure_block_lines = []
        #     for dirty_block_line in dirty_block_lines:
        #         # Отбираем только те строки блока, которые содержат хотя бы одну букву. При таком подходе первая и
        #         # вторая строки каждого блока автоматически отпадают.
        #         if re.search(r'[a-zA-Z]', dirty_block_line):
        #             pure_block_lines.append(dirty_block_line.strip())
        #     pure_block_lines_str = '\n'.join(pure_block_lines)
        #     all_text_lines.append(pure_block_lines_str)

        for block in blocks:
            # Игнорируем в каждом блоке первые (верхние) две строки (номер и временной код)
            block_text_lines = block.split('\n')[2:]
            block_text_lines_str = '\n'.join(block_text_lines)
            all_text_lines.append(block_text_lines_str)

        return all_text_lines

    def _lemmatize_tokens(self, unique_tokens):
        nlp = spacy.load("en_core_web_sm")
        # nlp = spacy.load("el_core_news_lg")
        lemmas = []
        for token in unique_tokens:
            doc_object = nlp(token)
            for item in doc_object:
                lemma = item.lemma_
                if lemma not in lemmas:
                    lemmas.append(lemma)

        return lemmas


######################

subtitle_filename = r'C:\Users\user\Desktop\Subtitles\Evolution 2001-en.srt'  # 1460 слов
subtitle_filename = r'C:\Users\user\Desktop\Subtitles\a-beautiful-mind-yify-english-en.srt'  # 1465 слов
subtitle_filename = r'C:\Users\user\Desktop\Subtitles\The Shawshank Redemption.srt'  # 1775 слов
subtitle_filename = r'C:\Users\user\Desktop\Subtitles\Lex Frieman, Zelenvsky.txt'  # 2170 слов
subtitle_filename = r'C:\Users\user\Desktop\Subtitles\Shrek 1 (2001)-en.srt'  # 1380 слов
subtitle_filename = r'C:\Users\user\Desktop\Subtitles\Jane Eyre-en.txt'  # ≈ 9400 слов
subtitle_filename = r'C:\Users\user\Desktop\Subtitles\Groundhog Day-en.srt'  # 1250 слов
subtitle_filename = r'C:\Users\user\Desktop\Subtitles\Rat Race-en.srt'  # 1460 слов
subtitle_filename = r'C:\Users\user\Desktop\Subtitles\The Terminal-en.srt'  # 1275 слов
subtitle_filename = r'C:\Users\user\Desktop\Subtitles\Silicon Valley (season 1) (all 8 episodes).txt'  # ??? слов

# base_folder = r'c:\Users\user\Desktop\Silicon_Valley - season 1.en'
# subtitle_filename = fr'{base_folder}\Silicon Valley - 1x01 - Minimum Viable Product.HDTV.KILLERS.en.srt'
# subtitle_filename = fr'{base_folder}\Silicon Valley - 1x02 - The Cap Table.HDTV.2HD.en.srt'
# subtitle_filename = fr'{base_folder}\Silicon Valley - 1x03 - Articles of Incorporation.HDTV.KILLERS.en.srt'
# subtitle_filename = fr'{base_folder}\Silicon Valley - 1x04 - Fiduciary Duties.HDTV.KILLERS.en.srt'
#
# subtitle_filename = fr'{base_folder}\Silicon Valley - 1x05 - Signaling Risk.HDTV.KILLERS.en.srt'
# subtitle_filename = fr'{base_folder}\Silicon Valley - 1x06 - Third Party Insourcing.HDTV.2HD.en.srt'
# subtitle_filename = fr'{base_folder}\Silicon Valley - 1x07 - Proof of Concept.HDTV.KILLERS.en.srt'
# subtitle_filename = fr'{base_folder}\Silicon Valley - 1x08 - Optimal Tip-to-Tip Efficiency.HDTV.KILLERS.en.srt'

if __name__ == '__main__':
    engSubtitlesProcessorAndPrinter = EngSubtitlesProcessorAndPrinter()

    # РАБОТА С БИЗНЕС-МЕТОДОМ №1
    # printable_version = engSubtitlesProcessorAndPrinter.make_printable_version(subtitle_filename)
    # print(printable_version)

    # РАБОТА С БИЗНЕС-МЕТОДОМ №2
    # res = engSubtitlesProcessorAndPrinter.find_tokens_and_lemmas([subtitle_filename])
    # [print(r) for r in res]

    # Все 23 серии 1-го сезона "Отчаянных домохозяек"
    sub_filenames = FilenameUtils.get_filenames_recursively(r"C:\Users\user\Desktop\DH subs (season 1)")
    # sub_filenames = FilenameUtils.get_filenames_recursively(r"C:\Users\user\Desktop\Ευτυχισμένοι Μαζί")
    res = engSubtitlesProcessorAndPrinter.find_tokens_and_lemmas(sub_filenames)
    [print(r) for r in res]
