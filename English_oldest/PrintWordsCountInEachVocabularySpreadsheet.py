from importlib.machinery import SourceFileLoader

# vocabularyWordsService = SourceFileLoader('VocabularyWordsService', '../CommonBusinessLogic/VocabularyWordsService.py').load_module()

excelDao = SourceFileLoader('ExcelDao', 'CommonDAO/LocalDAO/ExcelDaoEnglishTopics.py').load_module()

currentWorkbookFilename = excelDao.composeCurrentWorkbookFilename()

wordsAsTuples = excelDao.getWordsForMonitoring(currentWorkbookFilename)

print("TOPIC#   n of words")

counter = 1

for tuple in wordsAsTuples:
    print("Topic {0} – {1} words".format(counter, len(tuple)))
    counter = counter + 1
