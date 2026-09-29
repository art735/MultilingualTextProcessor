import re

import AppContext
from CharConstants import PIPE, HYPHEN, SPACE, COMMA, CURLY_APOSTROPHE, SLASH
from EllDefiniteArticleService import EllDefiniteArticleService
from MultilingualAnkiDao import MultilingualAnkiDao
from GrcDefiniteArticleService import GrcDefiniteArticleService
from GrcRegExFinder import GrcRegExFinder
from OdtFileTableDao import OdtFileTableDao
from View_enums import CurrentLanguageComboBoxEnum


class RitovaKhorikovValidator:
    base_dir = r'E:\Languages\Greek\Books'
    filename_ritova = fr'{base_dir}\Рытова M. Л. Новогреческий язык. Практический курс [1994]\Словарь из учебника (Рытова).odt'
    filename_khorikov = fr'{base_dir}\Хориков И. П. Учебник греческого языка [2006]\Словарь из учебника (Хориков).odt'

    # ell_nom_definite_articles = ("ο", "η", "ο/η", "το", "οι", "τα")

    adj_endings = (
        ', -ή, -ό', ', -η, -ο',
        ', -ά, -ό', ', -α, -ο',
        ', -ής, -ές', ', -ης, -ες',
        ', -ούσα, -όν', ', -ουσα, -ον',
        ', -ιά, -ύ', ', -ιά, -ί', ', -ιά, -ιό', ', -ιά, -ό',
        ', -εία, -ύ',
        ', -α, -ικο',
        ', -ού, -άδικο',
        # Исключения
        ', πάσα, παν', ', πολλή, πολύ',
        # доп. окончания из Анки
        ', -ία, -ιο', ', -ια, -ο', ', -ή, -όν', ', -ος, -ον',
        ', -ος, -ον', ', -ή, -όν', ', -η, -ον',
        ', -ία, -ιον', ', -α, -ον', ',-εία, -ύ',
    )

    all_col_data = []
    first_col_data = []

    def __init__(self):
        self.odtFileTableDao = OdtFileTableDao()
        self.grcRegExFinder = GrcRegExFinder()
        self.ellDefiniteArticleService = EllDefiniteArticleService()
        self.grcDefiniteArticleService = GrcDefiniteArticleService()

    def get_stripes(self):
        # language = CurrentLanguageComboBoxEnum.GERMAN.value
        language = CurrentLanguageComboBoxEnum.MODERN_GREEK.value
        # language = CurrentLanguageComboBoxEnum.ANCIENT_GREEK.value
        AppContext.switch_language(language)  # выбор языка должен происходить в самую первую очередь, даже ДО импорта

        multilingualAnkiDao = MultilingualAnkiDao()
        regular_cards = multilingualAnkiDao.get_regular_cards()
        aggregate_cards = multilingualAnkiDao.get_all_aggregate_cards()

        # Флаг, с помощью которого можно вручную подмешивать агрегатные карточки.
        # Алгоритм работы такой: сначала устанавливать данный флаг в значение False, чтобы разобраться хотя бы с
        # регулярными карточками, а затем установить его в True, чтобы устранить все недочёты и в агрегатных карточках.
        should_process_also_aggregate_cards = True

        if should_process_also_aggregate_cards:
            cards_to_process = regular_cards + aggregate_cards
        else:
            cards_to_process = regular_cards

        ignored_stripes = [
            # ['η παροικία', 'η ενορία', "parish ['pʰærɪʃ]", 'парафія (грец. παροικία: παρά – «біля», ο οίκος – «дім»)'],
            "parish ['pʰærɪʃ]",
            'парафія (грец. παροικία: παρά – «біля», ο οίκος – «дім»)',
            'δέκατος τρίτος',
            'δέκατος τέταρτος',
            'δέκατος πέμπτος',
            'δέκατος έκτος',
            'δέκατος έβδομος',
            'δέκατος όγδοος',
            'δέκατος ένατος',
            '- - -'
        ]

        results = []
        for card in cards_to_process:
            for stripe in card.front:
                if stripe not in ignored_stripes:
                    # у каждой полосы берём только первую строку
                    # TODO: искать карточки, в которых 2-я строка полосы полностью соотв. греч. слову!!! Это "слипшиеся"
                    #  синонимы, которые нужно "разлепить"
                    first_line = stripe.split('\n')[0]
                    if first_line not in ['VS.']:
                        results.append(first_line)

        return results

    def run(self):
        # UC#1 для .odt-файлов
        # for filename in [self.filename_ritova, self.filename_khorikov]:
        #     self.all_col_data = self.odtFileTableDao.read_single_file_all_tables_data(filename, ignore_empty_rows=False)
        #     self.first_col_data = self.get_1st_col_data(filename)
        #     self.validate()

        # UC#2 для Anki
        self.first_col_data = self.get_stripes()
        self.validate()

    def validate(self):
        # UC #1
        bad_lines = self.find_non_greek_characters()
        [print(bl) for bl in bad_lines]

        # UC #2
        bad_lines = validator.check_adjectives_dont_start_with_definite_article()
        [print(bl) for bl in bad_lines]

        # UC #3
        bad_lines = validator.check_wrong_definite_article()
        [print(bl) for bl in bad_lines]

        # # UC #4
        # duplicates = self.find_duplicates_among_1st_col_values()
        # if duplicates:
        #     raise Exception(f'Found duplicates in {filename}: {duplicates}')
        #     # [print(dup) for dup in duplicates]
        #     # Код для поиска дубликатов между словарями к томам 1 и 2 учебника Хорикова
        #     # for dup in duplicates:
        #     #     file1_data_row = [row for row in file1_data if row.split(PIPE)[0] == dup]
        #     #     file2_data_row = [row for row in file2_data if row.split(PIPE)[0] == dup]
        #     #     if file1_data_row != file2_data_row:
        #     #         print(f'{file1_data_row} != {file2_data_row}')

        # UC #5
        bad_lines = self.find_non_greek_symbols_after_stripping_nouns_and_adjectives()
        [print(bl) for bl in bad_lines]

        # # UC #6
        # # self.print_sorted_data()
        #
        # # UC #7
        # results = self.strip_adj_endings_by_moving_them_to_front_comment()
        # [print(r) for r in results]
        # print('\n* * * * *\n')

    def get_1st_col_data(self, filename):
        # all_tables_data = self.odtFileTableDao.read_single_file_all_tables_data(filename)
        first_col_data = [row.split(PIPE)[0] for row in self.all_col_data]
        # Удаляем шапку таблицы (точнее шапку 1-го столбца)
        if first_col_data and first_col_data[0] == 'Front': del first_col_data[0]
        return first_col_data

    # Находим все символы, которые не принадлежат греческому алфавиту. Особенно часто используется ошибочный символ
    # для греч. определённого артикля "o": из-за ошибок распознания данный символ может принадлежать к русскому или
    # английскому алфавиту, а нужно чтобы он принадлежал именно к греческому алфавиту!
    def find_non_greek_characters(self):
        ingored_on_this_step_chars = [SPACE, COMMA, HYPHEN, CURLY_APOSTROPHE, SLASH]
        bad_lines = []
        for line in self.first_col_data:
        # for line in ['τό ἡλιοτρόπιον']:
            non_greek_chars = self.grcRegExFinder.find_non_greek_symbols(line)
            # Исключаем символы, которые можно пока проигнорировать на данном этапе валидации. Позже к ним будет
            # более строгое отношение.
            non_greek_chars = [char for char in non_greek_chars if char not in ingored_on_this_step_chars]
            if non_greek_chars:
                bad_lines.append(f'{line} --> {non_greek_chars}')
                # bad_lines.append(f'{line}\n')
        return bad_lines

    # По ошибке AI иногда добавляет определённый артикль перед прилагательными. Нужно найти и исправить все такие случаи.
    def check_adjectives_dont_start_with_definite_article(self):
        # Регулярное выражение ищет текст в круглых скобках, который содержит хотя бы одну запятую.
        # [^)] – любой символ, кроме ).
        # [^)]* – снова любой символ, кроме ), сколько угодно раз. Это позволяет нам захватить содержимое после запятой до закрывающей скобки.
        pattern = re.compile(r'\(([^)]*?,[^)]*)\)')
        greek_article = ("ο ", "η ", "το ")
        bad_lines = []
        for line in self.first_col_data:
            # Три условия:
            # 1) начинается с определённого артикля
            # 2) само слово, следующее за артиклем начинается с маленькой буквы (отсеивает существительные вида: "ο Άγγλος (-Ιδα, η)")
            # 3. содержит текст в скобках, который содержит запятую
            if line.startswith(greek_article) and line.split()[1].islower() and pattern.search(line):
                bad_lines.append(line)
        return bad_lines

    # По ошибке вместо определённого артикля ж.р. "η" было добавлено "ή": "ή όρεξη" --> "η όρεξη".
    # Также иногда слово может иметь вид "H Κύπρος", что является двойной ошибкой:
    # 1) определённый артикль "η" написан с большой буквы (а должен быть написан с маленькой)
    # 2) определённый артикль только имеет вид буквы "ита", а на самом деле это английская большая "H", которую нужно
    # исправить на маленькую греческую букву "ита".
    def check_wrong_definite_article(self):
        EGNLISH_CAPITAL_AITCH = 'Η'

        wrong_start_sequences = (
            f'ή{SPACE}',
            f'{EGNLISH_CAPITAL_AITCH}{SPACE}',

            # Ищем случаи, когда артикль начинается с большой буквы
            # Singular
            f'{EllDefiniteArticleService.MASC_SG_NOM_ELL.capitalize()}{SPACE}',
            f'{EllDefiniteArticleService.FEM_SG_NOM_ELL.capitalize()}{SPACE}',
            f'{EllDefiniteArticleService.NEUT_SG_NOM_ELL.capitalize()}{SPACE}',
            # Plural
            f'{EllDefiniteArticleService.MASC_PL_NOM_ELL.capitalize()}{SPACE}',
            f'{EllDefiniteArticleService.FEM_PL_NOM_ELL.capitalize()}{SPACE}',
            f'{EllDefiniteArticleService.NEUT_PL_NOM_ELL.capitalize()}{SPACE}',
        )

        bad_lines = []
        for line in self.first_col_data:
            if line.startswith(wrong_start_sequences):
                bad_lines.append(line)
        return bad_lines

    def find_duplicates_among_1st_col_values(self):
        ignored_duplicates = [
            ''  # игнорируем пустую строку, т. к. она используется как логический разделитель между словами,
            # начинающимися с разных букв
        ]
        first_col_data = [row.split(PIPE)[0] for row in self.first_col_data if row.split(PIPE)[0] not in ignored_duplicates]
        duplicates = set([x for x in first_col_data if first_col_data.count(x) > 1])
        return duplicates

    def find_non_greek_symbols_after_stripping_nouns_and_adjectives(self):
        ignored_words = [
            'ό,τι', 'γι’αυτό', 'το σούπερ μάρκετ', 'η Νέα Υόρκη'
        ]

        results = []
        for line in self.first_col_data:
            if line not in ignored_words:
                # if line.startswith(self.ell_nom_definite_articles):
                if self.ellDefiniteArticleService.starts_with_definite_article(line):
                    # Стрипаем новогреческие артикли
                    line = self.ellDefiniteArticleService.strip_definite_article(line)
                elif self.grcDefiniteArticleService.starts_with_definite_article(line):
                    # Стрипаем древнегреческие артикли
                    line = self.grcDefiniteArticleService.strip_definite_article(line)

                # Со временем комментировать данное условие для большей строгости проверки
                if line.endswith(self.adj_endings):
                    line = line.split(',')[0]

                # Если после удаления артикля ПЕРЕД словом и окончаний прилагательных ПОСЛЕ слова, оно
                # не квалифицируется как слово, содержащее только разрешённые символы, добавляем его в результаты
                # для последующего вывода на экран и внимательного рассмотрения.
                if not self.grcRegExFinder.is_greek_word(line):
                    results.append(line)

        return results

    def print_sorted_data(self):
        sorted_data = sorted(self.first_col_data, key=self.make_sort_key)
        for line in sorted_data:
            print(line)

    # Формирует ключ для сортировки
    def make_sort_key(self, row):
        word = row.split(PIPE)[0]
        # Убираем перед ключом сортировки определённые артикли и их комбинации
        stripped_word = self.ellDefiniteArticleService.strip_definite_article(word)
        # Делаем ключ сортировки с маленькой буквы
        stripped_word = stripped_word.lower()
        # Убираем у ключа сортировки диакритику, чтобы она не влияла на порядок сортировки
        stripped_word = self.remove_greek_accents(stripped_word)
        return stripped_word

    # def strip_definite_article(self, word):
    #     # Компиляция регулярного выражения
    #     regex = re.compile(rf"^({'|'.join(map(re.escape, self.ell_nom_definite_articles))})\s+")
    #     stripped_word = regex.sub('', word)
    #     return stripped_word

    def remove_greek_accents(self, word):
        accents = {
            'ά': 'α',
            'έ': 'ε',
            'ή': 'η',
            'ί': 'ι',
            'ό': 'ο',
            'ύ': 'υ',
            'ώ': 'ω',
            'Ά': 'Α',
            'Έ': 'Ε',
            'Ή': 'Η',
            'Ί': 'Ι',
            'Ό': 'Ο',
            'Ύ': 'Υ',
            'Ώ': 'Ω'
        }
        for accented, plain in accents.items():
            word = word.replace(accented, plain)
        return word

    # Изначально у Рытовой и Хорикова прилагательные даются сразу с окончаниями, которые я переношу в поле
    # Front_comment, чтобы в поле Front осталась чистая лемма прилагательного, удобная как для работы пайплайна, так и
    # для озвучки в Анки.
    def strip_adj_endings_by_moving_them_to_front_comment(self):
        results = []
        for line in self.all_col_data:
            front, front_comment, back = line.split(PIPE)
            if front.endswith(self.adj_endings):
                new_front = front.split(',')[0]
                if front_comment:
                    new_front_comment = f'// {front}^^^{front_comment}'
                else:
                    new_front_comment = f'// {front}'
                new_back = back
                line = PIPE.join([new_front, new_front_comment, new_back])
            results.append(line)
        return results


######################################################################

if __name__ == '__main__':
    validator = RitovaKhorikovValidator()
    validator.run()
