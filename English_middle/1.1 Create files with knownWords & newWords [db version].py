# configDao = SourceFileLoader('ConfigDao', '../CommonDAO/LocalDAO/ConfigDao.py').load_module()
# dbDao = SourceFileLoader('DbDao', '../CommonDAO/LocalDAO/DbDao.py').load_module()
# excelDao = SourceFileLoader('ExcelDao', '../CommonDAO/LocalDAO/ExcelDaoEnglishTopics.py').load_module()
# txtDao = SourceFileLoader('TxtDao', '../CommonDAO/LocalDAO/TxtDao.py').load_module()

# wordMorphologyAndFrequencyProcessor = SourceFileLoader('WordMorphologyAndFrequencyProcessor',
#                               '../CommonBusinessLogic/WordMorphologyAndFrequencyProcessor.py').load_module()
#
# vocabularyWordsService = SourceFileLoader('VocabularyWordsService',
#                                           '../CommonBusinessLogic/VocabularyWordsService.py').load_module()
#
# printResultsService = SourceFileLoader('PrintResultsService',
#                                        '../CommonBusinessLogic/PrintResultsService.py').load_module()


import PrintResultsService
import WordMorphologyAndFrequencyProcessor
import ConfigDao
import DbDao
import ExcelDaoEnglishTopics

#######################################

# STEP 0
[themeNumber, themeName, topicNumber] = ConfigDao.getTopicEnvironmentFromConfig()

# STEP 1. Getting 1st argument - text
text = DbDao.getTopic(themeNumber, topicNumber)
# text = dbDao.getTopic('I', '1')
# text = dbDao.getAllTopicsByTheme('I')
# text = dbDao.getTopicsRange('I', '1', topicNumber)
# text = "I go to school"

# STEP 2. Getting 2nd argument - list of learnt words
# vocabularyWords = vocabularyWordsService.getVocabularyWordsFromSpreadsheets('ALL')
# vocabularyWords = vocabularyWordsService.getVocabularyWordsFromSpreadsheets('UP_TO_CURRENT_INCLUDING')
# vocabularyWords = vocabularyWordsService.getVocabularyWordsFromDb()

# mode = {'CURRENT_ONLY', 'UP_TO_CURRENT_INCLUDING', 'ALL'}
vocabularyWords = ExcelDaoEnglishTopics.getVocabularyWords('CURRENT_ONLY')

# STEP 3. Getting 3rd argument - list of ignored words
ignoredWords = ExcelDaoEnglishTopics.getIgnoredWordsFromCurrentWorkbook()

# MAIN PROCESSING

[knownWordsFreq_dict, wordsFreq_dict] = WordMorphologyAndFrequencyProcessor.process(text, vocabularyWords, ignoredWords)

# SENDING THE PROCESSED DATA TO THE OUTER WORLD
PrintResultsService.printResults(knownWordsFreq_dict, wordsFreq_dict)

# TODO сделать валидацию того, что соблюдается тождество:
# q(text) = q(knownWords) + q(newWords) + q(ingnoredWords)
# TODO прогнать эту валидацию для каждого топика в отдельности и всей темы в целом
