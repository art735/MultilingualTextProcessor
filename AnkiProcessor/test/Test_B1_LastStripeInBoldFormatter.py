from unittest import TestCase

from B1_LastStripeInBoldFormatter import B1_LastStripeInBoldFormatter


class Test_B1_LastStripeInBoldFormatter(TestCase):

    def setUp(self):
        self.b1_LastStripeInBoldFormatter = B1_LastStripeInBoldFormatter()
        # self.greenAndItalicAggregator = GreenAndItalicAggregator()

    # Тестирует работу метода FirstLineOfLastStripeBoldFormatter.make_1st_line_of_the_last_stripe_bold(...)
    def test_01(self):
        html_str = 's1<br><br>s2<br><br>Текст строки'
        expected_result = 's1<br><br>s2<br><br><b>Текст строки</b>'
        actual_result = self.b1_LastStripeInBoldFormatter.make_last_stripe_bold(html_str)
        self.assertEqual(expected_result, actual_result)

        # Тестировать, что уже существующая разметка корректно распознаётся и логика ничего в исходной строке не меняет
        html_str = 's1<br><br>s2<br><br><b>Текст строки</b>'
        expected_result = html_str
        actual_result = self.b1_LastStripeInBoldFormatter.make_last_stripe_bold(html_str)
        self.assertEqual(expected_result, actual_result)

        # ###########

        html_str = 's1<br><br>s2<br><br><p><i>Текст строки</i></p>'
        expected_result = 's1<br><br>s2<br><br><b><p><i>Текст строки</i></p></b>'
        actual_result = self.b1_LastStripeInBoldFormatter.make_last_stripe_bold(html_str)
        self.assertEqual(expected_result, actual_result)

        # Тестировать, что уже существующая разметка корректно распознаётся и логика ничего в исходной строке не меняет
        html_str = 's1<br><br>s2<br><br><b><p><i>Текст строки</i></p></b>'
        expected_result = html_str
        actual_result = self.b1_LastStripeInBoldFormatter.make_last_stripe_bold(html_str)
        self.assertEqual(expected_result, actual_result)

        # ###########

        html_str = 's1<br><br>нежирный текст'
        expected_result = 's1<br><br><b>нежирный текст</b>'
        actual_result = self.b1_LastStripeInBoldFormatter.make_last_stripe_bold(html_str)
        self.assertEqual(expected_result, actual_result)

        # Тестировать, что уже существующая разметка корректно распознаётся и логика ничего в исходной строке не меняет
        html_str = 's1<br><br><b>нежирный текст</b>'
        expected_result = html_str
        actual_result = self.b1_LastStripeInBoldFormatter.make_last_stripe_bold(html_str)
        self.assertEqual(expected_result, actual_result)

        # ###########

        html_str = 's1<br><br><p><i>нежирный текст</i></p>'
        expected_result = 's1<br><br><b><p><i>нежирный текст</i></p></b>'
        actual_result = self.b1_LastStripeInBoldFormatter.make_last_stripe_bold(html_str)
        self.assertEqual(expected_result, actual_result)

        # Тестировать, что уже существующая разметка корректно распознаётся и логика ничего в исходной строке не меняет
        html_str = 's1<br><br><b><p><i>нежирный текст</i></p></b>'
        expected_result = html_str
        actual_result = self.b1_LastStripeInBoldFormatter.make_last_stripe_bold(html_str)
        self.assertEqual(expected_result, actual_result)

        # ###########

        html_str = 's1<br><br><p>нежирный текст</p>'
        expected_result = 's1<br><br><b><p>нежирный текст</p></b>'
        actual_result = self.b1_LastStripeInBoldFormatter.make_last_stripe_bold(html_str)
        self.assertEqual(expected_result, actual_result)

        # Тестировать, что уже существующая разметка корректно распознаётся и логика ничего в исходной строке не меняет
        html_str = 's1<br><br><b><p>нежирный текст</p></b>'
        expected_result = html_str
        actual_result = self.b1_LastStripeInBoldFormatter.make_last_stripe_bold(html_str)
        self.assertEqual(expected_result, actual_result)

        # ###########

        # Содержимое многополосного поля Front, последняя полоса - однострочная
        html_str = 'modernist<br><br>theology<br><br>modernist theology'
        expected_result = 'modernist<br><br>theology<br><br><b>modernist theology</b>'
        actual_result = self.b1_LastStripeInBoldFormatter.make_last_stripe_bold(html_str)
        self.assertEqual(expected_result, actual_result)

        # Тестировать, что уже существующая разметка корректно распознаётся и логика ничего в исходной строке не меняет
        html_str = 'modernist<br><br>theology<br><br><b>modernist theology</b>'
        expected_result = html_str
        actual_result = self.b1_LastStripeInBoldFormatter.make_last_stripe_bold(html_str)
        self.assertEqual(expected_result, actual_result)

        # ###########

        # Содержимое многополосного поля Front, последняя полоса - многострочная
        html_str = 'modernist<br><br>theology<br><br>modernist theology<br>(<i>hint: м т</i>)'
        expected_result = 'modernist<br><br>theology<br><br><b>modernist theology</b><br>(<i>hint: м т</i>)'
        actual_result = self.b1_LastStripeInBoldFormatter.make_last_stripe_bold(html_str)
        self.assertEqual(expected_result, actual_result)

        # Тестировать, что уже существующая разметка корректно распознаётся и логика ничего в исходной строке не меняет
        html_str = 'modernist<br><br>theology<br><br><b>modernist theology</b><br>(<i>hint: м т</i>)'
        expected_result = html_str
        actual_result = self.b1_LastStripeInBoldFormatter.make_last_stripe_bold(html_str)
        self.assertEqual(expected_result, actual_result)

        # ###########

        # TODO
        # Последняя полоса состоит из 2-х строк и обе должны быть отформатированы жирным, но по ошибке была
        # отформатирована только верхняя полоса жирным, а нижняя осталась "обычной". Проверить, что бизнес-логика
        # отформатирует жирным и вторую строку последней полосы.
        html_str = 'приставка, которая указывает на:<br>1) начало действия<br>2) приближение, прикосновение, прикрепление<br>3) увеличение объёма<br><br>закрывать<br>(<i>sch...</i>)<br><br><b>1) запирать замком&nbsp;(<i>напр. велосипед</i>)</b><br>2) присоединять, подключать'
        expected_result = 'приставка, которая указывает на:<br>1) начало действия<br>2) приближение, прикосновение, прикрепление<br>3) увеличение объёма<br><br>закрывать<br>(<i>sch...</i>)<br><br><b>1) запирать замком&nbsp;(<i>напр. велосипед</i>)</b><br><b>2) присоединять, подключать</b>'
        actual_result = self.b1_LastStripeInBoldFormatter.make_last_stripe_bold(html_str)
        self.assertEqual(expected_result, actual_result)

        # Тестировать, что уже существующая разметка корректно распознаётся и логика ничего в исходной строке не меняет
        html_str = 'приставка, которая указывает на:<br>1) начало действия<br>2) приближение, прикосновение, прикрепление<br>3) увеличение объёма<br><br>закрывать<br>(<i>sch...</i>)<br><br><b>1) запирать замком&nbsp;(<i>напр. велосипед</i>)</b><br><b>2) присоединять, подключать</b>'
        expected_result = html_str
        actual_result = self.b1_LastStripeInBoldFormatter.make_last_stripe_bold(html_str)
        self.assertEqual(expected_result, actual_result)

        # ###########

        # Негативный сценарий. Поле не многополосное, а однополосное, значит ничего форматировать не нужно.
        html_str = r'modernist'
        expected_result = r'modernist'
        actual_result = self.b1_LastStripeInBoldFormatter.make_last_stripe_bold(html_str)
        self.assertEqual(expected_result, actual_result)
