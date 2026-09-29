from unittest import TestCase

from VerbConjugationFormatter import VerbConjugationFormatter


class Test_VerbConjugationFormatter(TestCase):

    def setUp(self):
        self.verbConjugationFormatter = VerbConjugationFormatter()

    # Название методов умышленно НЕ начинаются со слова 'test', чтобы они автоматом не запускались unittest-движком:
    # автоматом их запускать нельзя, т. к. они все содержат параметр business_method_callback, который я им передаю вручную.

    # Каждый test case должен содержать 2 вызова:
    # 1-й вызов проверяет, что добавляется нужное форматирование
    # 2-й вызов проверят, что форматирование не добавляется повторно!

    def test_1(self):
        # Положительный сценарий: тестировать, что форматирование нормально добавляется

        html_str = """geben<br><br>Präsens<br>ich gebe – wir geben<br>du gibst – ihr gebt<br>er/sie/es gibt – sie geben<br><br>Präteritum<br>ich gebe – wir geben<br>du gibst – ihr gebt<br>er/sie/es gibt – sie geben

        [ˈɡeːbn̩]<br><br>[ˈpʁɛːzɛns]<br>[ɪç ˈɡeːbə] – [viːɐ̯ ˈɡeːbn̩]<br>[duː ɡiːpst] – [iːɐ̯ ɡeːpt]<br>[eːɐ/ziː/ɛs̯ ɡiːpt] – [ziː ˈɡeːbn̩]<br><br>[pʁɛˈteːʁitʊm]<br>[ɪç ˈɡeːbə] – [viːɐ̯ ˈɡeːbn̩]<br>[duː ɡiːpst] – [iːɐ̯ ɡeːpt]<br>[eːɐ/ziː/ɛs̯ ɡiːpt] – [ziː ˈɡeːbn̩]

        давать<br><br>спряжение в Präsens<br><br>спряжение в Präteritum"""

        expected_result = """geben<br><br><b>Präsens</b><br>ich gebe – wir geben<br>du gibst – ihr gebt<br>er/sie/es gibt – sie geben<br><br><b>Präteritum</b><br>ich gebe – wir geben<br>du gibst – ihr gebt<br>er/sie/es gibt – sie geben

        [ˈɡeːbn̩]<br><br><b>[ˈpʁɛːzɛns]</b><br>[ɪç ˈɡeːbə] – [viːɐ̯ ˈɡeːbn̩]<br>[duː ɡiːpst] – [iːɐ̯ ɡeːpt]<br>[eːɐ/ziː/ɛs̯ ɡiːpt] – [ziː ˈɡeːbn̩]<br><br><b>[pʁɛˈteːʁitʊm]</b><br>[ɪç ˈɡeːbə] – [viːɐ̯ ˈɡeːbn̩]<br>[duː ɡiːpst] – [iːɐ̯ ɡeːpt]<br>[eːɐ/ziː/ɛs̯ ɡiːpt] – [ziː ˈɡeːbn̩]

        давать<br><br><i>спряжение в <b>Präsens</b></i><br><br><i>спряжение в <b>Präteritum</b></i>"""

        actual_result = self.verbConjugationFormatter.format_verb(html_str)
        self.assertEqual(expected_result, actual_result)

        # Тестировать, что уже существующая разметка корректно распознаётся и логика ничего в исходной строке не меняет
        html_str = """geben<br><br><b>Präsens</b><br>ich gebe – wir geben<br>du gibst – ihr gebt<br>er/sie/es gibt – sie geben<br><br><b>Präteritum</b><br>ich gebe – wir geben<br>du gibst – ihr gebt<br>er/sie/es gibt – sie geben

        [ˈɡeːbn̩]<br><br><b>[ˈpʁɛːzɛns]</b><br>[ɪç ˈɡeːbə] – [viːɐ̯ ˈɡeːbn̩]<br>[duː ɡiːpst] – [iːɐ̯ ɡeːpt]<br>[eːɐ/ziː/ɛs̯ ɡiːpt] – [ziː ˈɡeːbn̩]<br><br><b>[pʁɛˈteːʁitʊm]</b><br>[ɪç ˈɡeːbə] – [viːɐ̯ ˈɡeːbn̩]<br>[duː ɡiːpst] – [iːɐ̯ ɡeːpt]<br>[eːɐ/ziː/ɛs̯ ɡiːpt] – [ziː ˈɡeːbn̩]

        давать<br><br><i>спряжение в <b>Präsens</b></i><br><br><i>спряжение в <b>Präteritum</b></i>"""
        expected_result = html_str
        actual_result = self.verbConjugationFormatter.format_verb(html_str)
        self.assertEqual(expected_result, actual_result)
