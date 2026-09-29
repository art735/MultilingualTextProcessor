# -*- coding: utf-8 -*-

import regex as re

SPACE = ' '

def split_into_sentences(text):
    # 1. Разбиваем текст на отдельные предложения
    sentences = split_into_sentences_internal(text)

    # 2. Определяем стиль строк в исходном тексте: CRLF (\r\n), LF (\n), или CR (\r).
    # line_ending = macro_utils.resolve_line_ending(text)

    # Когда пользователь выделяет в окне Notepad++ только одну строку с текстом, разделитель CRLF не попадает в эту
    # выделенную область, а значит и не определяется алгоритмом корректно как CRLF-разделитель, а по остаточному
    # принципу выводится как '\n'-разделитель (см. метод macro_utils.resolve_line_ending(...))
    # Для корректного определения разделителя как CRLF нужно, чтобы выделение текста, сделанное пользователем,
    # содержало больше одной строки текста. Для консистентности работы задаём здесь разделитель вручную.
    line_ending = '\r\n'

    # 3. Склеиваем коллекцию предложений по исходному разделителю
    text = line_ending.join(sentences)

    return text


def split_into_sentences_internal(text):
    # Заменить 2 и более пробелов на один
    text = re.sub(' {2,}', SPACE, text)

    # Цель: сделать lookbehind регистронезависимым и расширить его на латиницу, кириллицу и греческий алфавит.
    # Правильный путь: использовать не жёсткие классы [A-Z] и [a-z], а Unicode-классы букв из библиотеки regex
    # (стандартный модуль re не даёт такой возможности).
    # \p{Lu} — любая заглавная буква (лат., рус., греч., вообще любая).
    # \p{Ll} — любая строчная буква.
    # \p{L} — любая буква.
    lookbehind = (
        r'(?<!\w\.\w\.)'  # X.X.
        r'(?<!\p{Lu}\p{Ll}\.)'  # Аб., Ab., Αβ.  (Любая загл.+строчн.)
        r'(?<=[.?!…])'  # конец предложения
    )

    quotes = r'"\'„“«»›‹”‚‘”’'
    quotes_class_optional = '[' + quotes + ']*'

    # «После конца предложения должен идти пробел + (опц. кавычки) + любая заглавная буква Юникода».
    # Работает для:
    # Латиницы (A, B, C…)
    # Кириллицы (А, Б, В, К…)
    # Греческих (Α, Β, Γ…)
    # Вообще всех алфавитов
    lookahead = r'(?=\s' + quotes_class_optional + r'\p{Lu})'

    pattern = lookbehind + quotes_class_optional + lookahead

    sentence_split_re = re.compile(pattern)

    positions = []
    for match in sentence_split_re.finditer(text):
        positions.append(match.end())

    # Без *-распаковки: вручную
    positions = [0] + positions + [len(text)]

    sentences = []
    for i in range(len(positions) - 1):
        start = positions[i]
        end = positions[i + 1]
        sentence = text[start:end].strip()
        sentences.append(sentence)

    return sentences

#####################################

test_text = 'Sentence 1! Sentence 2.'
test_text = 'Привет. Как дела? Всё хорошо!'
test_text = 'Γεια σου. Τι κάνεις; Όλα καλά!'

if __name__ == '__main__':
    res = split_into_sentences(test_text)
    print(res)

    # res = split_into_sentences_internal(test_text)
    # print(res)

    test1_input = [
        'She moved to the U.S. in 1995. Later, she started working in education.',
        'Dr. Smith will join us shortly. Please take a seat.',
        'It’s over... I can’t believe it… Are you happy now?',
        u'„Ich bin müde“, sagte er. „Ich gehe jetzt.“ Was willst du tun? „Nichts…“, flüsterte sie.',
        u'Das ist wahr.“ Nun gut.',
        u'Er sagte: „Ich komme gleich.“ Dann ging er.',
        u"""Dr. Jones, a noted historian from the U.S., gave a lecture on colonial history. It was well-received by both students and faculty. "History is not just about the past," he said. "It's about understanding our present." Mr. A.B. Carter, who also attended, agreed wholeheartedly. He added, "We often forget that context is everything… Don't we?" Afterwards, they had coffee at St. Mary’s Café. The event was organized by Ms. Taylor and co-hosted by Professor Lewis.""",
        'Привет. Как дела? Всё хорошо!',
        'Γεια σου. Τι κάνεις; Όλα καλά!',
    ]

    test1_er = [
        ['She moved to the U.S. in 1995.', 'Later, she started working in education.'],
        ['Dr. Smith will join us shortly.', 'Please take a seat.'],
        ['It’s over...', 'I can’t believe it…', 'Are you happy now?'],
        [u'„Ich bin müde“, sagte er.', u'„Ich gehe jetzt.“', u'Was willst du tun?', u'„Nichts…“, flüsterte sie.'],
        [u'Das ist wahr.“', u'Nun gut.'],
        [u'Er sagte: „Ich komme gleich.“', u'Dann ging er.'],
        [
            'Dr. Jones, a noted historian from the U.S., gave a lecture on colonial history.',
            'It was well-received by both students and faculty.',
            '"History is not just about the past," he said.',
            '"It\'s about understanding our present."',
            'Mr. A.B. Carter, who also attended, agreed wholeheartedly.',
            'He added, "We often forget that context is everything…',
            'Don\'t we?"',
            'Afterwards, they had coffee at St. Mary’s Café.',
            'The event was organized by Ms. Taylor and co-hosted by Professor Lewis.'
        ],
        ['Привет.', 'Как дела?', 'Всё хорошо!'],
        ['Γεια σου.', 'Τι κάνεις; Όλα καλά!'],
    ]

    all_ok = True
    for i in range(len(test1_input)):
        input_val = test1_input[i]
        expected = test1_er[i]
        result = split_into_sentences_internal(input_val)
        if result != expected:
            all_ok = False
            print("Case %d:" % (i + 1))
            print("Input:    %s" % input_val)
            print("Expected: %s" % expected)
            print("Got:      %s" % result)

    if all_ok:
        print("test1 - ok")
    else:
        print("test1 - failed")
