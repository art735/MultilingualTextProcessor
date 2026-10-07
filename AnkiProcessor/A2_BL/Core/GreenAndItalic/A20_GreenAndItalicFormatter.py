import re

import AnkiFieldHtmlIntoStripesAndLinesSplitter
import RegExConstants
from A0_CoreAnkiFormatter import A0_CoreAnkiFormatter
from A30_SquareBracketsContentsFormatter import A30_SquareBracketsContentsFormatter
from AnkiProcessorConstants import PIPE_DELIMITER
from CharConstants import HYPHEN, DASH, SPACE
from TextColorizer import TextColorizer
from TextFomatter import TextFormatter


HYPHEN_OR_DASH_CLASS = fr'[{HYPHEN}{DASH}]'


class RegexFragment(str):
    """
    Строка, содержащая уже готовый regex-фрагмент.

    Обычные строки в списках терминов считаются literal-текстом и поэтому
    автоматически обрабатываются через re.escape(). RegexFragment, наоборот,
    оставляется без изменений, т. к. его содержимое уже является regex.
    """
    pass


def regex_fragment(pattern):
    """
    Помечает строку как уже готовый regex-фрагмент.

    Это позволяет хранить в одном списке как обычные термины:
        'амер.'

    так и regex-конструкции:
        regex_fragment(r'(?:старо)?англ\.')
    """
    return RegexFragment(pattern)


def build_piped_terms(*term_lists):
    """
    Объединяет несколько списков терминов через PIPE_DELIMITER.

    Обычные строки экранируются через re.escape(), чтобы воспринимать их
    буквально.

    RegexFragment не экранируются, поскольку уже содержат готовый regex.
    """
    terms = []

    for term_list in term_lists:
        for term in term_list:
            if isinstance(term, RegexFragment):
                terms.append(term)
            else:
                terms.append(re.escape(term))

    return PIPE_DELIMITER.join(terms)


# Метасимвол \b в регулярных выражениях определяет границу слова. Граница слова (\b) в основном работает корректно
# для символов латинского алфавита и цифр, но с кириллицей могут возникать проблемы. В частности, для некоторых движков
# регулярных выражений граница слова может не учитываться должным образом перед или после кириллических букв и символов.
# Граница слова \b может не быть распознана после символов, таких как точка в словах на кириллице.
# \b перед шаблоном работает, потому что перед словом может быть пробел или начало строки.
# \b после точки (.) не распознаёт границу слова, поскольку точка не считается частью слова, и дальше нет символов,
# которые бы удовлетворяли определению границы слова.
# Если нужно, чтобы регулярное выражение работало с кириллическими символами, можно использовать следующий подход –
# не использовать \b после точки, а явно указать, что после точки может быть пробел или конец строки:
# r'\b(?:грам[.]|лингв[.])(?=\s|$)'
# Грамматические термины должны обязательно ограничиваться символом границы слова \b слева, чтобы, например,
# pattern 'амер[.]' не применялся к словам "замер." или "ламер.". А ограничить pattern справа символом границы слова \b
# нет, во-первых, технической возможности (для кириллицы в Python это не работает), а во-вторых нет особой нужды, т. к.
# после точки всегда будет идти какой-то не-словесный символ и ситуация с захватом части чужого слова
# становится маловероятной.
def get_optionally_delimited_terms_search_regex(terms, delimiters):
    # return fr'\b{terms}(?:{delimiters}{terms})*'
    # terms = fr'(?<!\w){terms}'  # нужна ли эта строка, особенно для terms, которые стоят после delimiters??????
    # TODO: проверить, что не захыватывается 'амер. - замер. - ламер.'
    return fr'(?<!\w){terms}(?:{delimiters}{terms})*'


# CASE 1. Грамматические термины и !!!их комбинации!!!

# Case 1.1 Выделять зелёным цветом и курсивом следующие термины и !их комбинации!, разделённые пробелом или
# пробел-дефис/тире-пробелом, независимо от того, заключены они в круглые скобки или нет.
grammar_terms_regex_group = r'(?:[Ss]g[.]|[Pp]l[.]|nom[.]|gen[.]|poss[.]|dat[.]|acc[.]|abl[.]|voc[.]|masc[.]|fem[.]|neut[.])'

