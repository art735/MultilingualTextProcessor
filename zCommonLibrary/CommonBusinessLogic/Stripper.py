from typing import Iterable


# Шаг #1. Удалить обрамляющие пробелы в строках
def _stripWhitespaces(data_list):
    stripped_data_list = list()
    for item in data_list:
        # если элемент списка является строкой
        if isinstance(item, str):
            stripped_data_list.append(item.strip())
        else:
            # если элемент списка можно итерировать (в данном случае это нужно для кортежа значений)
            if isinstance(item, Iterable):
                stripped_tuple = tuple(t.strip() for t in item)
                stripped_data_list.append(stripped_tuple)

    return stripped_data_list


# Шаг #2. Удалить из списка пустые элементы (в списке строк - это пустые строки; в списке кортежей - это такие кортежи, все значения которых пусты '')

# Python any() function returns True if any of the elements of a given iterable ( List, Dictionary, Tuple, set, etc) are True
# else it returns False.
# Parameters: Iterable: It is an iterable object such as a dictionary, tuple, list, set, etc.
# Returns: Python any() function returns true if any of the items is True.
# Здесь происходить отсеивание пустых кортежей (кортеж может быть любой размерности)
# Одномерный пустой кортеж: ('')
# Двумерный пустой кортеж: ('', '')
# Трёхмерный пустой кортеж: ('', '', '')
def _removeEmptyItems(stripped_list):
    return [e for e in stripped_list if any(e)]


def strip_and_remove_empty_items(data_list):
    stripped_data = _stripWhitespaces(data_list)
    ready_data = _removeEmptyItems(stripped_data)
    return ready_data

##########################################################

# test one-dimensional list
# test_list = ['a ', '', ' b', '', ' ', 'c', '']
# print(test_list)
# res = stripAndRemoveEmptyItems(test_list)
# print(res)

# test two-dimensional list
# test_list = [('a ', ' a'), ('a', ' '), (' a', ''), (' ', 'a'), ('', ''), ('b '), ('', ''), (' ', ' '), (' c', 'c '), (''), ('', '')]
# print(test_list)
# res = stripAndRemoveEmptyItems(test_list)
# print(res)
