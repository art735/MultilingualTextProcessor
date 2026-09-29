import AnkiProcessorConstants
import beautiful_soup_helper
from TextColorizer import TextColorizer
from user_enums import Mode

# tint [tɪnt] оттенок
OpenOffice_green_tints_dict = {
    'Turquoise': '#33ff99', 'Turquoise1': '#66ff99', 'Turquoise2': '#00ff66', 'Turquoise3': '#00cc33',
    'Turquoise4': '#009933', 'Turquoise5': '#007826', 'Turquoise6': '#00331a', 'Turquoise7': '#006633',
    'Turquoise8': '#339966', 'Turquoise9': '#66cc99', 'Turquoise10': '#99ffcc', 'Green': '#99ff66',
    'Green1': '#99ff99', 'Green2': '#66ff66', 'Green3': '#00cc00', 'Green4': '#009900',
    'Green5': '#006600', 'Green6': '#003300', 'Green7': '#336633', 'Green8': '#669966',
    'Green9': '#99cc99', 'Green10': '#ccffcc'
}

OpenOffice_green_tints = list(OpenOffice_green_tints_dict.values())
# print(len(OpenOffice_green_tints))

ANKI_GREEN_COLOR = "#00aa00"


class ColorTagProcessor:
    def __init__(self):
        self.textColorizer = TextColorizer()

    # !!! Main aggregated business method !!!
    def treat_colors(self, html_str):
        result = html_str

        result = self.unify_green_color_tints(result)
        result = self.remove_redundant_back_color_font_tag(result)

        return result

    # Business method
    def unify_green_color_tints(self, html_str):
        at_least_one_replace_took_place = False
        soup = beautiful_soup_helper.getBs(html_str)
        for font in soup.find_all('font'):
            # Метод .get() вернёт None, если атрибута нет, и условие просто не выполнится
            if font.get('color') in OpenOffice_green_tints:
                # if mode == Mode.SEARCH_ONLY:
                #     print("Found improper green color tint in '{0}'".format(html_str))
                #     # return html_str
                # elif mode == Mode.FIND_AND_REPLACE:
                font['color'] = ANKI_GREEN_COLOR
                # print(text + "\n* * *")
                at_least_one_replace_took_place = True

        result = html_str
        if at_least_one_replace_took_place:
            result = beautiful_soup_helper.soup_to_str(soup)

        return result

    # Business method
    def remove_redundant_back_color_font_tag(self, html_str):
        result = html_str

        soup = beautiful_soup_helper.getBs(html_str)
        all_black_font_tags = soup.find_all('font', color=lambda c: c == AnkiProcessorConstants.BLACK_COLOR_HTML)
        all_non_black_font_tags = soup.find_all(self.textColorizer.is_tag_not_black)
        # зелёный цвет, кроме тега font, может определяться ещё через inline-стиль тега <span>, поэтому
        # all_green_font_tags = soup.find_all(isTagGreen)

        # Если тегов <font> c не-чёрным цветом в разметке нет,
        # то и явный тег <font> с чёрным цветом (<font color="#000000">Это – Пауль. Он живёт в Галле.</font>) тоже не нужен
        at_least_one_replace_took_place = False
        # if len(all_non_black_font_tags) == 0 and len(all_green_font_tags) == 0 and len(all_black_font_tags) > 0:
        if len(all_non_black_font_tags) == 0 and len(all_black_font_tags) > 0:
            # if mode == Mode.SEARCH_ONLY:
            #     print("Found redundant black color <font> tag in '{0}'".format(html_str))
            # elif mode == Mode.FIND_AND_REPLACE:
            for black_font_tag in all_black_font_tags:
                black_font_tag.unwrap()
                at_least_one_replace_took_place = True

        if at_least_one_replace_took_place:
            result = beautiful_soup_helper.soup_to_str(soup)

        return result


#############################################################################

if __name__ == '__main__':
    colorTagProcessor = ColorTagProcessor()

    html_str = '<i>1) обозначает направление, отвечает на вопрос «куда?», употр. с <span style="color: rgb(0, 170, 0);">A</span> <b>перед, за</b><br>2) указывает на место, отвечает на вопрос «где?», употр. с <span style="color: rgb(0, 170, 0);">D</span> <b>перед, до</b></i><br><br>имя; фамилия&nbsp;(<i>N...</i>)<br><br><b><font color="#000000">имя&nbsp;(<i>V...</i>)</font></b>'
    # html_str = '<span style="color: rgb(0, 170, 0);">A</span>'
    res = colorTagProcessor.remove_redundant_back_color_font_tag(html_str)
    print(res)
