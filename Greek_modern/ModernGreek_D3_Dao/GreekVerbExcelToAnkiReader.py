import itertools

import xlrd

import Utils
# Custom user imports
import pos_reader_5_verbs_wks
import ExcelDaoUtils

########################### ---=== GLOBAL VARIABLES ===--- ###################################################
# Сформировать объекты КНИГИ файла Excel
# workbookFilename = '../../resources/Deutsch.xls'
greek_dictionary_excel_filename = 'E:/Languages/English/SVN repo/Python software/MultilingualTextProcessor/resources/Greek/Verb conjugations.xls'

# all_excel_filenames = [deutsch_lexikon_popov_excel_filename, Politik_excel_filename]
# all_excel_filenames = [Politik_excel_filename]
all_excel_filenames = [greek_dictionary_excel_filename]

# глобальный словарь, в который вычитаны все данные из всех Excel-файлов
ALL_DATA_DICT = dict()


##############################################################################################################

# обработчик нажатия на кнопку "Reload data from Excel"
def reloadDataFromExcel():
    global ALL_DATA_DICT  # подключение глобальной переменной
    ALL_DATA_DICT.clear()


# основной DAO-метод, который вызывается в бизнес-логике
def getDataAsDict():
    global ALL_DATA_DICT  # подключение глобальной переменной

    # если глобальная переменная ALL_DATA_DICT содержит данные, то их и использовать! Не дёргать каждый раз Excel-лист
    # и не читать из него данные каждый раз!!!! Пользоваться уже вычитанными ранее данными этим же методом!!!
    if len(ALL_DATA_DICT) > 0:
        return ALL_DATA_DICT

    # all_articles_and_pronouns_wks_tuples = list()
    # all_bare_nouns_wks_tuples = list()
    # all_bare_adjectives_wks_tuples = list()
    # all_numerals_wks_tuples = list()
    all_verbs_wks_tuples = list()
    # all_other_wks_tuples = list()

    verbs_wks_tuples = list()

    for excel_filename in all_excel_filenames:
        workbook = xlrd.open_workbook(excel_filename)

        # На основании объекта КНИГИ файла Excel, сформировать объекты ЛИСТОВ файла Excel
        # articles_and_pronouns_worksheet = workbook.sheet_by_name('Articles & Pronouns')
        # nouns_worksheet = workbook.sheet_by_name('Nouns')
        # adjectives_worksheet = workbook.sheet_by_name('Adjectives')
        # numerals_worksheet = workbook.sheet_by_name('Numerals')
        verbs_worksheet = workbook.sheet_by_name('Verbs')
        # other_worksheet = workbook.sheet_by_name('Other')

        # Для каждого листа сформировать список индексов столбцов, которые должны быть вычитаны (каждая группа столбцов,
        # формирующая самостоятельный кортеж (слово, транскрипция), должна быть указана отдельным подсписком)
        # и произвести вычитку данных с каждого листа
        # articles_and_pronouns_wks_tuples = pos_reader_1_articles_and_pronouns_wks.get_tuples(articles_and_pronouns_worksheet)
        # bare_nouns_wks_tuples = pos_reader_2_nouns_wks.get_tuples(nouns_worksheet)
        # bare_adjectives_wks_tuples = pos_reader_3_adjectives_wks.get_tuples(adjectives_worksheet)
        # numerals_wks_tuples = pos_reader_4_numerals_wks.get_tuples(numerals_worksheet)
        verbs_wks_tuples = pos_reader_5_verbs_wks.get_tuples(verbs_worksheet)
        # other_wks_tuples = pos_reader_6_other_wks.get_tuples(other_worksheet)

        # all_articles_and_pronouns_wks_tuples.extend(articles_and_pronouns_wks_tuples)
        # all_bare_nouns_wks_tuples.extend(bare_nouns_wks_tuples)
        # all_bare_adjectives_wks_tuples.extend(bare_adjectives_wks_tuples)
        # all_numerals_wks_tuples.extend(numerals_wks_tuples)
        all_verbs_wks_tuples.extend(verbs_wks_tuples)
        # all_other_wks_tuples.extend(other_wks_tuples)

    # Step #3. Объединить вычитанные на предыдущем шаге данные в единый список
    tuplesFromAllSheets = list()
    # tuplesFromAllSheets.extend(all_articles_and_pronouns_wks_tuples)
    # tuplesFromAllSheets.extend(all_bare_nouns_wks_tuples)
    # tuplesFromAllSheets.extend(all_bare_adjectives_wks_tuples)
    # tuplesFromAllSheets.extend(all_numerals_wks_tuples)
    tuplesFromAllSheets.extend(all_verbs_wks_tuples)
    # tuplesFromAllSheets.extend(all_other_wks_tuples)

    # Сконвертировать список кортежей (слово, транскрипция) в словарь {слово: транскрипция},
    # при этом дубликаты слов (или их форм) будут исключены сами собой (ключи словаря всегда уникальны)
    ALL_DATA_DICT = dict(Utils.convert_tuples_into_dictionary(tuplesFromAllSheets))
    return ALL_DATA_DICT


