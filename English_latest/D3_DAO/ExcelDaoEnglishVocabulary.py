import xlrd

import CommonDataReader
import ExcelDaoUtils

SINGLE_NEW_LINE = "\n"
DOUBLE_NEW_LINE = "\n\n"

WORDS_PRIMARY_COLUMN_INDEX = 1

########################### ---=== GLOBAL VARIABLES ===--- ###################################################
# Сформировать объекты КНИГИ файла Excel
# workbookFilename = '../../resources/Deutsch.xls'
workbookFilename = 'E:/Languages/[Git repo] MultilingualTextProcessor/resources/English/EnglishVocabulary.xls'

# специально здесь идёт ссылка на EnglishDictionary (а не EnglishVocabulary как должно быть в идеале), чтобы пока временно работать сразу
# со всеми словами без необходимости их перетаскивать порциями из файла EnglishDictionary в файл EnglishVocabulary
# workbookFilename = 'E:/Languages/[Git repo] MultilingualTextProcessor/resources/English/EnglishDictionary.xls'


englishVocabulary_workbook = xlrd.open_workbook(workbookFilename)

# На основании объекта КНИГИ файла Excel, сформировать объекты ЛИСТОВ файла Excel
main_worksheet = englishVocabulary_workbook.sheet_by_name('Main')


##############################################################################################################

# обработчик нажатия на кнопку "Reload data from Excel"
# нужен для того, чтобы сохраненные в Excel данные в момент уже запущенной программы, можно было подтянуть без переоткрытия приложения
def reloadDataFromExcel():
    # подлючение в метод глобальных переменных, в противном случае доступа к ним не будет: система будет создавать одноименные локальные переменные
    global englishVocabulary_workbook
    global main_worksheet

    englishVocabulary_workbook = xlrd.open_workbook(workbookFilename)
    # На основании объекта КНИГИ файла Excel, сформировать объекты ЛИСТОВ файла Excel
    main_worksheet = englishVocabulary_workbook.sheet_by_name('Main')


def getExcelWordsForValidation():
    # Произвести валидацию уникальности слов в ЛИСТАХ файла Excel
    # Параметром метода является список кортежей (worksheet_name, wordsToValidate_index)
    wordsToValidate = ExcelDaoUtils.get_words_for_uniqueness_validation([(main_worksheet, WORDS_PRIMARY_COLUMN_INDEX)
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
#     main_worksheet_indices = [
#         [WORDS_PRIMARY_COLUMN_INDEX, WORDS_PRIMARY_COLUMN_INDEX + 1],
#         [WORDS_SECONDARY_COLUMN_INDEX, WORDS_SECONDARY_COLUMN_INDEX + 1],
#         [WORDS_TERTIARY_COLUMN_INDEX, WORDS_TERTIARY_COLUMN_INDEX + 1]
#     ]
#     main_worksheet_tuples = ExcelDaoUtils.getWorksheetData(main_worksheet, main_worksheet_indices)
#
#     # первых две пары - это комбинации [число(в цифровом выражении), транскрипция] и [число(в буквенном выражении), транскрипция]
#     # numerals_worksheet_indices = [[0, 2], [1, 2], [4, 5], [7, 8], [9, 10], [11, 12], [13, 14]]
#     # numerals_worksheet_tuples = ExcelDaoUtils.getWorksheetData(numerals_worksheet, numerals_worksheet_indices)
#     # print(numerals_worksheet_tuples)
#
#
#     # Step #3. Объединить вычитанные на предыдущем шаге данные с каждого листа в единый список
#     tuplesFromAllSheets = list()
#     tuplesFromAllSheets.extend(main_worksheet_tuples)
#     # tuplesFromAllSheets.extend(numerals_worksheet_tuples)
#
#
#     return tuplesFromAllSheets

###########################################################################


#################################################


# def getDataAsDict():
#     # Сконвертировать список кортежей (слово, транскрипция) в словарь {слово: транскрипция},
#     # при этом дубликаты слов (или их форм) будут исключены сами собой (ключи словаря всегда уникальны)
#     return Utils.convert_tuples_into_dictionary(getDataAsList())

def get_EnglishVocabulary_dict():
    # return getDataAsDict()
    return CommonDataReader.get_data_from_worksheet(main_worksheet)

##############################################################

# excelData = getDataAsList()
# print(len(excelData))
# print(excelData)


# data_dict = getDataAsDict()
# print(data_dict['einzukaufen'])


# print(getDataAsDict())
# vocabulary_dict = get_EnglishVocabulary_dict()
# for k, v in vocabulary_dict.items():
#     print(k)
#     print(v)
