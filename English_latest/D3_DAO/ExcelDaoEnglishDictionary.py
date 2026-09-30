import xlrd

import CommonDataReader
import ExcelDaoUtils

SINGLE_NEW_LINE = "\n"
DOUBLE_NEW_LINE = "\n\n"

WORDS_PRIMARY_COLUMN_INDEX = 1  # столбец со словами из словаря
WORDS_SECONDARY_COLUMN_INDEX = WORDS_PRIMARY_COLUMN_INDEX + 4  # столбец с мн. ч. сущ., сравнит. степ. прил., past simple непр. глаголов
WORDS_TERTIARY_COLUMN_INDEX = WORDS_SECONDARY_COLUMN_INDEX + 2  # столбец с превосх. степ. прил., participle II непр. глаголов

########################### ---=== GLOBAL VARIABLES ===--- ###################################################
# Сформировать объекты КНИГИ файла Excel
# workbookFilename = '../../resources/Deutsch.xls'
workbookFilename = 'E:/Languages/[Git repo] MultilingualTextProcessor/resources/English/EnglishDictionary.xls'
englishDictionary_workbook = xlrd.open_workbook(workbookFilename)

# На основании объекта КНИГИ файла Excel, сформировать объекты ЛИСТОВ файла Excel
top4k_worksheet = englishDictionary_workbook.sheet_by_name('Top4k')


##############################################################################################################

# обработчик нажатия на кнопку "Reload data from Excel"
# нужен для того, чтобы сохраненные в Excel данные в момент уже запущенной программы, можно было подтянуть без переоткрытия приложения
def reloadDataFromExcel():
    # подлючение в метод глобальных переменных, в противном случае доступа к ним не будет: система будет создавать одноименные локальные переменные
    global englishDictionary_workbook
    global top4k_worksheet

    englishDictionary_workbook = xlrd.open_workbook(workbookFilename)
    # На основании объекта КНИГИ файла Excel, сформировать объекты ЛИСТОВ файла Excel
    top4k_worksheet = englishDictionary_workbook.sheet_by_name('Top4k')


def getExcelWordsForValidation():
    # Произвести валидацию уникальности слов в ЛИСТАХ файла Excel
    # Параметром метода является список кортежей (worksheet_name, wordsToValidate_index)
    wordsToValidate = ExcelDaoUtils.get_words_for_uniqueness_validation([(top4k_worksheet, WORDS_PRIMARY_COLUMN_INDEX)
                                                                         # (adjectives_worksheet, 0),
                                                                         # (numerals_worksheet, 1),
                                                                         # (verbs_worksheet, 0),
                                                                         # (other_worksheet, 0)
                                                                         ])

    return wordsToValidate


# def getDataAsList():
#     # Для каждого листа сформировать список индексов столбцов, которые должны быть вычитаны (каждая группа столбцов,
#     # формирующая самостоятельный кортеж (слово, транскрипция), должна быть указана отдельным подсписком)
#     # и произвести вычитку данных с каждого листа
#
#     top4k_worksheet_indices = [
#         [WORDS_PRIMARY_COLUMN_INDEX, WORDS_PRIMARY_COLUMN_INDEX + 1, WORDS_PRIMARY_COLUMN_INDEX + 2],
#         [WORDS_SECONDARY_COLUMN_INDEX, WORDS_SECONDARY_COLUMN_INDEX + 1],
#         [WORDS_TERTIARY_COLUMN_INDEX, WORDS_TERTIARY_COLUMN_INDEX + 1]
#     ]
#     top4k_worksheet_tuples = ExcelDaoUtils.getWorksheetData(top4k_worksheet, top4k_worksheet_indices)
#
#
#     # первых две пары - это комбинации [число(в цифровом выражении), транскрипция] и [число(в буквенном выражении), транскрипция]
#     # numerals_worksheet_indices = [[0, 2], [1, 2], [4, 5], [7, 8], [9, 10], [11, 12], [13, 14]]
#     # numerals_worksheet_tuples = ExcelDaoUtils.getWorksheetData(numerals_worksheet, numerals_worksheet_indices)
#     # print(numerals_worksheet_tuples)
#
#
#     # Step #3. Объединить вычитанные на предыдущем шаге данные с каждого листа в единый список
#     tuplesFromAllSheets = list()
#     tuplesFromAllSheets.extend(top4k_worksheet_tuples)
#     # tuplesFromAllSheets.extend(numerals_worksheet_tuples)
#
#
#     return tuplesFromAllSheets


# def getDataAsDict():
#     # Сконвертировать список кортежей вида (t_item_1, t_item_2, ..., t_item_n) в словарь { t_item_1: [t_item_2, ..., t_item_n] },
#     # при этом дубликаты слов (или их форм) будут исключены сами собой (ключи словаря всегда уникальны)
#     return Utils.convert_tuples_into_dictionary(getDataAsList())

def get_EnglishDictionary_dict():
    return CommonDataReader.get_data_from_worksheet(top4k_worksheet)

##############################################################

# word_freq_5k_worksheet = englishDictionary_workbook.sheet_by_name('word_freq_5k')
# indices = [[0, 1, 2]]
# word_freq_5k_tuples = ExcelDaoUtils.getWorksheetData(word_freq_5k_worksheet, indices)
# word_freq_5k_dict = Utils.convert_tuples_into_dictionary(word_freq_5k_tuples)
# print(len(word_freq_5k_tuples))
# print(word_freq_5k_tuples)

# excelData = get_EnglishDictionary_dict()
# print(len(excelData))
# print(excelData)

# Искать перевод слова для HugeDictionary в других листах
# for word, translation in excelData:
#     if len(translation) == 0: # если перевода слова в HugeDictionary нет - искать в другом списке слов (в другом Excel-листе)
#         translation = word_freq_5k_dict.get(word)
#         if translation is not None:
#             translation = re.sub(r'\n', '^^^', translation) # временно заменить Excel-ский newline на ^^^
#         else:
#             translation = LingvoTranslationDao.getTranslation(word) # в самом крайнем случае вычитывать перевод из Lingvo
#
#         res = "{0} * {1}".format(word, translation)
#         print(res)
