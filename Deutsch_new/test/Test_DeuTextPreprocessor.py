from unittest import TestCase

from DeuTextPreprocessor import DeuTextPreprocessor


class Test_DeuTextPreprocessor(TestCase):

    def setUp(self):
        # self.dashedArticledNounsComposer = DashedArticledNounsComposer()
        # self.pronounService = PronounService()
        self.deuTextPreprocessor = DeuTextPreprocessor()

    def test_preprocess(self):
        input_str = "1Das ist ein Test-Text mit deutschen Wörtern wie Fußgängerübergang und E-Mail2."
        expected_result = "1 Das ist ein Test-Text mit deutschen Wörtern wie Fußgängerübergang und E-Mail 2."
        actual_result = self.deuTextPreprocessor.preprocess(input_str)
        self.assertEquals(expected_result, actual_result)

        input_str = "Wo geht ’ s hier bitte zur Autobahn?"
        expected_result = "Wo geht ’s hier bitte zur Autobahn ?"
        actual_result = self.deuTextPreprocessor.preprocess(input_str)
        self.assertEquals(expected_result, actual_result)

        input_str = "Wo geht ’ s?"
        expected_result = "Wo geht ’s ?"
        actual_result = self.deuTextPreprocessor.preprocess(input_str)
        self.assertEquals(expected_result, actual_result)

        input_str = "Wo geht ’ s"
        expected_result = "Wo geht ’s"
        actual_result = self.deuTextPreprocessor.preprocess(input_str)
        self.assertEquals(expected_result, actual_result)

        input_str = "Wo geht ' s hier bitte zur Autobahn?"
        expected_result = "Wo geht 's hier bitte zur Autobahn ?"
        actual_result = self.deuTextPreprocessor.preprocess(input_str)
        self.assertEquals(expected_result, actual_result)

        input_str = "Wo geht ' s?"
        expected_result = "Wo geht 's ?"
        actual_result = self.deuTextPreprocessor.preprocess(input_str)
        self.assertEquals(expected_result, actual_result)

        input_str = "Wo geht ' s"
        expected_result = "Wo geht 's"
        actual_result = self.deuTextPreprocessor.preprocess(input_str)
        self.assertEquals(expected_result, actual_result)

        input_str = "Ich (will)"
        expected_result = "Ich ( will )"
        actual_result = self.deuTextPreprocessor.preprocess(input_str)
        self.assertEquals(expected_result, actual_result)

        input_str = "Ich ((will))"
        expected_result = "Ich ( ( will ) )"
        actual_result = self.deuTextPreprocessor.preprocess(input_str)
        self.assertEquals(expected_result, actual_result)

        input_str = "Ich (will-(das))"
        expected_result = "Ich ( will-(das) )"
        actual_result = self.deuTextPreprocessor.preprocess(input_str)
        self.assertEquals(expected_result, actual_result)

        input_str = "Ich (((will-(((das))))))"
        expected_result = "Ich ( ( ( will-(((das))) ) ) )"
        actual_result = self.deuTextPreprocessor.preprocess(input_str)
        self.assertEquals(expected_result, actual_result)

        input_str = "Ich kaufe (Auto)mobile"
        expected_result = "Ich kaufe (Auto)mobile"
        actual_result = self.deuTextPreprocessor.preprocess(input_str)
        self.assertEquals(expected_result, actual_result)

        input_str = "Ich kaufe ((Auto)mobile)"
        expected_result = "Ich kaufe ( (Auto)mobile )"
        actual_result = self.deuTextPreprocessor.preprocess(input_str)
        self.assertEquals(expected_result, actual_result)

        input_str = "Ich kaufe Auto(mobile)"
        expected_result = "Ich kaufe Auto(mobile)"
        actual_result = self.deuTextPreprocessor.preprocess(input_str)
        self.assertEquals(expected_result, actual_result)

        input_str = "Ich kaufe (Auto(mobile))"
        expected_result = "Ich kaufe ( Auto(mobile) )"
        actual_result = self.deuTextPreprocessor.preprocess(input_str)
        self.assertEquals(expected_result, actual_result)
