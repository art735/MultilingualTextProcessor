import re

import AnkiFieldHtmlIntoStripesAndLinesSplitter
from A20_GreenAndItalicFormatter import A20_GreenAndItalicFormatter
from TextColorizer import TextColorizer
from TextFomatter import TextFormatter


# Однострочные C++-комментарии: от // и до конца строки
# Символ // и всё, что идёт за ним в пределах одной строки
SEARCH_REGEX_SINGLE_LINE_CPP_COMMENT = r'//.*'

# Многострочные C++-комментарии: от /* до ближайшего */
# Модификатор (?s) заставляет точку '.' захватывать, в том числе, и символы переноса строки \n
SEARCH_REGEX_MULTI_LINE_CPP_COMMENT = r'(?s)/\*.*?\*/'

# Форматирует однострочные и многострочные C++-комментарии зелёным цветом и курсивом
# Данная логика вынесена в отдельный класс, т. к. она применяется не ко всем полям карточки, а в основном только в Front и Back
class A25_CppCommentsFormatter:
    """
    Класс для поиска и форматирования однострочных (//...) и многострочных (/*...*/)
    C++ комментариев зелёным цветом и курсивом.
    """

    def __init__(self):
        self.a20_GreenAndItalicFormatter = A20_GreenAndItalicFormatter()
        self.textColorizer = TextColorizer()
        self.textFormatter = TextFormatter()

    def format_cpp_comments(self, html_str):
        """
        Находит все однострочные и многострочные C++ комментарии в переданной HTML-строке
        и делает их зелёными и курсивными.
        """
        result = html_str

        # 1. Первым делом обрабатываем многострочные комментарии /* ... */.
        # Обработка выполняется на всём тексте целиком, так как комментарий может пересекать переносы строк.
        result = self.a20_GreenAndItalicFormatter.make_green_and_italic(
            result,
            SEARCH_REGEX_MULTI_LINE_CPP_COMMENT
        )

        # 2. Обрабатываем однострочные комментарии // ...
        # Для корректной работы с блоками/полосами разбиваем html_str через сплиттер.
        def _process_line(html_line):
            return self.a20_GreenAndItalicFormatter.make_green_and_italic(
                html_line,
                SEARCH_REGEX_SINGLE_LINE_CPP_COMMENT
            )

        result = AnkiFieldHtmlIntoStripesAndLinesSplitter.split_into_stripes_and_lines(
            result,
            _process_line
        )

        return result

##################################################

test_html_str = '// однострочный комментарий'
test_html_str = '/* многострочный комментарий на одной линии */'
test_html_str = '/* настоящий многострочный комментарий \n на разных \n\n строках */'
test_html_str = '/* настоящий многострочный комментарий <br> на разных <br><br> строках */'

if __name__ == '__main__':
    a25_CppCommentsFormatter = A25_CppCommentsFormatter()
    res = a25_CppCommentsFormatter.format_cpp_comments(test_html_str)
    print(res)