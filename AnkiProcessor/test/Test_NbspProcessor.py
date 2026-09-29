from unittest import TestCase

import NbspProcessor


class Test_NbspProcessor(TestCase):

    def test_1(self):
        # CASE #1. 'пробел + (' встречается дважды: 'сын (' и 'rgb ('.
        # В 1-м случае замена пробела на &nbsp; нужна, а во втором (создал сам его искуственно) - нет
        html_str = 'сын (<span style="color: rgb (0, 170, 0);"><i>sg. – pl. nom. – pl. gen.</i></span>)'
        expected_result = 'сын&nbsp;(<span style="color: rgb (0, 170, 0);"><i>sg. – pl. nom. – pl. gen.</i></span>)'
        actual_result = NbspProcessor.insert_nbsp_before_opening_parenthesis(html_str)
        self.assertEqual(expected_result, actual_result)

        # Негативный сценарий
        html_str = 'сын&nbsp;(<span style="color: rgb (0, 170, 0);"><i>sg. – pl. nom. – pl. gen.</i></span>)'
        expected_result = html_str
        actual_result = NbspProcessor.insert_nbsp_before_opening_parenthesis(html_str)
        self.assertEqual(expected_result, actual_result)

    def test_2(self):
        # CASE #2. Положительный сценарий
        html_str = 'Как Ваша фамилия (<i>N...</i>)?'
        expected_result = 'Как Ваша фамилия&nbsp;(<i>N...</i>)?'
        actual_result = NbspProcessor.insert_nbsp_before_opening_parenthesis(html_str)
        self.assertEqual(expected_result, actual_result)

        # Негативный сценарий
        html_str = 'Как Ваша фамилия&nbsp;(<i>N...</i>)?'
        expected_result = html_str
        actual_result = NbspProcessor.insert_nbsp_before_opening_parenthesis(html_str)
        self.assertEqual(expected_result, actual_result)
