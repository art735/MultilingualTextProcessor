import re

from A20_GreenAndItalicFormatter import A20_GreenAndItalicFormatter

# Q: В Анки-полях символом новой строки является не \n, а тег <br>
# A: Символ точки . в регулярных выражениях означает «любой символ» (кроме классического \n). Для движка регулярных
# выражений тег <br> — это не какой-то спецсимвол переноса, а просто 4 обычные буквы: <, b, r, >.
# Поэтому комбинация .*? без проблем «проглотит» любые <br>, пробелы и текст внутри /* ... */.

# Q: Почему модификатор (?s) всё равно полезно оставить?
# A: В исходном коде карточек Anki (если нажать Ctrl+Shift+X в редакторе) всё равно могут присутствовать невидимые
# символы \n для визуального форматирования самого HTML-кода. Если убрать (?s), регулярка может споткнуться об этот
# невидимый перенос и не закрыть комментарий.

# 1. (?s)/\*.*?\*/ — многострочный комментарий.
#    Здесь <br> рассматривается как обычный текст, поэтому комментарий
#    может спокойно пересекать HTML-теги <br>.
#
# 2. //(?:(?!<br\s*/?>)[^\n])* — однострочный комментарий.
#    Останавливаемся на первом <br> или \n.
SEARCH_REGEX_CPP_COMMENTS = r'(?s)/\*.*?\*/|//(?:(?!<br\s*/?>)[^\n])*'


class A25_CppCommentsFormatter:
    """
    Форматирует C++ комментарии зелёным цветом и курсивом.

    Обычные случаи передаются в общий механизм A20/A0.
    Комментарии, пересекающие HTML-теги <br>, дополнительно
    форматируются напрямую в исходном HTML.
    """

    def __init__(self):
        self.open_tag = '<span style="color: rgb(0, 170, 0);"><i>'
        self.close_tag = '</i></span>'
        self.a20_GreenAndItalicFormatter = A20_GreenAndItalicFormatter()

    def format_cpp_comments(self, html_str):

        # ----------------------------------------------------------
        # ШАГ 1.
        # Обычная обработка через существующий механизм A20/A0.
        # Это сохраняет всю уже имеющуюся логику проекта.
        # ----------------------------------------------------------
        processed_html_str = self.a20_GreenAndItalicFormatter.make_green_and_italic(html_str, SEARCH_REGEX_CPP_COMMENTS)

        # ----------------------------------------------------------
        # ШАГ 2.
        # Дополнительная обработка комментариев, которые пересекают
        # HTML-теги <br>.
        #
        # A0 не может найти такой комментарий обратно в soup,
        # потому что после get_text() он становится одним plain-text
        # match, а в HTML он находится в нескольких NavigableString.
        #
        # Поэтому здесь ищем непосредственно в HTML.
        # ----------------------------------------------------------

        processed_html_str = self._format_comments_across_html_tags(processed_html_str)

        return processed_html_str

    def _format_comments_across_html_tags(self, html_str):
        """
        Форматирует многострочные C++ комментарии, пересекающие
        HTML-теги <br>.

        Уже отформатированные комментарии сначала временно заменяются
        placeholder-ами, чтобы повторный вызов formatter-а не создавал
        вложенные <span><i>...</i></span>.
        """

        # ----------------------------------------------------------
        # 1. Защищаем уже существующие наши форматированные участки.
        # ----------------------------------------------------------

        already_formatted_regex = re.compile(
            re.escape(self.open_tag)
            + r'.*?'
            + re.escape(self.close_tag),
            re.DOTALL
        )

        protected_fragments = []

        def protect_match(match):
            index = len(protected_fragments)

            placeholder = f'\x00CPP_COMMENT_FORMATTED_{index}\x00'

            protected_fragments.append(match.group(0))

            return placeholder

        html_str = already_formatted_regex.sub(protect_match, html_str)

        # ----------------------------------------------------------
        # 2. Ищем непосредственно многострочные комментарии.
        # ----------------------------------------------------------

        multiline_comment_regex = re.compile(
            r'(?s)/\*.*?\*/'
        )

        def replace_match(match):
            comment = match.group(0)

            # Нас интересуют здесь именно комментарии,
            # пересекающие HTML-тег <br>.
            if re.search(r'<br\s*/?>', comment, re.IGNORECASE):
                return (
                    f'{self.open_tag}'
                    f'{comment}'
                    f'{self.close_tag}'
                )

            # Комментарии без <br> оставляем как есть:
            # ими уже занимался A20/A0.
            return comment

        html_str = multiline_comment_regex.sub(replace_match, html_str)

        # ----------------------------------------------------------
        # 3. Возвращаем ранее отформатированные фрагменты.
        # ----------------------------------------------------------

        for index, fragment in enumerate(protected_fragments):
            placeholder = f'\x00CPP_COMMENT_FORMATTED_{index}\x00'
            html_str = html_str.replace(
                placeholder,
                fragment
            )

        return html_str


