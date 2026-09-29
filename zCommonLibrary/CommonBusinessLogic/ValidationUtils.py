import Utils


def validate_vocabulary_uniqueness(repository_name, words_to_validate_list, ignored_words_list):
    is_valid = False
    duplicates = []

    pure_words_to_validate_list = Utils.subtract_lists(words_to_validate_list, ignored_words_list)
    pure_words_to_validate_set = set(pure_words_to_validate_list)

    if len(pure_words_to_validate_set) < len(pure_words_to_validate_list):
        duplicates = Utils.find_duplicates(pure_words_to_validate_list)
        # print(f"!!! DUPLICATES FOUND IN '{repository_name}' !!!")
        # [print(dup) for dup in duplicates]
    else:
        is_valid = True

    # В вызывающем коде проверяется флаг is_valid и если он False, можно обратиться к списку дубликатов duplicates
    return is_valid, duplicates


# TODO Подключить данный метод в бизнес-логику валидации!!!!!!
# Валидировать уникальность строк словаря
# Удостовериться, что список кортежей (слово + транскрипция) не содержит дубликатов, а также
# удостовериться, что список чисто слов содержит только уникальные элементы
def validate_no_duplicates(list_of_tuples):
    isValidationSuccessful = True

    # проверка уникальности кортежей
    if len(list_of_tuples) != len(set(list_of_tuples)):
        print("Среди кортежей словаря (слово + транскрипция) имеются дубликаты!!!")
        isValidationSuccessful = False

    # проверка уникальности слов из 1-го столбца словаря
    words_list = [single_tuple[0] for single_tuple in list_of_tuples]
    validate_no_word_duplicates(words_list)


def validate_no_word_duplicates(words_list):
    is_validation_ok = True
    # проверка уникальности слов из 1-го столбца словаря
    if len(words_list) != len(set(words_list)):
        duplicates = Utils.find_duplicates(words_list)
        print("Среди слов словаря в 1-м столбце имеются дубликаты: {}".format(duplicates))
        is_validation_ok = False
    #
    # if is_validation_ok:
    #     print("Словарь НЕ содержит дубликатов! Валидация успешна!!!")

    return is_validation_ok
