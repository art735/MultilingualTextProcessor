from unittest import TestCase

from bs4 import BeautifulSoup

import beautiful_soup_helper


class Test_beautiful_soup_helper(TestCase):

    def _performReplacement(self, html_str, replacement):
        soup = beautiful_soup_helper.getBs(html_str)
        soup.span.replace_with(replacement)
        return beautiful_soup_helper.soup_to_str(soup)

    # Тестировать тот факт, что в soup.replace_with замена обычной строкой создаёт проблему преобразования
    # угловых скобок в &lt; и &gt; а замена в soup.replace_with на целый объект beautiful soup этой проблемы не создаёт
    def test_replace_with(self):
        html_str = '<b>abc<span>more data</span>xyz</b>'

        # Делаем замену средствами beatiful soup, например, тега span с его содержимым на, например, тег div со своим содержимым
        # и убеждаемся, что ожидаемый рез-т не равен фактическому из-за того,
        # что угловые скобки почему-то заменились на &lt; и &gt;
        expected_result = html_str.replace('<span>more data</span>', '<div>replacement</div>')
        # Теперь делаем ту же замену с помощью не литеральной строки, а той же строки,
        # но упакованной в BeautifulSoup объект и убеждаемся, что ER = AR
        actual_result = self._performReplacement(html_str, beautiful_soup_helper.getBs('<div>replacement</div>'))
        self.assertEqual(expected_result, actual_result)

    # Тестировать ситуацию того, что soup автоматом заменяет –&nbsp; на \xa0
    def test_nbsp(self):
        html_str = '–&nbsp;phrase'
        soup = beautiful_soup_helper.getBs(html_str)
        expected_result = html_str
        actual_result = beautiful_soup_helper.soup_to_str(soup)
        # Убедиться, что теперь ER = AR потому, что конвертацию из soup сделали 'правильным' методом
        self.assertEqual(expected_result, actual_result)

    # Тестировать ситуацию того, что soup автоматом заменяет <br> на </br> и методы борьбы с этим
    def test_br(self):
        html_str = 'abc<br>xyz'
        soup = beautiful_soup_helper.getBs(html_str)
        expected_result = html_str
        actual_result = beautiful_soup_helper.soup_to_str(soup)
        self.assertEqual(expected_result, actual_result)

    # Тестировать ситуацию того, что soup автоматом заменяет <img> на </img>
    def test_img(self):
        html_str = '<img src="Bodensee.png">'
        soup = beautiful_soup_helper.getBs(html_str)
        expected_result = html_str
        actual_result = beautiful_soup_helper.soup_to_str(soup)
        # Убедиться, что теперь ER = AR потому, что конвертацию из soup сделали 'правильным' методом
        self.assertEqual(expected_result, actual_result)
