from BaseRegExFinder import BaseRegExFinder


class DeuRegExFinder(BaseRegExFinder):
    # Немецкое слово - это слово, которое:
    # - содержит прописные и строчные буквы немецкого алфавита
    # - содержит букву é (das Café) (заимствование из французского языка???)
    # - содержит дефис в любой позиции: в начале слова (-lich), в середине слова (Test-Text), в конце слова (Bundes-);
    # но дефис не может стоять сам по себе и считаться немецким словом.
    # - содержит открывающую круглую скобку в начале или середине слова и закрывающую круглую скобку в середине или
    # конце слова: (Auto)mobile, Auto(mobile), Str(aßen)-bahn. Одновременное наличие открывающей круглой скобки
    # в начале слова и закрывающей круглой скобки в конце слова не допускается: (Automobile).
    # Количество открывающих и закрывающих круглых скобок в слове должно совпадать, но это проверяется не регулярным
    # выражением, а логикой внутри метода BaseRegExFinder.is_token_a_language_specific_word(...)
    # Особо обратить внимание:
    # - отдельно стоящая буква считается валидным немецким словом, но отдельно стоящий дефис(-ы) или
    # открывающая/закрывающая круглая скобка(-и) не могут считаться валидным немецким словом.

    german_letters = r'a-zA-ZäöüÄÖÜßé'
    german_letters_with_hyphen_and_parentheses = fr'{german_letters}\-\(\)'

    # german_letters_class = fr'[{german_letters}]'  # в конце класса - дефис как допустимый символ немецкого слова
    # german_letters_with_parentheses_class = fr'[{german_letters_with_hyphen_and_parentheses}]'

    # Возможные случаи начала слова
    # start_with_letter = fr'{german_letters_class}'
    # start_with_open_bracket = r'\('

    # Основная часть слова, включая возможность наличия скобок
    # word_core = fr'{german_letters_with_parentheses_class}+'

    # Возможные случаи конца слова
    # end_with_letter = fr'{german_letters_class}'  # Заканчивается буквой
    # end_with_close_bracket = r'\)'  # Заканчивается закрывающей скобкой

    # Возможные варианты композиции слов (все случаи кроме того, когда слово начинается и заканчивается скобками)
    # word_var1 = fr'{start_with_letter}{word_core}{end_with_letter}'
    # word_var2 = fr'{start_with_open_bracket}{word_core}{end_with_letter}'
    # word_var3 = fr'{start_with_letter}{word_core}{end_with_close_bracket}'

    # Здесь должна быть обязательно non-capturing group (а не capturing group), иначе
    # re.split(self.language_specific_word_pattern, text) в методе
    # surround_with_spaces_non_language_specific_inclusions(...) будет работать неправильно.
    # Регулярное выражение в Python по умолчанию ищет первое совпадение и останавливается на нём,
    # что иногда может привести к тому, что будут проверены не все альтернативы.
    # Регулярные выражения проверяют альтернативы слева направо. Если один из вариантов (например, word_var1)
    # является более общим или более коротким, чем другие, он будет захвачен первым, и остальные не будут проверены.
    # Чтобы избежать этого, упорядочьте варианты так, чтобы более длинные или специфичные варианты шли первыми:
    # word_var3 - это более специфичный вариант, т. к. предполагает наличие закрывающей скобки и он в списке вариантов
    # должен идти первым! За ним должен идти word_var2, как более специфичный, чем word_var1.
    # Читать подробные требования к формату word_pattern в комментарии к конструктору класса BaseRegExFinder
    # german_word_pattern = fr'(?:{word_var3}|{word_var2}|{word_var1})'

    # Единственный случай, когда данная регулярка будет работать не так как нужно по бизнес-правилам: это когда ей
    # попадётся немецкое слово в скобках (der Mann). Этот случай успешно захватывается регуляркой, но по сути
    # не является валидным немецким словом, и этот случай будет обрабатываться доп. проверкой в if.
    # Регулярка - не идеальна, зато простая и дальше проще if-проверками отсеять невалидные случаи, чем наворачивать и
    # тестировать сложную регулярку.
    # german_word_pattern = fr'(?:{german_letters_with_parentheses_class}+)'

    # optional_word_start = fr'[\-\(]?'
    # word_core = fr'(?:{german_letters_with_parentheses_class}+)'
    # optional_word_end = fr'[\-\)]?'

    # german_word_pattern = fr'(?:{optional_word_start}{word_core}{optional_word_end})'
    # german_word_pattern = fr'(?:{german_letters}(?:[\-\({0}]+{german_letters})*[\-\){0}]*)'

    # Не допускаем, чтобы слово было заключено в скобки
    negative_lookahead_of_word_in_parentheses = r'(?!^\([^)]*\)$)'

    # Не допускаем, чтобы слово состояло исключительно из дефисов и/или скобок в любой комбинации и любой длины
    negative_lookahead_of_word_of_hyphens_and_parentheses_only = r'(?!^[\-\(\)]+$)'

    # Не допускаем, в слове двух и более дефисов подряд
    negative_lookahead_of_two_and_more_consecutive_hyphens = r'(?!.*[\-]{2,}.*)'

    # Несколько lookahead-ов может идти подряд, т. е. их можно использовать последовательно,
    # т. к. они НЕ перемещают указатель в строке.
    # Все идущие подряд lookahead-ы должны выполняться, чтобы шаблон считался соответствующим.
    # Склеиваем все lookahead-ы в одну строку (без каких-либо разделителей).
    negative_lookaheads = (
        fr'{negative_lookahead_of_word_in_parentheses}'
        fr'{negative_lookahead_of_word_of_hyphens_and_parentheses_only}'
        fr'{negative_lookahead_of_two_and_more_consecutive_hyphens}'
    )

    german_word_core = fr'[{german_letters_with_hyphen_and_parentheses}]+'

    german_word_pattern = fr'(?:{negative_lookaheads}{german_word_core})'

    def __init__(self):
        # Вызов конструктора базового класса
        super().__init__(self.german_word_pattern)

    def find_all_german_words(self, text):
        return super().find_all_language_specific_words(text)

    def is_token_a_canonical_word(self, token: str):
        return super().is_token_a_language_specific_word(token)

        # is_a_german_word = super().is_token_a_language_specific_word(token)
        # if is_a_german_word:
        #     # Проверяем, что token не соответствует ни одному из регулярных выражений
        #     # 1-й паттерн в списке: захватывает отдельно стоящий(-е) дефис(ы) (не в составе слова)
        #     # is_not_in_ignored_words = not any(re.match(p, token) for p in [r'(?<!\w)[\-]+(?!\w)'])
        #     is_not_in_ignored_words = True
        #     # Проверяем, что token не находится в круглых скобках
        #     is_not_in_parentheses = not (token.startswith('(') and token.endswith(')'))
        #     is_equal_quantity_of_parentheses = token.count('(') == token.count(')')
        #     if is_not_in_ignored_words and is_not_in_parentheses and is_equal_quantity_of_parentheses:
        #         return True
        #
        # return False

    #     return self.test(token)

    # def test(self, token: str):
    #     german_letters = r'a-zA-ZäöüÄÖÜßé'
    #     german_word_pattern = fr'''
    #         (?:
    #             (?!^\([^)]*\)$)                 # negative lookahead: не допускаем, чтобы слово было заключено в скобки
    #             (?!^[\-\(\)]+$)                 # negative lookahead: не допускаем, чтобы слово состояло исключительно из дефисов и скобок в любой комбинации и любой длины
    #             [{german_letters}\-\(\)]+       # В середине могут быть буквы, дефисы и скобки
    #         )
    #     '''
    #
    #     anchored_german_word_pattern = fr'^{german_word_pattern}$'
    #     pattern = re.compile(anchored_german_word_pattern, re.VERBOSE)
    #
    #     match = re.match(pattern, token)
    #     if match:
    #         return True
    #     else:
    #         return False

    def search_token_for_german_word(self, token):
        return super().search_token_for_language_specific_word(token)

    def contains_german_symbols(self, word):
        return super().contains_language_specific_symbols(word)

    def surround_with_spaces_non_german_inclusions(self, text):
        return super().surround_with_spaces_non_language_specific_inclusions(text)

        # Пример строки
        # text = "123abc456def789ghi"

        # Используем метод класса в качестве предиката
        # predicate = self.is_token_a_german_word
        #
        # # Используем groupby для группировки символов по предикату
        # groups = itertools.groupby(text, key=predicate)
        #
        # # Собираем группы, отфильтровывая группы, которые соответствуют предикату (т. е. цифры)
        # # Собираем группы, отфильтровывая группы, которые соответствуют предикату (т. е. цифры)
        # split_result = [''.join(group) for k, group in groups if not k]
        #
        # return split_result


