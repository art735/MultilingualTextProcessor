import xlrd

import ExcelDaoUtils
import FileContentsSplitter
import GermanExcelWorkbooksDao
from GermanPronounDeclensionEntity import GermanPronounDeclensionEntity


class GermanPronounDeclensionDao:

    def __init__(self):
        self.workbook = xlrd.open_workbook(GermanExcelWorkbooksDao.deutsch_lexikon_popov_excel_filename)

        # На основании объекта КНИГИ файла Excel, сформировать объекты ЛИСТОВ файла Excel
        self.articles_and_pronouns_worksheet = self.workbook.sheet_by_name('Articles & Pronouns')

    def convert_excel_rows_to_entities(self):

        tuples = self._get_tuples()

        # Разбиваем список кортежей на список списков, где разделителем служит строка, содержащая лемму слова
        delimiter_cb = lambda row: True if row[0] else False
        # Добавляем строку в результаты ВСЕГДА, т. е. без дополнительных условий
        addition_condition_cb = lambda row: True
        grouped_sheet_data = FileContentsSplitter.split_file_contents_by_delimiter(
            tuples, delimiter_cb, addition_condition_cb, include_line_with_delimiter_in_results=True)

        # Удаляем кортежи, состоящие полностью из пустых строк
        # any(t) returns True if any item in an iterable are true, otherwise it returns False
        grouped_sheet_data = [[tup for tup in sublist if any(tup)] for sublist in grouped_sheet_data]

        results = []
        for pronoun_rows in grouped_sheet_data:
            pronoun_declension_entity = GermanPronounDeclensionEntity()
            for i in range(0, len(pronoun_rows)):
                row = pronoun_rows[i]

                # если работаем с 1-й строкой местоимения (строкой, содержащей лемму, транскрипцию и перевод)
                if i == 0:
                    # TODO: подумать как различать sie (sg.) и sie (pl.): лемма у них одинаковая
                    pronoun_declension_entity.lemma = row[0]
                    pronoun_declension_entity.transcription = row[1]
                    pronoun_declension_entity.translation = row[2]

                match i:
                    case 0:
                        case_abbr = 'N '
                    case 1:
                        case_abbr = 'G '
                    case 2:
                        case_abbr = 'D '
                    case 3:
                        case_abbr = 'A '

                row_declensions = self.convert_tuple_to_ready_string(row, 3)
                row_transcriptions = self.convert_tuple_to_ready_string(row, 4)

                pronoun_declension_entity.declensions.front.append(case_abbr + row_declensions)
                pronoun_declension_entity.declensions.transcription.append(row_transcriptions)

            results.append(pronoun_declension_entity)

        return results

    def _get_tuples(self):
        # articles_and_pronouns_worksheet_indices = [[0, 1], [4, 5], [6, 7], [8, 9], [10, 11]]
        articles_and_pronouns_worksheet_indices = [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11]
        articles_and_pronouns_worksheet_tuples = ExcelDaoUtils.getWorksheetData(self.articles_and_pronouns_worksheet,
                                                                                articles_and_pronouns_worksheet_indices)

        return articles_and_pronouns_worksheet_tuples

    def convert_tuple_to_ready_string(self, tup, start_index):
        # Список, где элементы берутся с шагом 2, и при этом фильтруются, чтобы исключить пустые строки.
        # Словоформы начинаются с start_index=1, а их транскрипции начинаются с start_index=2
        filtered_values = [item for item in tup[start_index::2] if item]
        if len(filtered_values) > 1:
            # Значения строки должны быть объединены с помощью запятых, а последний элемент (мн. ч.) отделяется
            # точкой запятой.
            sg_piece = ', '.join(filtered_values[:-1])
            pl_piece = filtered_values[-1]
            line = f'{sg_piece}; {pl_piece}'
        elif filtered_values:
            line = filtered_values[0]
        else:
            line = ''
        return line


##############################################

if __name__ == '__main__':
    germanPronounDeclensionDao = GermanPronounDeclensionDao()

    res = germanPronounDeclensionDao.convert_excel_rows_to_entities()
    [print(r) for r in res]
