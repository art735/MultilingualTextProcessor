import re

from LowerServices.GrcConstants import PIPE, NEWLINE


# https://www.ebible.gr/lexicon/strong
# - в чётных строках (i%2==0) находятся начальные формы слов: сплитим содержимое строки по пробелу и объединяем полученные непустые куски с помощью пайпа |
# - в нечётных строках находятся словоформы слова из предыдущей строки: присоединяем содержимое этой строчки "как есть" с помощью пайпа к результату предыдущего этапа
def run(input_text):
    if len(input_text) == 0:
        return ''

    processed_lines = list()
    lines = re.split('\n', input_text)

    if len(lines) % 2 != 0:
        return "ERROR: number of lines must be an even number!"

    for i in range(0, len(lines), 2):
        first_line = PIPE.join(lines[i].split())
        second_line = lines[i + 1]
        processed_lines.append(first_line + PIPE + second_line)

    result = NEWLINE.join(processed_lines)
    return result

#########################

# text = "ἀγαθοποιέω 10\nἀγαθοποιεῖτε 1,  ἀγαθοποιῆσαι 2,  ἀγαθοποιῆτε 1,  ἀγαθοποιοῦντας 3,  ἀγαθοποιοῦντες 1,  ἀγαθοποιοῦσαι 1,  ἀγαθοποιῶν 1"
# res = run(text)
# print(res)
