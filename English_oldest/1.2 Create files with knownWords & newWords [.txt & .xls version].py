from importlib.machinery import SourceFileLoader

configDao = SourceFileLoader('ConfigDao', 'CommonDAO/LocalDAO/ConfigDao.py').load_module()
excelDao = SourceFileLoader('ExcelDao', 'CommonDAO/LocalDAO/ExcelDaoEnglishTopics.py').load_module()
txtDao = SourceFileLoader('TxtDao', 'CommonDAO/LocalDAO/TxtDao.py').load_module()

wordMorphologyAndFrequencyProcessor = SourceFileLoader('WordMorphologyAndFrequencyProcessor',
                                                       'CommonBusinessLogic/WordMorphologyAndFrequencyProcessor.py').load_module()
printResultsService = SourceFileLoader('PrintResultsService',
                                       'CommonBusinessLogic/PrintResultsService.py').load_module()
validationService = SourceFileLoader('ValidationService', 'CommonBusinessLogic/ValidationUtils.py').load_module()
utils = SourceFileLoader('Utils', 'CommonBusinessLogic/Utils.py').load_module()
vocabularyWordsService = SourceFileLoader('VocabularyWordsService',
                                          'CommonBusinessLogic/VocabularyWordsService.py').load_module()

# Получать список новых слов (newWords) сразу для всего текста целиком бывает затруднительно с точки зрения
# его дальнейшей проработки: список может содержать сотню и больше слов.
# Поэтому данный скрипт является альтернативным методом получения списка новых слов небольшими порциями.
# Для этого, текст разбивается на абзацы и каждый абзац считается как бы новым текстом и
# запуская скрипт последовательно для кадого абзаца и проводя после каждого такого запуска обработку слов
# оказывается возможным небольшими итерациями КОНСИСТЕНТНО составить словарь для целого топика.
#
# ИСХОДНЫЕ ДАННЫЕ:
# 1. Иметь файл topic_paragraph.txt с i-м абзацем исходного текста
# 2. Иметь .xls-файл со словами, которые считаются уже проработанными
#
# АЛГОРИТМ РАБОТЫ:
# 1. Скопировать название текста и первый абзац исходного текста в файл topic_paragraph.txt
# 2. Запустить данный скрипт
# 3. Скопировать из консоли список новых слов, вставить их в .xls-файл в соответствующий worksheet и проводить их ручную доработку.
# 4. Запустить ещё раз данный скрипт, чтобы убедиться, что с учётом пополнившагося словаря, новых слов в текущем абзаце исходного текста больше нет.
# 5. Скопировать следующий абзац исходного текста в файл topic_paragraph.txt и повторить заново все шаги.
#
# ИТОГИ:
# В .xls-файле будет сформирован список новых слов для текущего топика.

#######################################

currentWorkbookFilename = excelDao.composeCurrentWorkbookFilename()

# STEP 1. Getting 1st argument - list of learnt words
# vocabularyWords = vocabularyWordsService.getVocabularyWordsFromSpreadsheets('ALL')
vocabularyWords = vocabularyWordsService.getVocabularyWordsFromSpreadsheets('UP_TO_CURRENT_INCLUDING')
# vocabularyWords = vocabularyWordsService.getVocabularyWordsFromDb()

# STEP 2. Getting 2nd argument - text
text = txtDao.readTextFromFile('../resources/!topic_paragraph.txt')

# STEP 3. Getting 3rd argument - list of ignored words
ignoredWords = excelDao.getIgnoredWordsFromCurrentWorkbook(currentWorkbookFilename)
# ignoredWords = ['i', 'max', 'kovaliov']

# MAIN PROCESSING
[knownWordsFreq_dict, wordsFreq_dict] = wordMorphologyAndFrequencyProcessor.process(text, vocabularyWords, ignoredWords)

# SENDING THE PROCESSED DATA TO THE OUTER WORLD
printResultsService.printResults(knownWordsFreq_dict, wordsFreq_dict)
