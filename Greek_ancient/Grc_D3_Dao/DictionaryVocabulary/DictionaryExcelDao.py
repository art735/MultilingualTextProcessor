from GrcRegExFinder import GrcRegExFinder
from BaseExcelDao import BaseExcelDao
from DictionaryVocabularyWorksheetReader import DictionaryVocabularyWorksheetReader


class DictionaryExcelDao(BaseExcelDao):
    def __init__(self):
        # параметры, определяемые на этом уровне и передаваемые в базовый класс
        self.workbook_filename = 'Ancient Greek/John Gresham Machen (dictionary).xls'
        self.worksheetReader = DictionaryVocabularyWorksheetReader()
        self.grcRegExFinder = GrcRegExFinder()
        # вызов конструктора базового класса
        super().__init__(self.workbook_filename, self.worksheetReader)


###########################################################################

dictionaryExcelDao = DictionaryExcelDao()

# dictionaryExcelDao.print_all_data()

# res = dictionaryExcelDao.get_1st_col_words_for_validation()
# print(res)
# print(len(res))
