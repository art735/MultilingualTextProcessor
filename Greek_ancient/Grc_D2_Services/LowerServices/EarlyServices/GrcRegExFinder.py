import re

from BaseRegExFinder import BaseRegExFinder
from CharConstants import HYPHEN

class GrcRegExFinder(BaseRegExFinder):
    # Древнегреческие буквы в Юникоде, включая буквы с диакритическими знаками.
    # Здесь две строки склеиваются в одну
    greek_letters = (
        r'\u0370-\u03FF'  # Основной греческий и коптский
        r'\u1F00-\u1FFF'  # Греческий расширенный
    )

    # other_allowed_symbols = r'\s()\-#\[\],’/'
    other_allowed_symbols = f'{HYPHEN}'
    all_allowed_symbols = f'{greek_letters}{other_allowed_symbols}'
    forbidden_symbols = f'[^{all_allowed_symbols}]'

    # Читать подробные требования к формату word_pattern в комментарии к конструктору класса BaseRegExFinder
    greek_word_pattern = f'(?:[{all_allowed_symbols}]+)'
    # Не используется в логике базового класса, но используется в дополнительных методах текущего класса
    non_greek_word_pattern = f'(?:{forbidden_symbols}+)'

    def __init__(self):
        # Вызов конструктора базового класса
        super().__init__(self.greek_word_pattern)

    def find_all_greek_words(self, text):
        return super().find_all_language_specific_words(text)

    def is_greek_word(self, token):
        return super().is_token_a_language_specific_word(token)

    def search_token_for_greek_word(self, token):
        return super().search_token_for_language_specific_word(token)

    def contains_greek_symbols(self, word):
        return super().contains_language_specific_symbols(word)

    def surround_with_spaces_non_greek_inclusions(self, text):
        return super().surround_with_spaces_non_language_specific_inclusions(text)

    ################################################################
    # Дополнительные методы, которых нет в базовом классе и которые появились в результате распознавания словариков
    # в конце учебников Рытовой и Хорикова.
    ################################################################

    # Данный метод позволяет находить все символы, которые не принадлежат греческому алфавиту, хотя внешне выглядят
    # очень похоже на греч. буквы: например, артикль "o", который в результате распознавания мог быть написан с помощью
    # буквы русского или английского алфавита, но не греческого. Такая ошибка приведёт к тому, что слово в словарике
    # будет присутствовать, но не будет найдено алгоритмом поиска лемм.
    def find_non_greek_symbols(self, line):
        non_greek_symbols = re.findall(self.forbidden_symbols, line)
        return non_greek_symbols


#########################################################

input_text = "# 1Ἀρχὴ τοῦ εὐαγγελίου Ἰησοῦ Χριστοῦ [υἱοῦ θεοῦ]."

test_word = 'ἡ θύρα'

if __name__ == '__main__':
    grcRegExFinder = GrcRegExFinder()

    # res = GrcRegExFinder.find_all_greek_words(input_text)
    # print(res)

    # res = GrcRegExFinder.surround_with_spaces_non_greek_inclusions(input_text)
    # print(res)

    # res = grcRegExFinder.is_greek_word("1Ἀρχὴ")
    # res = grcRegExFinder.is_greek_word("Ἀρχὴ1")
    # res = grcRegExFinder.is_greek_word("Ἀρχὴ")
    # res = grcRegExFinder.is_greek_word("Ἀρχὴ τοῦ εὐαγγελίου Ἰησοῦ Χριστοῦ")
    # res = grcRegExFinder.is_greek_word("ἈρχὴτοῦεὐαγγελίουἸησοῦΧριστοῦ")
    res = grcRegExFinder.is_greek_word(test_word)
    print(res)