# разделители, которыми данные грамматические термины могут отделяться друг от друга
delimiters1_regex_group = fr'(?:{SPACE}|{SPACE}{HYPHEN_OR_DASH_CLASS}{SPACE})'

search_regex1 = get_optionally_delimited_terms_search_regex(
    grammar_terms_regex_group,
    delimiters1_regex_group
)


# Case 1.2 Выделять зелёным цветом и курсивом следующие термины и !их комбинации!, разделённые пробелом или
# пробел-дефис/тире-пробелом, только при условии, что они заключены в тексте в круглые скобки.
# Konjunktiv II? - означает захват строки "Konjunktiv I" или "Konjunktiv II", причём римские цифры будут захватываться
# в жадной манере, т. е. сначала по возможности будет стараться захватить "II", и только потом "I"
grammar_terms = (
    r'(?:Infinitiv|Präsens|Präteritum|Konjunktiv II?|Partizip II?|Perfect|Imperativ|'
    r'Nominativ|Genitiv|Dativ|Akkusativ|declension)'
)  # наличие скобок здесь (regex group) обязательно!

optionally_delimited_terms_search_regex = get_optionally_delimited_terms_search_regex(
    grammar_terms,
    delimiters1_regex_group
)

search_regex2 = RegExConstants.parentheses_lookarounds.format(
    optionally_delimited_terms_search_regex
)


# CASE 2. Термины !без комбинаций!

# Case 2.1 Форматировать зелёным цветом и курсивом следующие слова/фразы, заключённые в круглые скобки

search_regex_adj_deklination = RegExConstants.parentheses_lookarounds.format(
    r'(?:Starke|Schwache|Gemischte).*?'
)

search_regex_parenthesized_phrases = RegExConstants.parentheses_lookarounds.format(
    r'(?:спряжение в Präsens|склонение по всем падежам|3 степени сравнения)'
)


# Case 2.2 Выделять зелёным цветом и курсивом следующие термины (они могут быть как в скобках, так и без них)
# Эти термины, в основном, ожидаются в словаре (а не фразах)
# В OpenOffice слово 'нем.' в выражении '(нем.)' нормально захватывается с помощью \b...\b нотации, а в Python - нет.
# Поэтому в Python приходится делать доп. обёртку в lookaround-s скобок

# Термины временно разбиты на разные списки чисто ради удобства заполнения этих списков по каким-ни-каким категориям.
# Дальше по коду эти термины всё равно объединяются в один общий regex.
# Эти термины должны форматироваться курсивом и зелёным если они встречаются в переводе слова:
# - отдельно (без скобок или в скобках)
# - в комбинации с другими терминами (комбинации могут быть разделены [,;]?\s - «пробел, перед которым могут стоять
# запятая или точка с запятой»)
#
# В списках ниже обычные строки являются literal-терминами и будут автоматически экранироваться через re.escape().
# Элементы, обёрнутые в regex_fragment(...), являются готовыми regex-фрагментами и поэтому НЕ экранируются.
#
# Например:
#     'амер.'
# превращается в:
#     'амер\.'
#
# а:
#     regex_fragment(r'(?:старо)?англ\.')
# остаётся:
#     '(?:старо)?англ\.'
#
# Благодаря этому в одном списке можно безопасно использовать как простые термины, так и термины с regex-логикой.

english = [
    regex_fragment(r'(?:старо)?англ\.'),
    'амер.',
    'брит.',
    'ирл.',
    'шотл.'
]

# german = ['древнегерм.', 'старонем.', 'нижненем.', 'сев.-нем.', 'ю-нем.', 'австр.', 'нем.']  # 'старонем.' должно идти первее 'нем.'
german = [
    'древнегерм.',
    regex_fragment(r'(?:старо|верхне|нижне|сев\.-|ю-)?нем\.'),
    'австр.'
]

# greek = ['др.-греч.', 'новогреч.', 'греч.', 'эол.']  # 'др.-греч.' и 'новогреч.' должно идти первее 'греч.'
greek = [
    regex_fragment(r'(?:др\.-|ново)?греч\.'),
    'эол.'
]

