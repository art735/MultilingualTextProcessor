from A0_CoreAnkiFormatter import A0_CoreAnkiFormatter
from BaseParsAndBracketsFormatter import BaseParsAndBracketsFormatter
from TextFomatter import TextFormatter


class SquareBracketsContentsUnitalicizer(BaseParsAndBracketsFormatter):
    def __init__(self):
        opening_bracket_symbol = '['
        closing_bracket_symbol = ']'

        # a0_CoreAnkiFormatter = A0_CoreAnkiFormatter()
        textFormatter = TextFormatter()
        is_formatting_already_existent_cb = textFormatter.is_text_not_italic_recursive_upwards
        # process_tag_cb = a0_CoreAnkiFormatter.make_italic
        process_tag_cb = lambda parent_tag, soup: parent_tag.unwrap() if parent_tag.name in ['i', 'em'] else None

        super().__init__(opening_bracket_symbol, closing_bracket_symbol,
                         is_formatting_already_existent_cb, process_tag_cb)

    # Принимает html-строку и список текстовых фрагментов в скобках (plain text) и делает (если нужно) содержимое
    # каждого фрагмента курсивом
    def unitalicize(self, html_str, square_brackets_pairs):
        result = super().make_formatting(html_str, square_brackets_pairs)
        return result


####################################

if __name__ == '__main__':
    squareBracketsContentsUnitalicizer = SquareBracketsContentsUnitalicizer()

    html_str = '[<i>амер.</i>]'
    match_text_pairs = ['[амер.]']

    # res = squareBracketsContentsUnitalicizer.unitalicize(html_str, match_text_pairs)
    # print(res)
