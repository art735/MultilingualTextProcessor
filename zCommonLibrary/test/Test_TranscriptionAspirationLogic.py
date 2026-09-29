from unittest import TestCase

from TranscriptionAspirationService import TranscriptionAspirationService


class Test_TranscriptionAspirationLogic(TestCase):

    def setUp(self):
        self.transcriptionAspirationService = TranscriptionAspirationService()

    def test1_aspirationInNonAccentedSyllables_positiveScenarios(self):
        ########## Test [ptk] before vowels are aspired ##########

        # test "p" before vowel is aspired
        input_str = "[pɪŋk]"
        expected_result = "[pʰɪŋk]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)

        # test "t" before vowel is aspired
        input_str = "[tu]"
        expected_result = "[tʰu]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)

        # test "k" before vowel is aspired
        input_str = "[kæt]"
        expected_result = "[kʰæt]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)

        # test several words in a single transcription are properly aspired
        input_str = "[pɪŋk tu kæt]"
        expected_result = "[pʰɪŋk tʰu kʰæt]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)

    def test2_aspirationInNonAccentedSyllables_negativeScenarios(self):
        ########## Test [ptk] before consonants are NOT aspired ##########

        # test "p" before consonant is not aspired
        input_str = "[præŋk]"
        expected_result = "[præŋk]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)

        # test "t" before consonant is not aspired
        input_str = "[trɪk]"
        expected_result = "[trɪk]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)

        # test "k" before consonant is not aspired
        input_str = "[klaud]"
        expected_result = "[klaud]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)

        # test several words in a single transcription are NOT aspired
        input_str = "[præŋk trɪk klaud]"
        expected_result = "[præŋk trɪk klaud]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)

        # TODO: спорный момент, не понятно должна быть аспирация или нет. Пока нет...
        # PROS: [t] стоит (1) перед гласной и (2) слог ударный
        # CONS: [t] не является первой буквой слога, т. е. не стоит в начале слога
        input_str = "[stænd]"
        expected_result = "[stænd]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)

    def test3_aspirationInAccentedSyllables_positiveScenarios(self):
        # test "p" before vowel is aspired
        input_str = "['pʌpi]"  # stress on the 1st syllable
        expected_result = "['pʰʌpi]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)

        input_str = "[ə'pend]"  # stress on the 2nd syllable
        expected_result = "[ə'pʰend]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)

        # test "t" before vowel is aspired
        input_str = "['telɪfəun]"  # stress on the 1st syllable
        expected_result = "['tʰelɪfəun]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)

        input_str = "[ə'tæk]"  # stress on the 2nd syllable
        expected_result = "[ə'tʰæk]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)

        # test "k" before vowel is aspired
        input_str = "['kɔli]"  # stress on the 1st syllable
        expected_result = "['kʰɔli]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)

        input_str = "[ə'kɔːd]"  # stress on the 2nd syllable
        expected_result = "[ə'kʰɔːd]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)

        # test several words in a single transcription are properly aspired
        input_str = "['pʌpi ə'pend 'telɪfəun ə'tæk 'kɔli ə'kɔːd]"
        expected_result = "['pʰʌpi ə'pʰend 'tʰelɪfəun ə'tʰæk 'kʰɔli ə'kʰɔːd]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)

    def test4_aspirationInAccentedSyllables_negativeScenarios(self):
        # test "p" before consonant is NOT aspired
        input_str = "['praɪvɪt]"  # stress on the 1st syllable
        expected_result = "['praɪvɪt]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)

        input_str = "[ə'prəuʧ]"  # stress on the 2nd syllable
        expected_result = "[ə'prəuʧ]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)

        # test "t" before consonant is NOT aspired
        input_str = "['treɪnɪŋ]"  # stress on the 1st syllable
        expected_result = "['treɪnɪŋ]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)

        input_str = "[ɪn'trɪnzɪk]"  # stress on the 2nd syllable
        expected_result = "[ɪn'trɪnzɪk]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)

        # test "k" before consonant is NOT aspired
        input_str = "['klɔzɪt]"  # stress on the 1st syllable
        expected_result = "['klɔzɪt]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)

        input_str = "[rɪ'kleɪm]"  # stress on the 2nd syllable
        expected_result = "[rɪ'kleɪm]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)

        # test several words in a single transcription are NOT aspired
        input_str = "['praɪvɪt ə'prəuʧ 'treɪnɪŋ ɪn'trɪnzɪk 'klɔzɪt rɪ'kleɪm]"
        expected_result = "['praɪvɪt ə'prəuʧ 'treɪnɪŋ ɪn'trɪnzɪk 'klɔzɪt rɪ'kleɪm]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)

    def test5_aspirationInSyllablesWithDoubleAccent_positiveScenarios(self):
        # test "p" is aspired in both accented syllables
        input_str = "[ˌpɒlɪˈpɛərɪəm]"
        expected_result = "[ˌpʰɒlɪˈpʰɛərɪəm]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)

        input_str = "[ˈpɒlɪˌpɛərɪəm]"  # artificially swapped accents for testing purposes only
        expected_result = "[ˈpʰɒlɪˌpʰɛərɪəm]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)

        # test "t" is aspired in both accented syllables
        input_str = "[ˈtɛlɪˌtɛkst]"
        expected_result = "[ˈtʰɛlɪˌtʰɛkst]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)

        input_str = "[ˌtɛlɪˈtɛkst]"  # artificially swapped accents for testing purposes only
        expected_result = "[ˌtʰɛlɪˈtʰɛkst]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)

        # test "k" is aspired in both accented syllables
        input_str = "[ˌkəʊˈkæptɪn]"
        expected_result = "[ˌkʰəʊˈkʰæptɪn]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)

        input_str = "[ˈkəʊˌkæptɪn]"  # artificially swapped accents for testing purposes only
        expected_result = "[ˈkʰəʊˌkʰæptɪn]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)

    def test6(self):
        # 1. Слоги со звуком [p]
        # 1.1) Проверяем, что аспирируется только ударный слог при наличии такого же безударного слога
        input_str = "[per'petuum]"
        expected_result = "[per'pʰetuum]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)
        # 1.2) Проверяем, что аспирируются оба ударных слога
        input_str = "[ˌper'petuum]"
        expected_result = "[ˌpʰer'pʰetuum]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)

        # 2. Слоги со звуком [t]
        # 2.1) Проверяем, что аспирируется только ударный слог при наличии такого же безударного слога
        input_str = "[test'test]"
        expected_result = "[test'tʰest]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)
        # 2.2) Проверяем, что аспирируются оба ударных слога
        input_str = "[ˌtʰest'test]"
        expected_result = "[ˌtʰest'tʰest]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)

        # 3. Слоги со звуком [k]
        # 3.1) Проверяем, что аспирируется только ударный слог при наличии такого же безударного слога
        input_str = "[ka'ka]"
        expected_result = "[ka'kʰa]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)
        # 3.2) Проверяем, что аспирируются оба ударных слога
        input_str = "[ˌkʰa'ka]"
        expected_result = "[ˌkʰa'kʰa]"
        actual_result = self.transcriptionAspirationService.aspirate(input_str)
        self.assertEqual(expected_result, actual_result)
