from unittest import TestCase

import CharConstants
from Tokenizer import Tokenizer


class Test_Tokenizer(TestCase):

    def setUp(self):
        self.tokenizer = Tokenizer()

    # Testing Tokenizer.pre_process_text_by_deleting_unnecessary_symbols(text)
    def test1(self):
        text = 'a   \n\n\n\n\n\n   b       \n\n\n              c'
        expected_result = 'a b c'
        actual_result = self.tokenizer.pre_process_text_by_deleting_unnecessary_symbols(text)
        self.assertEqual(expected_result, actual_result)

        text = "d" + CharConstants.NON_BREAKING_SPACE + CharConstants.NON_BREAKING_SPACE + CharConstants.NON_BREAKING_SPACE + \
               " e" + CharConstants.NON_BREAKING_SPACE + "f"
        expected_result = 'd e f'
        actual_result = self.tokenizer.pre_process_text_by_deleting_unnecessary_symbols(text)
        self.assertEqual(expected_result, actual_result)

        text = 'g \t\t\t\t           h        \t\t\t\t\t             i'
        expected_result = 'g h i'
        actual_result = self.tokenizer.pre_process_text_by_deleting_unnecessary_symbols(text)
        self.assertEqual(expected_result, actual_result)

        text = 'j          k                 l'
        expected_result = 'j k l'
        actual_result = self.tokenizer.pre_process_text_by_deleting_unnecessary_symbols(text)
        self.assertEqual(expected_result, actual_result)

    def test2(self):
        text = "be (was, were; been)"

        expected_result = ["be", "was", "were", "been"]
        actual_result = self.tokenizer.tokenize(text)
        self.assertEqual(expected_result, actual_result)
