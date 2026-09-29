import re
import warnings

from bs4 import BeautifulSoup

import beautiful_soup_helper
from Core import CommonTextIssuesRemover

# Подавляем предупреждения
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')


class DivStripper:
    def strip_div_tags(self, html_str):
        result = CommonTextIssuesRemover.fix_problems(html_str)

        soup = beautiful_soup_helper.getBs(result)
        for div in soup.find_all('div'):
            # заменить тег div его же содержимым, перед которым поставить <br>
            div.insert_before(soup.new_tag("br"))
            div.unwrap()

        result = beautiful_soup_helper.soup_to_str(soup)

        # Ещё раз убедиться, что базовые правила форматирования соблюдены
        # Особенно в плане <br>, который из-за замен div-ов мог появиться:
        # - в начале текста
        # - в середине текста (и здесь могла возникнуть ситуация, когда целых три <br> шли бы подряд)
        result = CommonTextIssuesRemover.fix_problems(result)

        return result

    # Регулярное выражение для поиска вложенных <div>-ов
    # def search_innermost_div_contents(self, html_str):
    #     match = re.finditer(r'<div>((?:(?!<div>).)*?)</div>', html_str, flags=re.DOTALL | re.MULTILINE)
    #     return match

##########################################################

test_html_str = '[hɛʁ ˈʃɛːpɐs voːnt ɪn ˈʁɔstɔk]<br>[viː ˈbɪtə voː voːnt hɛʁ ˈʃɛːpɐs]'
test_html_str = 'abc <br> xyz'
test_html_str = 'лгать<div><br></div><div>ложь</div>'
test_html_str = '<div></div>'
test_html_str = '<div>savage (<i><font color="#00aa00">noun &amp; adj.</font></i>)</div><div><br></div><div>garden</div><div><br></div><b>«Savage Garden»</b>'

if __name__ == "__main__":
    divStripper = DivStripper()
    res = divStripper.strip_div_tags(test_html_str)
    print(res)
