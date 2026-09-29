from Base.BaseWorksheetReader import BaseWorksheetReader
from ExcelEntities.DictionaryVocabularyEntity import DictionaryVocabularyEntity


class DictionaryVocabularyWorksheetReader(BaseWorksheetReader):  # наследуется от BaseWorksheetReader

    def __init__(self):
        columns_dict = {
            0: 'LEMMA_COLUMN_INDEX',
            # 1: 'LEMMA_OCCURRENCES_COUNT_COLUMN_INDEX',
            1: 'MORPHOLOGICAL_FORMS_COLUMN_INDEX',
            2: 'WORD_ARTICLE_COLUMN_INDEX',
            3: 'TRANSLATION_COLUMN_INDEX'
        }
        super().__init__(columns_dict)

    def get_data_from_worksheet(self, worksheet):
        sheet_data = super().get_data_from_worksheet(worksheet)

        # В результате склейки столбцов получаем следующие индексы данных:
        # 0 - lemma
        # 1 - morphological forms
        # 2 - word article
        # 3 - translation

        # KEY - lemma
        # VALUE - all the consecutive Excel rows related to KEY
        result = []
        for row in sheet_data:
            lemma = row[0]
            # lemma_occurrences_count = row[1]
            # lemma_occurrences_count = -1  # фиксированное значение просто как заполнитель
            morphological_forms_str = row[1]
            word_article = row[2]
            translation = row[3]
            result.append(DictionaryVocabularyEntity(lemma, morphological_forms_str, word_article, translation))

        return result