italian = [
    regex_fragment(r'(?:поздне)?лат\.'),
    'итал.'
]

# slavonic = ['ст.-слав.', 'церк.-слав.', 'слав.']
slavonic = [
    regex_fragment(r'(?:ст\.-|церк\.-)?слав\.')
]

other_langs = [
    'араб.',
    'гавайск.',
    'датск.',
    'ивр.',
    'исп.',
    'польск.',
    'фр.',
    'япон.'
]

search_terms_langs = [
    *english,
    *german,
    *greek,
    *italian,
    *slavonic,
    *other_langs
]


# 'pron. pers.' и 'pron. poss.' должны в будущем piped-списке стоять первее, чем просто 'pron.'. Это нужно для того,
# чтобы движок мог их захватывать, т. к. regex работает только до 1-го захвата
english_morph_terms = [
    'adj.',
    'adv.',
    regex_fragment(r'pron\.\s?(?:pers\.|poss\.|indef\.)?'),
    'cj.',
    'prp.',
    'prtc.'
]

russian_morph_terms = [
    'сущ.',
    'прил.',
    'числ.',
    'мест.',
    'фраз. гл.',
    'мн. ч.',
    'прист.',
    'межд.',
    'сравн. ст.',
    'прист.',
    'предик.'
]

search_terms_med = [
    'med.',
    regex_fragment(r'med\.-pass\.'),
    regex_fragment(r'тж\. med\.')
]

search_terms_gram = [
    *english_morph_terms,
    *russian_morph_terms,
    *search_terms_med,
    'грам.',
    'лингв.',
    'inv.'
]


# Сначала идёт термин со словом 'от', затем этот же термин без слова 'от'. Более длинный термин должен идти раньше,
# чтобы захват был корректным.
search_terms_with_optional_from_part = [
    # 'сокр. от', 'сокр.',
    # 'уменьш. от', 'уменьш.',
    regex_fragment(r'(?:сокр\.|уменьш\.)(?: от)?')  # 'сокр.', 'уменьш.', 'сокр. от', 'уменьш. от'
]


search_terms_misc = [
    *search_terms_with_optional_from_part,
    'colloq.',
    'авт.',
    'акуст.',
    'анат.',
    'архит.',
    'астр.',
    'библ.',
    'биол.',
    'биотех.',
    'бот.',
    'бран.',
    'букв.',
    'бухг.',
    'вежл.',
    'воен.',
    'возд.',
    'высок.',
    'геогр.',
    'геол.',
    'геральд.',
    'горн.',
    'груб.',
    'диал.',
    'досл.',
    'жарг.',
    'зоол.',
    'идиом.',
    'информ.',
    'ирон.',
    'ист.',
    'карт.',
    'книжн.',
    'комп.',
    'косм.',
    'крим.',
    'кул.',
    'лит.',
    'лог.',
    'мат.',
    'матем.',
    'мед.',
    'миф.',
    'мор.',
    'муз.',
    'неодобр.',
    'общ.',
    'обыкн.',
    'охот.',
    regex_fragment(r'(?:тж\. )?перен\.'),
    'полигр.',
    'полит.',
    'поэт.',
    'презр.',
    'преим.',
    'пренебр.',
    'прям.',
    'психол.',
    'разг.',
    'редк.',
    'рел.',
    'рит.',
    'социол.',
    'спорт.',
    'ср.-век.',
    'стр.',
    'страд.',
    'строит.',
    'студ.',
    'театр.',
    'тех.',
    'тлв.',
    'уст.',
    'устар.',
    'устарев.',
    'физ.',
    'физиол.',
    'филос.',
    'фин.',
    'хим.',
    'церк.',
    'шахм.',
    'шутл.',
    'эвф.',
    'эк.',
    'эл.',
    'юр.'
]


# Здесь больше не нужно вручную различать обычные строки и regex-фрагменты.
# build_piped_terms() сам вызывает re.escape() только для обычных строк,
# а готовые RegexFragment оставляет без изменений.
piped_search_terms = build_piped_terms(
    search_terms_langs,
    search_terms_gram,
    search_terms_misc
)

