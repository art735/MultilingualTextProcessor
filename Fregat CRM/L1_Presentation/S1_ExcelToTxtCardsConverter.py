from openpyxl import load_workbook
from pathlib import Path

import Fregat_constants
from PhoneFieldProcessor import PhoneFieldProcessor


class ExcelToTxtCardsConverter:

    def __init__(self, input_file):
        self.input_file = Path(input_file)
        self.phone_field_processor = PhoneFieldProcessor()

    def convert(self, starting_id=None):
        """
        Конвертирует данные Excel в текстовые карточки.

        :param starting_id:
            ID записи, с которой необходимо начать обработку.
            Если None, обрабатывается весь Excel.
            Если ID указан, все предыдущие записи игнорируются.
        """

        workbook = load_workbook(
            self.input_file,
            data_only=True  # Получаем вычисленные значения формул, если они сохранены в Excel
        )

        try:
            sheet = workbook.active

            headers = [
                cell.value
                for cell in sheet[1]
            ]

            cards = []

            # Если starting_id не передан, начинаем обработку сразу.
            starting_id_found = starting_id is None

            for row in sheet.iter_rows(
                min_row=2,
                values_only=True  # Получаем непосредственно значения ячеек, без объектов Cell
            ):
                if all(value is None for value in row):
                    continue

                # ID записи всегда берётся из первого столбца Excel
                record_id = row[0] if row else None

                # Пропускаем записи до тех пор, пока не встретим starting_id.
                # Сама запись с указанным ID включается в результат.
                if not starting_id_found:

                    if record_id is None:
                        continue

                    if (
                        self._normalize_id(record_id)
                        != self._normalize_id(starting_id)
                    ):
                        continue

                    starting_id_found = True

                card = self._process_row(
                    headers,
                    row
                )
                cards.append(card)

            # Проверяем, удалось ли найти starting_id
            if not starting_id_found:
                raise ValueError(
                    f"Запись с ID '{starting_id}' не найдена в Excel."
                )

            result = "\n\n\n".join(cards)

            print(result)

            # Диагностический вывод
            # print("Путь к файлу:", self.input_file.resolve())
            # print("Листы книги:", workbook.sheetnames)
            # print("Активный лист:", sheet.title)
            # print("Заголовки столбцов:", headers)

        finally:
            workbook.close()

    @staticmethod
    def _normalize_id(value):
        """
        Нормализует ID для корректного сравнения.

        Например:
        902 == 902.0 == "902"
        """

        if isinstance(value, float) and value.is_integer():
            value = int(value)

        return str(value).strip()

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

    # Обработка всего Excel
    # converter.convert()

    # Обработка начиная с записи с ID 902 включительно
    converter.convert(starting_id=902)

    # Допускается также передача ID в виде строки
    # converter.convert(starting_id="902")