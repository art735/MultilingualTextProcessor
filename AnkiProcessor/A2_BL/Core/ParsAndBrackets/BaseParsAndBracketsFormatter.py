import beautiful_soup_helper


class BaseParsAndBracketsFormatter:
    def __init__(self, opening_bracketing_symbol, closing_bracketing_symbol,
                 is_formatting_already_existent_cb, process_tag_cb):

        # bracketing_symbol - это общее название для круглой или квадратной скобки. (с) ChatGPT
        self.opening_bracketing_symbol = opening_bracketing_symbol
        self.closing_bracketing_symbol = closing_bracketing_symbol

        # Флаг, проверяющий работаем ли мы с круглыми скобками
        self.are_bracketing_symbols_parentheses = (self.opening_bracketing_symbol == '(' and
                                                   self.closing_bracketing_symbol == ')')

        self.is_formatting_already_existent_cb = is_formatting_already_existent_cb
        self.process_tag_cb = process_tag_cb

    def make_formatting(self, html_str: str, plain_text_matches: list):
        result = html_str

        for plain_text_match in plain_text_matches:
            result = self._format_single_bracketing_symbols_pair(result, plain_text_match)

        return result

    def _format_single_bracketing_symbols_pair(self, html_str: str, match_text: str):

        soup = beautiful_soup_helper.getBs(html_str)

        # Следующая логика только для круглых скобок, но не для квадратных
        if self.are_bracketing_symbols_parentheses:
            # Step #1. Ищем match_text среди text_nodes.
            # Успех на этом этапе будет в том случае, если match_text ещё никак не форматировался и различные форматирующие
            # теги ещё не разделили его на отдельные текстовые узлы.
            i = 0
            # Итерируемся по всем текстовым узлам
            text_nodes = soup.find_all(string=True)
            while i < len(text_nodes):
                text_node = text_nodes[i]
                if match_text in text_node:
                    # Убираем круглые скобки по краям
                    par_trimmed_match_text = match_text[1:-1]
                    # Оборачиваем содержимое скобок в курсивные теги
                    wrapped_match_text = fr'(<i>{par_trimmed_match_text}</i>)'
                    # Обычная текстовая замена
                    replaced_str = text_node.replace(match_text, wrapped_match_text)
                    # bs-замена
                    text_node.replace_with(beautiful_soup_helper.getBs(replaced_str))

                    # После каждой замены узла, нужно перестраивать целиком всё дерево
                    soup = beautiful_soup_helper.recreate_soup_tree_structure(soup)

                    # Если произошли изменения в узлах дерева soup или сам объект soup был подменён, и если количество
                    # текстовых узлов превышает 1, продолжать дальше итерироваться по списку узлов уже нельзя!
                    # Нужно заново найти все текстовые узлы text_nodes и заново начать (i = 0) по ним итерироваться,
                    # пока весь список узлов не будет перебран полностью.
                    if len(text_nodes) > 1:
                        text_nodes = soup.find_all(string=True)
                        i = 0
                        # "continue" - перейти к следующей итерации цикла; позволяет здесь избавиться от нагромождений
                        # else-веток, использовавшихся для увеличения счётчика.
                        continue

                i += 1

        # Step #2. Если на предыдущем шаге не удалось найти целиком match_text среди текстовых узлов, будем
        # итерироваться по всем текстовым узлам и, встретив открывающую скобку, начнём складывать последовательные
        # текстовые узлы в отдельный буфер, пока не встретится закрывающая круглая скобка и скобки не будут
        # сбалансированы.
        # Буфер, в который будем складывать текстовые узлы, относящиеся к одной паре сбалансированных скобок
        par_related_text_nodes_buffer = []
        par_opened = False
        i = 0
        text_nodes = soup.find_all(string=True)
        while i < len(text_nodes):
            text_node = text_nodes[i]

            # Как только встретилась открывающая скобка, накапливаем последовательные текстовые узлы в специальный
            # буфер, пока не выполнится условие: встретилась закрывающая скобка И скобки в буфере сбалансированы
            if self.opening_bracketing_symbol in text_node:
                par_opened = True

            if par_opened:
                par_related_text_nodes_buffer.append(text_node)

                # Как только встретится закрывающая скобка И скобки в буфере окажутся сбалансированы, прекращаем
                # режим накопления и обрабатываем накопившуюся последовательность текстовых узлов
                if self.closing_bracketing_symbol in text_node:
                    # Объединяем содержимое буфера в строку
                    buffer_str = ''.join(par_related_text_nodes_buffer)
                    if self._are_pars_balanced(buffer_str):
                        if match_text in buffer_str:
                            # Форматируем содержимое скобок курсивом
                            # updated_soup_str = self.italicize_text_nodes_sequence(par_related_text_nodes_buffer, soup)
                            updated_soup_str = self.process_text_nodes_sequence(par_related_text_nodes_buffer, soup)
                            old_soup_str = beautiful_soup_helper.soup_to_str(soup)

                            # Если произошли изменения в узлах дерева soup или сам объект soup был подменён, и если
                            # количество текстовых узлов превышает 1, продолжать дальше итерироваться по списку узлов
                            # уже нельзя! Нужно заново найти все текстовые узлы text_nodes и заново начать (i = 0) по
                            # ним итерироваться, пока весь список узлов не будет перебран полностью.
                            if updated_soup_str != old_soup_str:
                                soup = beautiful_soup_helper.getBs(updated_soup_str)
                                if len(text_nodes) > 1:
                                    text_nodes = soup.find_all(string=True)
                                    # Очищаем буфер и сбрасываем флаг
                                    par_related_text_nodes_buffer = []
                                    par_opened = False
                                    i = 0
                                    continue  # Начинаем цикл заново без выполнения i += 1

                        # Очищаем буфер и сбрасываем флаг
                        par_related_text_nodes_buffer = []
                        par_opened = False
            i += 1

        result = beautiful_soup_helper.soup_to_str(soup)
        return result

    def _are_pars_balanced(self, str_to_check: str):
        open_pars_count = str_to_check.count(self.opening_bracketing_symbol)
        closed_pars_count = str_to_check.count(self.closing_bracketing_symbol)
        result = open_pars_count == closed_pars_count
        return result

    def process_text_nodes_sequence(self, par_related_text_nodes, soup):
        # Если крайний левый текстовый узел чётко заканчивается открывающей круглой скобкой, а крайний правый -
        # закрывающей круглой скобкой, это значит, что содержимое скобок заключено в какой-либо тег(-и) (не обязательно
        # курсивные теги), а значит содержимое скобок имеет РОДИТЕЛЬСКИЙ ТЕГ!
        # Берём родительские теги не у крайних текстовых узлов, а у второго и предпоследнего текстовых узлов и
        # смотрим какой из родителей (левый или правый) стоит ближе к корню дерева: именно этот родитель и должен
        # считаться общим родителем для всего содержимого скобок!
        if (par_related_text_nodes[0].endswith(self.opening_bracketing_symbol) and
                par_related_text_nodes[-1].startswith(self.closing_bracketing_symbol)):
            left_parent = par_related_text_nodes[1].find_parent()
            steps_up_to_top_from_left = self._count_steps_up_to_tree_top(left_parent)

            right_parent = par_related_text_nodes[-2].find_parent()
            steps_up_to_top_from_right = self._count_steps_up_to_tree_top(right_parent)

            if steps_up_to_top_from_left == steps_up_to_top_from_right:
                parent_tag = left_parent  # здесь без разницы какого из двух родителей брать
            elif steps_up_to_top_from_left < steps_up_to_top_from_right:
                parent_tag = left_parent
            else:
                parent_tag = right_parent

            # проверить является ли parent_tag отформатированным курсивом и если нет - отформатировать его
            if self.is_formatting_already_existent_cb(parent_tag) is False:
                # сам объект parent_tag курсивом не обрастает, но в объекте soup эти изменения происходят!
                self.process_tag_cb(parent_tag, soup)
        # В противном случае заменяем в крайних текстовых узлах открывающую и закрывающую скобки на самих себя +
        # курсивные теги:
        # - левая скобка - первая с конца строки открывающая скобка в 0-м текстовом узле
        # - правая скобка - первая с начала строки закрывающая скобка в последнем текстовом узле
        # Следующая ветка только для круглых скобок
        elif self.are_bracketing_symbols_parentheses:
            left_node = par_related_text_nodes[0]
            left_index = left_node.rfind(self.opening_bracketing_symbol)  # rfind = reverse find - искать с конца строки
            left_node_updated = self._replace_in_str_by_index(left_node, left_index, '(<i>')
            left_node.replace_with(left_node_updated)

            right_node = par_related_text_nodes[-1]
            right_index = right_node.find(self.closing_bracketing_symbol)
            right_node_updated = self._replace_in_str_by_index(right_node, right_index, '</i>)')
            right_node.replace_with(right_node_updated)

        soup_str = beautiful_soup_helper.soup_to_str(soup)
        return soup_str

    def _count_steps_up_to_tree_top(self, tag):
        counter = 0
        while tag.parent:
            tag = tag.parent
            counter += 1

        return counter

    def _replace_in_str_by_index(self, original_str, index, replacement):
        result = original_str
        if index != -1:
            result = original_str[:index] + replacement + original_str[index + 1:]
        return result
