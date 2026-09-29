from GrcRegExFinder import GrcRegExFinder
from BaseExcelDao import BaseExcelDao
from EBibleLexiconWorksheetReader import EBibleLexiconWorksheetReader


class EBibleLexiconExcelDao(BaseExcelDao):
    def __init__(self):
        # параметры, определяемые на этом уровне и передаваемые в базовый класс
        self.workbook_filename = 'Ancient Greek/eBible lexicon.xls'
        self.worksheetReader = EBibleLexiconWorksheetReader()
        self.grcRegExFinder = GrcRegExFinder()
        # вызов конструктора базового класса
        super().__init__(self.workbook_filename, self.worksheetReader)


###########################################################################

eBibleLexiconExcelDao = EBibleLexiconExcelDao()

# eBibleLexiconExcelDao.print_all_data()

# res = eBibleLexiconExcelDao.get_1st_col_words_for_validation()
# print(res)
# print(len(res))
