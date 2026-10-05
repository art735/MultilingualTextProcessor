import re
import unicodedata


class ChurchSlavonicTextNormalizer:
    """
    Нормализатор входного церковнославянского текста.

    Назначение:
        - очистка технических Unicode-артефактов;
        - нормализация Unicode;
        - унификация пробелов;
        - устранение пробелов перед/после пунктуации;
        - исправление смешения Latin/Cyrillic homoglyphs;
        - сохранение церковнославянской орфографии и диакритики.

    ВАЖНО:
        Нормализуется сам исходный текст, поэтому предложения,
        которые попадут дальше в result_dict, уже будут очищены.

    Пример:

        "2 но в зако́не Госпо́дни во́ля eго́, и в зако́не Его́..."

    превращается в:

        "2 но в зако́не Госпо́дни во́ля его́, и в зако́не Его́..."
    """

    # ------------------------------------------------------------------
    # Latin -> Cyrillic homoglyphs.
    #
    # Включаем только символы, для которых визуальное смешение
    # с кириллицей достаточно вероятно.
    #
    # Эти замены НЕ выполняются безусловно для каждого Latin token.
    # Они выполняются внутри token, если token содержит кириллические
    # символы.
    # ------------------------------------------------------------------
    LATIN_TO_CYRILLIC_HOMOGLYPHS = str.maketrans({
        "A": "А",
        "B": "В",
        "C": "С",
        "E": "Е",
        "I": "І",
        "K": "К",
        "M": "М",
        "O": "О",
        "P": "Р",
        "T": "Т",
        "X": "Х",
        "Y": "У",

        "a": "а",
        "c": "с",
        "e": "е",
        "i": "і",
        "k": "к",
        "m": "м",
        "o": "о",
        "p": "р",
        "t": "т",
        "x": "х",
        "y": "у",
    })

    # ------------------------------------------------------------------
    # Технические невидимые символы.
    # ------------------------------------------------------------------
    INVISIBLE_CHARS = {
        "\ufeff",  # ZERO WIDTH NO-BREAK SPACE / BOM
        "\u200b",  # ZERO WIDTH SPACE
        "\u200c",  # ZERO WIDTH NON-JOINER
        "\u200d",  # ZERO WIDTH JOINER
        "\u2060",  # WORD JOINER
    }

    # ------------------------------------------------------------------
    # Unicode whitespace, который следует заменить обычным пробелом.
    # ------------------------------------------------------------------
    SPACE_CATEGORIES = {
        "Zs",  # Space Separator
    }

    @classmethod
    def normalize_text(cls, text):
        """
        Полностью нормализует входной текст.

        Нормализация производится ДО токенизации.
        """

        if not isinstance(text, str):
            raise TypeError(
                f"text must be str, got {type(text).__name__}"
            )

        # --------------------------------------------------------------
        # 1. Unicode canonical normalization.
        #
        # Например:
        # е + COMBINING ACUTE ACCENT
        #
        # приводится к канонической Unicode-форме там, где это возможно.
        #
        # При этом старые буквы и церковнославянские диакритики
        # не удаляются.
        # --------------------------------------------------------------
        text = unicodedata.normalize("NFC", text)

        # --------------------------------------------------------------
        # 2. Удаляем невидимые технические символы.
        # --------------------------------------------------------------
        for char in cls.INVISIBLE_CHARS:
            text = text.replace(char, "")

        # --------------------------------------------------------------
        # 3. Унифицируем переводы строк.
        # --------------------------------------------------------------
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # --------------------------------------------------------------
        # 4. Нормализуем каждую строку отдельно.
        # --------------------------------------------------------------
        normalized_lines = [
            cls._normalize_line(line)
            for line in text.split("\n")
        ]

        return "\n".join(normalized_lines)

    @classmethod
    def _normalize_line(cls, line):
        """
        Нормализует одну строку текста.
        """

        # --------------------------------------------------------------
        # Unicode spaces -> обычный пробел.
        # --------------------------------------------------------------
        line = "".join(
            " "
            if unicodedata.category(char) in cls.SPACE_CATEGORIES
            else char
            for char in line
        )

        # --------------------------------------------------------------
        # Tab / vertical tab / form feed / прочие whitespace,
        # кроме перевода строки, -> обычный пробел.
        # --------------------------------------------------------------
        line = re.sub(r"[^\S\n]+", " ", line)

        # --------------------------------------------------------------
        # Повторяющиеся пробелы.
        # --------------------------------------------------------------
        line = re.sub(r" {2,}", " ", line)

        # --------------------------------------------------------------
        # Пробел перед пунктуацией.
        #
        # "слово , слово" -> "слово, слово"
        # "слово ."       -> "слово."
        #
        # Для дефиса такую замену намеренно не делаем:
        # дефис может иметь смысловую функцию.
        # --------------------------------------------------------------
        line = re.sub(
            r"\s+([,.;:!?…»”\)\]\}])",
            r"\1",
            line
        )

        # --------------------------------------------------------------
        # Пробел после открывающей пунктуации.
        #
        # "( слово" -> "(слово"
        # "« слово" -> "«слово"
        # --------------------------------------------------------------
        line = re.sub(
            r"([«“\(\[\{])\s+",
            r"\1",
            line
        )

        line = line.strip()

        # --------------------------------------------------------------
        # Самое важное:
        # исправляем смешение Latin/Cyrillic непосредственно
        # в тексте строки.
        #
        # Поэтому уже result_dict получит исправленное предложение.
        # --------------------------------------------------------------
        line = cls._normalize_mixed_script_tokens(line)

        return line

    @classmethod
    def _normalize_mixed_script_tokens(cls, text):
        """
        Находит token в тексте и исправляет смешение Latin/Cyrillic.

        Ключевое правило:

            если token содержит хотя бы один Cyrillic-символ,
            все известные Latin homoglyphs внутри этого token
            преобразуются в Cyrillic.

        Таким образом:

            eго́   -> его́
            Еgó   -> Его́
            Госпо́дeн -> Госпо́ден

        Но:

            Amen

        останется:

            Amen

        потому что token целиком состоит из Latin.
        """

        result = []
        current_token = []

        def flush_token():
            if not current_token:
                return

            token = "".join(current_token)
            normalized_token = cls.normalize_token(token)

            result.append(normalized_token)
            current_token.clear()

        length = len(text)

        for index, char in enumerate(text):

            if cls._is_token_char(char):
                current_token.append(char)
                continue

            # Апостроф внутри token.
            if (
                char in {"'", "’"}
                and current_token
                and index + 1 < length
                and cls._is_token_char(text[index + 1])
            ):
                current_token.append(char)
                continue

            flush_token()
            result.append(char)

        flush_token()

        return "".join(result)

    @classmethod
    def normalize_token(cls, token):
        """
        Нормализует один token.

        Этот метод используется как для исходного текста,
        так и для формирования ключа дедупликации.

        Важно:
            исходный token не приводится автоматически к lower().
            Сохраняется исходный регистр.

        Поэтому:

            Его́ -> Его́
            его́ -> его́
        """

        if not isinstance(token, str):
            raise TypeError(
                f"token must be str, got {type(token).__name__}"
            )

        token = unicodedata.normalize("NFC", token)

        has_cyrillic = any(
            cls._is_cyrillic_char(char)
            for char in token
        )

        # Если в token есть кириллица, то Latin homoglyphs
        # считаем ошибочными и заменяем.
        if has_cyrillic:
            token = token.translate(
                cls.LATIN_TO_CYRILLIC_HOMOGLYPHS
            )

        return token

    @classmethod
    def normalize_token_key(cls, token):
        """
        Формирует канонический ключ token для дедупликации.

        Например все варианты:

            eго́
            его́
            Eго́
            Его́

        дают один и тот же ключ.
        """

        token = cls.normalize_token(token)

        return token.casefold()

    @classmethod
    def _is_token_char(cls, char):
        """
        Буквы, цифры и Unicode combining marks считаются частью token.
        """

        category = unicodedata.category(char)

        return (
            char.isalpha()
            or char.isdigit()
            or category in {"Mn", "Mc", "Me"}
        )

    @staticmethod
    def _is_cyrillic_char(char):
        """
        Определяет, относится ли символ к Cyrillic Unicode block.

        Используем имя Unicode, а не диапазон кодов.
        """

        return "CYRILLIC" in unicodedata.name(char, "")