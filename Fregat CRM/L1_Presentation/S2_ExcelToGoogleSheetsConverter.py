
from openpyxl import load_workbook
from pathlib import Path
import re

import Fregat_constants
from PhoneFieldProcessor import PhoneFieldProcessor

# 1. Читает ID из первого столбца Excel.
# 2. Получает обработанные контакты через PhoneFieldProcessor.process().
#    Поэтому порядок контактов, в том числе приоритет директора, сохранится.
# 3. Разделяет номер телефона и имя контакта на два столбца.
# 4. Преобразовывает телефон в формулу HYPERLINK.
# 5. Оставляет ID только в первой строке группы, а между разными записями добавляет пустую строку.
# 6. Опционально начинает обработку с указанного ID (starting_id),
#    игнорируя все предыдущие записи.
class ExcelToGoogleSheetsConverter:

    def __init__(self, input_file):
        self.input_file = Path(input_file)
        self.phone_field_processor = PhoneFieldProcessor()

    # 1. convert(starting_id=902) — начинает обработку с первой записи с ID 902 включительно.
    # 2. Все строки до найденного ID пропускаются без обработки телефонов.
    # 3. После нахождения ID обрабатываются все последующие записи независимо от их ID.
    # 4. Если указанный ID отсутствует, выбрасывается ValueError.
    # 5. ID корректно сравниваются даже в случае, когда в Excel он хранится как 902.0, а в аргументе передаётся 902.
    # Важная деталь: после нахождения starting_id фильтрация прекращается. То есть в результат попадут все последующие
    # записи, независимо от их ID. Это именно режим начала выгрузки с определённой позиции в Excel,
    # а не фильтрация по условию ID >= starting_id.
    # Всё это нужно для того, чтобы контакты клиентов, которые уже были прозвонены, не повторялись в выгрузке для работы
    # с последующими клиентами.
    def convert(self, starting_id=None):
        """
        Формирует TSV-текст для последующей вставки в Google Sheets.

        :param starting_id:
            ID записи, с которой необходимо начать обработку.
            Если None, обрабатывается весь Excel.
            Если ID указан, все предыдущие записи игнорируются.

        :return:
            Строка с данными в формате TSV.

        :raises ValueError:
            Если указанный starting_id отсутствует в Excel.
        """

        workbook = load_workbook(
            self.input_file,
            data_only=True
        )

        try:
            sheet = workbook.active

            headers = [
                cell.value
                for cell in sheet[1]
            ]

            phone_column_index = self._find_column_index(
                headers,
                Fregat_constants.PHONE_HEADER
            )

            director_column_index = self._find_column_index(
                headers,
                Fregat_constants.DIRECTOR_HEADER,
                required=False
            )

            record_blocks = []

            # Определяем, нужно ли искать начальный ID.
            # Если starting_id не передан, начинаем обработку сразу.
            starting_id_found = starting_id is None

            for row in sheet.iter_rows(
                min_row=2,
                values_only=True
            ):

                if all(value is None for value in row):
                    continue

                # ID записи всегда берётся из первого столбца
                record_id = row[0] if row else None

                if record_id is None:
                    continue

                # Пропускаем записи до тех пор, пока не встретим starting_id.
                # Сама запись с указанным ID включается в результат.
                if not starting_id_found:

                    if (
                        self._normalize_id(record_id)
                        != self._normalize_id(starting_id)
                    ):
                        continue

                    starting_id_found = True

                phone_value = row[phone_column_index]

                director_name = (
                    row[director_column_index]
                    if director_column_index is not None
                    else ""
                )

                # Получаем контакты с учётом сортировки директора
                processed_phones = self.phone_field_processor.process(
                    phone_value,
                    director_name
                )

                contacts = self._extract_contacts(processed_phones)

                if not contacts:
                    continue

                record_lines = []

                for contact_index, (phone, contact_name) in enumerate(contacts):

                    # ID записывается только в первой строке группы
                    current_id = (
                        self._clean_tsv_value(record_id)
                        if contact_index == 0
                        else ""
                    )

                    hyperlink = self._create_hyperlink(phone)

                    record_lines.append(
                        "\t".join([
                            current_id,
                            hyperlink,
                            self._clean_tsv_value(contact_name)
                        ])
                    )

                record_blocks.append(
                    "\n".join(record_lines)
                )

            # Проверяем, удалось ли найти starting_id
            if not starting_id_found:
                raise ValueError(
                    f"Запись с ID '{starting_id}' не найдена в Excel."
                )

            # Между разными записями оставляем пустую строку
            return "\n\n".join(record_blocks)

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

    def _find_column_index(self, headers, column_name, required=True):
        """
        Находит индекс столбца по названию.
        """

        column_index = next(
            (
                index
                for index, header in enumerate(headers)
                if header is not None
                and str(header).strip().upper() == column_name
            ),
            None
        )

        if column_index is None and required:
            raise ValueError(
                f"В Excel отсутствует столбец '{column_name}'"
            )

        return column_index

    def _extract_contacts(self, processed_phones):
        """
        Извлекает телефон и имя из результата PhoneFieldProcessor.

        Формат исходной строки:
        +380501112233 - Иванов Иван
        """

        contacts = []

        for line in processed_phones.splitlines():

            line = line.strip()

            if not line or line.upper() == f"{Fregat_constants.PHONE_HEADER}:":
                continue

            phone, separator, contact_name = line.partition(" - ")

            if not separator:
                # Если разделителя нет, проверяем, действительно ли
                # полученная строка содержит телефон.
                if any(char.isdigit() for char in phone):
                    contact_name = ""
                else:
                    contact_name = phone
                    phone = ""

            contacts.append((
                phone.strip(),
                contact_name.strip()
            ))

        return contacts

    def _create_hyperlink(self, phone):
        """
        Формирует формулу Google Sheets:

        =HYPERLINK("tel:+380664800418", "+38 066 480 04 18")
        """

        if not phone:
            return ""

        digits = re.sub(r"\D", "", phone)

        if not digits:
            return ""

        # Убираем международный префикс 00, если он присутствует
        if digits.startswith("00"):
            digits = digits[2:]

        # Приводим украинский номер без кода страны к международному виду
        # Например: 0664800418 -> +380664800418
        if len(digits) == 10 and digits.startswith("0"):
            digits = "38" + digits

        international_phone = f"+{digits}"

        # Форматируем украинский номер для визуального отображения
        if digits.startswith("380") and len(digits) == 12:

            visible_phone = (
                f"+38 {digits[2:5]} "
                f"{digits[5:8]} "
                f"{digits[8:10]} "
                f"{digits[10:12]}"
            )

        else:
            # Для номеров других форматов сохраняем исходное отображение
            visible_phone = phone.strip()

        return (
            f'=HYPERLINK("tel:{international_phone}", '
            f'"{visible_phone}")'
        )

    @staticmethod
    def _clean_tsv_value(value):
        """
        Убирает табуляции и переносы строк, чтобы они
        не нарушали структуру трёх столбцов.
        """

        if value is None:
            return ""

        if isinstance(value, float) and value.is_integer():
            value = int(value)

        return re.sub(
            r"[\t\r\n]+",
            " ",
            str(value)
        ).strip()


############################################################################################

if __name__ == "__main__":

    converter = ExcelToGoogleSheetsConverter(
        input_file=r"E:\! Documents\Artem\Work\Завод 'Фрегат'\для создания CRM.xlsx"
    )

    # Обработка всего Excel
    # result = converter.convert()

    # Обработка начиная с записи с ID 902 включительно
    result = converter.convert(starting_id=900)

    # Допускается также передача ID в виде строки
    # result = converter.convert(starting_id="902")

    print(result)
