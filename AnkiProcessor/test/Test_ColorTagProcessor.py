from unittest import TestCase

from ColorTagProcessor import ColorTagProcessor


class Test_ColorTagProcessor(TestCase):

    def setUp(self):
        self.colorTagProcessor = ColorTagProcessor()

    def test1(self):
        # Тестирование работы метода 'unifyGreenColorTints' и обёртки над всеми бизнес-методами модуля - treatColors
        # т. е. проверка того, что обёртка не ломает работу вложенного в неё метода
        self.tc_1(self.colorTagProcessor.unify_green_color_tints)
        self.tc_1(self.colorTagProcessor.treat_colors)

    def test2(self):
        # Тестирование работы метода 'removeRedundantBackColorFontTag' и обёртки над всеми бизнес-методами модуля - treatColors
        # т. е. проверка того, что обёртка не ломает работу вложенного в неё метода
        self.tc_2(self.colorTagProcessor.remove_redundant_back_color_font_tag)
        self.tc_2(self.colorTagProcessor.treat_colors)

    # Тестировать как различные оттенки зелёного приводятся к единственному нормативному варианту
    def tc_1(self, business_method_callback):
        # CASE #1
        html_str = """abc<br>(<font color="#009900">sg. – pl.</font>)"""
        expected_result = """abc<br>(<font color="#00aa00">sg. – pl.</font>)"""
        actual_result = business_method_callback(html_str)
        assert expected_result == actual_result

        # CASE #2
        html_str = """<i><font color="#00aa00">лингв.</font></i> перегласовка<br><br>* * *<br><br><i><b>Умла́ут, умля́ут</b> (<font color="#009900">нем.</font> Umlaut – перегласовка) – это фонетическое явление в некоторых германских и других языках, заключающееся в изменении артикуляции и тембра гласных: частичная или полная ассимиляция предыдущего гласного последующему, обычно – коренного гласного гласному окончания (суффикса или флексии).</i>"""
        expected_result = """<i><font color="#00aa00">лингв.</font></i> перегласовка<br><br>* * *<br><br><i><b>Умла́ут, умля́ут</b> (<font color="#00aa00">нем.</font> Umlaut – перегласовка) – это фонетическое явление в некоторых германских и других языках, заключающееся в изменении артикуляции и тембра гласных: частичная или полная ассимиляция предыдущего гласного последующему, обычно – коренного гласного гласному окончания (суффикса или флексии).</i>"""
        actual_result = business_method_callback(html_str)
        assert expected_result == actual_result

        # CASE #3. Проверить, что тег <img> НЕ превращается в </img>
        html_str = '<img src="Bodensee.png">'
        expected_result = html_str
        actual_result = business_method_callback(html_str)
        assert expected_result == actual_result

    # Тестировать как избыточный тег чёрного цвета корректно удаляется, а его содержимое, конечно, остаётся
    def tc_2(self, business_method_callback):
        # CASE #1
        html_str = '<font color="#000000">Это – Пауль. Он живёт в Галле.</font>'
        expected_result = 'Это – Пауль. Он живёт в Галле.'
        actual_result = business_method_callback(html_str)
        assert expected_result == actual_result

        # Тестировать, что в отсутствие тега font строка не меняется и логика не падает
        html_str = 'Это – Пауль. Он живёт в Галле.'
        expected_result = html_str
        actual_result = business_method_callback(html_str)
        assert expected_result == actual_result

        # CASE #2.1 Если в разметке присутствует тег font с цветом текста, отличным от чёрного, мы ничего не трогаем
        # т. е. не удаляем тег font с чёрным цветом
        html_str = '<font color="#000000"><b>дéвичья  <font color="#00ab00"><b>имя</b></font> фамилия</b></font>'
        expected_result = html_str
        actual_result = business_method_callback(html_str)
        assert expected_result == actual_result

        # CASE #2.2 тот же случай, что и CASE #2.1, но зелёный цвет выражен через rgb(0, 170, 0), а не через <font color="#00ab00">
        html_str = '<i>1) обозначает направление, отвечает на вопрос «куда?», употр. с <span style="color: rgb(0, 170, 0);">A</span> <b>перед, за</b><br>2) указывает на место, отвечает на вопрос «где?», употр. с <span style="color: rgb(0, 170, 0);">D</span> <b>перед, до</b></i><br><br>имя; фамилия&nbsp;(<i>N...</i>)<br><br><b><font color="#000000">имя&nbsp;(<i>V...</i>)</font></b>'
        expected_result = html_str
        actual_result = business_method_callback(html_str)
        assert expected_result == actual_result
