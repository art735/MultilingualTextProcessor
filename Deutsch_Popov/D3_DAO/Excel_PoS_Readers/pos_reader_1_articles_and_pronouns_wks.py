import ExcelDaoUtils

articles_and_pronouns_worksheet_indices = [[0, 1], [4, 5], [6, 7], [8, 9], [10, 11]]


def get_tuples(articles_and_pronouns_worksheet):
    articles_and_pronouns_worksheet_tuples = ExcelDaoUtils.getWorksheetData(articles_and_pronouns_worksheet,
                                                                            articles_and_pronouns_worksheet_indices)
    return articles_and_pronouns_worksheet_tuples