def getExcelWordsForValidation():
    # Произвести валидацию уникальности слов в ЛИСТАХ файла Excel
    # Параметром метода является список кортежей (worksheet_name, wordsToValidate_index)

    words_per_sheet_dict = dict()
    tuples_to_validate = list()
    # words_to_validate = list()

    for excel_filename in all_excel_filenames:
        workbook = xlrd.open_workbook(excel_filename)

        # На основании объекта КНИГИ файла Excel, сформировать объекты ЛИСТОВ файла Excel
        # articles_and_pronouns_worksheet = workbook.sheet_by_name('Articles & Pronouns')
        # nouns_worksheet = workbook.sheet_by_name('Nouns')
        # adjectives_worksheet = workbook.sheet_by_name('Adjectives')
        # numerals_worksheet = workbook.sheet_by_name('Numerals')
        verbs_worksheet = workbook.sheet_by_name('Verbs')
        # other_worksheet = workbook.sheet_by_name('Other')

        # Вторым элементом кортежа является индекс стобца, из которого нужно брать слова для валидации уникальности
        # nouns_tuple = (nouns_worksheet, 0)
        # adjectives_tuple = (adjectives_worksheet, 0)
        # numerals_tuple = (numerals_worksheet, 1)
        verbs_tuple = (verbs_worksheet, 0)
        # other_tuple = (other_worksheet, 0)

        # tuples_to_validate.append(nouns_tuple)
        # tuples_to_validate.append(adjectives_tuple)
        # tuples_to_validate.append(numerals_tuple)
        tuples_to_validate.append(verbs_tuple)
        # tuples_to_validate.append(other_tuple)

        words_to_validate = ExcelDaoUtils.get_words_for_uniqueness_validation(tuples_to_validate)
        words_per_sheet_dict[excel_filename] = words_to_validate
        tuples_to_validate.clear()

    return words_per_sheet_dict


def make_up_aspect_specific_data(aspect):
    anki_back_conjugation_hint = """спряжение в {0} аспекте:
1) Ενεργητική:
- {1}
- {2}
- {3}
2) Υποτακτική
3) Προστακτική
{4}"""

    if aspect == 'aoristic':
        present_tense_name = 'Ενεστώτας'
        past_tense_name = 'Αόριστος'
        future_tense_name = 'Μέλλοντας απλός'

        anki_front_present_tense_list = [present_tense_name]
        anki_front_past_tense_list = [past_tense_name]
        anki_front_future_tense_list = [future_tense_name]
        anki_back_conjugation_hint = anki_back_conjugation_hint.format('аористическом', present_tense_name,
                                                                       past_tense_name, future_tense_name, 'Απαρέμφατο')
        start_column_index = 2
    elif aspect == 'imperfective':
        present_tense_name = 'Ενεστώτας'
        past_tense_name = 'Παρατατικός'
        future_tense_name = 'Μέλλοντας συνεχής'

        anki_front_present_tense_list = [present_tense_name]
        anki_front_past_tense_list = [past_tense_name]
        anki_front_future_tense_list = [future_tense_name]
        anki_back_conjugation_hint = (anki_back_conjugation_hint
                                      .format('имперфективном', present_tense_name, past_tense_name,
                                              future_tense_name, '')
                                      .strip())  # удаляет символы [ \t\n\r\f\v] в начале и конце строки
        start_column_index = 4
    elif aspect == 'perfective':
        present_tense_name = 'Παρακείμενος'
        past_tense_name = 'Υπερσυντέλικος'
        future_tense_name = 'Μέλλοντας τετελεσμένος'

        anki_front_present_tense_list = [present_tense_name]
        anki_front_past_tense_list = [past_tense_name]
        anki_front_future_tense_list = [future_tense_name]
        anki_back_conjugation_hint = (anki_back_conjugation_hint
                                      .format('перфектном', present_tense_name, past_tense_name,
                                              future_tense_name, '')
                                      .strip())  # удаляет символы [ \t\n\r\f\v] в начале и конце строки
        start_column_index = 6

    # выполняется безусловно, не входит ни в один из if-ов
    anki_back_conjugation_hint = '<i>{0}</i>'.format(anki_back_conjugation_hint)
    # anki_back_conjugation_hint = "'AAA{}BBB'".format(anki_back_conjugation_hint)

    return [anki_front_present_tense_list, anki_front_past_tense_list, anki_front_future_tense_list,
            anki_back_conjugation_hint, start_column_index]


