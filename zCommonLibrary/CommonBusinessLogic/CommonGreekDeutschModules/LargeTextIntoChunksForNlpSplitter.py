

class LargeTextIntoChunksForNlpSplitter:
    def __init__(self):
        pass

    # ValueError: [E088] Text of length 1,018,486 exceeds maximum of 1,000,000.
    # The parser and NER models require roughly 1GB of temporary memory per 100,000 characters in the input.
    # This means long texts may cause memory allocation errors.
    # If you're not using the parser or NER, it's probably safe to increase the `nlp.max_length` limit.
    # The limit is in number of characters, so you can check whether your inputs are too long by checking `len(text)`.
    # Подстраховываемся и разбиваем входной текст на блоки после каждых (chunk_size + ближайший символ \n) символов.
    # Этот подход должен предотвратить ошибку нехватки памяти при обработке больших текстов.
    # Правильность работы метода подтверждается юнит-тестом: TestBaseSpaCyEngineWrapper.py
    def split_large_text(self, input_str, chunk_size=10000):
        chunks = []
        start = 0
        while start < len(input_str):
            # Определяем конец текущего блока размером chunk_size
            end = start + chunk_size

            # Если достигли конца текста, добавляем оставшуюся часть
            if end >= len(input_str):
                chunks.append(input_str[start:])
                break

            # Ищем ближайший символ новой строки после текущего блока
            newline_pos = input_str.find('\n', end)

            # Если не нашли новой строки, берём оставшийся текст
            if newline_pos == -1:
                chunks.append(input_str[start:])
                break

            # Добавляем блок текста, завершающийся на новой строке
            chunks.append(input_str[start:newline_pos + 1])

            # Обновляем начальную позицию для следующего блока
            start = newline_pos + 1

        return chunks