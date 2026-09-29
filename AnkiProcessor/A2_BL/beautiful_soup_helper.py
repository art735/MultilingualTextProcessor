import re
import warnings

from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
from bs4.formatter import HTMLFormatter

from CharConstants import NBSP_html

# Подавляем предупреждения
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

# We need to pass the whole BeautifulSoup object as a replacement argument (instead of just div.replace_with("<br>"))
# in order to avoid replacing tag angular brackets <> with &lt; and &gt;
# данный фабричный метод нужен, как минимум, в случае необходимости замены тега другим значением:
# если заменять не целым объектом BeautifulSoup(...), а непосредственно самим значением,
# угловые скобки <> будут преобразовываться в &lt; и &gt;
def getBs(arg):
    return BeautifulSoup(arg, 'html.parser')


# Custom HTMLFormatter to keep initial tag attribute order
class UnsortedAttributes(HTMLFormatter):
    def attributes(self, tag):
        for k, v in tag.attrs.items():
            yield k, v


def soup_to_str(soup):
    # Обратные преобразования символов из soup-представления в обычную строку
    # при условии, что для приготовления soup использовался 'html.parser'

    # extract data from soup object preserving original tag attribute order (otherwise BeautifulSoup will sort
    # tag attributes alphabetically)
    # result = str(soup.encode(formatter=UnsortedAttributes()).decode('utf-8'))

    result = str(soup)

    result = (result
              # Заменить неразрывный пробел в Unicode-кодировке на неразрывный пробел в html-представлении
              .replace('\u00A0', f'{NBSP_html}')

              # BeautifulSoup при парсинге самостоятельно преобразовывает <br> в <br/>; в конце работы эти изменения
              # нужно откатить.
              # Искать любой из 2-х вариантов тега br (</br> или <br/>) и заменить на канонический для Anki <br>
              .replace('</br>', '<br>').replace('<br/>', '<br>')

              # Вернуть угловым скобкам их обычное представление.
              .replace('&lt;', '<').replace('&gt;', '>')

              # Вернуть '&amp;' на '&', чтобы &nbsp; не превратился в &amp;nbsp
              .replace('&amp;', '&')
              )

    # Убрать закрывающий слэш в теге img: <img/> -> <img>
    # <img src="Bodensee.png"/> -> <img src="Bodensee.png">
    result = re.sub(r'<img(.*?)/>', r'<img{0}>'.format(r'\g<1>'), result)

    return result


# После каждой замены узла с помощью replace_with, нужно перестраивать целиком всё дерево. Иногда работает
# без перестройки дерева, а иногда - нет. Поэтому лучше подстраховываться и каждый раз перестраивать.
def recreate_soup_tree_structure(soup):
    updated_html = soup_to_str(soup)
    soup = getBs(updated_html)
    return soup


def strip_all_tags(html):
    soup = getBs(html)
    # метод strip() - это обычный Python-метод, который убирает конечные пробелы
    plain_text = soup.get_text().strip()
    return plain_text


# Удалить в html-строке все теги, кроме <br>. Метод используется для очистки форматирования многих полей Анки-карточек
# (кроме поля Image, где нужно сохранить ещё и тег <img>).
# В частности метод используется для очистки форматирования поля Transcription при добавлении в транскрипцию различных
# диакритических значков задним числом.
def strip_all_tags_except_br_tag(html):
    # soup = getBs(html)
    # for tag in soup.find_all(True):  # Находим все теги
    #     if tag.name not in ['br']:
    #         tag.unwrap()  # Удаляем теги, оставляя их содержимое
    #
    # # Преобразуем результат обратно в строку
    # result = soup_to_str(soup)
    # return result
    return _strip_all_tags_except_specified(html, ['br'])


# Метод нужен для очистки всего форматирования в Анки-карточках, а тег <br> нужно там оставлять для поддержания
# форматирования текста с переносами строк
def strip_all_tags_except_br_and_img_tags(html):
    # soup = getBs(html)
    # for tag in soup.find_all(True):  # Находим все теги
    #     if tag.name not in ['br', 'img']:
    #         tag.unwrap()  # Удаляем теги, оставляя их содержимое
    #
    # # Преобразуем результат обратно в строку
    # result = soup_to_str(soup)
    # return result
    return _strip_all_tags_except_specified(html, ['br', 'img'])


# Данный метод используется в бизнес-логике подчёркиваний правил чтения греческого языка
def strip_all_tags_except_u_tag(html):
    return _strip_all_tags_except_specified(html, ['u'])


def _strip_all_tags_except_specified(html, tag_names):
    soup = getBs(html)
    for tag in soup.find_all(True):  # Находим все теги
        if tag.name not in tag_names:
            tag.unwrap()  # Удаляем теги, оставляя их содержимое
    # Преобразуем результат обратно в строку
    result = soup_to_str(soup)
    return result


def is_html(possibly_html_text):
    soup = getBs(possibly_html_text)
    # Проверяем, содержит ли текст HTML-теги
    return bool(soup.find()) or possibly_html_text.strip().startswith("<")


##########################

if __name__ == '__main__':
    html = """
    <p>Это <b>пример</b> <i>текста</i> с <a href="#">разными</a> тегами.<br>Сохранить 
    <img alt="5 Tips to Guide" src="paste-c33eebf.jpg"> только <br> теги.</p>
    """

    # res = strip_all_tags_except_br_and_img_tags(html)
    # print(res)

    # test_str = """
    # [ˈteːləfoːn], [teleˈfoːn]<br><span style="color: rgb(0, 170, 0);"><i>// на YouGlish ударение в основном на 1-й слог</i></span><br><br>[ˈanʃlʊs]<br><br>[teleˈfoːnʔanˌʃlʊs]<br><span style="color: rgb(0, 170, 0);"><i>// YouGlish и AI (ChatGTP, Claude, Gemini, Le Chat) подтверждают именно такой вариант транскрипции</i></span>
    # """
    # print(is_html(test_str))

    html_str = '<img src="Bodensee.png">'
    # res = unifyGreenColorTints(html_str, Mode.SEARCH_ONLY)
    soup = getBs(html_str)
    result = soup_to_str(soup)
    print(result)
