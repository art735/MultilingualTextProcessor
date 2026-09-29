NEWLINE = '\n'
SINGLE_NEW_LINE = '\n'
DOUBLE_NEW_LINE = '\n\n'

SPACE = ' '
DOUBLE_SPACE = f'{SPACE}{SPACE}'
NON_BREAKING_SPACE = '\xc2\xa0'
NBSP_unicode = '\u00A0'
NBSP_html = '&nbsp;'

HYPHEN = '-'
DASH = '–'
COMMA = ','

SPACE_DASH_SPACE = f'{SPACE}{DASH}{SPACE}'

LEFT_SINGLE_QUOTATION_MARK = "‘"  # U+2018
RIGHT_SINGLE_QUOTATION_MARK = "’"  # U+2019

STRAIGHT_APOSTROPHE = "'"  # U+0027
CURLY_APOSTROPHE = RIGHT_SINGLE_QUOTATION_MARK  # U+2019

# Возможные знаки ударения в транскрипциях слов
ACCENT_MARK1 = "'"
ACCENT_MARK2 = "ˈ"
ACCENT_MARK3 = "ˌ"
ACCENT_MARKS_REGEX_CLASS = f'[{ACCENT_MARK1}{ACCENT_MARK2}{ACCENT_MARK3}]'

SLASH = '/'
PIPE = '|'

OPEN_PARENTHESIS = '('
CLOSE_PARENTHESIS = ')'

# Используются при обозначении в транскрипциях зубных и альвеолярных согласных
COMBINING_LOW_LINE = '\u0332'  # Unicode "Combining Low Line" (соединительная нижняя линия)
BRIDGE_BELOW = '\u032A'  # Unicode "Bridge Below" (подстрочный мостик)
