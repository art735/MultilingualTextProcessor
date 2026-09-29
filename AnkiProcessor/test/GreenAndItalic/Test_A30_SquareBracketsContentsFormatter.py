from unittest import TestCase

from A30_SquareBracketsContentsFormatter import A30_SquareBracketsContentsFormatter
from GreenAndItalicAggregator import GreenAndItalicAggregator


class Test_A30_SquareBracketsContentsFormatter(TestCase):

    def setUp(self):
        self.squareBracketsContentsFormatter = A30_SquareBracketsContentsFormatter()
        self.greenAndItalicAggregator = GreenAndItalicAggregator()

    # Название методов умышленно НЕ начинаются со слова 'test', чтобы они автоматом не запускались unittest-движком:
    # автоматом их запускать нельзя, т. к. все они содержат параметр business_method_callback, который я им передаю вручную.

    # Каждый test case должен содержать 2 вызова:
    # 1-й вызов проверяет, что добавляется нужное форматирование
    # 2-й вызов проверят, что форматирование не добавляется повторно!

    def tc_41(self, business_method_callback):
        html_str = '<p>Это пример текста: <span style="color: rgb(0, 170, 0);">[<i>амер.</i>] <i>grasshopper</i></span>, а также другие слова.</p>'
        expected_result = '<p>Это пример текста: <span style="color: rgb(0, 170, 0);">[амер.] <i>grasshopper</i></span>, а также другие слова.</p>'
        actual_result = html_str
        # вызываем логику 3 раза, чтобы убедиться, что при 2-м и 3-м запуске не ломается тот результат, который был
        # достигнут при 1-м запуске
        for i in range(0, 3):
            actual_result = business_method_callback(actual_result)
        self.assertEqual(expected_result, actual_result)

    # реальный юнит-тест, который запускает на выполнение соотв. tc_ метод
    def test_41(self):
        self.tc_41(self.squareBracketsContentsFormatter.unitalicize_square_brackets_contents)
        self.tc_41(self.greenAndItalicAggregator.execute_all_the_methods)
