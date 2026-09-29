from GrcRegExFinder import GrcRegExFinder
from BaseExcelDao import BaseExcelDao
from MorphFormsWorksheetReader import MorphFormsWorksheetReader


class MorphFormsExcelDao(BaseExcelDao):
    def __init__(self):
        # параметры, определяемые на этом уровне и передаваемые в базовый класс
        self.workbook_filename = 'Ancient Greek/John Gresham Machen (morph forms).xls'
        self.worksheetReader = MorphFormsWorksheetReader()
        self.grcRegExFinder = GrcRegExFinder()
        # вызов конструктора базового класса
        super().__init__(self.workbook_filename, self.worksheetReader)


###########################################################################

morphFormsExcelDao = MorphFormsExcelDao()

# morphFormsExcelDao.print_all_data()

# res = morphFormsExcelDao.get_1st_col_words_for_validation()
# print(res)
# print(len(res))
