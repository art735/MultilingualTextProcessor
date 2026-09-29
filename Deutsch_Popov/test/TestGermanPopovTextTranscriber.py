from unittest import TestCase

from GermanPopovTextTranscriber import GermanPopovTextTranscriber


class TestWiktionaryToExcelService(TestCase):

    def setUp(self):
        self.germanPopovTextTranscriber = GermanPopovTextTranscriber()

    def test_preprocessBeforeTranscribing(self):
        text = 'DM 10'
        expected_result = '10 Mark'
        actual_result = self.germanPopovTextTranscriber.preprocess_before_transcribing(text)
        self.assertEqual(expected_result, actual_result)

        text = 'DM 10,-'
        expected_result = '10 Mark'
        actual_result = self.germanPopovTextTranscriber.preprocess_before_transcribing(text)
        self.assertEqual(expected_result, actual_result)

        text = 'DM 10,50'
        expected_result = '10 Mark 50'
        actual_result = self.germanPopovTextTranscriber.preprocess_before_transcribing(text)
        self.assertEqual(expected_result, actual_result)

        text = 'DM 10,50'
        expected_result = '10 Mark 50'
        actual_result = self.germanPopovTextTranscriber.preprocess_before_transcribing(text)
        self.assertEqual(expected_result, actual_result)

        # Проверить, что число парсится только перед DM и не парсится в остальных случаях.
        text = 'Es 12 hat 12,- DM 10,50 gekostet 12,99.'
        expected_result = 'Es 12 hat 12,- 10 Mark 50 gekostet 12,99.'
        actual_result = self.germanPopovTextTranscriber.preprocess_before_transcribing(text)
        self.assertEqual(expected_result, actual_result)
