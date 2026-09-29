import pprint
from collections import Counter

import xlrd

import AppContext
from FilenameUtils import FilenameUtils
from MultilingualWorksheetReaders import MultilingualFirstColumnWorksheetReader, \
    MultilingualFirstTwoColumnsWorksheetReader, MultilingualFirstThreeColumnsWorksheetReader
from View_enums import CurrentLanguageComboBoxEnum


class MultilingualExcelDao:
    def __init__(self, lang_code=None):
        self.filenameUtils = FilenameUtils(lang_code)

        # Worksheet readers
        self.multilingualFirstColumnWorksheetReader = MultilingualFirstColumnWorksheetReader()
        self.multilingualFirstTwoColumnsWorksheetReader = MultilingualFirstTwoColumnsWorksheetReader()
        self.multilingualFirstThreeColumnsWorksheetReader = MultilingualFirstThreeColumnsWorksheetReader()

        # Business collections. Все три коллекции во внутреннем представлении Dao-объекта являются СПИСКАМИ (строк или
        # кортежей строк), чтобы их было удобно валидировать на уникальность.
        # Наружу некоторые из них отдаются в виде словарей.
        self.ignored_tokens = []
        self.manual_lemmas = []
        self.morph_forms = []

        self._fill_business_collections()

    def get_ignored_tokens(self):
        return self.ignored_tokens

    def get_manual_lemmas_dict(self):
        manual_lemmas_dict = {token: lemma for token, lemma in self.manual_lemmas}
        return manual_lemmas_dict

    def get_morph_forms_dict(self):
        morph_forms_dict = {token_grammaticized: piped_row for token_grammaticized, piped_row in self.morph_forms}
        return morph_forms_dict

    def _fill_business_collections(self):
        # Для каждого иностранного языка в базовой для него папке может храниться несколько Excel-файлов. Каждый такой
        # файл будет хранить информацию из того или иного сериала, или учебника. Заполняем коллекции ignored_tokens,
        # manual_lemmas_dict и morph_forms_dict проходясь сквозняком по всем Excel-файлам и всем листам в пределах
        # каждого файла.
        excel_filenames = self.filenameUtils.get_all_excel_filenames()
        for excel_filename in excel_filenames:
            workbook = xlrd.open_workbook(excel_filename)
            for sheet_name in workbook.sheet_names():
                sheet = workbook.sheet_by_name(sheet_name)
                # Проверяем шаблон на ВХОЖДЕНИЕ в название листа, а не на РАВЕНСТВО названию листа. Это даёт большую
                # гибкость в хранении в одной Excel-книге ignored_tokens-листов для разных случаев:
                # "ignored_tokens (A1)", "ignored_tokens (A2)", "ignored_tokens (B1)" и т. д. Это же правило относится
                # и к 'manual_lemmas'-листам и 'morph_forms'-листам.
                if 'ignored_tokens' in sheet_name:
                    sheet_ignored_tokens = self._get_ignored_tokens_from_excel(sheet)
                    self.ignored_tokens.extend(sheet_ignored_tokens)
                elif 'manual_lemmas' in sheet_name:
                    sheet_manual_lemmas = self._get_manual_lemmas_from_excel(sheet)
                    self.manual_lemmas.extend(sheet_manual_lemmas)
                elif 'morph_forms' in sheet_name:
                    sheet_morph_forms = self._get_morph_forms_from_excel(sheet)
                    self.morph_forms.extend(sheet_morph_forms)
        # После заполнения коллекций данными из Excel, валидируем их уникальность, т. е. боремся с дубликатами
        self._validate_1st_column_uniqueness()

    # Вычитывает игнорируемые токены
    def _get_ignored_tokens_from_excel(self, sheet):
        sheet_ignored_tokens = self.multilingualFirstColumnWorksheetReader.get_data_from_worksheet(sheet)
        return sheet_ignored_tokens

    # Вычитывает "ручные" леммы, т. е. леммы тех слов, которые spaCy не смог правильно лемматизировать
    def _get_manual_lemmas_from_excel(self, sheet):
        sheet_manual_lemmas = self.multilingualFirstTwoColumnsWorksheetReader.get_data_from_worksheet(sheet)
        return sheet_manual_lemmas

    # Вычитывает морфологические формы
    def _get_morph_forms_from_excel(self, sheet):
        sheet_morph_forms = self.multilingualFirstThreeColumnsWorksheetReader.get_data_from_worksheet(sheet)
        return sheet_morph_forms

    def _validate_1st_column_uniqueness(self):
        msg = "'{}' collection contains duplicates: {}"
        messages = []

        def _find_duplicates(lst):
            return [item for item, count in Counter(lst).items() if count > 1]

        # Здесь должен быть именно столбик if-ов, но не if-elif-elif
        # Step 1. Валидируем уникальность ignored_tokens
        if len(self.ignored_tokens) != len(set(self.ignored_tokens)):
            duplicates = _find_duplicates(self.ignored_tokens)
            messages.append(msg.format('ignored_tokens', duplicates))

        # Две нижеследующие коллекции будут отдаваться вызывающему коду в виде словарей, поэтому дополнительно
        # проверять уникальность значений в 1-м столбце!
        # Step 2. Валидируем уникальность manual_lemmas
        if len(self.manual_lemmas) != len(set(self.manual_lemmas)):
            duplicates = _find_duplicates(self.manual_lemmas)
            messages.append(msg.format('manual_lemmas', duplicates))
        # Проверка уникальности token в manual_lemmas
        tokens = [token for token, _ in self.manual_lemmas]  # Извлекаем только token
        if len(tokens) != len(set(tokens)):
            duplicates = _find_duplicates(tokens)
            messages.append(msg.format('manual_lemmas (tokens)', duplicates))

        # Step 3. Валидируем уникальность morph_forms
        if len(self.morph_forms) != len(set(self.morph_forms)):
            duplicates = _find_duplicates(self.morph_forms)
            messages.append(msg.format('morph_forms', duplicates))
        # Проверка уникальности token в morph_forms
        token_grammaticized_lst = [token_grammaticized for token_grammaticized, _ in self.morph_forms]  # Извлекаем только token_grammaticized
        if len(token_grammaticized_lst) != len(set(token_grammaticized_lst)):
            duplicates = _find_duplicates(token_grammaticized_lst)
            messages.append(msg.format('morph_forms (token_grammaticized)', duplicates))

        if messages:
            raise Exception('\n'.join(messages))

    def pretty_print_all_collections(self):
        pprint.pprint(self.ignored_tokens)
        print(len(self.ignored_tokens))
        print('\n* * *\n')
        pprint.pprint(self.manual_lemmas)
        print(len(self.manual_lemmas))
        print('\n* * *\n')
        pprint.pprint(self.morph_forms)
        print(len(self.morph_forms))

    # При нормально написанной валидации коллекций, данный метод фактически не нужен. Он нужен как средство проверки
    # самого алгоритма валидации.
    def test_corresponding_collections_len(self):
        if len(self.ignored_tokens) != len(self.get_ignored_tokens()):
            raise Exception('len(self.ignored_tokens) != len(self.get_ignored_tokens())')
        if len(self.manual_lemmas) != len(self.get_manual_lemmas_dict()):
            raise Exception('len(self.manual_lemmas) != len(self.get_manual_lemmas_dict())')
        if len(self.morph_forms) != len(self.get_morph_forms_dict()):
            raise Exception('len(self.morph_forms) != len(self.get_morph_forms_dict())')


###########################################################################

if __name__ == '__main__':
    language = CurrentLanguageComboBoxEnum.GERMAN.value
    # language = CurrentLanguageComboBoxEnum.MODERN_GREEK.value
    # language = CurrentLanguageComboBoxEnum.ANCIENT_GREEK.value
    AppContext.switch_language(language)

    multilingualExcelDao = MultilingualExcelDao()
    # multilingualExcelDao.pretty_print_all_collections()

    pprint.pprint(multilingualExcelDao.get_ignored_tokens())
    print(len(multilingualExcelDao.get_ignored_tokens()))
    print('\n* * *\n')
    pprint.pprint(multilingualExcelDao.get_manual_lemmas_dict())
    print(len(multilingualExcelDao.get_manual_lemmas_dict()))
    print('\n* * *\n')
    pprint.pprint(multilingualExcelDao.get_morph_forms_dict())
    print(len(multilingualExcelDao.get_morph_forms_dict()))

    # multilingualExcelDao.test_corresponding_collections_len()
