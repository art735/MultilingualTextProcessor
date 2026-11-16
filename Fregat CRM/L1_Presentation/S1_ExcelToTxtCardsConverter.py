from openpyxl import load_workbook
from pathlib import Path

import Fregat_constants
from PhoneFieldProcessor import PhoneFieldProcessor


class ExcelToTxtCardsConverter:

    def __init__(self, input_file):
        self.input_file = Path(input_file)
        self.phone_field_processor = PhoneFieldProcessor()

    def convert(self):
        workbook = load_workbook(
            self.input_file,
            data_only=True  # Получаем вычисленные значения формул, если они сохранены в Excel
        )

        sheet = workbook.active

        headers = [
            cell.value
            for cell in sheet[1]
        ]

        cards = []

        for row in sheet.iter_rows(
            min_row=2,
            values_only=True  # Получаем непосредственно значения ячеек, без объектов Cell
        ):
            if all(value is None for value in row):
                continue

            card = self._process_row(
                headers,
                row
            )
            cards.append(card)

        result = "\n\n\n".join(cards)

        print(result)

        # Диагностический вывод
        # print("Путь к файлу:", self.input_file.resolve())
        # print("Листы книги:", workbook.sheetnames)
        # print("Активный лист:", sheet.title)
        # print("Заголовки столбцов:", headers)

        workbook.close()

    def _process_row(self, headers, row):
        fields = []

        director_column_index = next(
            (
                index
                for index, header in enumerate(headers)
                if header is not None
                and str(header).strip().upper() == Fregat_constants.DIRECTOR_HEADER
            ),
            None
        )

        director_full_name = (
            row[director_column_index]
            if director_column_index is not None
            else ""
        )

        director_full_name = str(director_full_name or "").strip()

        for header, value in zip(headers, row):

            if header is None:
                continue

            if value is None:
                value = ""

            if str(header).strip().upper() == Fregat_constants.PHONE_HEADER:

                # Разбиваем строку с телефонами на отдельные записи по символу ";"
                # Удаляем пробельные символы по краям и префикс "tel:"
                # Разделяем номер телефона и имя контакта по первому дефису,
                # удаляя пробельные символы по краям и отбрасывая пустые части
                # Объединяем непустые части через нормализованный разделитель " - "
                # и добавляем табуляцию в начале строки
                # Формируем итоговое поле с заголовком и списком телефонов
                field = self.phone_field_processor.process(
                    value,
                    director_full_name
                )

            else:
                field = f"{header}: {value}"

            fields.append(field)

        return "\n".join(fields)


############################################################################################

if __name__ == "__main__":
    converter = ExcelToTxtCardsConverter(
        input_file=r"E:\! Documents\Artem\Work\Завод 'Фрегат'\для создания CRM.xlsx"
    )

    converter.convert()