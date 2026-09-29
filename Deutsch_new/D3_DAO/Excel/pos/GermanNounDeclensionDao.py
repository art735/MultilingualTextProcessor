import xlrd

import ExcelDaoUtils
import FileContentsSplitter
from CharConstants import SLASH
from GermanExcelWorkbooksDao import GermanExcelWorkbooksDao
from GermanNounDeclensionEntity import GermanNounDeclensionEntity

nouns_worksheet_indices = [0, 1, 2, 4, 5, 6, 7]


def get_tuples():
    noun_tuples = []
    for filename in GermanExcelWorkbooksDao.all_excel_filenames:
        workbook = xlrd.open_workbook(filename)
        nouns_worksheet = workbook.sheet_by_name('Nouns')
        nouns_worksheet_tuples = ExcelDaoUtils.getWorksheetData(nouns_worksheet, nouns_worksheet_indices)
        noun_tuples.extend(nouns_worksheet_tuples)

    return noun_tuples


# Реализует логику вычитки существительных из Excel-файлов из листа 'Nouns'.
class GermanNounDeclensionDao:

    def __init__(self):
        self.current_noun_entity = None  # заполняется по частям в разных методах, поэтому сделана полем класса

    def convert_excel_rows_to_entities(self):

        tuples = get_tuples()

        # Разбиваем список кортежей на список списков, где разделителем служит строка, содержащая слово в 0-м столбце
        # (начальная форма слова)
        delimiter_cb = lambda row: True if row[0] else False
        # Добавляем строку в результаты ВСЕГДА, т. е. без дополнительных условий
        addition_condition_cb = lambda row: True
        grouped_sheet_data = FileContentsSplitter.split_file_contents_by_delimiter(
            tuples, delimiter_cb, addition_condition_cb, include_line_with_delimiter_in_results=True)

        # Удаляем кортежи, состоящие полностью из пустых строк
        # any(t) returns True if any item in an iterable are true, otherwise it returns False
        grouped_sheet_data = [[tup for tup in sublist if any(tup)] for sublist in grouped_sheet_data]
        noun_entities = []
        for noun_rows in grouped_sheet_data:
            self.current_noun_entity = GermanNounDeclensionEntity()
            for i, noun_row in enumerate(noun_rows):
                # если работаем с 1-й строкой существительного (строкой, содержащей слово, транскрипцию и перевод)
                if i == 0:
                    self.current_noun_entity.word = noun_row[0]
                    self.current_noun_entity.transcription = noun_row[1]
                    self.current_noun_entity.translation = noun_row[2]
                    # Здесь используются индексы не в пределах Excel-листа, а в пределах noun_row!
                    # Отличие состоит в том, что в Excel-листе имеется пустой столбец между словом и его падежными
                    # формами, а в noun_row этого пустого столбца нет, поэтому индексы падежных форм смещены на 1.
                    # Конвертируем pl. nom.
                    self._convert_row_to_entity(noun_row, 5)
                else:  # конвертируем падежные формы для gen., dat., acc.
                    # sg.-часть
                    self._convert_row_to_entity(noun_row, 3)
                    # pl.-часть
                    self._convert_row_to_entity(noun_row, 5)
            # end of inner loop
            noun_entities.append(self.current_noun_entity)
        # end of outer loop
        return noun_entities

    def _convert_row_to_entity(self, noun_row, start_index):
        front = noun_row[start_index]
        transcription = noun_row[start_index + 1]

        # Если ячейка содержит слеш (нередкая для существительных ситуация, особенно для формы gen. sg.)
        # des Bahnhofes / des Bahnhofs	[ˈbaːnˌhoːfəs] / [ˈbaːnˌhoːfs]
        if SLASH in front:
            if SLASH not in transcription:
                raise Exception(f"Noun form '{front}' contains slash, but its corresponding transcription - not!")
            front_pieces = front.split(SLASH)
            transcription_pieces = noun_row[start_index + 1].split(SLASH)
            for front_piece, transcription_piece in zip(front_pieces, transcription_pieces):
                self._add_front_and_transcription(front_piece, transcription_piece)
        else:
            self._add_front_and_transcription(front, transcription)

    def _add_front_and_transcription(self, front, transcription):
        front = front.strip()
        transcription = transcription.strip()
        if front:
            self.current_noun_entity.declensions_dict[front] = transcription


####################################################################################

if __name__ == '__main__':
    germanNounDao = GermanNounDeclensionDao()

    # noun_tuples = germanNounDao._get_tuples()
    # print(len(noun_tuples))
    # [print(t) for t in noun_tuples]

    noun_entities = germanNounDao.convert_excel_rows_to_entities()
    print(len(noun_entities))
    [print(ne) for ne in noun_entities]
