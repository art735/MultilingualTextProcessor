import PythonAndPipVersionValidator
import ValidationUtils
from DictionaryExcelDao import DictionaryExcelDao
from EBibleLexiconExcelDao import EBibleLexiconExcelDao
from MorphFormsExcelDao import MorphFormsExcelDao
from VocabularyExcelDao import VocabularyExcelDao


def validate_all_repos_uniqueness():
    dictionaryExcelDao = DictionaryExcelDao()
    ValidationUtils.validate_no_word_duplicates(dictionaryExcelDao.get_all_sheets_data_dict().keys())

    eBibleLexiconExcelDao = EBibleLexiconExcelDao()
    ValidationUtils.validate_no_word_duplicates(eBibleLexiconExcelDao.get_all_sheets_data_dict().keys())

    morphFormsExcelDao = MorphFormsExcelDao()
    ValidationUtils.validate_no_word_duplicates(morphFormsExcelDao.get_all_sheets_data_dict().keys())

    vocabularyExcelDao = VocabularyExcelDao()
    ValidationUtils.validate_no_word_duplicates(vocabularyExcelDao.get_all_sheets_data_dict().keys())


def validate():
    validate_all_repos_uniqueness()
    PythonAndPipVersionValidator.validate()

############################################################################


# validate()
