import ExcelDaoEnglishDictionary
import ExcelDaoEnglishVocabulary
import ValidationUtils


def validate_englishDictionary_uniqueness():
    dictionaryWords = ExcelDaoEnglishDictionary.getExcelWordsForValidation()
    ValidationService.validate_vocabulary_uniqueness('EnglishDictionary.xls', dictionaryWords, [])


def validate_englishVocabulary_uniqueness(excel_filename):
    vocabularyWords = ExcelDaoEnglishVocabulary.getExcelWordsForValidation()
    ValidationUtils.validate_vocabulary_uniqueness(excel_filename, vocabularyWords, [])

# def validateExcelWordColumnUniqueness():
#     validate_englishDictionary_uniqueness()
#     validate_englishVocabulary_uniqueness()
