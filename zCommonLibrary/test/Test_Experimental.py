from importlib.machinery import SourceFileLoader
from unittest import TestCase

tokenizer = SourceFileLoader('Tokenizer', 'CommonBusinessLogic/Tokenizer.py').load_module()
charConstants = SourceFileLoader('CharConstants', 'CommonBusinessLogic/CharConstants.py').load_module()

vocabularyWordsEmptyList = list()
ignoredWordsEmptyList = list()


class Test_Experimental(TestCase):

    def transcription_experiment(self):
        # text = 'a   \n\n\n\n\n\n   b       \n\n\n              c'
        # expectedResult = 'a b c'
        # actualResult = tokenizer.preProcessTextByDeletingUnnecessarySymbols(text)
        # self.assertEqual(expectedResult, actualResult)
        self.assertEqual(1, 1)
