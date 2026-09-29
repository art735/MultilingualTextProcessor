import ExcelDaoUtils


def get_tuples(numerals_worksheet):
    # первых две пары - это комбинации [число(в цифровом выражении), транскрипция] и [число(в буквенном выражении), транскрипция]
    numerals_worksheet_indices = [[0, 2], [1, 2], [4, 5], [7, 8], [9, 10], [11, 12], [13, 14]]
    numerals_worksheet_tuples = ExcelDaoUtils.getWorksheetData(numerals_worksheet, numerals_worksheet_indices)
    return numerals_worksheet_tuples
