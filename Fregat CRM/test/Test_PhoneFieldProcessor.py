import pytest

from PhoneFieldProcessor import PhoneFieldProcessor


class TestPhoneFieldProcessor:

    @pytest.fixture
    def processor(self):
        return PhoneFieldProcessor()

    def test_format_phones(self, processor):
        """
        Проверяет форматирование телефонных записей:
        удаление tel:, пробелов и пустых записей.
        """

        value = (
            " tel:+380501112233 - Иванов Иван ;"
            ";"
            "tel:+380672223344 - Петров Пётр;"
            " "
            "tel:+380633334455 - Сидоров Сидор "
        )

        result = processor.process(value)

        expected = (
            "ТЕЛЕФОНЫ:\n"
            "\t+380501112233 - Иванов Иван\n"
            "\t+380672223344 - Петров Пётр\n"
            "\t+380633334455 - Сидоров Сидор"
        )

        assert result == expected

    def test_director_marker_contact_goes_first(self, processor):
        """
        Контакт с подстрокой '(директор)' должен идти первым.
        """

        value = (
            "tel:+380501112233 - Иванов Иван;"
            "tel:+380672223344 - Петров Пётр (директор);"
            "tel:+380633334455 - Сидоров Сидор"
        )

        result = processor.process(value)

        expected = (
            "ТЕЛЕФОНЫ:\n"
            "\t+380672223344 - Петров Пётр (директор)\n"
            "\t+380501112233 - Иванов Иван\n"
            "\t+380633334455 - Сидоров Сидор"
        )

        assert result == expected

    def test_director_marker_is_case_insensitive(self, processor):
        """
        Проверяет, что маркер '(директор)' распознаётся
        независимо от регистра.
        """

        value = (
            "tel:+380501112233 - Иванов Иван;"
            "tel:+380672223344 - Петров Пётр (ДИРЕКТОР)"
        )

        result = processor.process(value)

        expected = (
            "ТЕЛЕФОНЫ:\n"
            "\t+380672223344 - Петров Пётр (ДИРЕКТОР)\n"
            "\t+380501112233 - Иванов Иван"
        )

        assert result == expected

    def test_director_full_name_goes_first(self, processor):
        """
        Контакт с именем, полностью совпадающим с ФИО директора,
        должен идти первым.
        """

        value = (
            "tel:+380501112233 - Иванов Иван Иванович;"
            "tel:+380672223344 - Петров Пётр Петрович;"
            "tel:+380633334455 - Сидоров Сидор Сидорович"
        )

        result = processor.process(value, director_full_name="Петров Пётр Петрович")

        expected = (
            "ТЕЛЕФОНЫ:\n"
            "\t+380672223344 - Петров Пётр Петрович\n"
            "\t+380501112233 - Иванов Иван Иванович\n"
            "\t+380633334455 - Сидоров Сидор Сидорович"
        )

        assert result == expected

    def test_director_full_name_is_case_insensitive(self, processor):
        """
        Сравнение ФИО директора с именем контакта
        должно выполняться без учёта регистра.
        """

        value = (
            "tel:+380501112233 - Иванов Иван;"
            "tel:+380672223344 - ПЕТРОВ ПЁТР ПЕТРОВИЧ"
        )

        result = processor.process(value, director_full_name="Петров Пётр Петрович")

        expected = (
            "ТЕЛЕФОНЫ:\n"
            "\t+380672223344 - ПЕТРОВ ПЁТР ПЕТРОВИЧ\n"
            "\t+380501112233 - Иванов Иван"
        )

        assert result == expected

    def test_director_full_name_requires_exact_match(self, processor):
        """
        Проверяет, что частичное совпадение ФИО
        не приводит к перемещению контакта.
        """

        value = (
            "tel:+380501112233 - Иванов Иванович;"
            "tel:+380672223344 - Петров Пётр"
        )

        result = processor.process(value, director_full_name="Иванов Иван")

        expected = (
            "ТЕЛЕФОНЫ:\n"
            "\t+380501112233 - Иванов Иванович\n"
            "\t+380672223344 - Петров Пётр"
        )

        assert result == expected

    def test_multiple_director_contacts_keep_original_order(self, processor):
        """
        Если несколько контактов подходят под условия,
        их взаимный порядок должен сохраняться.
        """

        value = (
            "tel:+380501112233 - Иванов Иван;"
            "tel:+380672223344 - Петров Пётр (директор);"
            "tel:+380633334455 - Сидоров Сидор;"
            "tel:+380991112233 - Смирнов Сергей Сергеевич"
        )

        result = processor.process(value, director_full_name="Смирнов Сергей Сергеевич")

        expected = (
            "ТЕЛЕФОНЫ:\n"
            "\t+380672223344 - Петров Пётр (директор)\n"
            "\t+380991112233 - Смирнов Сергей Сергеевич\n"
            "\t+380501112233 - Иванов Иван\n"
            "\t+380633334455 - Сидоров Сидор"
        )

        assert result == expected

    def test_empty_value(self, processor):
        """
        Проверяет обработку пустого значения.
        """

        result = processor.process("")

        assert result == "ТЕЛЕФОНЫ:\n"

    def test_none_value(self, processor):
        """
        Проверяет обработку None.
        """

        result = processor.process(None)

        assert result == "ТЕЛЕФОНЫ:\n"