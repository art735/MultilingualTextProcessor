import unicodedata

from ChurchSlavonicTextNormalizer import ChurchSlavonicTextNormalizer


class ChurchSlavonicTokenizer:
    """
    Токенизатор церковнославянского текста.

    Ответственность класса:
        - разбить предложение на token;
        - сохранить церковнославянские диакритики;
        - считать буквы Unicode частью token;
        - считать combining marks частью уже начатого token;
        - игнорировать цифры и числа;
        - считать пунктуацию и whitespace разделителями;
        - корректно обрабатывать внутренние апострофы;
        - нормализовать token;
        - приводить все token к нижнему регистру.

    Класс НЕ занимается:
        - дедупликацией;
        - чтением morph_dict;
        - определением POS;
        - лемматизацией;
        - формированием prompt.
    """

    _COMBINING_MARK_CATEGORIES = {"Mn", "Mc", "Me"}

    _INTERNAL_APOSTROPHES = {"'", "’"}

    def tokenize(self, sentence):
        """
        Разбивает предложение на список token.

        Пример:

            "2 но в зако́не Госпо́дни во́ля Его́."

        ->

            [
                "но",
                "в",
                "зако́не",
                "госпо́дни",
                "во́ля",
                "его́"
            ]

        Числа и цифры полностью игнорируются.
        Пунктуация не попадает в результат.
        Все token приводятся к нижнему регистру.
        """

        if not isinstance(sentence, str):
            raise TypeError(
                f"sentence must be str, got {type(sentence).__name__}"
            )

        tokens = []
        current_token = []

        for index, char in enumerate(sentence):

            # ----------------------------------------------------------
            # Буква начинает или продолжает token.
            # ----------------------------------------------------------
            if char.isalpha():
                current_token.append(char)
                continue

            # ----------------------------------------------------------
            # Combining mark является частью token только если
            # перед ним уже есть буква.
            #
            # Например:
            #
            #   о + U+0301 = о́
            #
            # не должен потеряться при токенизации.
            # ----------------------------------------------------------
            if (
                current_token
                and self._is_combining_mark(char)
            ):
                current_token.append(char)
                continue

            # ----------------------------------------------------------
            # Апостроф внутри слова.
            # ----------------------------------------------------------
            if self._is_internal_apostrophe(
                    sentence,
                    index,
                    current_token,
            ):
                current_token.append(char)
                continue

            # ----------------------------------------------------------
            # Любой другой символ является разделителем.
            #
            # В том числе:
            #   - цифры;
            #   - знаки препинания;
            #   - пробелы;
            #   - дефисы;
            #   - тире;
            #   - скобки и т. д.
            # ----------------------------------------------------------
            self._flush_current_token(
                current_token,
                tokens,
            )

        self._flush_current_token(
            current_token,
            tokens,
        )

        return tokens

    @classmethod
    def _is_combining_mark(cls, char):
        """
        Проверяет, является ли символ Unicode combining mark.
        """

        return (
            unicodedata.category(char)
            in cls._COMBINING_MARK_CATEGORIES
        )

    @classmethod
    def _is_internal_apostrophe(
            cls,
            sentence,
            index,
            current_token,
    ):
        """
        Проверяет, является ли апостроф частью token.

        Апостроф сохраняется только тогда, когда:

            1. перед ним уже есть token;
            2. после него начинается буква.

        Например:

            слово'слово
            слово’слово

        Апострофы в остальных местах считаются разделителями.
        """

        if not current_token:
            return False

        char = sentence[index]

        if char not in cls._INTERNAL_APOSTROPHES:
            return False

        next_index = index + 1

        if next_index >= len(sentence):
            return False

        # После апострофа должна идти именно буква.
        #
        # Это важно, поскольку цифры token-ами не являются.
        return sentence[next_index].isalpha()

    @staticmethod
    def _flush_current_token(
            current_token,
            tokens,
    ):
        """
        Завершает накопление текущего token.

        На этом этапе:
            1. token нормализуется;
            2. token приводится к нижнему регистру;
            3. token добавляется в результат.
        """

        if not current_token:
            return

        token = "".join(current_token)

        # --------------------------------------------------------------
        # Нормализация Latin/Cyrillic homoglyphs и Unicode.
        # --------------------------------------------------------------
        token = ChurchSlavonicTextNormalizer.normalize_token(
            token
        )

        # --------------------------------------------------------------
        # Все token должны быть в нижнем регистре.
        # --------------------------------------------------------------
        token = token.lower()

        tokens.append(token)

        current_token.clear()

#########################################################################

text_to_tokenize = """
1 Блаже́н муж, и́же не и́де на сове́т нечести́вых и на пути́ гре́шных не ста, и на седа́лищи губи́телей не се́де,
2 но в зако́не Госпо́дни во́ля eго́, и в зако́не Его́ поучи́тся день и нощь.
"""

if __name__ == "__main__":
    churchSlavonicTokenizer = ChurchSlavonicTokenizer()

    for line in text_to_tokenize.split("\n"):
        tokens = churchSlavonicTokenizer.tokenize(line)
        tokens_str = "\n".join(tokens)
        output = f'{line}\n{tokens_str}\n'
        print(output)



