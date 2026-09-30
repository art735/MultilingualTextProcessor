import FileContentsSplitter
from GrcRegExFinder import GrcRegExFinder

grcRegExFinder = GrcRegExFinder()

matthew_chapters = {
    1: 25,  # Глава 1 имеет 25 стихов
    2: 23,  # Глава 2 имеет 23 стиха
    3: 17,  # Глава 3 имеет 17 стихов
    4: 25,  # Глава 4 имеет 25 стихов
    5: 48,  # Глава 5 имеет 48 стихов
    6: 34,  # Глава 6 имеет 34 стиха
    7: 29,  # Глава 7 имеет 29 стихов
    8: 34,  # Глава 8 имеет 34 стиха
    9: 38,  # Глава 9 имеет 38 стихов
    10: 42,  # Глава 10 имеет 42 стиха
    11: 30,  # Глава 11 имеет 30 стихов
    12: 50,  # Глава 12 имеет 50 стихов
    13: 58,  # Глава 13 имеет 58 стихов
    14: 36,  # Глава 14 имеет 36 стихов
    15: 39,  # Глава 15 имеет 39 стихов
    16: 28,  # Глава 16 имеет 28 стихов
    17: 27,  # Глава 17 имеет 27 стихов
    18: 35,  # Глава 18 имеет 35 стихов
    19: 30,  # Глава 19 имеет 30 стихов
    20: 34,  # Глава 20 имеет 34 стиха
    21: 46,  # Глава 21 имеет 46 стихов
    22: 46,  # Глава 22 имеет 46 стихов
    23: 39,  # Глава 23 имеет 39 стихов
    24: 51,  # Глава 24 имеет 51 стих
    25: 46,  # Глава 25 имеет 46 стихов
    26: 75,  # Глава 26 имеет 75 стихов
    27: 66,  # Глава 27 имеет 66 стихов
    28: 20,  # Глава 28 имеет 20 стихов
}


# TODO: удалить этот метод и воспользоваться утилитным из модуля FileContentsReader
def get_file_text():
    lines = []
    base_dir = r'E:\Languages\[Git repo] MultilingualTextProcessor\resources\Greek\\'
    filename = 'TAGNT (Matt).txt'
    file_path = base_dir + filename
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # text = file.read()
            lines = file.readlines()
        # print(lines)
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    return lines


def is_str_constituted_of_comma_separated_greek_words(input_str):
    result = False
    if ',' in input_str:
        line_pieces = [lp.strip() for lp in input_str.split(',')]
        # в методе all() условие должно выполняться для всех строк списка
        result = all(grcRegExFinder.is_greek_word(lp) for lp in line_pieces)
    return result


def is_value_in_nested_list(nested_list, value_to_find):
    for sublist in nested_list:
        if value_to_find in sublist:
            return True
    return False


def process(allow_duplicates=True, add_verse_numbering=True):
    # Вычитываем содержимое файла
    file_text = get_file_text()

    # Разбиваем содержимое файла на список списков, где разделителем служит строка, содержащая фразу "Dictionary form"
    delimiter_cb = lambda line: True if 'Dictionary form' in line else False
    # Обрабатываем строку, если она содержит знак '=', который свидетельствует о том, что строка относится к словарику
    # стиха, а не к чему-то другому
    addition_condition_cb = lambda line: True if '=' in line else False
    all_verses_list = FileContentsSplitter.split_file_contents_by_delimiter(file_text, delimiter_cb,
                                                                            addition_condition_cb, False)

    # Согласно ChatGTP-4o точка после сокращения имени евангелиста в греч. и англ. Библиях не ставится,
    # а в синодальном переводе - ставится!
    numbered_verse_formattable_str = "Μτ {0}:{1}|Mt {0}:{1}"

    chapter_number = 1
    verse_number = 1

    all_results = []
    current_verse_results = []

    for current_verse_list in all_verses_list:

        if add_verse_numbering:
            # Формируем строку с нумерацией
            numbered_verse = numbered_verse_formattable_str.format(chapter_number, verse_number)
            current_verse_results.append(numbered_verse)

            # Увеличиваем номер стиха
            verse_number += 1

            # Если номер стиха превышает количество стихов в текущей главе, переходим к следующей главе
            if verse_number > matthew_chapters[chapter_number]:
                chapter_number += 1
                verse_number = 1

            # Если мы прошли все главы, завершаем цикл
            # if chapter_number > len(matthew_chapters):
            #     break

        for line in current_verse_list:
            # Разбиваем строку на части только по первому вхождению знака "=", явно задав в методе split
            # параметр maxsplit=1
            # Т. е. независимо от кол-ва знаков "=" в строке, на выходе всегда получится 2 части:
            # 1) греческое слово
            # 2) перевод, который в редких случаях тоже может содержать знак "=" и этот знак "="
            # не должен участвовать в разбивании строки на более мелкие части.
            line_pieces = [lp.strip() for lp in line.split('=', 1)]
            first_part = line_pieces[0]

            if (grcRegExFinder.is_greek_word(first_part) or
                    is_str_constituted_of_comma_separated_greek_words(first_part)):

                restored_pipe_separated_line = "|".join(line_pieces)

                # Флажок, который является параметром по умолчанию и регулирует ситуацию с дубликатами одних и тех
                # же слов от стиха к стиху
                if allow_duplicates:
                    current_verse_results.append(restored_pipe_separated_line)
                else:
                    if (restored_pipe_separated_line not in current_verse_results and
                            not is_value_in_nested_list(all_results, restored_pipe_separated_line)):
                        current_verse_results.append(restored_pipe_separated_line)
        # end of inner loop
        all_results.append(current_verse_results)
        current_verse_results = []
    # end of outer loop

    # # удаляем все лишние пробелы-разделителя из конца списка
    # while results[-1] == ' ':
    #     results.pop()

    # Шаг 1: Объединение элементов внутри каждого внутреннего списка
    inner_joined = ['\n'.join(inner_list) for inner_list in all_results]

    # Шаг 2: Объединение полученных строк с использованием другого разделителя
    output = '\n\n'.join(inner_joined)

    # print(final_result)

    # пробел использовался как логический разделитель между стихами Евангелия
    # кол-во стихов = кол-во разделителей между ними + 1
    # no_of_verses = all_results.count(' ') + 1
    # print("No of verses: \n" + str(no_of_verses))

    # return results
    return output


####################

out = process(allow_duplicates=False, add_verse_numbering=True)
# out = process(allow_duplicates=False, add_verse_numbering=False)  # от Матфея - 1699 слов
print(out)
