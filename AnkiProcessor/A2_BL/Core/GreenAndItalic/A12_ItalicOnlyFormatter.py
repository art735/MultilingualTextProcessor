# Поскольку в стандартной библиотеке "re" нет поддержки рекурсии в регулярных выражениях, пользуемся пакетом regex
import regex as re

import beautiful_soup_helper
from A0_CoreAnkiFormatter import A0_CoreAnkiFormatter
from AnkiProcessorConstants import PIPE_DELIMITER, BR_DELIMITER
from ParContentsItalicizer import ParContentsItalicizer
from TextFomatter import TextFormatter

# Регулярное выражение для захвата круглых скобок любой вложенности вместе с их содержимым:
# \( – захватывает открывающую круглую скобку
# (?:[^()]+|(?R))* – захватывает 0 или более совпадений с одним из 2-х операндов оператора ИЛИ:
# [^()]+ – захватывает любой текст, не содержащий скобок. Круглые скобки внутри класса символов [] в регулярных
# выражениях можно указывать без экранирования обратными слешами, т. к. они воспринимаются просто как обычные символы,
# а не как специальные символы, которые обычно используются для группировки или захвата).
# | – оператор ИЛИ: если первая часть ИЛИ-выражения (|) соответствует проверяемому тексту, остальные части
# не проверяются.
# (?R) — рекурсивная ссылка на сам шаблон (т. е. вместо «(?R)» можно целиком скопировать и вставить всё регулярное
# выражение), которая позволяет захватывать вложенные скобки. Рекурсивная ссылка не поддерживается стандартным
# модулем "re", нужно устанавливать библиотеку regex.
# \) – захватывает закрывающую круглую скобку.
# !!! Leaving a Way Out of the Recursion !!!
# Whenever you paste the whole expression in place of the recursion marker (?R), you inherit another (?R).
# To avoid madness and infinite loops, you need to make sure that at some stage the (?R) will stop breeding.
# It can be achieved by one of two ways:
# 1) adding a question mark after the (?R). This ensures that if a recursion level fails, the engine can continue
# with the match at the level just above.
# 2) making the (?R) part of an alternation (в этом случае рекурсивная ссылка должна стоять СПРАВА от знака ИЛИ).
# (c) https://www.rexegg.com/regex-recursion.php
opening_par = r'\('
par_contents_core = r'(?:[^()]+|(?R))*'
closing_par = r'\)'
par_contents_regex = fr'{opening_par}{par_contents_core}{closing_par}'

# Общие замечания по форматированию содержимого скобок курсивом. В большинстве случаев на первом этапе происходит
# захват всего содержимого всех сбалансированных скобок. Затем скобки по краям отбрасываются и их содержимое
# проверяется на соответствие тому или иному шаблону. Поэтому все дальнейшие регулярные выражения (кроме специально
# оговоренных) ищут соответствие среди содержимого предварительно захваченных сбалансированных скобок.

# CASE #1. Содержимое скобок начинается со специального термина и дальше может идти свободный текст
terms = ['досл.', 'разг.']
terms_regex = PIPE_DELIMITER.join([fr'^{re.escape(term)}.*$' for term in terms])

# CASE #2. Содержимое скобок полностью занято заранее определённым текстом
pars_entire_contents = [
    # Regex #2.1 Сделать курсивом содержимое скобок, в котором после букв идёт многоточие
    r'[a-zA-Z]+[.]{3}',

    # Regex #2.2 Сделать курсивом содержимое таких скобок: (где?), (куда?)
    # re.escape здесь применяется ради экранирования знака вопроса, чтобы он воспринимался именно как знак вопроса,
    # а не как квантификатор
    re.escape('где?'),
    re.escape('куда?')
]

pars_entire_contents_regex = PIPE_DELIMITER.join([fr'^(?:{pars_full_filler})$'
                                                  for pars_full_filler in pars_entire_contents])

# CASE #3. Содержимое скобок начинается с "hint:". Данный случай является исключением из общего подхода искать сначала
# все сбалансированные скобки, а потом уже проверять их содержимое на соответствие определённому шаблону.
# В выражениях с hint: происходит как раз работа с НЕ-сбалансированными скобками и нужно захватывать жадным
# квантификатором всё содержимое, пока не встретится закрывающая скобка в конце строки (html-разметка предварительно
# разбивается по символу '<br>' на отдельные строки). Поэтому здесь не обойтись без lookarounds.
open_par_positive_lookbehind = r'(?<=\()'
closing_par_at_the_end_of_str_positive_lookahead = r'(?=\)$)'
hint_regex = fr'{open_par_positive_lookbehind}hint:.*{closing_par_at_the_end_of_str_positive_lookahead}'


