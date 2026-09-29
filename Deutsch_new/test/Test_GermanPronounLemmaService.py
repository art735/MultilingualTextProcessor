from unittest import TestCase

from GermanPronounLemmaService import GermanPronounLemmaService


class Test_GermanPronounLemmaService(TestCase):

    def setUp(self):
        # self.dashedArticledNounsComposer = DashedArticledNounsComposer()
        self.germanPronounLemmaService = GermanPronounLemmaService()

    def test_personal_pronouns(self):
        lemma = ''

        token = 'meiner'
        morph_dict = {
            "Case": ["Gen"],
            "Number": ["Sing"],
            "Person": ["1"],
            "PronType": ["Prs"]
        }
        expected_result = self.germanPronounLemmaService.get_pronoun_lemma(token, lemma, morph_dict)
        actual_result = "ich"
        self.assertEqual(expected_result, actual_result)

        token = 'unser'
        morph_dict = {
            "Case": ["Gen"],
            "Number": ["Plur"],
            "Person": ["1"],
            "PronType": ["Prs"]
        }
        expected_result = self.germanPronounLemmaService.get_pronoun_lemma(token, lemma, morph_dict)
        actual_result = "wir"
        self.assertEqual(expected_result, actual_result)

        token = 'dir'
        morph_dict = {
            "Case": ["Dat"],
            "Number": ["Sing"],
            "Person": ["2"],
            "PronType": ["Prs"]
        }
        expected_result = self.germanPronounLemmaService.get_pronoun_lemma(token, lemma, morph_dict)
        actual_result = "du"
        self.assertEqual(expected_result, actual_result)

        token = 'euch'
        morph_dict = {
            "Case": ["Dat"],
            "Number": ["Plur"],
            "Person": ["2"],
            "PronType": ["Prs"]
        }
        expected_result = self.germanPronounLemmaService.get_pronoun_lemma(token, lemma, morph_dict)
        actual_result = "ihr"
        self.assertEqual(expected_result, actual_result)

        token = 'ihn'
        morph_dict = {
            "Case": ["Acc"],
            "Number": ["Sing"],
            "Person": ["3"],
            "Gender": ["Masc"],
            "PronType": ["Prs"]
        }
        expected_result = self.germanPronounLemmaService.get_pronoun_lemma(token, lemma, morph_dict)
        actual_result = "er"
        self.assertEqual(expected_result, actual_result)

        token = 'sie'
        morph_dict = {
            "Case": ["Acc"],
            "Number": ["Plur"],
            "Person": ["3"],
            "PronType": ["Prs"]
        }
        expected_result = self.germanPronounLemmaService.get_pronoun_lemma(token, lemma, morph_dict)
        actual_result = "sie"
        self.assertEqual(expected_result, actual_result)
