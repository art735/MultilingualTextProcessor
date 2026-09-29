from unittest import TestCase

from A12_ItalicOnlyFormatter import A12_ItalicOnlyFormatter
from GreenAndItalicAggregator import GreenAndItalicAggregator


class Test_A12_ItalicOnlyFormatter(TestCase):

    def setUp(self):
        self.a12_ItalicOnlyFormatter = A12_ItalicOnlyFormatter()
        self.greenAndItalicAggregator = GreenAndItalicAggregator()

    # Название методов умышленно НЕ начинаются со слова 'test', чтобы они автоматом не запускались unittest-движком:
    # автоматом их запускать нельзя, т. к. все они содержат параметр business_method_callback, который я им передаю вручную.

    # Каждый test case должен содержать 2 вызова:
    # 1-й вызов проверяет, что добавляется нужное форматирование
    # 2-й вызов проверят, что форматирование не добавляется повторно!

    # Тестировать регулярное выражение A12_ItalicOnlyFormatter.terms_regex
    def tc_01(self, business_method_callback):
        # Положительный сценарий: тестировать, что форматирование нормально добавляется
        html_str = '(досл. «озеро в котловине»)'
        expected_result = '(<i>досл. «озеро в котловине»</i>)'
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # Тестировать, что уже существующая разметка корректно распознаётся и логика ничего в исходном тексте не меняет
        html_str = '(<i>досл. «озеро в котловине»</i>)'
        expected_result = html_str
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # Положительный сценарий: тестировать, что форматирование нормально добавляется
        html_str = 'маульташен<br>(досл. «пастевой карман»)'
        expected_result = 'маульташен<br>(<i>досл. «пастевой карман»</i>)'
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # Тестировать, что уже существующая разметка корректно распознаётся и логика ничего в исходной строке не меняет
        html_str = 'маульташен<br>(<i>досл. «пастевой карман»</i>)'
        expected_result = html_str
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # ###########

        # Положительный сценарий: тестировать, что форматирование нормально добавляется
        html_str = 'маульташен<br>(досл. «пастевой карман» разг.)'
        expected_result = 'маульташен<br>(<i>досл. «пастевой карман» разг.</i>)'
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # Тестировать, что уже существующая разметка корректно распознаётся и логика ничего в исходном тексте не меняет
        html_str = 'маульташен<br>(<i>досл. «пастевой карман» разг.</i>)'
        expected_result = html_str
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # ###########

        # Положительный сценарий: тестировать, что форматирование нормально добавляется
        html_str = 'маульташен<br>(досл. «пастевой карман» разг. (досл. разг. это содержимое внутр. скобок))'
        expected_result = 'маульташен<br>(<i>досл. «пастевой карман» разг. (досл. разг. это содержимое внутр. скобок)</i>)'
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # Тестировать, что уже существующая разметка корректно распознаётся и логика ничего в исходном тексте не меняет
        html_str = 'маульташен<br>(<i>досл. «пастевой карман» разг. (досл. разг. это содержимое внутр. скобок)</i>)'
        expected_result = html_str
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # ###########

        # Положительный сценарий: тестировать, что форматирование нормально добавляется
        html_str = 'разг. (досл. «чёрный лес»)'
        expected_result = 'разг. (<i>досл. «чёрный лес»</i>)'
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # Тестировать, что уже существующая разметка корректно распознаётся и логика ничего в исходном тексте не меняет
        html_str = 'разг. (<i>досл. «чёрный лес»</i>)'
        expected_result = html_str
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

    # реальный юнит-тест, который запускает на выполнение соотв. tc_ метод
    def test_01(self):
        self.tc_01(self.a12_ItalicOnlyFormatter.format_italic_only)
        # self.tc_01(self.greenAndItalicAggregator.execute_all_the_methods)

    ##########################

    def tc_021(self, business_method_callback):
        # Положительный сценарий: тестировать, что форматирование нормально добавляется
        html_str = 'имя (N...)'
        expected_result = 'имя (<i>N...</i>)'
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # Тестировать, что уже существующая разметка корректно распознаётся и логика ничего в исходной строке не меняет
        html_str = 'имя (<i>N...</i>)'
        expected_result = html_str
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # Тестировать, что любое кол-во точек, кроме 3-х, не даёт основания делать содержимое скобок курсивом

        html_str = 'имя (N.)'  # одна точка после одной буквы
        expected_result = html_str
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        html_str = 'имя (Na..)'  # две точки после двух букв
        expected_result = html_str
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        html_str = 'имя (Name....)'  # четыре точки после четырёх букв
        expected_result = html_str
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

    # реальный юнит-тест, который запускает на выполнение соотв. tc_ метод
    def test_021(self):
        self.tc_021(self.a12_ItalicOnlyFormatter.format_italic_only)
        # self.tc_021(self.greenAndItalicAggregator.execute_all_the_methods)

    ##########################

    # Тестировать (где?) и (куда?) в разных вариантах
    def tc_022(self, business_method_callback):
        html_str = 'у окна (где?)'
        expected_result = 'у окна (<i>где?</i>)'
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # Тестировать, что уже существующая разметка корректно распознаётся и логика ничего в исходной строке не меняет
        html_str = 'у окна (<i>где?</i>)'
        expected_result = html_str
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # ###########

        html_str = 'у окна (куда?)'
        expected_result = 'у окна (<i>куда?</i>)'
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # Тестировать, что уже существующая разметка корректно распознаётся и логика ничего в исходной строке не меняет
        html_str = 'у окна (<i>куда?</i>)'
        expected_result = html_str
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # ###########

        html_str = 'у окна (где?, куда?) где? куда?'
        expected_result = 'у окна (где?, куда?) где? куда?'
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # Тестировать, что уже существующая разметка корректно распознаётся и логика ничего в исходной строке не меняет
        html_str = 'у окна (где?, куда?) где? куда?'
        expected_result = html_str
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # ###########

        html_str = 'у окна (где?, куда?) к двери (куда?)'
        expected_result = 'у окна (где?, куда?) к двери (<i>куда?</i>)'
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # Тестировать, что уже существующая разметка корректно распознаётся и логика ничего в исходной строке не меняет
        html_str = 'у окна (где?, куда?) к двери (<i>куда?</i>)'
        expected_result = html_str
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # ###########

        html_str = 'Ты (куда?) идёшь куда? же (я(не знаю))?'
        expected_result = 'Ты (<i>куда?</i>) идёшь куда? же (я(не знаю))?'
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # Тестировать, что уже существующая разметка корректно распознаётся и логика ничего в исходной строке не меняет
        html_str = 'Ты (<i>куда?</i>) идёшь куда? же (я(не знаю))?'
        expected_result = html_str
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # ###########

        html_str = 'Ты (я(не знаю)) (к<span style="background-color: rgb(255, 255, 0);">у<b>д</b>а</span>?) идёшь куда? же?'
        expected_result = 'Ты (я(не знаю)) (<i>к<span style="background-color: rgb(255, 255, 0);">у<b>д</b>а</span>?</i>) идёшь куда? же?'
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # Тестировать, что уже существующая разметка корректно распознаётся и логика ничего в исходной строке не меняет
        html_str = 'Ты (я(не знаю)) (<i>к<span style="background-color: rgb(255, 255, 0);">у<b>д</b>а</span>?</i>) идёшь куда? же?'
        expected_result = html_str
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # ###########

        html_str = 'Ты (<span>куда?</span>) идёшь?'
        expected_result = 'Ты (<i><span>куда?</span></i>) идёшь?'
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # Тестировать, что уже существующая разметка корректно распознаётся и логика ничего в исходной строке не меняет
        html_str = 'Ты (<i><span>куда?</span></i>) идёшь?'
        expected_result = html_str
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # реальный юнит-тест, который запускает на выполнение соотв. tc_ метод

    def test_022(self):
        self.tc_022(self.a12_ItalicOnlyFormatter.format_italic_only)
        # self.tc_022(self.greenAndItalicAggregator.execute_all_the_methods)

    # Тестировать как форматируется курсивом содержимое скобок, начинающееся с hint:
    # hint-строки, если их несколько в тестовой строке, должны отделяться друг от друга символами <br>,
    # на этот момент есть жёсткая завязка в бизнес-логике
    def tc_03(self, business_method_callback):
        html_str = '(hint: 1) а; 2) б; 3) в, г)'
        expected_result = '(<i>hint: 1) а; 2) б; 3) в, г</i>)'
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # Тестировать, что уже существующая разметка корректно распознаётся и логика ничего в исходной строке не меняет
        html_str = '(<i>hint: 1) а; 2) б; 3) в, г</i>)'
        expected_result = html_str
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # ###########

        html_str = 'word1<br>(hint: 1) а; 2) б; 3) в, г)<br><br>word2<br>(hint: 1) а (и т. д.); 2) б)<br><br>word3<br>(hint: 1) а; 2) б; 3) в)'
        expected_result = 'word1<br>(<i>hint: 1) а; 2) б; 3) в, г</i>)<br><br>word2<br>(<i>hint: 1) а (и т. д.); 2) б</i>)<br><br>word3<br>(<i>hint: 1) а; 2) б; 3) в</i>)'
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # Тестировать, что уже существующая разметка корректно распознаётся и логика ничего в исходной строке не меняет
        html_str = 'word1<br>(<i>hint: 1) а; 2) б; 3) в, г</i>)<br><br>word2<br>(<i>hint: 1) а (и т. д.); 2) б</i>)<br><br>word3<br>(<i>hint: 1) а; 2) б; 3) в</i>)'
        expected_result = html_str
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # ###########

        html_str = 'Подсказка (hint: 1) а; 2) б)<br><br>и ещё такая же без скобок – hint: 1) а; 2) б'
        expected_result = 'Подсказка (<i>hint: 1) а; 2) б</i>)<br><br>и ещё такая же без скобок – hint: 1) а; 2) б'
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # Тестировать, что уже существующая разметка корректно распознаётся и логика ничего в исходной строке не меняет
        html_str = 'Подсказка (<i>hint: 1) а; 2) б</i>)<br><br>и ещё такая же без скобок – hint: 1) а; 2) б'
        expected_result = html_str
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

    # реальный юнит-тест, который запускает на выполнение соотв. tc_ метод
    def test_03(self):
        self.tc_03(self.a12_ItalicOnlyFormatter.format_italic_only)
        # self.tc_03(self.greenAndItalicAggregator.execute_all_the_methods)

    ##########################

    # Тест метода A12_ItalicOnlyFormatter.make_italic_all_contents_of_all_balanced_pars(...)
    # Любое содержимое сбалансированных скобок должно форматироваться курсивом, а содержимое скобок, начинающееся
    # с "hint:", должно игнорироваться данным методом. Для случая с "hint:" есть специальный метод
    # A12_ItalicOnlyFormatter.make_italic_hint(...)
    def tc_04(self, business_method_callback):
        html_str = '(Привет!)'
        expected_result = '(<i>Привет!</i>)'
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # Тестировать, что уже существующая разметка корректно распознаётся и логика ничего в исходной строке не меняет
        html_str = '(<i>Привет!</i>)'
        expected_result = html_str
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # ###########

        html_str = '(Привет (медвежонок)!)'
        expected_result = '(<i>Привет (медвежонок)!</i>)'
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # Тестировать, что уже существующая разметка корректно распознаётся и логика ничего в исходной строке не меняет
        html_str = '(<i>Привет (медвежонок)!</i>)'
        expected_result = html_str
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        # ###########

        # Тестировать, что hint: (будь он курсивный или нет) не претерпевает никаких изменений

        html_str = 'word1<br>(hint: 1) а; 2) б)<br><br>word2<br>(hint: 1) а (и т. д.); 2) б)'
        expected_result = html_str
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

        html_str = 'word1<br>(<i>hint: 1) а; 2) б</i>)<br><br>word2<br>(<i>hint: 1) а (и т. д.); 2) б</i>)'
        expected_result = html_str
        actual_result = business_method_callback(html_str)
        self.assertEqual(expected_result, actual_result)

    # реальный юнит-тест, который запускает на выполнение соотв. tc_ метод
    def test_04(self):
        self.tc_04(self.a12_ItalicOnlyFormatter.make_italic_all_contents_of_all_balanced_pars)
        # self.tc_04(self.greenAndItalicAggregator.execute_all_the_methods)
