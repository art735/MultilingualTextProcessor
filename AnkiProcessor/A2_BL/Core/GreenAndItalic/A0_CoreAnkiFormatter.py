# Поскольку в стандартной библиотеке "re" нет поддержки рекурсии в регулярных выражениях, пользуемся пакетом regex
import cssutils
import regex as re

from AnkiProcessorConstants import GREEN_COLOR_HTML, GREEN_COLOR_RGB, BLUE_COLOR_HTML, BLUE_COLOR_RGB
import beautiful_soup_helper


class A0_CoreAnkiFormatter:

    # CORE METHOD
    def make_formatting(self, html_str, search_regex, is_formatting_already_existent_cb, process_tag_cb):

        # Step 1. Ищем в stripped html-строке регулярным выражением текстовые фрагменты, которые требуют форматирования
        # и возвращаем их в виде списка.
        plain_text_matches = self.make_formatting_step1_get_plain_text_matches(html_str, search_regex)

        # Step 2. Применяем форматирование к каждому текстовому фрагменту.
        formatted_html = self.make_formatting_step2_make_html_formatting(html_str, plain_text_matches,
                                                                         is_formatting_already_existent_cb,
                                                                         process_tag_cb)

        return formatted_html

    def make_formatting_step1_get_plain_text_matches(self, html_str, search_regex):

        soup = beautiful_soup_helper.getBs(html_str)

        # Собираем весь текст из HTML, игнорируя теги.
        # Ни join по пустой строке ''.join(soup.stripped_strings), ни join по пробелу ' '.join(soup.stripped_strings)
        # не могут сами по себе восстановить корректный plain text html-строки, т. к. в одних случаях это приводит к
        # тому, что слова слипаются друг с другом, а в других случаях к тому, что скобки (круглые и квадратные)
        # не окаймляют слово вплотную (как в оригинале), а отделяются от него пробелами. Всё эти недостатки приводят к
        # тому, что регулярные выражения не могут захватить тот plain text, который они должны захватывать будь он
        # правильно отформатирован.
        combined_text = soup.get_text()

        # Ищем совпадения в тексте.
        # re.finditer() полезен при работе с большими текстами или при поиске множества совпадений,
        # так как не требует создания полного списка совпадений в памяти, как re.findall().
        # Вместо этого он возвращает объекты совпадений по мере необходимости.
        # Каждый элемент, возвращаемый re.finditer(), является объектом Match, который содержит информацию
        # о конкретном совпадении, включая его позицию в тексте и группы, если они заданы.
        # re.finditer() особенно полезен, когда нужно обрабатывать каждое совпадение индивидуально,
        # например, для дальнейшей обработки текста, замены или анализа расположения совпадений в тексте.
        # plain_text_matches = []
        # for plain_text_match in list(re.finditer(search_regex, combined_text)):
        #     plain_text_matches.append(plain_text_match.group())

        plain_text_matches = re.findall(search_regex, combined_text)
        return plain_text_matches

    def make_formatting_step2_make_html_formatting(self, html_str, plain_text_matches,
                                                   is_formatting_already_existent_cb, process_tag_cb):

        soup = beautiful_soup_helper.getBs(html_str)

        # Итерируемся по найденным ранее совпадениям plain text-а с регулярным выражением и ищем для каждого из них
        # текстовые узлы в объекте soup.
        for match_text in plain_text_matches:

            # Текстовый узел, который ищется с помощью выражения `soup.find_all(string=True)`, — это часть
            # HTML-документа, представляющая собой непосредственно текст, находящийся между тегами.
            # Такой узел не включает в себя другие теги или атрибуты, а содержит только текстовое содержимое.
            # Другими словами, когда используется выражение `soup.find_all(string=True)`, оно находит и возвращает
            # все текстовые узлы в документе, игнорируя структуру тегов. Эти узлы могут быть фрагментами текста внутри
            # различных HTML-элементов (`<p>`, `<div>`, `<span>` и др.), но без включения самих этих тегов.
            # Например, в html-строке «Ты (<i>куда?</i>) идёшь?» будут следующие текстовые узлы:
            # - «Ты (»
            # - «куда?»
            # - «) идёшь?»
            # А в html-строке «<div>Привет <b>мир</b>!</div>» будут такие текстовые узлы:
            # - «Привет »
            # - «мир»
            # - «!»

            # Текстовые узлы имеют тип данных NavigableString. BeautifulSoup-ская NavigableString отличается от
            # Python-ской str тем, что первая встроена в структуру BeautifulSoup объекта и, в частности, хранит ссылку
            # на обрамляющий её тег (NavigableString.parent)!
            # Параметр 'string' указывает на то, что поиск текстового узла осуществляется среди СОДЕРЖИМОГО тегов,
            # а не среди их имён (по умолчанию). Ищатся только те текстовые узлы, которые содержат текст,
            # указанный в качестве параметра.
            # re.escape() автоматически добавляет обратные слэши перед всеми символами, которые могут быть
            # интерпретированы как специальные символы регулярных выражений. Эти символы должны восприниматься soup-ом
            # как обычные текстовые символы.
            i = 0
            text_nodes = soup.find_all(string=re.compile(re.escape(match_text)))
            while i < len(text_nodes):
                text_node = text_nodes[i]

                # if match_text in text_node:
                text_node_tag = text_node.find_parent()

                if is_formatting_already_existent_cb(text_node_tag) is False:
                    # Отдаём в callback старый объект soup, а получаем новый объект soup, воссозданный после
                    # произведённых замен в структуре дерева
                    soup = process_tag_cb(match_text, text_node_tag, soup)

                    # Если произошли изменения в узлах дерева soup или сам объект soup был подменён, и если количество
                    # текстовых узлов превышает 1, продолжать дальше итерироваться по списку узлов уже нельзя!
                    # Нужно заново найти все текстовые узлы text_nodes и заново начать (i = 0) по ним итерироваться,
                    # пока весь список узлов не будет перебран полностью.
                    # Рано или поздно is_formatting_already_existent_cb callback скажет, что форматирование уже
                    # существует и алгоритм не будет продвигаться дальше к заменам узлов.
                    if len(text_nodes) > 1:
                        text_nodes = soup.find_all(string=re.compile(re.escape(match_text)))
                        i = 0
                        # "continue" - перейти к следующей итерации цикла; позволяет здесь избавиться от нагромождений
                        # else-веток, использовавшихся для увеличения счётчика.
                        continue

                i += 1
            # end of while loop
        # end of for loop

        result = beautiful_soup_helper.soup_to_str(soup)
        return result

    # Метод в методе: внешний метод возвращает не конкретное значение, а логику работы внутреннего метода!
    # Внешний метод возвращает callback! Однострочный callback можно было бы вернуть в виде lambda-выражения,
    # а развесистый многострочный callback возвращается в виде целого метода!
    def get_find_and_replace_callback(self, replacement):

        def find_and_replace_callback(match_text, text_node_tag, soup):
            # Выполняем простую текстовую замену среди содержимого тега
            updated_str = re.sub(re.escape(match_text), replacement, str(text_node_tag))

            # Перед вызовом replace_with проверяется, есть ли у элемента родительский элемент.
            # Если родитель есть, это значит, что элемент является частью дерева, и его можно безопасно заменить.
            # В противном случае выполнение replace_with вызовет ошибку.
            parent = text_node_tag.parent
            if parent:
                # Выполняем замену в bs-дереве: старое содержимое тега заменяется на новое содержимое этого же тега
                text_node_tag.replace_with(beautiful_soup_helper.getBs(updated_str))
                soup = beautiful_soup_helper.recreate_soup_tree_structure(soup)
            else:
                # Поскольку родительского тега у text_node_tag нет - replace_with выполнить нельзя, а объект подменить
                # нужно и известно, что этот объект - корневой. Просто присваиваем переменной soup новый объект.
                soup = beautiful_soup_helper.getBs(updated_str)

            # Метод возвращает обновлённую html-строку
            return soup

        return find_and_replace_callback

    def is_text_formatted_recursive_upwards_base(self, is_tag_formatted_callback, tag):
        while tag:
            if is_tag_formatted_callback(tag):
                return True
            tag = tag.parent
        return False

    # Проверяет, содержит ли тег форматирование нужным цветом. На момент написания данного комментария в качестве
    # параметра attribute могут передаваться следующие значения:
    # 'color' (для работы TextColorizer)
    # 'background-color' (для работы TextHighlighter)
    def is_tag_styled(self, tag, attribute, color_html, color_rgb):
        result = False

        if tag is not None:
            # Case 1. Покраска в определённый цвет осуществлена с помощью тега <font>.
            # Такой вариант наблюдается в Anki в тех случаях, когда текст карточки был скопирован напрямую из OO Writer
            # и вставлен в Anki из буфера обмена.
            is_tag_colored_with_font = (tag.name == 'font') and (
                    tag.has_attr(attribute) and tag[attribute] == color_html)

            # Case 2. Покраска в определённый цвет осуществлена с помощью inline-стиля тега <span>.
            # Такой вариант наблюдается тогда, когда покраска в определённый цвет осуществлена средствами самого Anki.
            is_tag_styled = False
            if (tag.name == 'span') and (tag.has_attr('style')):
                # парсим inline-стиль с помощью сторонней библиотечки cssutils
                span_style = cssutils.parseStyle(tag['style'])
                # attribute = 'color' or 'background-color'
                property_value = span_style.getPropertyValue(attribute)
                if property_value == color_rgb:
                    is_tag_styled = True

            result = is_tag_colored_with_font or is_tag_styled

        return result
