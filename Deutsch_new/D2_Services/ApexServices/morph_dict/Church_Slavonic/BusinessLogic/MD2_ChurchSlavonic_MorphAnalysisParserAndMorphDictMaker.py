from __future__ import annotations

from typing import Dict, List, Tuple

from MorphDictToStrConverter import MorphDictToStrConverter

TokenData = Tuple[str, str, str, str]
ParsedData = Dict[str, List[TokenData]]


class ParseError(ValueError):
    """Ошибка разбора входных текстовых данных."""
    pass

"""
Парсер:
- считает пустые строки между предложениями как разделители блоков;
- считает каждый непустой блок отдельным предложением/ключом;
- первую строку блока принимает за предложение;
- остальные строки разбирает как token|lemma|pos;
- сохраняет предложение даже при отсутствии token-строк;
- формирует именно кортежи из 4 элементов: (token, lemma, pos, "");
- проверяет пустые поля, неправильное количество |, дублирующиеся предложения;
- в случае ошибки сообщает номер строки и содержимое проблемной строки.
"""
class MD2_ChurchSlavonic_MorphAnalysisParserAndMorphDictMaker:
    def __init__(self):
        self.morphDictToStrConverter = MorphDictToStrConverter()

    def parse_and_make(self, text: str) -> ParsedData:
        """
        Преобразует текст вида:

            Предложение 1
            token|lemma|pos
            token|lemma|pos

            Предложение 2

            Предложение 3
            token|lemma|pos

        в словарь:

            {
                "Предложение 1": [
                    ("token", "lemma", "pos", ""),
                    ...
                ],
                "Предложение 2": [],
                "Предложение 3": [
                    ...
                ]
            }

        Валидация:
        - каждый блок должен иметь непустую первую строку — предложение;
        - в token-строке должно быть ровно 3 поля;
        - разделитель — ровно два символа '|';
        - token, lemma и pos не могут быть пустыми;
        - предложение не должно содержать '|';
        - одинаковые предложения запрещены, чтобы не было
          незаметного перезаписывания значения в dict.
        """

        if not isinstance(text, str):
            raise TypeError(
                f"text должен быть строкой, получено: {type(text).__name__}"
            )

        # Убираем BOM, если текст был сохранён, например, в UTF-8 with BOM.
        text = text.lstrip("\ufeff")

        result: ParsedData = {}

        # splitlines() корректно работает с \n, \r\n и \r.
        lines = text.splitlines()

        # Из текущих строк собираем блок:
        # [(номер_строки, строка), ...]
        block: list[tuple[int, str]] = []

        def process_block(block_lines: list[tuple[int, str]]) -> None:
            """Разбирает один блок и добавляет его в result."""
            if not block_lines:
                return

            sentence_line_no, sentence_raw = block_lines[0]
            sentence = sentence_raw.strip()

            if not sentence:
                raise ParseError(
                    f"Строка {sentence_line_no}: пустое предложение."
                )

            # "|" зарезервирован как разделитель token|lemma|pos.
            if "|" in sentence:
                raise ParseError(
                    f"Строка {sentence_line_no}: предложение содержит символ '|', "
                    f"который зарезервирован как разделитель: {sentence_raw!r}"
                )

            if sentence in result:
                raise ParseError(
                    f"Строка {sentence_line_no}: дублирующееся предложение "
                    f"{sentence!r}. Оно уже было определено ранее."
                )

            values: List[TokenData] = []

            for line_no, raw_line in block_lines[1:]:
                line = raw_line.strip()

                if not line:
                    # Теоретически такого быть не должно, поскольку пустые
                    # строки уже используются как разделители блоков.
                    continue

                parts = line.split("|")

                if len(parts) != 3:
                    raise ParseError(
                        f"Строка {line_no}: ожидалось ровно 3 поля "
                        f"token|lemma|pos, получено {len(parts)}: {raw_line!r}"
                    )

                token, lemma, pos = (part.strip() for part in parts)

                if not token:
                    raise ParseError(
                        f"Строка {line_no}: пустое поле token: {raw_line!r}"
                    )

                if not lemma:
                    raise ParseError(
                        f"Строка {line_no}: пустое поле lemma: {raw_line!r}"
                    )

                if not pos:
                    raise ParseError(
                        f"Строка {line_no}: пустое поле pos: {raw_line!r}"
                    )

                values.append((token, lemma, pos, ""))

            # Даже если values == [], предложение всё равно попадает в словарь.
            result[sentence] = values

        # Разбиваем вход на блоки по пустым строкам.
        for line_no, raw_line in enumerate(lines, start=1):
            if raw_line.strip() == "":
                process_block(block)
                block = []
            else:
                block.append((line_no, raw_line))

        # Последний блок может не заканчиваться пустой строкой.
        process_block(block)

        result_str = self.morphDictToStrConverter.morph_dict_to_str(result)
        return result_str


#####################################################

text = """
Псалом 1:
псалом|псало́м|NOUN

1 Блаже́н муж, и́же не и́де на сове́т нечести́вых и на пути́ гре́шных не ста, и на седа́лищи губи́телей не се́де,:
блаже́н|блаже́нный|ADJ
муж|муж|NOUN
и́же|и́же|PRON
не|не|PART
и́де|ити́|VERB

2 но в зако́не Госпо́дни во́ля его́, и в зако́не Его́ поучи́тся день и нощь.:

7 Это предложение без token-строк.
"""

if __name__ == "__main__":
    md2_ChurchSlavonic_MorphAnalysisParserAndMorphDictMaker = MD2_ChurchSlavonic_MorphAnalysisParserAndMorphDictMaker()
    result = md2_ChurchSlavonic_MorphAnalysisParserAndMorphDictMaker.parse_and_make(text)
    print(result)

# try:
#     data = parse_sentences(text)
#
# except (ParseError, TypeError) as exc:
#     print(f"Ошибка разбора: {exc}")
#
# else:
#     print(data)