##################################################

test_html_str = '// однострочный комментарий'
test_html_str = '/* многострочный комментарий на одной линии */'
test_html_str = '/* настоящий многострочный комментарий \n на разных \n\n строках */'
test_html_str = '/* настоящий многострочный комментарий <br> на разных <br><br> строках */'
# test_html_str = 'versus<br>// English'

if __name__ == '__main__':
    a25_CppCommentsFormatter = A25_CppCommentsFormatter()
    res = a25_CppCommentsFormatter.format_cpp_comments(test_html_str)
    print(res)

    input1 = [
        # POSITIVE TESTS
        '// однострочный комментарий',
        '/* многострочный комментарий на одной линии */',
        '/* настоящий многострочный комментарий \n на разных \n\n строках */',
        '/* настоящий многострочный комментарий <br> на разных <br><br> строках */',

        # NEGATIVE TESTS: разметка уже однажды покрашенных комментариев не должна меняться, т. е. не должны добавляться
        # вложенные теги
        '<span style="color: rgb(0, 170, 0);"><i>// однострочный комментарий</i></span>',
        '<span style="color: rgb(0, 170, 0);"><i>/* многострочный комментарий на одной линии */</i></span>',
        '<span style="color: rgb(0, 170, 0);"><i>/* настоящий многострочный комментарий \n на разных \n\n строках */</i></span>',
        '<span style="color: rgb(0, 170, 0);"><i>/* настоящий многострочный комментарий <br> на разных <br><br> строках */</i></span>',
    ]

    er1 = [
        # POSITIVE TESTS
        '<span style="color: rgb(0, 170, 0);"><i>// однострочный комментарий</i></span>',
        '<span style="color: rgb(0, 170, 0);"><i>/* многострочный комментарий на одной линии */</i></span>',
        '<span style="color: rgb(0, 170, 0);"><i>/* настоящий многострочный комментарий \n на разных \n\n строках */</i></span>',
        '<span style="color: rgb(0, 170, 0);"><i>/* настоящий многострочный комментарий <br> на разных <br><br> строках */</i></span>',

        # NEGATIVE TESTS
        '<span style="color: rgb(0, 170, 0);"><i>// однострочный комментарий</i></span>',
        '<span style="color: rgb(0, 170, 0);"><i>/* многострочный комментарий на одной линии */</i></span>',
        '<span style="color: rgb(0, 170, 0);"><i>/* настоящий многострочный комментарий \n на разных \n\n строках */</i></span>',
        '<span style="color: rgb(0, 170, 0);"><i>/* настоящий многострочный комментарий <br> на разных <br><br> строках */</i></span>',
    ]

    if all(a25_CppCommentsFormatter.format_cpp_comments(input_val) == er for input_val, er in zip(input1, er1)):
        print("test - ok")
    else:
        print("test - failed")