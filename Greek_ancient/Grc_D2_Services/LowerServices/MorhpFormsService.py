from MorphFormsExcelDao import MorphFormsExcelDao


class MorphFormsService:
    def __init__(self):
        self.morphFormsExcelDao = MorphFormsExcelDao()
        self.excel_morph_forms_dict = self.morphFormsExcelDao.get_all_sheets_data_dict()

    # Выясняем присутствует ли форма слова в первом столбце
    def is_word_among_1st_col_words(self, word):
        if word in self.excel_morph_forms_dict.keys():
            return True
        return False
