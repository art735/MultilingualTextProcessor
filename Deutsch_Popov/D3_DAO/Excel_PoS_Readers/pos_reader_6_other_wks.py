import ExcelDaoUtils


def get_tuples(other_worksheet):
    other_worksheet_indices = [0, 1]
    other_worksheet_tuples = ExcelDaoUtils.getWorksheetData(other_worksheet, other_worksheet_indices)
    return other_worksheet_tuples