search_terms = fr'(?:{piped_search_terms})'


# разделители, которыми данные термины могут отделяться друг от друга
delimiters2_regex_group = r'(?:[,;]?\s)'

search_regex3 = get_optionally_delimited_terms_search_regex(
    search_terms,
    delimiters2_regex_group
)


# Case 2.3 Выделять зелёным цветом и курсивом tag-и в Basic карточках с грамматикой (т. е. в поле Front)
# Т[12] - самоучитель Попова состоит из 2-х томов
# У[1-8] - каждый том содержит 8 занятий
# Зан[1-5] - каждое занятие содержит максимум 5 занятий
search_regex_tag = r'#\sТ[12]У[1-8]Зан[1-5]'


# Case 2.4 Выделять зелёным цветом и курсивом отдельностоящую букву, обозначающую падеж,
# за которой следует закрывающая круглая скобка или пробел
# N = Nominativ
# G = Genitiv
# D = Dativ
# A = Akkusativ

positive_lookahead_closing_parenthesis_or_space = r'(?=[\)\s])'

search_regex_cases = r'{0}{1}'.format(
    r'(?<!\w)[NGDA]',
    positive_lookahead_closing_parenthesis_or_space
)

# CASE 3. Строки-комментарии

# Case 3.1 Выделять зелёным цветом и курсивом строку, сформированную как однострочный C++-комментарий
# (?m) - это флаг многострочности (чтобы ^ срабатывал в начале каждой строки)
# search_regex_cpp_comment = r'(?m)^\s*//.*'


class A20_GreenAndItalicFormatter:
    def __init__(self):
        # self.a0_CoreAnkiFormatter = A0_CoreAnkiFormatter()
        self.textColorizer = TextColorizer()
        self.textFormatter = TextFormatter()
        self.a30_squareBracketsContentsFormatter = A30_SquareBracketsContentsFormatter()

    def format_green_and_italic(self, html_str):
        def _process(html_line):
            processed_html_line = html_line

            processed_html_line = self.make_green_and_italic(processed_html_line, search_regex1)
            processed_html_line = self.make_green_and_italic(processed_html_line, search_regex2)
            processed_html_line = self.make_green_and_italic(processed_html_line, search_regex_adj_deklination)
            processed_html_line = self.make_green_and_italic(processed_html_line, search_regex_parenthesized_phrases)
            processed_html_line = self.make_green_and_italic(processed_html_line, search_regex3)
            processed_html_line = self.make_green_and_italic(processed_html_line, search_regex_tag)
            # processed_html_line = self.make_green_and_italic(processed_html_line, search_regex_cpp_comment)

            # Временно отключил, т. к. A0_CoreAnkiFormatter.make_formatting работает неправильно:
            # он сначала ищет все plain_text_matches, а потом перебирает их, что в строке "A = Atomicity" приводит
            # к выделению обоих больших букв "A" зелёным и курсивом, хотя регулярное выражение захватывает только
            # ту букву "A", которая стоит в самом начале строки. Но из-за того, что plain_text_matches хранит просто
            # букву "A", теряется понимание того, что одну из них нужно выделять, а другую нет.
            # Здесь все буквы "A" будут выделяться, что является логической ошибкой.
            # В контексте выделения большинства терминов с помощью A0_CoreAnkiFormatter.make_formatting данная ошибка
            # себя не проявляла, а здесь стало очевидно, что такой подход является ошибочным.
            # processed_html_line = self.make_green_and_italic(processed_html_line, search_regex_cases)

            return processed_html_line

        # Разбиваем html_str на отдельные полосы, а те, в свою очередь, на отдельные строки и ищем регулярными
        # выражениями последовательности символов, к которым можно применить форматирование. Поиск в целой html_str
        # без разбивки на отдельные полосы и строки почему не всегда даёт правильный результат: иногда не захватывает
        # нужные последовательности, а иногда хоть и захватывает, но неправильно.
        processed_html_str = AnkiFieldHtmlIntoStripesAndLinesSplitter.split_into_stripes_and_lines(
            html_str,
            _process
        )

        return processed_html_str

    def make_green_and_italic(self, html_str, search_regex):
        # В Анки при форматировании текста курсивом и зелёным (или зелёным и курсивом) порядок добавления тегов
        # к форматируемому тексту зависит от последовательности действий пользователя:
        # более внутренний тег соотв. 1-му действию пользователя, а более внешний тег - 2-му действию пользователя.
        # Более того, Анки может впоследствии переставлять теги местами. Так что завязки на последовательность
        # тегов быть не должно.
        result = html_str

        result = self.textColorizer.colorize_green(result, search_regex)
        result = self.textFormatter.format_italic(result, search_regex)

        return result


