



class PhoneFieldProcessor:

    DIRECTOR_MARKER = "(директор)"

    def process(self, value, director_full_name=None):
        """
        Обрабатывает поле с телефонами.

        Контакты директора перемещаются в начало списка.

        :param value: Строка с телефонными записями.
        :param director_full_name: Полное ФИО директора.
        :return: Отформатированная строка с телефонами.
        """

        phones = str(value if value is not None else "").split(";")

        contacts = []

        for phone in phones:

            # Пропускаем пустые записи
            if not phone.strip():
                continue

            # Удаляем пробелы по краям и префикс "tel:"
            phone = phone.strip().removeprefix("tel:")

            # Разделяем номер телефона и имя контакта
            parts = [
                part.strip()
                for part in phone.split("-", maxsplit=1)
                if part.strip()
            ]

            # Формируем строку контакта
            formatted_phone = "\t" + " - ".join(parts)

            # Определяем имя контакта
            contact_name = parts[1] if len(parts) > 1 else ""

            # Проверяем, является ли контакт контактом директора
            is_director = self._is_director(
                contact_name,
                director_full_name
            )

            contacts.append((is_director, formatted_phone))

        # Сортировка стабильная:
        # контакты директора перемещаются в начало,
        # порядок остальных контактов сохраняется.
        contacts.sort(
            key=lambda contact: not contact[0]
        )

        phone_lines = [
            formatted_phone
            for _, formatted_phone in contacts
        ]

        return "ТЕЛЕФОНЫ:\n" + "\n".join(phone_lines)

    def _is_director(self, contact_name, director_full_name):
        """
        Определяет, является ли контакт контактом директора.
        """

        normalized_contact_name = contact_name.strip().casefold()

        # Условие 1: имя содержит маркер/подстроку "(директор)"
        if self.DIRECTOR_MARKER.casefold() in normalized_contact_name:
            return True

        # Условие 2: имя полностью совпадает с ФИО директора
        if director_full_name:
            normalized_director_name = director_full_name.strip().casefold()

            if normalized_contact_name == normalized_director_name:
                return True

        return False

############################################################################################

phone_field = (
    " tel:+380501112233 - Иванов Иван ;"
    ";"
    "tel:+380672223344 - Петров Пётр;"
    " "
    "tel:+380633334455 - Сидоров Сидор "
)

# Контакт с подстрокой '(директор)' должен идти первым.
phone_field = (
    "tel:+380501112233 - Иванов Иван;"
    "tel:+380672223344 - Петров Пётр (директор);"
    "tel:+380633334455 - Сидоров Сидор"
)

if __name__ == "__main__":
    phoneFieldProcessor = PhoneFieldProcessor()

    res = phoneFieldProcessor.process(phone_field)
    print(res)
