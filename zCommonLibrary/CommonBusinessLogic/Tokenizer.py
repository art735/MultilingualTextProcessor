import re

import CharConstants


# from nltk.stem.wordnet import wordnet
# from nltk.stem.wordnet import WordNetLemmatizer
# utils = SourceFileLoader('Utils', '../CommonBusinessLogic/Utils.py').load_module()
# charConstants = SourceFileLoader('CharConstants', '../../CommonBusinessLogic/CharConstants.py').load_module()
# charConstants = SourceFileLoader('CharConstants', '$PROJECT_DIR$/CommonBusinessLogic/CharConstants.py').load_module()


# re.sub(pattern, repl, string, count=0, flags=0)
# Return the string obtained by replacing the leftmost NON-OVERLAPPING occurrences of pattern in string by the replacement repl.
# If the pattern isn’t found, string is returned unchanged.
# repl can be a string or a function; if it is a string, any backslash escapes in it are processed.

class Tokenizer:
    def __init__(self):
        pass

    # флаг strip_apostrophe ввёл ради NT Greek (там апостроф не нужно удалять на конце слов, напр.: κατ’)
    def tokenize(self, text, consider_number_as_token=True, strip_apostrophe=True):
        text = self.pre_process_text_by_deleting_unnecessary_symbols(text)
        # print(text)

        raw_tokens = self._split_text_into_tokens(text)
        # print(raw_tokens)

        tokens = self._strip_tokens(raw_tokens, consider_number_as_token, strip_apostrophe)
        # print(tokens)

        return tokens

    def pre_process_text_by_deleting_unnecessary_symbols(self, text):
        # Replace one or more NEWLINE ('\n') characters with a whitespace
        pattern = "\n+"
        text = re.sub(pattern, CharConstants.SPACE, text)
        # print("Count of NEWLINE replacements is " + str(number_of_replacements))

        # Replace one of more NON_BREAKING_SPACE characters with a whitespace
        pattern = "[{0}]+".format(CharConstants.NON_BREAKING_SPACE)
        text = re.sub(pattern, CharConstants.SPACE, text)
        # print("Count of NON-BREAKING SPACE replacements is " + str(number_of_replacements))

        # Replace one or more TAB symbols with a whitespace
        pattern = "\t+"
        text = re.sub(pattern, CharConstants.SPACE, text)
        # print("Count of TAB replacements is " + str(number_of_replacements))

        # Replace two or more whitespaces with a single whitespace
        pattern = "\s\s+"
        text = re.sub(pattern, CharConstants.SPACE, text)
        # print("Count of WHITESPACE replacements is " + str(number_of_replacements))

        # Replace 'usual' apostrophe with a 'curly' apostrophe
        # pattern = USUAL_APOSTROPHE
        text = re.sub(CharConstants.STRAIGHT_APOSTROPHE, CharConstants.CURLY_APOSTROPHE, text)

        # Заменяем два подряд идущих дефиса на тире
        text = text.replace(f'{CharConstants.HYPHEN}{CharConstants.HYPHEN}', CharConstants.DASH)

        return text

    def _split_text_into_tokens(self, text):
        tokens = text.split(CharConstants.SPACE)
        return tokens

    # флаг strip_apostrophe ввёл ради NT Greek (там апостроф не нужно удалять на конце слов, напр.: κατ’)
    def _strip_tokens(self, tokens, consider_number_as_token, strip_apostrophe):
        pureTokens = list()

        # for i in range(0, len(tokens)):
        for i, token in enumerate(tokens):
            # re.sub means 'substitute'
            pattern = r'[.,«»"“”„_{}\[\]()№|/:–;;?!]'  # два символа "точка с запятой" разные!, несмотря на внешнюю схожесть. 2-й из них взят из NA28
            pure_token = re.sub(pattern, '', token)

            # remove hyphen at the beginning of the token
            pure_token = re.sub("^-", '', pure_token)

            if strip_apostrophe:
                # метод .lstrip() удаляет символы только в начале строки
                # метод .rstrip() удаляет символы только в конце строки
                # метод .strip() удаляет символы как в начале, так и в конце строки
                pure_token = pure_token.strip(CharConstants.STRAIGHT_APOSTROPHE)
                pure_token = pure_token.strip(CharConstants.CURLY_APOSTROPHE)
                pure_token = pure_token.strip(CharConstants.LEFT_SINGLE_QUOTATION_MARK)
                pure_token = pure_token.strip(CharConstants.RIGHT_SINGLE_QUOTATION_MARK)

            # Remove TRAILING 's ($ sign is used in regexp to select only TRAILING symbols)
            # pattern = "{0}$".format("[{0}{1}]s".format(CharConstants.STRAIGHT_APOSTROPHE, CharConstants.CURLY_APOSTROPHE))
            pure_token = re.sub(pattern, '', pure_token)

            pureTokens.append(pure_token)
        # end of for-loop here

        # Remove digits
        # pureTokens = [token for token in pureTokens if token.isdigit() is False]

        # булевый параметр метода
        if not consider_number_as_token:
            # Remove tokens, containing digits

            # Check if any digit (or sequence of digits) is at the beginning, in the middle or at the end of the token:
            # 1) .* (any number of any symbols at the beginning of the token)
            # 2) [0-9]+ (one or more number of digits)
            # 3) .* (any number of any symbols at the end of the token)
            pattern = ".*[0-9]+.*"
            pureTokens = [token for token in pureTokens if not re.search(pattern, token)]

        # Remove empty strings
        pureTokens = [token for token in pureTokens if any(token)]

        return pureTokens


########################################

text = '- Guten Тag, Herr Smirnow! Ich heiße Fred Neumann.'
text = '[Folge 01]'
text = 'So, das war’s!'

if __name__ == '__main__':
    tokenizer = Tokenizer()
    output = tokenizer.tokenize(text, True, strip_apostrophe=False)
    print(output)
