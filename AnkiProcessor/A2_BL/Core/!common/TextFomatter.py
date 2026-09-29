import beautiful_soup_helper
from A0_CoreAnkiFormatter import A0_CoreAnkiFormatter
from AnkiProcessorConstants import YELLOW_COLOR_RGB, YELLOW_COLOR_HTML


# Обёртка над логикой класса A0_CoreAnkiFormatter
class TextFormatter:
    def __init__(self):
        self.a0_CoreAnkiFormatter = A0_CoreAnkiFormatter()

    # Последовательность кнопок в текстовом процессоре: B (bold), I (italic), U (underline)

    # BOLD
    def format_bold(self, html_str, search_regex):
        bold_replacement = r'<b>{0}</b>'.format(r'\g<0>')
        return self.a0_CoreAnkiFormatter.make_formatting(html_str, search_regex, self._is_text_bold_recursive_upwards,
                                                         self.a0_CoreAnkiFormatter.get_find_and_replace_callback(
                                                             bold_replacement))

    def _is_text_bold_recursive_upwards(self, tag):
        result = self.a0_CoreAnkiFormatter.is_text_formatted_recursive_upwards_base(self.is_tag_bold, tag)
        return result

    def is_tag_bold(self, tag):
        result = False
        if tag is not None:
            result = (tag.name == 'b')
        return result

    # ITALIC

    # Для форматирования курсивом содержимого скобок есть отдельный класс ParContentsItalicizer, который завязан на
    # поиск содержимого вместе с окружающими его скобками и дальнейшее форматирование таких найденных
    # последовательностей.
    # Если же регулярное выражение составлено так, что содержимое скобок обёрнуто в lookarounds, применяем данный метод.
    def format_italic(self, html_str, search_regex):
        italic_replacement = r'<i>{}</i>'.format(r'\g<0>')
        return self.a0_CoreAnkiFormatter.make_formatting(html_str, search_regex, self.is_text_italic_recursive_upwards,
                                                         self.a0_CoreAnkiFormatter.get_find_and_replace_callback(
                                                             italic_replacement))

    def is_text_italic_recursive_upwards(self, tag):
        result = self.a0_CoreAnkiFormatter.is_text_formatted_recursive_upwards_base(self.is_tag_italic, tag)
        return result

    def is_tag_italic(self, tag):
        result = False
        if tag is not None:
            result = (tag.name in ['i', 'em'])
        return result

    def unitalicize(self, html_str, search_regex):
        return self.a0_CoreAnkiFormatter.make_formatting(html_str, search_regex,
                                                         self.is_text_not_italic_recursive_upwards,
                                                         self._remove_italic_formatting_cb)

    # У callback-а, производящего замены в bs-дереве, сигнатура - это три перечисленных в скобках параметра.
    # Нужны они в данном конкретном callback-е или нет - не важно. Контракт должен соблюдаться.
    def _remove_italic_formatting_cb(self, match_text, text_node_tag, soup):

        tag_name = text_node_tag.name.lower()
        if tag_name == 'i' or tag_name == 'em':
            text_node_tag.unwrap()  # Removes the <i> or <em> tag, keeping its contents
            soup = beautiful_soup_helper.recreate_soup_tree_structure(soup)

        return soup

    # По сравнению с базовым методом is_text_formatted_recursive_upwards_base(...) здесь поменяны местами возвращаемые
    # значения: из цикла возвращается False, а в конце метода - True
    def is_text_not_italic_recursive_upwards(self, tag):
        while tag:
            # Здесь проверяем является ли тег курсивным. Если хоть на одном уровне ответ ДА, значит метод возвращает
            # False, т. е. текст не прошёл положительную проверку на не-курсивность.
            if self.is_tag_italic(tag):
                return False
            tag = tag.parent
        return True

    # UNDERLINED
    def format_underlined(self, html_str, search_regex):
        underlined_replacement = r'<u>{0}</u>'.format(r'\g<0>')
        return self.a0_CoreAnkiFormatter.make_formatting(html_str, search_regex, self._is_text_underlined_recursive_upwards,
                                                         self.a0_CoreAnkiFormatter.get_find_and_replace_callback(
                                                             underlined_replacement))

    def _is_text_underlined_recursive_upwards(self, tag):
        result = self.a0_CoreAnkiFormatter.is_text_formatted_recursive_upwards_base(self.is_tag_underlined, tag)
        return result

    def is_tag_underlined(self, tag):
        result = False
        if tag is not None:
            result = (tag.name == 'u')
        return result
