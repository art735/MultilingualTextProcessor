from A0_CoreAnkiFormatter import A0_CoreAnkiFormatter
from AnkiProcessorConstants import GREEN_COLOR_RGB, GREEN_COLOR_HTML, BLUE_COLOR_HTML, BLUE_COLOR_RGB, BLACK_COLOR_HTML, \
    BLACK_COLOR_RGB


# Обёртка над логикой класса A0_CoreAnkiFormatter
class TextColorizer:
    def __init__(self):
        self.a0_CoreAnkiFormatter = A0_CoreAnkiFormatter()

    def colorize_green(self, html_str, search_regex):
        result = self._colorize(html_str, search_regex, GREEN_COLOR_RGB, self._is_text_green_recursive_upwards)
        return result

    def colorize_blue(self, html_str, search_regex):
        result = self._colorize(html_str, search_regex, BLUE_COLOR_RGB, self._is_text_blue_recursive_upwards)
        return result

    def _colorize(self, html_str, search_regex, color_rgb, is_already_colorized_cb):
        color_replacement = fr'<span style="color: {color_rgb};">{{}}</span>'.format(r'\g<0>')
        result = self.a0_CoreAnkiFormatter.make_formatting(
            html_str,
            search_regex,
            is_already_colorized_cb,
            self.a0_CoreAnkiFormatter.get_find_and_replace_callback(color_replacement)
        )
        return result

    # GREEN
    def _is_text_green_recursive_upwards(self, tag):
        result = self.a0_CoreAnkiFormatter.is_text_formatted_recursive_upwards_base(self._is_tag_green, tag)
        return result

    def _is_tag_green(self, tag):
        is_green = self.a0_CoreAnkiFormatter.is_tag_styled(tag, 'color', GREEN_COLOR_HTML, GREEN_COLOR_RGB)
        return is_green

    # BLUE
    def _is_text_blue_recursive_upwards(self, tag):
        result = self.a0_CoreAnkiFormatter.is_text_formatted_recursive_upwards_base(self._is_tag_blue, tag)
        return result

    def _is_tag_blue(self, tag):
        result = self.a0_CoreAnkiFormatter.is_tag_styled(tag, 'color', BLUE_COLOR_HTML, BLUE_COLOR_RGB)
        return result

    # BLACK
    # def _is_text_black_recursive_upwards(self, tag):
    #     result = self.a0_CoreAnkiFormatter.is_text_formatted_recursive_upwards_base(self._is_tag_black, tag)
    #     return result

    def is_tag_black(self, tag):
        result = self.a0_CoreAnkiFormatter.is_tag_styled(tag, 'color', BLACK_COLOR_HTML, BLACK_COLOR_RGB)
        return result

    def is_tag_not_black(self, tag):
        return not self.is_tag_black(tag)
