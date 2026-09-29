import re

# Константы для замены
EM_DASH = "—"
EN_DASH = "–"
OPEN_CURLY_QUOTE = "“"
CLOSE_CURLY_QUOTE = "”"
SPACE = ' '

# Правила замены: список кортежей (тип_замены, что_заменить, на_что_заменить)
# Тип_замены: "simple" для обычной замены строки, "regex" для регулярного выражения
REPLACEMENT_RULES = [
    # Замена длинного тире (EM_DASH) на короткое (EN_DASH)
    ("simple", EM_DASH, EN_DASH),

    # Замена прямых кавычек вокруг русского текста на кучерявые (захватывающая regex-группа здесь играет важную роль)
    # ("regex", r'"([А-Яа-я\s]*)"', lambda m: f"{OPEN_CURLY_QUOTE}{m.group(1)}{CLOSE_CURLY_QUOTE}"),

    # т.е. / т.д. / т.к. / т.п. --> т. е. / т. д. / т. к. / т. п.
    # regex: ПЕРЕД и ПОСЛЕ аббревиатуры не должно быть символа слова; \b здесь не работает
    ("regex", r'(?<!\w)(т\.)([дезкнпч]\.)(?!\w)', fr'\g<1>{SPACE}\g<2>'),
]

def make_replacements(field_value):
    # Применяем все правила замены
    for rule_type, source, target in REPLACEMENT_RULES:
        if rule_type == "simple":
            # Простая замена строки
            if source in field_value:
                field_value = field_value.replace(source, target)
        elif rule_type == "regex":
            # Замена с использованием регулярного выражения
            field_value = re.sub(source, target, field_value)

    # В конце — обработка кучерявых кавычек для русского текста
    field_value = _replace_straight_quotes_russian(field_value)

    return field_value

# Заменяет прямые кавычки вокруг русского текста на кучерявые, начиная всегда с нечётной кавычки, чтобы замены в исходной строке:
# "embedded device" как "встраиваемое устройство"
# были выполнены так:
# "embedded device" как “встраиваемое устройство”
# а не:
# "embedded device“ как ”встраиваемое устройство"
# По причине того, что замены нужно начинать всегда с нечётной прямой кавычки (а не с первой попавшейся), захват и
# замена с помощью регулярного выражения не подходит, нужна более сложная логика.
def _replace_straight_quotes_russian(text):
    result = []
    in_quote = False
    last_quote_index = -1

    i = 0
    while i < len(text):
        char = text[i]
        if char == '"':
            if in_quote:
                # закрывающая кавычка
                quoted_text = text[last_quote_index + 1:i]
                if re.fullmatch(r'[А-Яа-яЁё\s]+', quoted_text):
                    result[last_quote_index] = OPEN_CURLY_QUOTE
                    result.append(CLOSE_CURLY_QUOTE)
                else:
                    # если текст не русский — оставить как есть
                    result[last_quote_index] = '"'
                    result.append('"')
                in_quote = False
            else:
                last_quote_index = len(result)
                result.append('"')  # временно добавим прямую кавычку
                in_quote = True
        else:
            result.append(char)
        i += 1

    return ''.join(result)



############################################

test_str = 'кодинг, т.е. программирование'
test_str = '"embedded device" как "встраиваемое устройство"'

if __name__ == '__main__':
    res = make_replacements(test_str)
    print(res)


    input1 = [
        # Замена длинного тире (EM_DASH) на короткое (EN_DASH)
        'a — b',

        # Замена прямых кавычек вокруг русского текста на кучерявые
        '"термин"', '"несколько терминов через пробелы"', '"embedded device" как "встраиваемое устройство"',

        # т.е. --> т. е.
        'кодинг, т.е. программирование',
        # т.д. --> т. д.
        'яблоки, груши и т.д. по тексту', '(яблоки, груши и т.д.)',
        # т.к. --> т. к.
        'устройства IoT используют Lua для настройки, т.к. язык лёгкий',
        # т.п. --> т. п.
        'C, C++ и т.п.', 'и т.п. вещи',
        'т.е. и т.д. и т.п.'
    ]

    er1 = [
        # Замена длинного тире (EM_DASH) на короткое (EN_DASH)
        'a – b',

        # Замена прямых кавычек вокруг русского текста на кучерявые
        '“термин”', '“несколько терминов через пробелы”', '"embedded device" как “встраиваемое устройство”',

        # т.е. --> т. е.
        'кодинг, т. е. программирование',
        # т.д. --> т. д.
        'яблоки, груши и т. д. по тексту', '(яблоки, груши и т. д.)',
        # т.к. --> т. к.
        'устройства IoT используют Lua для настройки, т. к. язык лёгкий',
        # т.п. --> т. п.
        'C, C++ и т. п.', 'и т. п. вещи',
        'т. е. и т. д. и т. п.'
    ]

    if all(make_replacements(input_val) == er for input_val, er in zip(input1, er1)):
        print('test1 ok')
    else:
        print('test1 failed')
