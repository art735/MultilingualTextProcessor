import re

import beautiful_soup_helper
from A0_CoreAnkiFormatter import A0_CoreAnkiFormatter
from BaseParsAndBracketsFormatter import BaseParsAndBracketsFormatter
from TextFomatter import TextFormatter


# class ParContentsUnitalicizer(BaseParsAndBracketsFormatter):
#     special_words = ['ся']
#
#     def __init__(self):
#         opening_bracket_symbol = '('
#         closing_bracket_symbol = ')'
#
#         textFormatter = TextFormatter()
#         is_formatting_already_existent_cb = textFormatter.is_text_not_italic_recursive_upwards
#         process_tag_cb = lambda parent_tag, soup: parent_tag.unwrap() if parent_tag.name in ['i', 'em'] else None
#
#         super().__init__(opening_bracket_symbol, closing_bracket_symbol,
#                          is_formatting_already_existent_cb, process_tag_cb)
#
#     # Принимает html-строку и список текстовых фрагментов в скобках (plain text) и делает (если нужно) содержимое
#     # каждого фрагмента курсивом
#     def unitalicize(self, html_str):
#         result = super().make_formatting(html_str, self.special_words)
#         return result


class ParContentsUnitalicizer():
    special_words = ['ся']

    def unitalicize(self, html_str):
        soup = beautiful_soup_helper.getBs(html_str)

        for italic_tag in soup.find_all(['i', 'em']):
            # Получаем текст до и после тега <i>
            previous_text = italic_tag.previous_sibling
            next_text = italic_tag.next_sibling

            # # Проверяем, есть ли скобки вокруг тега
            if previous_text and next_text:
                prev_str = str(previous_text).strip()
                next_str = str(next_text).strip()
                if prev_str.endswith('(') and next_str.startswith(')'):
                    text = italic_tag.get_text().strip()
                    # Убираем курсив:
                    # 1) вокруг специально оговоренных последовательностей символов, взятых в круглые скобки
                    # 2) вокруг одиночных символов, взятых в круглые скобки
                    if text in self.special_words or len(text) == 1:
                        # Заменяем тег <i> на его содержимое (unitalicize)
                        italic_tag.unwrap()

        # Возвращаем обработанную HTML-строку
        result = beautiful_soup_helper.soup_to_str(soup)
        return result

####################################

html_str = 'брать(<i>ся</i>) руками'
html_str = '1) брать(<i>ся</i>) руками, трогать; хватать<br>2) доставать, брать<br>3) ловить; поймать<br><br>попастьСЯ, быть пойманным'
html_str = '<i>ся</i> 1) брать(<i>ся</i>) руками'
html_str = '<i>ся</i>'

if __name__ == '__main__':
    parContentsUnitalicizer = ParContentsUnitalicizer()
    res = parContentsUnitalicizer.unitalicize(html_str)
    print(res)

    input1 = [
        '<i>ся</i>',
        '(<i>ся</i>)',
        '1) брать(<i>ся</i>) руками, трогать; хватать'
    ]

    er1 = [
        '<i>ся</i>',  # без изменений, т. к. текст (технически тег) не в скобках
        '(ся)',
        '1) брать(ся) руками, трогать; хватать'
    ]

    if all(parContentsUnitalicizer.unitalicize(input_val) == er for input_val, er in zip(input1, er1)):
        print("test - ok")
    else:
        print("test - failed")
