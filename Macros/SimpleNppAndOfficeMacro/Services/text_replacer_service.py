# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import sys
from collections import OrderedDict

import macro_utils

# Здесь можно узнать код символа
# https://www.babelstone.co.uk/Unicode/whatisit.html
EN_DASH = "–"  # U+2013 : EN DASH
EM_DASH = "—"  # U+2014 : EM DASH
HORIZONTAL_BAR = "―"  # U+2015 : HORIZONTAL BAR {quotation dash}

SPACE = ' '
HYPHEN = '-'
DASH = '–'

def make_replacements(text):
    line_ending = macro_utils.resolve_line_ending(text)

    # Чтобы сохранить CRLF в конце Notepad++ строк, разбиваем текст по разделителю на отдельные Python-строки,
    # обрабатываем их, и затем склеиваем обратно по тому же самому разделителю.
    lines = text.split(line_ending)
    for i in range(len(lines)):
        line = lines[i]

        if isinstance(line, str) and sys.version_info[0] < 3:
            line = unicode(line, 'utf-8')  # только для Python 2

        for j in range(0, 1):  # количество прогонов всех замен для каждой строки. По умолчанию 1, можно делать 2.
            for pattern, replacement in get_find_and_replace_dict().items():
                line = re.sub(pattern, replacement, line)

        lines[i] = line

    # Объединить строки обратно с правильным разделителем
    text = line_ending.join(lines)

    return text

# Словарь find_and_replace_dict специально НЕ сделан глобальной переменной, а обёрнут в данный метод, чтобы при
# обращении к словарю, можно было добавить дополнительную логику его адаптации к Python2-среде.
# Данный метод, по сути, является геттером, который инкапсулирует словарь и добавляет бизнес-логику возможной
# модификации словаря при его затребовании вызывающим кодом. А вызывается данный метод как из текущего модуля,
# так и из Python2-макроса для OpenOffice.
def get_find_and_replace_dict():
    # В Python2 словарь - это неупорядоченная структура данных. Словари стали упорядоченными начиная с
    # Python 3.7 (порядок вставки ключей в словарь стал гарантированно сохраняться).
    # В Python2 упорядочить пары ключ-значение (в виде кортежей) можно с помощью OrderedDict.
    # Поскольку OpenOffice ориентирован именно на Python2 (2025 год), используем OrderedDict вместо обычного
    # словаря.
    # Что касается Notepad++, то его плагин 'Python Script' можно обновить до состояния поддержки Python3.
    # ВАЖНО: для поиска пробела использовать именно ' ', а не \s, т. к. \s вызывает ошибку работы в LibreOffice.
    # TODO: после внесения изменений в словарь обязательно нужно перезапускать LiberOffice Writer и Notepad++ чтобы
    #  изменения вступили в силу. Без перезагрузки приложений в них будет выполняться старая закешированная версия кода.
    find_and_replace_dict = OrderedDict([
        # Заменить табуляцию на пробел
        (r'\t', SPACE),

        # Заменить длинное тире, HORIZONTAL_BAR или "--" на обычное тире
        (r'|'.join([EM_DASH, HORIZONTAL_BAR, '--']), EN_DASH),

        # Заменить пробел-дефис-пробел на пробел–тире–пробел
        (r'{}{}{}'.format(SPACE, HYPHEN, SPACE), r'{}{}{}'.format(SPACE, DASH, SPACE)),

        # Удалить символ '*'
        (r'\*', ''),

        # Удаление markdown-а в начале строки
        (r'^#{1,6}[ ]*', ''),
        (r'^>[ ]*', ''),
        # удаление emoji из диапазона символов Unicode, где большинство emoji и расположены
        (r'^[\U0001F300-\U0001FAFF][ ]*', ''),

        # Заменить 2 и более пробелов на один пробел
        (r'[ ]{2,}', SPACE),

        # Удалить пробелы и другие символы (всего 6 вариантов [ \t\n\r\f\v]) по краям строк
        # LibreOffice не поддерживает замену по лябда-функции, поэтому нужно переписать в виде регулярного выражения
        (r'^[ ]+|[ ]+$', ''),

        # Заменить '\[' на '['
        (r'\\\[', '['),
    ])

    # Импорт "from __future__ import unicode_literals" решил эту проблему!
    # # Пересборка словаря для корректной работы в Python2 с приведением всех ключей и значений к Unicode.
    # if sys.version_info[0] < 3:
    #     # unicode() — это встроенная функция в Python 2.x
    #     # Она не импортируется из библиотек, а уже присутствует в интерпретаторе.
    #     # В Python 2 есть два типа строк:
    #     # 1) str — это байтовая строка (8-бит)
    #     # 2) unicode — это Юникод-строка (16/32-бит, в зависимости от сборки)
    #     # Функция unicode(s, encoding) используется для декодирования байтовой строки в Unicode.
    #     # В Python 3 все строки по умолчанию — Unicode (str), а unicode как тип — удалён.
    #     # Если попытаться вызвать unicode() в Python 3 — будет NameError.
    #     # Если нужно написать код, который работает и в Python 2, и в Python 3, можно использовать такой трюк:
    #     find_and_replace_dict = OrderedDict([
    #         (_to_unicode(k), _to_unicode(v))
    #         for k, v in find_and_replace_dict.items()
    #     ])

    return find_and_replace_dict


# # Явная юникодификация строки для совместимости с Python2
# def _to_unicode(obj):
#     if isinstance(obj, str):
#         return unicode(obj, 'utf-8')
#     else:
#         return obj

#########################################################################

test_text = """
привет - мир

**gasdf  **
bbb *************
"""

test_text = '### 💡 Исправленный и рабочий код:'
test_text = '### 📦 Что делает этот код:'
test_text = '🔹 Эспандер'
test_text = '* \[ˈlæŋɡwɪdʒ]'


if __name__ == '__main__':
    res = make_replacements(test_text)
    print(res)

    test1_input = [
    """
привет - мир

    **gasdf  **
bbb *************

""",
        '### 💡 Исправленный и рабочий код:',
        '### 📦 Что делает этот код:',
        '🔹 Эспандер',
        '> эспандер',
        '📘 Например',
        '* \[ˈlæŋɡwɪdʒ]'
    ]
    test1_er = [
    """
привет – мир

gasdf
bbb

""",
        'Исправленный и рабочий код:',
        'Что делает этот код:',
        'Эспандер',
        'эспандер',
        'Например',
        '[ˈlæŋɡwɪdʒ]'
    ]
    if all(make_replacements(input_val) == er for input_val, er in zip(test1_input, test1_er)):
        print("test1 - ok")
    else:
        print("test1 - failed")
