import itertools

import BrEngAmEngSplitter
from RepositoryItem import RepositoryItem

WORDS_PRIMARY_COLUMN_INDEX = 1  # столбец со словами из словаря
WORDS_SECONDARY_COLUMN_INDEX = WORDS_PRIMARY_COLUMN_INDEX + 4  # столбец с мн. ч. сущ., сравнит. степ. прил., past simple непр. глаголов
WORDS_TERTIARY_COLUMN_INDEX = WORDS_SECONDARY_COLUMN_INDEX + 2  # столбец с превосх. степ. прил., participle II непр. глаголов


def get_data_from_worksheet(worksheet):
    main_worksheet_indices = [
        WORDS_PRIMARY_COLUMN_INDEX, WORDS_PRIMARY_COLUMN_INDEX + 1, WORDS_PRIMARY_COLUMN_INDEX + 2,
        WORDS_SECONDARY_COLUMN_INDEX, WORDS_SECONDARY_COLUMN_INDEX + 1,
        WORDS_TERTIARY_COLUMN_INDEX, WORDS_TERTIARY_COLUMN_INDEX + 1
    ]

    columns_list = list()
    for i in main_worksheet_indices:
        columns_list.append(worksheet.col_values(i))

    # склеиваем список столбцов Excel так, чтобы получился список строк Excel
    sheet_data = list()
    sheet_data.extend(list(itertools.zip_longest(*columns_list, fillvalue="")))

    # В результате склейки столбцов получаем следующие индексы данных:
    # 0 - word itself (with possible pos tag)
    # 1 - transcription
    # 2 - translation
    # 3,4 - wordform(s) with transcription(s) (plural for nouns; present/past simple for verbs; comparative for adjectives)
    # 5,6 - wordform(s) with transcription(s) (participle II for verbs; superlative for adjectives)

    # tuple1_start_index = 3
    # tuple2_start_index = tuple1_start_index + 2

    # KEY - english word cell
    # VALUE - all the consecutive Excel rows related to KEY
    sheet_data_dict = dict()
    for row in sheet_data:
        if row[0]:  # словарная статья может занимать несколько Excel-строк
            word = row[0]
            sheet_data_dict[word] = list()
        sheet_data_dict[word].append(row)

    repository_dict = dict()
    for word, rows in sheet_data_dict.items():
        repo_item = _create_repository_item(rows)

        if '\n' in word:  # если английское слово имеет брит. и амер. варианты написания
            split_repo_item_dict = BrEngAmEngSplitter.split(repo_item)
            repository_dict.update(split_repo_item_dict)  # add minor dictionary items to a major dictionary
        else:
            repository_dict[word.lower()] = repo_item

    return repository_dict


def _create_repository_item(word_rows):
    # morphological_forms = list()
    # word = ""
    repo_item = None
    for row in word_rows:
        if row[0]:  # если работаем со строкой Excel, содержащей слово-транскрипция-перевод
            word = row[
                0]  # слово "как есть", без приведения к нижнему регистру (оно осуществл. внутри конструктора типа RepositoryItem)
            transcription = row[1]
            translation = row[2]
            repo_item = RepositoryItem(word, transcription, translation)

        # выполняется в любом случае независимо от if
        tuple1 = (row[3], row[4])
        tuple2 = (row[5], row[6])
        repo_item.add_morphological_forms([tuple1, tuple2])

    # return {word.lower(): repo_item}
    return repo_item
