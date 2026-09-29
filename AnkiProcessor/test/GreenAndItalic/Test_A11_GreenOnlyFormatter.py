from unittest import TestCase

from A11_GreenOnlyFormatter import A11_GreenOnlyFormatter
from GreenAndItalicAggregator import GreenAndItalicAggregator


class Test_A11_GreenOnlyFormatter(TestCase):

    def setUp(self):
        self.a11_GreenOnlyFormatter = A11_GreenOnlyFormatter()
        self.greenAndItalicAggregator = GreenAndItalicAggregator()

    # Название методов умышленно НЕ начинаются со слова 'test', чтобы они автоматом не запускались unittest-движком:
    # автоматом их запускать нельзя, т. к. все они содержат параметр business_method_callback, который я им передаю вручную.

    # Каждый test case должен содержать 2 вызова:
    # 1-й вызов проверяет, что добавляется нужное форматирование
    # 2-й вызов проверят, что форматирование не добавляется повторно!

    def tc_01(self, business_method_callback):
        html_str = 'сокращение [амер.] означает "американский"'
        expected_result = 'сокращение <span style="color: rgb(0, 170, 0);">[амер.]</span> означает "американский"'
        actual_result = html_str
        # вызываем логику 3 раза, чтобы убедиться, что при 2-м и 3-м запуске не ломается тот результат, который был
        # достигнут при 1-м запуске
        for i in range(0, 3):
            actual_result = business_method_callback(actual_result)
        self.assertEqual(expected_result, actual_result)

    # реальный юнит-тест, который запускает на выполнение соотв. tc_ метод
    def test_01(self):
        self.tc_01(self.a11_GreenOnlyFormatter.format_green_only)
        self.tc_01(self.greenAndItalicAggregator.execute_all_the_methods)
