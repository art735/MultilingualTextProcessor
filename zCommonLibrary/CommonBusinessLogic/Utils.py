import re


def subtract_lists(list_a, list_b):
    diff = [x for x in list_a if x not in list_b]
    return diff


# Create the intersection of two lists
def list_intersection(list1, list2):
    intersection = [value for value in list1 if value in list2]
    return intersection


# Удалить дубликаты в списке кортежей, сохраняя при этом первоначальный порядок следования кортежей
# Хорошо подходит для валидации словаря, ведь словарь (слово + транскрипция) - это список кортежей
def remove_duplicate_tuples_from_list(tuples):
    return sorted(set(tuples), key=tuples.index)


def find_duplicates(elemements):
    duplicates = set([x for x in elemements if elemements.count(x) > 1])
    return duplicates


# Список кортежей (любой размерности) конвертируется в словарь, у которого:
# key - первый элемент кортежа
# value - остальные элементы кортежа в виде отдельного кортежа
def convert_tuples_into_dictionary(tuples):
    dictionary = dict()
    for t in tuples:
        # key = t[0].lower()
        # убрал вызов метода lower(), чтобы он не приводил немецкие существительные к нижнему регистру, а остальные
        # слова в Excel-листе и так пишутся с маленькой буквы. Даже если какие-то из них и нужно приводить к нижнему
        # регистру, это нужно делать точечно для каждой категории в отдельности в файле GermanExcelWorkbooksDao.py, а не здесь!
        key = t[0]
        if len(t) == 2:
            value = t[1]
        elif len(t) > 2:
            value = t[1:]  # взять у кортежа t все элементы от 1-го до конца (т. е. все, кроме 0-го)

        dictionary.setdefault(key, value)

    return dictionary


### Служебные функции, используемые как минимум в проекте «Deutsch_new» ###

# Разбивает строку на подстроки по разделителю
def split_by(text, split_character):
    pieces = [line.strip() for line in text.split(split_character) if line.strip()]
    return pieces
