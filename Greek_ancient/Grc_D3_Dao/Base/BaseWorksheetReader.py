import itertools


class BaseWorksheetReader:

    def __init__(self, columns_dict):
        self.columns_dict = columns_dict

    def get_data_from_worksheet(self, worksheet):
        worksheet_indices = self.columns_dict.keys()

        columns_list = []
        for i in worksheet_indices:
            columns_list.append(worksheet.col_values(i))  # вычитываем данные из конкретного столбца Excel-листа

        # склеиваем список столбцов Excel так, чтобы получился список строк Excel
        sheet_data = list(itertools.zip_longest(*columns_list, fillvalue=""))

        return sheet_data