#########################################################

input_text = "123Das ist ein Test-Text mit deutschen Wörtern wie Fußgängerübergang und E-Mail2."
input_text = "a123."
input_text = "Das ist ein -- Test-Text"
input_text = "a--b"
input_text = "a---b"
# input_text = "(Das)"
# input_text = "Test-Text"
# input_text = "Test - Text"
# input_text = "--"

if __name__ == '__main__':
    deuRegExFinder = DeuRegExFinder()

    # res = deuRegExFinder.find_all_german_words(input_text)
    # print(res)

    # res = deuRegExFinder.surround_with_spaces_non_german_inclusions(input_text)
    # print(res)

    # res = deuRegExFinder.is_token_a_german_word("1Das")
    # res = deuRegExFinder.is_token_a_german_word("Das1")
    # res = deuRegExFinder.is_token_a_german_word("Das")
    # res = deuRegExFinder.is_token_a_german_word("Das ist ein Test-Text")
    # res = deuRegExFinder.is_token_a_german_word("DasisteinTest-Text")
    # res = deuRegExFinder.is_token_a_german_word("-")
    # res = deuRegExFinder.is_token_a_german_word("--")
    # res = deuRegExFinder.is_token_a_german_word("VS_02_2803")
    # res = deuRegExFinder.is_token_a_german_word("Bundes-")
    # res = deuRegExFinder.is_token_a_german_word("Café")
    # res = deuRegExFinder.is_token_a_german_word("-lich")
    # res = deuRegExFinder.is_token_a_german_word("-")

    # res = deuRegExFinder.is_token_a_german_word("Auto(mobile)")
    # res = deuRegExFinder.is_token_a_german_word("Verkehr(smittel)")
    # res = deuRegExFinder.is_token_a_german_word("Str(aßen)-bahn")

    # res = deuRegExFinder.is_token_a_german_word("Ich")
    # res = deuRegExFinder.is_token_a_german_word("(will)")
    # res = deuRegExFinder.is_token_a_german_word("ab")
    # res = deuRegExFinder.is_token_a_german_word("-")
    # res = deuRegExFinder.is_token_a_german_word("a-b")
    # print(res)
