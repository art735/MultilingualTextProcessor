import unicodedata

from ChurchSlavonicTextNormalizer import ChurchSlavonicTextNormalizer


class ChurchSlavonicTokenizer:
    """
    Токенизатор церковнославянского текста.

    Ответственность класса:
        - разбить предложение на token;
        - сохранить церковнославянские диакритики;
        - считать буквы, цифры и combining marks частью token;
        - считать пунктуацию и whitespace разделителями;
        - корректно обрабатывать внутренние апострофы;
        - перед выдачей token выполнить его нормализацию.

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

            "2 но в зако́не Госпо́дни во́ля его́."

        ->

            [
                "2",
                "но",
                "в",
                "зако́не",
                "Госпо́дни",
                "во́ля",
                "его́"
            ]

        Пунктуация не попадает в результат.
        """

        if not isinstance(sentence, str):
            raise TypeError(
                f"sentence must be str, got {type(sentence).__name__}"
            )

        tokens = []
        current_token = []

        for index, char in enumerate(sentence):

            if self._is_token_char(char):
                current_token.append(char)
                continue

            if self._is_internal_apostrophe(
                    sentence,
                    index,
                    current_token,
            ):
                current_token.append(char)
                continue

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
    def _is_token_char(cls, char):
        """
        Определяет, является ли символ частью token.

        Поддерживаются:
            - буквы Unicode;
            - цифры;
            - combining marks.

        Благодаря Unicode-подходу корректно обрабатываются
        древние кириллические символы и церковнославянские
        диакритические знаки.
        """

        category = unicodedata.category(char)

        return (
                char.isalpha()
                or char.isdigit()
                or category in cls._COMBINING_MARK_CATEGORIES
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
            2. после него идёт продолжение token.

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

        return cls._is_token_char(sentence[next_index])

    @staticmethod
    def _flush_current_token(
            current_token,
            tokens,
    ):
        """
        Завершает накопление текущего token.
        """

        if not current_token:
            return

        token = "".join(current_token)

        token = ChurchSlavonicTextNormalizer.normalize_token(
            token
        )

        tokens.append(token)

        current_token.clear()