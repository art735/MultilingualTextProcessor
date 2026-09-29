import re

from A0_CoreAnkiFormatter import A0_CoreAnkiFormatter
from AnkiProcessorConstants import PIPE_DELIMITER
from CharConstants import SPACE, HYPHEN
from SquareBracketsContentsUnitalicizer import SquareBracketsContentsUnitalicizer
from TextColorizer import TextColorizer

# positive_lookbehind_open_square_bracket = r'(?<=\[)'
# positive_lookahead_closing_square_bracket = r'(?=\])'

# Содержимое квадратных скобок для убирания курсива
words_of_interest = ['амер.', 'лат.', 'разг.', 'др.-греч.', 'новогреч.', 'др.-греч., новогреч.', 'фр.', 'итал.',
                     'книжн.', 'masc.', 'fem.', 'neut.', 'colloq.', 'сущ.; мн. ч.', 'фраз. гл.',
                     'pron. adv.', 'pron. indef.', 'adv.', 'prp.', 'cj.',
                     'LingvoUniversal', 'LingvoComputer', 'высокий стиль']

# re.escape нужен для того, чтобы точка после сокращений воспринималась как их неотъемлемая, т. е. как часть
# строки поиска, а не как специальный символ регулярного выражения. Т. е. точка экранируется.
piped_and_escaped_words_of_interest_str = PIPE_DELIMITER.join([re.escape(word) for word in words_of_interest])
square_bracketed_terms_regex = fr'\[(?:{piped_and_escaped_words_of_interest_str})\]'

hebrew_annotation_allowed_chars = fr'[\u0590-\u05FF{SPACE}{HYPHEN}]'
hebrew_annotation_regex = fr'\[{hebrew_annotation_allowed_chars}+\]'


class A30_SquareBracketsContentsFormatter:

    def __init__(self):
        self.a0_CoreAnkiFormatter = A0_CoreAnkiFormatter()
        self.textColorizer = TextColorizer()
        self.squareBracketsContentsUnitalicizer = SquareBracketsContentsUnitalicizer()

    # Данный метод вызывается самым первым в C10_GreenAndItalicFormatter.make_green_and_italic(...); там и читать
    # подробный комментарий.
    def make_green(self, html_str):
        result = html_str
        result = self.textColorizer.colorize_green(result, square_bracketed_terms_regex)
        result = self.textColorizer.colorize_green(result, hebrew_annotation_regex)
        return result

    def unitalicize_square_brackets_contents(self, html_str):
        # Вычитываем пары квадратных скобок
        plain_text_matches = (self.a0_CoreAnkiFormatter
                              .make_formatting_step1_get_plain_text_matches(html_str, square_bracketed_terms_regex))

        # Убираем форматирование курсивом у содержимого квадратных скобок согласно plain_text_matches
        result = self.squareBracketsContentsUnitalicizer.unitalicize(html_str, plain_text_matches)
        return result


################################################

if __name__ == '__main__':
    a30_squareBracketsContentsFormatter = A30_SquareBracketsContentsFormatter()

    # test_html_str = '''
    # <p>Это пример текста: [<span style="color: rgb(0, 170, 0);"><i>амер.</i></span>] и [амер.], а также другие слова.</p>
    # '''

    # test_html_str = 'Это пример текста: [<span style="color: rgb(0, 170, 0);"><i>амер.</i></span>] и [амер.], а также другие слова.'
    # test_html_str = 'Это пример текста: [<span style="color: rgb(0, 170, 0);"><i>амер.</i></span>] и [амер.], а также другие слова.'
    # test_html_str = 'Это пример текста: [<span style="color: rgb(0, 170, 0);"><i>амер.</i></span>]'
    test_html_str = 'маульташен<br>(<i><span style="color: rgb(0, 170, 0);">досл.</span> «пастевой карман» <span style="color: rgb(0, 170, 0);">разг.</span> (<span style="color: rgb(0, 170, 0);">досл.</span> <span style="color: rgb(0, 170, 0);">разг.</span> это содержимое внутр. скобок)</i>)'
    test_html_str = '<p>Это пример текста: <span style="color: rgb(0, 170, 0);">[<i>амер.</i>] <i>grasshopper</i></span>, а также другие слова.</p>'
    test_html_str = '[LingvoUniversal]'
    test_html_str = '[מ - צ - א]<br>לִמצוֹא<br>מוֹצֵא – מוֹצֵאת – מוֹצאִים – מוֹצאוֹת'

    result = test_html_str
    for i in range(0, 1):
        result = a30_squareBracketsContentsFormatter.make_green(result)
    print(result)
