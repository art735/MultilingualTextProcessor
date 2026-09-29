import re

from CharConstants import CURLY_APOSTROPHE, STRAIGHT_APOSTROPHE


def replace_apostrophe_space_accent(text):
    # Соответствие неударных заглавных греческих букв их ударным аналогам
    accent_map = {
        'Α': ' Ά',
        'Ε': ' Έ',
        'Η': ' Ή',
        'Ι': ' Ί',
        'Ο': ' Ό',
        'Υ': ' Ύ',
        'Ω': ' Ώ',
    }

    # Функция замены, которую вызывает re.sub
    def replacer(match):
        letter = match.group(1)
        return accent_map.get(letter, letter)

    # Замена: ищем ' + пробел + заглавную неударную греческую букву
    return re.sub(fr"[{CURLY_APOSTROPHE}{STRAIGHT_APOSTROPHE}]\s?([ΑΕΗΙΟΥΩ])", replacer, text)


###########################################

text = """

"""

res = replace_apostrophe_space_accent(text)
print(res)
