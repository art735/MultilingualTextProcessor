# # coding: utf-8
# from __future__ import unicode_literals
#
# from apso_utils import console, msgbox
# import re
#
# #import uno
import TableUtils
import UnoUtils


class S2_TextReplacer:
    def __init__(self, doc):
        self.doc = doc

        # self.search_descriptor = doc.createSearchDescriptor()
        # self.search_descriptor.SearchRegularExpression = True

        self.replace_descriptor = doc.createReplaceDescriptor()
        self.replace_descriptor.SearchRegularExpression = True

    def replace_all(self, search_str, replace_str):
        self.replace_descriptor.SearchString = search_str
        self.replace_descriptor.ReplaceString = replace_str
        self.doc.replaceAll(self.replace_descriptor)

    def run(self):
        # WHITESPACE = " "
        # HYPHEN = "-"

        # *** Заменить два и более пробела одним пробелом ***

        # первая часть регулярки - \s - ищет в тексте ровно один пробел
        # вторая часть регулярки - \s+ - ищет в тексте количество пробелов "один и более"
        # итоговая регулярка ищет в тексте два и более пробела и заменяет их одним пробелом
        self.replace_all("\s\s+", " ")

        # *** Удалить пробел в начале и в конце абзаца ***

        # ^ - начало абзаца
        # $ - конец абзаца
        self.replace_all("^\s|\s$", "")

        # *** Заменить длинное тире на обычное тире ***

        # Здесь можно узнать код символа
        # https://www.babelstone.co.uk/Unicode/whatisit.html

        # U+2013 : EN DASH
        EN_DASH = "–"

        # U+2014 : EM DASH
        EM_DASH = "—"

        # U+2015 : HORIZONTAL BAR {quotation dash}
        HORIZONTAL_BAR = "―"

        self.replace_all(EM_DASH, EN_DASH)
        self.replace_all(HORIZONTAL_BAR, EN_DASH)

        # *** Заменить два подряд идущих дефиса на обычное тире ***
        self.replace_all("--", EN_DASH)

        # *** Заменить пробел-дефис-пробел на пробел-тире-пробел ***
        self.replace_all("\s-\s", " – ")

        # *** Убедиться, что тире отделяется от окружающих его букв (но не цифр в датах) пробелами ***
        # self.replaceAll("([:alpha:])–([:alpha:])", "$1 – $2")

        # а) поставить пробел между (не-цифрой или не-пробелом) и тире
        self.replace_all("([^0-9\s])(–)", "$1 $2")

        # б) поставить пробел между тире и (не-цифрой или не-пробелом)
        self.replace_all("(–)([^0-9\s])", "$1 $2")

        # *** Заменить машинописный апостроф на кудрявый апостроф ***

        # U+0027 : APOSTROPHE {single quote; APL quote}
        APOSTROPHE = "'"

        # U+2019 : RIGHT SINGLE QUOTATION MARK {single comma quotation mark}
        RIGHT_SINGLE_QUOTATION_MARK = "’"

        self.replace_all(APOSTROPHE, RIGHT_SINGLE_QUOTATION_MARK)

        # *** Удалить пробел перед НЕКОТОРЫМИ знаками препинания ***

        # В русском языке 10 знаков препинания:
        # точка, запятая, точка с запятой, двоеточие, восклицательный знак, вопросительный знак, многоточие,
        # тире, кавычки, скобки.

        # многоточие в данной регулярке - это один символ, выглядящий как три точки, а не три разных точки
        # формула регулярки: пробел + positive lookahead
        self.replace_all("\s(?=[.,;:!?])", "")

        # удалить пробел перед троеточием: будь оно представлено в тексте единым символом, изображающим троеточие, или тремя отдельными точками
        self.replace_all("\s(?=…|[.]{3})", "")

        # *** Удалить пробел после открывающей круглой скобки и перед закрывающей круглой скобкой ***

        # These lookarounds are NOT captured by regexp
        openParenthesisPositiveLookbehind = "(?<=\()"
        closingParenthesisPositiveLookahead = "(?=\))"
        WHITESPACE_REGEX = "\s"

        # найти пробел после открывающей скобки и удалить его
        self.replace_all(openParenthesisPositiveLookbehind + WHITESPACE_REGEX, "")

        # найти пробел перед закрывающей скобкой и удалить его
        self.replace_all(WHITESPACE_REGEX + closingParenthesisPositiveLookahead, "")

        # *** Сделать неразрывный пробел в сокращениях т.д., т.е., т.п.

        # U+00A0 : Non-breaking space [NBSP]
        NBSP = " "

        # т.д., т.е., т.п., т.ч. с пробелом и без становятся с неразрывным пробелом
        # запись \s? означает "нет пробела или один пробел"
        self.replace_all("(т\.)\s?([дезкнпч]\.)", "$1" + NBSP + "$2")

        # *** Сделать неразрывный пробел в сокращении н.э.

        # н.э. с пробелом и без становится с неразрывным пробелом
        self.replace_all("(н\.)\s?(э\.)", "$1" + NBSP + "$2")

        # *** Сделать пробел между цифрой/числом и следующими сокращениями НЕРАЗРЫВНЫМ:
        # г. (год), например 1905 г.
        # гг. (годы), например 1941–1945 гг.

        # |квантификатор +| после [:digit:] можно и не ставить, он просто подчёркивает,
        # что ищем не обязательно одну последнюю цифру, а можно и набор цифр (номер года состоит обычно из 4-х цифр)
        # (гг?\.) - данная группа ищет букву г, за которой следует или не следует ещё одна буква г, за которой следует точка, т.е. ищет (г.) или (гг.)
        self.replace_all("([:digit:]+)\s?(гг?\.)", "$1" + NBSP + "$2")

        # *** Сделать пробел между цифрой/числом и следующими сокращениями НЕРАЗРЫВНЫМ:
        # мм (миллиметр), м (метр), км (километр)
        # мг (миллиграмм), г (грамм), кг (килограмм)

        # [мк]? - класс приставок: м (милли-), к (кило-); приставка может быть или не быть (квантификтор ?)
        # м|г - это буквы м (метр) или г (грамм)
        self.replace_all("([:digit:]+)\s?([мк]?(м|г))", "$1" + NBSP + "$2")

        # *** Поставить букву ё в словах Еще/еще/Ее/ее ***

        # the metacharacter \b is an anchor like the caret and the dollar sign,
        # it matches at a position that is called a “word boundary”. This match is zero-length.
        # for \b in Python to match a word boundary, it should be in a "raw" string
        # формула выражения: positive lookbehind + е, обрамлённые символом границы слова \b...\b
        self.replace_all(r"(?<=\b[Ее]щ?)е\b", "ё")

        # *** Заменить в диапазоне исторических дат дефис на тире ***

        # positive lookbehind + HYPHEN + positive lookahead
        self.replace_all("(?<=[0123456789XVI])-(?=[0123456789XVI])", EN_DASH)

        # *** По ГОСТу пробел СТАВИТСЯ в тексте после следующих знаков:
        # - «точка» (отключил из-за особенностей оформления словариков)
        # - «запятая»
        # - «двоеточие»
        # - «точка с запятой»
        # - «восклицательный знак»
        # - «вопросительный знак»
        self.replace_all("([,:;!?])([:alpha:])", "$1 $2")

        # отдельная регулярка для многоточия (будь оно представлено единым символом, или тремя отдельными точками)
        # self.replaceAll("(…|[.]{3})([:alpha:])", "$1 $2")

        # *** По ГОСТу пробел СТАВИТСЯ в тексте после следующих знаков:
        # - «параграф» §
        # - «номер» №
        # - «решётка» # (добавил от себя как альтернативу знаку №)
        # - в регулярке во второй группе в скобках к буквам добавлены ещё и цифры (по сравнению с регулярками выше)
        self.replace_all("([§№#])([:alnum:])", "$1 $2")

        ###############################################

        # ПРОВЕРИТЬ РАБОТОСПОСОБНОСТЬ ЭТОГО КОДА!!!
        tables = doc.getTextTables()
        for table_name in tables.getElementNames():
            table = tables.getByName(table_name)
            TableUtils.disable_setting_allow_row_to_break_across_pages_and_columns(table)

        UnoUtils.show_messagebox('Info', 'GeneralFormatter has worked!')
        # msgbox("GeneralFormatter has worked!!!")