def makeAnkiCard(single_verb_excel_rows, aspect):
    aspect_specific_data = make_up_aspect_specific_data(aspect)

    anki_front_verb_dictionary_form = ""

    anki_front_present_tense_list = aspect_specific_data[0]
    anki_front_past_tense_list = aspect_specific_data[1]
    anki_front_future_tense_list = aspect_specific_data[2]

    anki_front_Υποτακτική_list = ['Υποτακτική']
    anki_front_Προστακτική_list = ['Προστακτική']
    anki_front_Απαρέμφατο_list = ['Απαρέμφατο']

    anki_back_translation = ""
    anki_back_conjugation_hint = aspect_specific_data[3]

    start_column_index = aspect_specific_data[4]

    counter = 0

    for t in single_verb_excel_rows:
        if any(t):  # returns True if any item in an iterable are true, otherwise it returns False
            # пустая строка в Excel используется как разделитель.
            # продолжать цикл только если строка не пустая, т. е. имеем дело со строкой данных, а не строкой-разделителем

            if t[
                0]:  # если работаем с 1-й строкой каждого глагола (строкой, содержащей начальную словарную форму глагола и его перевод)
                anki_front_verb_dictionary_form = t[0]
                anki_back_translation = t[1]

            if 0 <= counter <= 2:
                # не относится к ' if t[0] != "": ', выполняется в любом случае
                anki_front_present_tense_list.append(
                    t[start_column_index] + SPACE_DASH_SPACE + t[start_column_index + 1])

            elif 3 <= counter <= 5:
                anki_front_past_tense_list.append(t[start_column_index] + SPACE_DASH_SPACE + t[start_column_index + 1])

            elif 6 <= counter <= 8:
                anki_front_future_tense_list.append(
                    t[start_column_index] + SPACE_DASH_SPACE + t[start_column_index + 1])

            elif 9 <= counter <= 11:
                anki_front_Υποτακτική_list.append(t[start_column_index] + SPACE_DASH_SPACE + t[start_column_index + 1])

            elif counter == 12:
                anki_front_Προστακτική_list.append(t[start_column_index] + SPACE_DASH_SPACE + t[start_column_index + 1])

            elif counter == 13 and aspect == 'aoristic':
                anki_front_Απαρέμφατο_list.append(t[2])

            counter += 1

            if counter == 14:  # случай, когда обработали все строки Excel, относящиеся к данному глаголу

                # формируем строковое представление карточки для Anki
                anki_front = DOUBLE_NEW_LINE.join([anki_front_verb_dictionary_form,
                                                   SINGLE_NEW_LINE.join(anki_front_present_tense_list),
                                                   SINGLE_NEW_LINE.join(anki_front_past_tense_list),
                                                   SINGLE_NEW_LINE.join(anki_front_future_tense_list),
                                                   SINGLE_NEW_LINE.join(anki_front_Υποτακτική_list),
                                                   SINGLE_NEW_LINE.join(anki_front_Προστακτική_list)])
                if aspect == 'aoristic':
                    anki_front += DOUBLE_NEW_LINE + SINGLE_NEW_LINE.join(anki_front_Απαρέμφατο_list)

                anki_back = DOUBLE_NEW_LINE.join([anki_back_translation, anki_back_conjugation_hint])
                anki_card = DOUBLE_NEW_LINE.join([anki_front, anki_back])

    return anki_card


def get_verbs_for_anki(aspect):
    verbs_worksheet_indices = [0, 1,  # greek verbs and its russian traslation
                               3, 4,  # aoristic aspect
                               6, 7,  # imperfective aspect
                               9, 10  # perfective aspect
                               ]

    sheet_data = list()
    columns_list = list()

    for i in verbs_worksheet_indices:
        for excel_filename in all_excel_filenames:
            workbook = xlrd.open_workbook(excel_filename)
            verbs_worksheet = workbook.sheet_by_name('Verbs')
            columns_list.append(verbs_worksheet.col_values(i))

    # склеиваем список столбцов Excel так, чтобы получился список строк Excel
    sheet_data.extend(list(itertools.zip_longest(*columns_list, fillvalue="")))

    # key - verb in infinitive
    # value - verb data in Anki format
    anki_cards_dict = dict()

    sheet_data_dict = dict()
    for row in sheet_data:
        if row[0]:  # если работаем со строкой Excel, содержащей инфинитив глагола
            verb_infinitive = row[0]
            sheet_data_dict[verb_infinitive] = list()
        sheet_data_dict[verb_infinitive].append(row)

    for infinitive, rows in sheet_data_dict.items():
        anki_cards_dict[infinitive] = makeAnkiCard(rows, aspect)

    return anki_cards_dict


##############################################################

verb_dict = get_verbs_for_anki('aoristic')
# verb_dict = get_verbs_for_anki('imperfective')
# verb_dict = get_verbs_for_anki('perfective')
for key, val in verb_dict.items():
    if key == 'είμαι':
        print(val)

# verb_dict = getVerbsForAwesomeTTS()
# for key, val in verb_dict.items():
#     print(val)


# verbs = getInfinitiv_PartizipIIPairs()
# print(verbs)


# adjectives = getAdjectivesComparisonDegrees()
# print(adjectives)

# wordsToValidate = getExcelWordsForValidation()
# print(len(wordsToValidate))