class A12_ItalicOnlyFormatter:

    def __init__(self):
        self.a0_CoreAnkiFormatter = A0_CoreAnkiFormatter()
        self.textFormatter = TextFormatter()
        self.parContentsItalicizer = ParContentsItalicizer()

    # Main method
    def format_italic_only(self, html_str):
        result = html_str

        # CASE #1. Содержимое скобок начинается со специального термина и дальше может идти свободный текст
        result = self._make_par_contents_italic(result, terms_regex)

        # CASE #2. Содержимое скобок полностью занято заранее определённым текстом
        result = self._make_par_contents_italic(result, pars_entire_contents_regex)

        # CASE #3. Содержимое скобок начинается с «hint:»
        result = self.make_italic_hint(result, hint_regex)

        return result

    def _make_par_contents_italic(self, html_str, search_regex):

        # Вычитываем все пары сбалансированных скобок
        all_balanced_pars = self.a0_CoreAnkiFormatter.make_formatting_step1_get_plain_text_matches(html_str,
                                                                                                   par_contents_regex)
        # Оставляем только те пары скобок, содержимое которых удовлетворяет регулярному выражению
        valid_balanced_pars = []
        for balanced_pars in all_balanced_pars:
            # проверяем соответствует ли содержимое скобок определённому шаблону
            par_contents_match = re.match(search_regex, balanced_pars[1:-1])
            if par_contents_match:
                valid_balanced_pars.append(balanced_pars)

        # Применяем форматирование курсивом к содержимому скобок
        result = self.parContentsItalicizer.italicize(html_str, valid_balanced_pars)

        return result

    def make_italic_hint(self, html_str: str, search_regex):

        lines_to_restore_initial_html = []

        # В большинстве случаев "hint:" является ПОСЛЕДНЕЙ строкой полосы, но нельзя исключать, что под "hint:" ещё
        # будет располагаться, например, комментарий вида // или /* комментарий */. Поэтому не завязываемся
        # на какие-л. условности, а просто ищем "hint:" среди всех возможных полос Анки-поля.
        # Здесь важно не отфильтровывать пустые строки после split, т. к. затем они сыграют свою правильную роль при
        # восстановлении снова единой html_str из обработанных кусочков.
        html_str_lines = html_str.split(BR_DELIMITER)
        for html_str_line in html_str_lines:
            processed_html_line = self.textFormatter.format_italic(html_str_line, search_regex)
            lines_to_restore_initial_html.append(processed_html_line)

        result = BR_DELIMITER.join(lines_to_restore_initial_html)
        return result

    # Данный метод НЕ вызывается в текущем классе. Он вызывается в AnkiCardsAppearanceProcessor в составе того или
    # иного профиля форматирующих методов. Его бизнес-задача – быть однократно вызванным для форматирования содержимого
    # ВСЕХ СКОБОК курсивом во всех карточках на начальном этапе их форматирования. Затем это форматирование можно
    # будет вручную постепенно отменять или редактировать.
    # Случаев, когда скобки, даже не начинающиеся спец. терминами, должны быть курсивными гораздо больше, чем случаев,
    # когда их содержимое должно остаться "прямым".
    # Данный метод не должен пытаться форматировать содержимое скобок, начинающееся с "hint:", так как там скобки
    # по определению не сбалансированы и курсив будет применён к ним неправильно.
    def make_italic_all_contents_of_all_balanced_pars(self, html_str):

        lines_to_restore_initial_html = []
        html_str_lines = html_str.split(BR_DELIMITER)
        for html_str_line in html_str_lines:
            soup = beautiful_soup_helper.getBs(html_str_line)
            line_plain_text = soup.get_text()
            # Если html-кусочек содержит нежелательную последовательность - игнорируем его для форматирования,
            # т. е. просто добавляем его в результирующий список без каких-либо изменений
            if re.search(hint_regex, line_plain_text):
                lines_to_restore_initial_html.append(html_str_line)
            # в противном случае форматируем содержимое скобок курсивом
            else:
                processed_html_line = self._make_par_contents_italic(html_str_line, '^.*$')
                lines_to_restore_initial_html.append(processed_html_line)

        result = BR_DELIMITER.join(lines_to_restore_initial_html)
        return result


##########################

# html_str = 'имя (N...)'
# html_str = '(досл. «озеро в котловине»)'
# html_str = 'разг. (досл. «чёрный лес»)'
# html_str = 'маульташен<br>(досл. «пастевой карман» разг.)'
# html_str = '(досл. содержимое1)'
# html_str = "(досл. содержимое1) какой-то текст (содержимое2) ещё текст (досл. содержимое3) (досл. содержимое4 какой-то текст (содержимое5)) ещё текст"
# html_str = 'у окна (где?, куда?)'
# html_str = 'у окна (где?, куда?) к двери (куда?)'
# html_str = 'у окна (где?, куда?) к двери (<i>куда?</i>)'
# html_str = '(<i>куда?</i>)'
# html_str = '(hint: 1) а; 2) б; 3) в, г)'
# html_str = 'word1<br>(hint: 1) а; 2) б; 3) в, г)<br><br>word2<br>(hint: 1) а (и т. д.); 2) б)<br><br>word3<br>(hint: 1) а; 2) б; 3) в)'
# html_str = 'Ты (я(не знаю)) (к<span style="background-color: rgb(255, 255, 0);">у<b>д</b>а</span>?) идёшь куда? же?'

# html_str = 'Подсказка (hint: 1) а; 2) б)'
# html_str = 'Подсказка hint: 1) а; 2) б'
# html_str = 'Подсказка (hint: 1) а; 2) б)<br><br>и ещё такая же без скобок – hint: 1) а; 2) б'
# html_str = 'word1<br>(hint: 1) а; 2) б)<br><br>word2<br>(hint: 1) а (и т. д.); 2) б)'

html_str = 'приставка, которая указывает на:<br>1) начало действия<br>2) приближение, прикосновение, прикрепление<br>3) увеличение объёма<br><br>закрывать<br>(<i>sch...</i>)<br><br><b>1) запирать замком&nbsp;(<i>напр. велосипед</i>)<br>2) присоединять, подключать</b>'
html_str = '<b>1) запирать замком&nbsp;(<i>напр. велосипед</i>)<br>2) присоединять, подключать</b>'

if __name__ == '__main__':
    a12_ItalicOnlyFormatter = A12_ItalicOnlyFormatter()
    res = a12_ItalicOnlyFormatter.make_italic_all_contents_of_all_balanced_pars(html_str)
    print(res)
