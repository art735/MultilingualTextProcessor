from Base.BaseWorksheetReader import BaseWorksheetReader
from ExcelEntities.EBibleLexiconEntity import EBibleLexiconEntity


class EBibleLexiconWorksheetReader(BaseWorksheetReader):

    def __init__(self):
        columns_dict = {
            0: 'LEMMA_COLUMN_INDEX',
            1: 'LEMMA_OCCURRENCES_COUNT_COLUMN_INDEX',
            2: 'MORPHOLOGICAL_FORMS_COLUMN_INDEX',
            3: 'WORD_ARTICLE_COLUMN_INDEX',
            4: 'TRANSLATION_COLUMN_INDEX'
        }
        super().__init__(columns_dict)

    def get_data_from_worksheet(self, worksheet):
        sheet_data = super().get_data_from_worksheet(worksheet)

        # В результате склейки столбцов получаем следующие индексы данных:
        # 0 - lemma
        # 1 - lemma occurrences
        # 2 - morphological forms
        # 3 - word article
        # 4 - translation

        # KEY - lemma
        # VALUE - all the consecutive Excel rows related to KEY
        result = []
        for row in sheet_data:
            lemma = row[0]
            lemma_occurrences_count = row[1]
            morphological_forms_str = row[2]
            word_article = row[3]
            translation = row[4]
            result.append(
                EBibleLexiconEntity(lemma, lemma_occurrences_count, morphological_forms_str, word_article, translation))

        return result
