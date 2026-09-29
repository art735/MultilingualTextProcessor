import itertools

import Stripper


def isFloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


# удалить лишние пробелы вокруг слова,
# которые могли случайно скопироваться в Excel вместе со словом или его транскрипцией
def _stripEveryVocabularyEntry(tuples):
    result = list()
    single_tuple_items_list = list()
    for t in tuples:
        for index, tuple_item in enumerate(t):
            # токеном текста, который нужно транскрибировать, может быть и число и для него тоже нужно поставлять транскрипцию из Excel-словаря
            # поэтому для числительных в Excel-словаре хранится не только словесное их выражение, но и числовое
            # целые числа вычитываются из Excel-словаря библиотекой xlrd как вещественные, поэтому нужен доп. труд по их конвертации в целочисленные значения
            if isFloat(tuple_item):
                tuple_item = int(float(tuple_item))

            tuple_item = str(tuple_item).strip()
            single_tuple_items_list.append(tuple_item)

        recreated_tuple = tuple(single_tuple_items_list)
        result.append(recreated_tuple)
        single_tuple_items_list.clear()

    return result


# Параметр worksheet - это лист Excel-книги, из которого производится вычитывание данных
# Параметр column_indices - список индексов колонок (счёт начинается с 0), из которых будут вычитываться данные
# column_indices может быть задан в двух форматах:
# 1) в виде "плоского" списка индексов, например, [1, 2] - в этом случае из Excel-листа будут вычитаны столбцы с указанными номерами и их соотв. значения объединены в один кортеж
# 2) в виде вложенного списка, [[0,1], 4, [6,7], [8,9], 10] - в этом случае внутренние списки означают номера столбцов, значения которых будут объединены в кортежи между собой и
# все эти кортежи внутренних списков будут объединены в один общий список (этот вариант нужен для Excel-файла с немецкими словами)
def getWorksheetData(worksheet, column_indices):
    sheet_data = list()
    columns_list = list()

    for i in column_indices:
        if isinstance(i, list):  # если внутренний элемент списка является не числом, а списком! - используем рекурсию
            vals = getWorksheetData(worksheet, i)  # !!! РЕКУРСИЯ !!!
            sheet_data.extend(vals)
            continue  # после отработки рекурсии прерываем текущую итерацию и заходим на новую

        # Handles the following situation 'IndexError: list index out of range'
        # Когда происходит попытка вычитки столбца, в котором нет ни одного значения,
        # библиотечка xlrd бросает исключение 'IndexError: list index out of range' и чтобы данная ошибка не прерывала
        # работу всей программы, здесь данная ошибка ловится и игнорируется
        try:
            columns_list.append(worksheet.col_values(i))
        except IndexError:  # xlrd library's error 'IndexError: list index out of range'
            pass
            # print("No data in column: " + str(i))
    # end of loop
    sheet_data.extend(list(itertools.zip_longest(*columns_list, fillvalue="")))

    # get rid of everything that is "falsy", e. g. empty strings, empty tuples, zeros
    sheet_data = [t for t in sheet_data if
                  any(t)]  # If the iterable object is empty, the any() function will return False.
    sheet_data = _stripEveryVocabularyEntry(sheet_data)
    return sheet_data


def get_words_for_uniqueness_validation(wks_tuples):
    words_to_validate = []
    for wks_tuple in wks_tuples:
        worksheet = wks_tuple[0]
        word_col_index = wks_tuple[1]
        first_col_words = worksheet.col_values(word_col_index)
        first_col_words = Stripper.strip_and_remove_empty_items(first_col_words)
        words_to_validate.extend(first_col_words)

    return words_to_validate