###################################################################################################


# test_html_str = '(sg. – pl.)'
test_html_str = 'пришёл (Präsens)'
# test_html_str = '(78Präteritum)'
# test_html_str = '# Т1У3Зан2'
# test_html_str = 'Вы (вежл.) уже здесь?'
# test_html_str = 'нем. лингв. степень'
# test_html_str = '(лингв.) степень'
# test_html_str = '(грам. лингв.) степень'
# test_html_str = 'сын<br>(sg. – pl. nom. – pl. gen.)'
# test_html_str = 'сын<br>(<span style="color: rgb(0, 170, 0);"><i>sg. – pl. nom. – pl. gen.</i></span>)'
# test_html_str = '<span style="color: rgb(0, 170, 0);">[амер.]</span><br>1) авто джип<br>2) авиа небольшой разведывательный самолёт<br>3) <span style="color: rgb(0, 170, 0);"><i>воен.; жарг.</i></span> новичок, новобранец'
# test_html_str = '<span style="color: rgb(0, 170, 0);">[амер.]</span><br>1) авто джип<br>2) авиа небольшой разведывательный самолёт<br>3) <span style="color: rgb(0, 170, 0);"><i>воен.; жарг.</i></span> новичок, новобранец'
# test_html_str = 'Это пример текста: [амер.] и другие слова.'
# test_html_str = 'маульташен<br>(<i>досл. «пастевой карман» разг. (досл. разг. это содержимое внутр. скобок)</i>)'
# test_html_str = 'маульташен<br>(<i>досл. «пастевой карман» разг.</i>)'
# test_html_str = 'маульташен<br>(<i>досл. «пастевой карман» разг.</i>)'
# test_html_str = '(досл. содержимое1)'
# test_html_str = '(<i>досл. содержимое1</i>)'
test_html_str = 'z<br><br>высок. показывать; указывать'
test_html_str = 'амер.; разг. человек'
# test_html_str = '<br><br>высок. показывать; указывать'
# test_html_str = 'отделяемая глагольная приставка, которая указывает на:<br>1) направленность движения изнутри наружу<br>2) отделение части чего-л.<br>3) расширение<br>4) отклонение от прежнего пути<br>5) завершение действия<br><br>высок. показывать; указывать&nbsp;(<i>на кого-л. / что-л.</i>)<br>(<i>w...</i>)<br><br><b>(<i>документально</i>) доказывать, подтверждать</b>'
test_html_str = '(sg. – pl.)'
test_html_str = '1) зоол. корова; бык (как единица крупного рогатого скота)<br>2) pl. крупный рогатый скот<br>(sg. – pl.)<br><br>отбивная<br><br>говяжья отбивная'
# test_html_str = 'pl. крупный рогатый скот<br>(sg. – pl.)<br><br>отбивная<br><br>говяжья отбивная'
test_html_str = """
разг.; сокр. от brother
1) брат
2) преим. амер. братан, старик; дружище, приятель (дружелюбное обращение)

1) байдарочное весло; весло для каноэ
2) сокр. от paddle wheel колёсный пароход
3) лопасть или лопатка (гребного колеса)

1. пряжка
2. англ. готовиться к бою (to buckle on a sword – пристегнуть меч)
"""

test_html_str = """
2) староангл. готовиться к бою
"""

if __name__ == '__main__':
    a20_GreenAndItalicFormatter = A20_GreenAndItalicFormatter()
    res = a20_GreenAndItalicFormatter.format_green_and_italic(test_html_str)
    print(res)

# print(len(search_terms_misc))
# print(sorted(search_terms_misc))