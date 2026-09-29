from importlib.machinery import SourceFileLoader
from unittest import TestCase

vocabularyWordsService = SourceFileLoader('VocabularyWordsService',
                                          'CommonBusinessLogic/VocabularyWordsService.py').load_module()


# charConstants = SourceFileLoader('CharConstants', '../CommonBusinessLogic/CharConstants.py').load_module()
#
# vocabularyWordsEmptyList = list()
# ignoredWordsEmptyList = list()

class Test_VocabularyWordsService(TestCase):

    # Test compound NOUNS preprocession
    def test1(self):
        vocabularyCompoundNouns = ["man (pl. men)", "craftsman (pl. craftsmen)", "crisis (pl. crises)"]

        expectedResult = dict()
        expectedResult[vocabularyCompoundNouns[0]] = "man"
        expectedResult[vocabularyCompoundNouns[1]] = "craftsman"
        expectedResult[vocabularyCompoundNouns[2]] = "crisis"

        actualResult = vocabularyWordsService.preprocessCompoundVocabularyWords(vocabularyCompoundNouns)
        self.assertEqual(expectedResult, actualResult)

    # Test compound ADJECTIVES preprocession
    def test2(self):
        vocabularyCompoundAdjectives = ["good (better, best)", "nice (nicer, nicest)", "easy (easier, easiest)"]

        expectedResult = dict()
        expectedResult[vocabularyCompoundAdjectives[0]] = "good"
        expectedResult[vocabularyCompoundAdjectives[1]] = "nice"
        expectedResult[vocabularyCompoundAdjectives[2]] = "easy"

        actualResult = vocabularyWordsService.preprocessCompoundVocabularyWords(vocabularyCompoundAdjectives)
        self.assertEqual(expectedResult, actualResult)

    # Test compound VERBS preprocession
    def test3(self):
        vocabularyCompoundVerbs = ["to love", "to be (was, were; been)", "to see (saw; seen)"]

        expectedResult = dict()
        expectedResult[vocabularyCompoundVerbs[0]] = "love"
        expectedResult[vocabularyCompoundVerbs[1]] = "be"
        expectedResult[vocabularyCompoundVerbs[2]] = "see"

        actualResult = vocabularyWordsService.preprocessCompoundVocabularyWords(vocabularyCompoundVerbs)
        self.assertEqual(expectedResult, actualResult)

    def test1_unfoldWords(self):
        # excelDao = SourceFileLoader('ExcelDao', '../CommonDAO/LocalDAO/ExcelDaoEnglishTopics.py').load_module()
        # vocabularyTuple = excelDao.getVocabularyTuplesUpToCurrentTopic()

        vocabularyTuple = [('to be (was, were; been)', '[biː] ([wɔz], [wɜː]; [biːn])')]
        expectedResult = [('be', '[biː]'), ('was', '[wɔz]'), ('were', '[wɜː]'), ('been', '[biːn]')]
        actualResult = vocabularyWordsService.unfold(vocabularyTuple)
        self.assertEqual(expectedResult, actualResult)

    def test2_unfoldWords(self):
        # excelDao = SourceFileLoader('ExcelDao', '../CommonDAO/LocalDAO/ExcelDaoEnglishTopics.py').load_module()
        # vocabularyTuple = excelDao.getVocabularyTuplesUpToCurrentTopic()

        vocabularyTuple = [('to see (saw; seen)', '[siː] ([sɔː]; [siːn])')]
        expectedResult = [('see', '[siː]'), ('saw', '[sɔː]'), ('seen', '[siːn]')]
        actualResult = vocabularyWordsService.unfold(vocabularyTuple)
        self.assertEqual(expectedResult, actualResult)
