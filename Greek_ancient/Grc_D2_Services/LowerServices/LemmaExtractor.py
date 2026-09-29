import re

NEWLINE = '\n'


# Данный метод извлекает леммы из списка-словаря греческих слов, который содержит слова в том виде,
# в котором я его форматирую для учёбы
def extract(text):
    results = []
    lines = [s for s in text.split(NEWLINE) if len(s)]  # взять в дальнейшую работу только непустые строки
    for line in lines:
        stripped = re.sub(r'^([ὁἡ]|τό)\s', r'', line)  # strip definite article at the beginning of the word
        stripped = re.sub(r'\d+', r'', stripped)  # strip digits/numbers
        truncated = stripped.split(',')[
            0]  # если словарная статья содержит запятую(-ые), взять только то, что находится до первой запятой
        unspaced = truncated.split(' ')[
            0]  # если оставшаяся часть содержит пробел, взять только то, что находится до пробела
        results.append(unspaced)
    output = NEWLINE.join(results)
    return output
