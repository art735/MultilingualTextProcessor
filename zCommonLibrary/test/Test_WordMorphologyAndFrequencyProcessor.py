import collections
from importlib.machinery import SourceFileLoader
from unittest import TestCase

wordMorphologyAndFrequencyProcessor = SourceFileLoader('WordMorphologyAndFrequencyProcessor',
                                                       'CommonBusinessLogic/WordMorphologyAndFrequencyProcessor.py').load_module()

tokenizer = SourceFileLoader('Tokenizer', 'CommonBusinessLogic/Tokenizer.py').load_module()

vocabularyWordsEmptyList = list()
ignoredWordsEmptyList = list()


class Test_WordMorphologyAndFrequencyProcessor(TestCase):

    # Simple test
    def test1(self):
        text = 'a b'

        expectedResultKnownWords = dict()
        expectedResultNewWords = collections.OrderedDict([('a', 1), ('b', 1)])
        expectedResult = [expectedResultKnownWords, expectedResultNewWords]

        actualResult = [knownWordsFreq_dict, wordsFreq_dict] = wordMorphologyAndFrequencyProcessor.process(text,
                                                                                                           vocabularyWordsEmptyList,
                                                                                                           ignoredWordsEmptyList)

        self.assertEqual(expectedResult, actualResult)

    # Testing tokens, starting with a digit (such tokens should be skipped)
    def test2(self):
        text = '1968 60s 1896–1966 1st 2nd ball3pen 3rd'

        expectedResultKnownWords = dict()
        expectedResultNewWords = collections.OrderedDict()
        expectedResult = [expectedResultKnownWords, expectedResultNewWords]

        actualResult = [knownWordsFreq_dict, wordsFreq_dict] = wordMorphologyAndFrequencyProcessor.process(text,
                                                                                                           vocabularyWordsEmptyList,
                                                                                                           ignoredWordsEmptyList)

        self.assertEqual(expectedResult, actualResult)

    # Testing tokens in possessive case
    def test3(self):
        text = "father, father's, fathers, fathers'; mother, mother's, mothers, mothers'"
        vocabularyWords = ["father", "mother", "brother", "sister"]

        expectedResultKnownWords = dict([('father', 4), ('mother', 4)])
        expectedResultNewWords = collections.OrderedDict()
        expectedResult = [expectedResultKnownWords, expectedResultNewWords]

        actualResult = [knownWordsFreq_dict, wordsFreq_dict] = wordMorphologyAndFrequencyProcessor.process(text,
                                                                                                           vocabularyWords,
                                                                                                           ignoredWordsEmptyList)

        self.assertEqual(expectedResult, actualResult)

    # Testing if wordMorphologyAndFrequencyProcessor recognizes "bookshelves" as a "bookshelf"
    def test4(self):
        text = "bookshelves"
        vocabularyWords = ["bookshelf"]
        actualResult = [knownWordsFreq_dict, wordsFreq_dict] = wordMorphologyAndFrequencyProcessor.process(text,
                                                                                                           vocabularyWords,
                                                                                                           ignoredWordsEmptyList)

        expectedResultKnownWords = dict([('bookshelf', 1)])
        expectedResultNewWords = collections.OrderedDict()
        expectedResult = [expectedResultKnownWords, expectedResultNewWords]

        self.assertEqual(expectedResult, actualResult)

    def test5(self):
        text = "I am busy"
        vocabularyWords = ["I", "to be (was, were; been)", "busy"]
        # vocabularyWords = ["I", "to be", "busy"]
        actualResult = [knownWordsFreq_dict, wordsFreq_dict] = wordMorphologyAndFrequencyProcessor.process(text,
                                                                                                           vocabularyWords,
                                                                                                           ignoredWordsEmptyList)

        expectedResultKnownWords = collections.OrderedDict([("i", 1), ("to be (was, were; been)", 1), ("busy", 1)])
        expectedResultNewWords = collections.OrderedDict()
        expectedResult = [expectedResultKnownWords, expectedResultNewWords]

        self.assertEqual(expectedResult, actualResult)

    def test6(self):
        text = "I am busy, I was busy. You are a boy, you were a boy. "
        text += "She is a girl, she was a girl. You are child, they were children."

        vocabularyWords = ["I", "to be (was, were; been)", "busy", "you", "a", "boy", "she", "girl", "they",
                           "child (pl. children)"]
        actualResult = [knownWordsFreq_dict, wordsFreq_dict] = wordMorphologyAndFrequencyProcessor.process(text,
                                                                                                           vocabularyWords,
                                                                                                           ignoredWordsEmptyList)

        expectedResultKnownWords = collections.OrderedDict([
            ("i", 2), ("to be (was, were; been)", 8), ("busy", 2), ("you", 3), ("a", 4), ("boy", 2),
            ("she", 2), ("girl", 2), ("child (pl. children)", 2), ("they", 1)
        ])
        expectedResultNewWords = collections.OrderedDict()
        expectedResult = [expectedResultKnownWords, expectedResultNewWords]

        self.assertEqual(expectedResult, actualResult)
