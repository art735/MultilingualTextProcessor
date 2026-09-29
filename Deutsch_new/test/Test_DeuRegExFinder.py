from unittest import TestCase

from DeuRegExFinder import DeuRegExFinder


class Test_DeuRegExFinder(TestCase):

    def setUp(self):
        self.deuRegExFinder = DeuRegExFinder()

    def test_is_token_a_german_word(self):
        # Немецкое слово содержит прописные и строчные буквы немецкого алфавита
        token = "A"  # "A" — может использоваться как сокращение для слова "Antwort" (ответ).
        self.assertTrue(self.deuRegExFinder.is_token_a_canonical_word(token))
        token = "I"  # "I" — используется в некоторых диалектах и разговорной речи как сокращение от "Ich" (я).
        self.assertTrue(self.deuRegExFinder.is_token_a_canonical_word(token))
        token = "i"
        self.assertTrue(self.deuRegExFinder.is_token_a_canonical_word(token))
        token = "zu"
        self.assertTrue(self.deuRegExFinder.is_token_a_canonical_word(token))
        token = "Das"
        self.assertTrue(self.deuRegExFinder.is_token_a_canonical_word(token))
        token = "Vogel"
        self.assertTrue(self.deuRegExFinder.is_token_a_canonical_word(token))

        # Немецкое слово содержит букву é (das Café) (заимствование из французского языка???)
        token = "Café"
        self.assertTrue(self.deuRegExFinder.is_token_a_canonical_word(token))

        # Немецкое слово содержит дефис в любой позиции:
        # - в начале слова (-lich)
        # - в середине слова (Test-Text)
        # - в конце слова (Bundes-).
        # Но дефис не может стоять сам по себе и считаться немецким словом.
        token = "-lich"
        self.assertTrue(self.deuRegExFinder.is_token_a_canonical_word(token))
        token = "Test-Text"
        self.assertTrue(self.deuRegExFinder.is_token_a_canonical_word(token))
        token = "Bundes-"
        self.assertTrue(self.deuRegExFinder.is_token_a_canonical_word(token))
        # Негативные сценарии
        token = "-"
        self.assertFalse(self.deuRegExFinder.is_token_a_canonical_word(token))
        token = "--"
        self.assertFalse(self.deuRegExFinder.is_token_a_canonical_word(token))
        token = "--lich"
        self.assertFalse(self.deuRegExFinder.is_token_a_canonical_word(token))
        token = "Bundes--"
        self.assertFalse(self.deuRegExFinder.is_token_a_canonical_word(token))
        token = "Test--Text"
        self.assertFalse(self.deuRegExFinder.is_token_a_canonical_word(token))
        token = "a--b"
        self.assertFalse(self.deuRegExFinder.is_token_a_canonical_word(token))
        token = "---"
        self.assertFalse(self.deuRegExFinder.is_token_a_canonical_word(token))

        # Немецкое слово содержит открывающую круглую скобку в начале или середине слова и
        # закрывающую круглую скобку в середине или конце слова: (Auto)mobile, Auto(mobile), Str(aßen)-bahn.
        # Одновременное наличие открывающей круглой скобки в начале слова и закрывающей круглой скобки в конце слова
        # не допускается: (Automobile).
        token = "Automobile"
        self.assertTrue(self.deuRegExFinder.is_token_a_canonical_word(token))
        token = "(Auto)mobile"
        self.assertTrue(self.deuRegExFinder.is_token_a_canonical_word(token))
        token = "Auto(mobile)"
        self.assertTrue(self.deuRegExFinder.is_token_a_canonical_word(token))
        token = "Str(aßen)-bahn"
        self.assertTrue(self.deuRegExFinder.is_token_a_canonical_word(token))
        # Негативные сценарии
        token = "(Automobile)"
        self.assertFalse(self.deuRegExFinder.is_token_a_canonical_word(token))
        token = "("
        self.assertFalse(self.deuRegExFinder.is_token_a_canonical_word(token))
        token = ")"
        self.assertFalse(self.deuRegExFinder.is_token_a_canonical_word(token))
        token = "()"
        self.assertFalse(self.deuRegExFinder.is_token_a_canonical_word(token))

        # Другие негативные сценарии

        token = "1Das"
        self.assertFalse(self.deuRegExFinder.is_token_a_canonical_word(token))

        token = "Das1"
        self.assertFalse(self.deuRegExFinder.is_token_a_canonical_word(token))

        token = "Das ist ein Test-Text"
        self.assertFalse(self.deuRegExFinder.is_token_a_canonical_word(token))

        token = "VS_02_2803"
        self.assertFalse(self.deuRegExFinder.is_token_a_canonical_word(token))

        # Несовпадающее количество открывающих и закрывающих круглых скобок проверяется не регулярным выражением, а
        # логикой внутри метода BaseRegExFinder.is_token_a_language_specific_word(...)
        token = "Auto(mobile"
        self.assertFalse(self.deuRegExFinder.is_token_a_canonical_word(token))
        token = "(Automobile"
        self.assertFalse(self.deuRegExFinder.is_token_a_canonical_word(token))
        token = "Automobile)"
        self.assertFalse(self.deuRegExFinder.is_token_a_canonical_word(token))

    def test_surround_with_spaces_non_german_inclusions(self):
        input_str = "123Das ist ein Test-Text mit deutschen Wörtern wie Fußgängerübergang und E-Mail2."
        expected_result = "123 Das ist ein Test-Text mit deutschen Wörtern wie Fußgängerübergang und E-Mail 2."
        actual_result = self.deuRegExFinder.surround_with_spaces_non_german_inclusions(input_str)
        self.assertEquals(expected_result, actual_result)

        input_str = "Ich ((will))"
        expected_result = "Ich ( ( will ) )"
        actual_result = self.deuRegExFinder.surround_with_spaces_non_german_inclusions(input_str)
        self.assertEquals(expected_result, actual_result)

        input_str = "Test-Text"
        expected_result = "Test-Text"
        actual_result = self.deuRegExFinder.surround_with_spaces_non_german_inclusions(input_str)
        self.assertEquals(expected_result, actual_result)

        input_str = "Test - Text"
        expected_result = "Test - Text"
        actual_result = self.deuRegExFinder.surround_with_spaces_non_german_inclusions(input_str)
        self.assertEquals(expected_result, actual_result)

        input_str = "-"
        expected_result = "-"
        actual_result = self.deuRegExFinder.surround_with_spaces_non_german_inclusions(input_str)
        self.assertEquals(expected_result, actual_result)

        input_str = "--"
        expected_result = "- -"
        actual_result = self.deuRegExFinder.surround_with_spaces_non_german_inclusions(input_str)
        self.assertEquals(expected_result, actual_result)

        input_str = "a-b"
        expected_result = "a-b"
        actual_result = self.deuRegExFinder.surround_with_spaces_non_german_inclusions(input_str)
        self.assertEquals(expected_result, actual_result)

        input_str = "a--b"
        expected_result = "a- -b"
        actual_result = self.deuRegExFinder.surround_with_spaces_non_german_inclusions(input_str)
        self.assertEquals(expected_result, actual_result)

        # Берём 1-й символ - «a»: negative lookahead проверяет: идёт ли после него два дефиса?
        # Ответ ДА, значит «a» не захвачен.
        # Берём 1-й дефис: negative lookahead проверяет: идёт ли после него два дефиса?
        # Ответ ДА, значит 1-й дефис не захвачен.
        # Берём 2-й дефис: negative lookahead проверяет: идёт ли после него два дефиса?
        # Ответ НЕТ, но дефис сам по себе не может быть валидным токеном (это проверяет ещё один из lookahead-ов).
        # Берём 3-й дефис: negative lookahead проверяет: идёт ли после него два дефиса?
        # Ответ НЕТ, но дефис сам по себе не может быть валидным токеном (это проверяет ещё один из lookahead-ов).
        # Берём последний символ – «b»: это валидный случай и дефис перед ним тоже может идти?
        # Поэтому в итоге захватывается «-b».
        input_str = "a---b"
        expected_result = "a-- -b"
        actual_result = self.deuRegExFinder.surround_with_spaces_non_german_inclusions(input_str)
        self.assertEquals(expected_result, actual_result)

        input_str = "Das ist ein--Test-Text"
        expected_result = "Das ist ein- -Test-Text"
        actual_result = self.deuRegExFinder.surround_with_spaces_non_german_inclusions(input_str)
        self.assertEquals(expected_result, actual_result)

        input_str = "-lich Test-Text Bundes-"
        expected_result = "-lich Test-Text Bundes-"
        actual_result = self.deuRegExFinder.surround_with_spaces_non_german_inclusions(input_str)
        self.assertEquals(expected_result, actual_result)

        input_str = "abc -lich Test-Text Bundes- xyz"
        expected_result = "abc -lich Test-Text Bundes- xyz"
        actual_result = self.deuRegExFinder.surround_with_spaces_non_german_inclusions(input_str)
        self.assertEquals(expected_result, actual_result)
