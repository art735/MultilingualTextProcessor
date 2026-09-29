import AnkiFieldHtmlIntoStripesAndLinesSplitter
from A11_GreenOnlyFormatter import A11_GreenOnlyFormatter
from A12_ItalicOnlyFormatter import A12_ItalicOnlyFormatter
from A20_GreenAndItalicFormatter import A20_GreenAndItalicFormatter
from A30_SquareBracketsContentsFormatter import A30_SquareBracketsContentsFormatter
from ParContentsUnitalicizer import ParContentsUnitalicizer


class GreenAndItalicAggregator:

    def __init__(self):
        self.a11_GreenOnlyFormatter = A11_GreenOnlyFormatter()
        self.a12_ItalicOnlyFormatter = A12_ItalicOnlyFormatter()
        self.a20_GreenAndItalicFormatter = A20_GreenAndItalicFormatter()

        self.a30_squareBracketsContentsFormatter = A30_SquareBracketsContentsFormatter()

    def execute_all_the_methods(self, html_str):
        # Разбиваем содержимое Anki-поля на отдельные полосы, обрабатываем каждую полосу в отдельности и затем
        # склеиваем результаты обратно в единую html-строку.
        # Такая разбивка нужна для того, чтобы регулярные выражения корректно находили необходимые участки текста для
        # форматирования, т. к. часть из них правильно работает только в том случае, если видит какой-либо термин
        # (который нужно отформатировать зелёным и курсивом, например) только в самом начале строки и работает
        # неправильно, если термин находится в середине строки (видимо не отрабатывает разделитель границ слова \b
        # для кириллицы).
        def _process(html_line):
            processed_html_line = html_line

            processed_html_line = self.a11_GreenOnlyFormatter.format_green_only(processed_html_line)
            processed_html_line = self.a12_ItalicOnlyFormatter.format_italic_only(processed_html_line)
            processed_html_line = self.a20_GreenAndItalicFormatter.format_green_and_italic(processed_html_line)
            processed_html_line = self.a30_squareBracketsContentsFormatter.unitalicize_square_brackets_contents(processed_html_line)

            return processed_html_line

        processed_html_str = AnkiFieldHtmlIntoStripesAndLinesSplitter.split_into_stripes_and_lines(html_str, _process)
        return processed_html_str


####################################

html_str = 'маульташен<br>(досл. «пастевой карман» разг. (досл. разг. это содержимое внутр. скобок))'
# html_str = '(досл. содержимое1)'
# html_str = '(<i>досл. содержимое1</i>)'

if __name__ == '__main__':
    greenAndItalicAggregator = GreenAndItalicAggregator()
    res = greenAndItalicAggregator.execute_all_the_methods(html_str)
    print(res)
