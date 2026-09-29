# from importlib.machinery import SourceFileLoader
# excelDao = SourceFileLoader('ExcelDao', '../CommonDAO/LocalDAO/ExcelDaoEnglishTopics.py').load_module()
# vocabularyWordsService = SourceFileLoader('VocabularyWordsService',
#                                           '../CommonBusinessLogic/VocabularyWordsService.py').load_module()


import VocabularyWordsService
import ExcelDaoEnglishTopics


def lookUpNewWords(topicVocabularyNewWords, tuplesTop5000):
    results = list()
    for wordToLookUp in topicVocabularyNewWords:
        res = _findWordIn5000Dictionary(wordToLookUp, tuplesTop5000)
        results.append(res)

    return results


def _findWordIn5000Dictionary(wordToLookUp, tuplesTop5000):
    result = [wordToLookUp, None, None]

    for row in tuplesTop5000:
        if wordToLookUp == row[0]:
            transcription = row[1]
            translation = row[2]
            result = [wordToLookUp, transcription, translation]
            break
    res = "{0}\t{1}\t{2}".format(result[0], result[1], result[2])
    return res


##########################################################################

top5000WorkbookFilename = "../resources/Top5000.xls"

# STEP 1
# raw words - это слова из словарика "как есть":
# - глаголы с предшествующей частицей to, например "to look"
# - неправильные глаголы с предшествующей частицей to и двумя формами в скобках, напр. "to go (went; gone)"
vocabularyWords = ExcelDaoEnglishTopics.getVocabularyWords('CURRENT_ONLY')
trimmedVocabularyWords = VocabularyWordsService.trim(vocabularyWords)
# list1 = ["a", "b", "c"]
# list2 = [["aaa"], ["bbb"], ["ccc"]]

# result = list(itertools.chain(*topicVocabularyNewWords))

# topicVocabularyNewWords = [x for x in topicVocabularyNewWords]
# topicVocabularyNewWords = *topicVocabularyNewWords

# wordsToLookUp = ['family', 'madfdf', 'cat']


# STEP 2
top5kTuples = ExcelDaoEnglishTopics.getTop5kWords()

# STEP 3. Main processing logic of the collections read from Excel-files
results = lookUpNewWords(trimmedVocabularyWords, top5kTuples)

for result in results:
    print(result)
