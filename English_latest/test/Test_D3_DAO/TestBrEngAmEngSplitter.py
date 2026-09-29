from unittest import TestCase

import BrEngAmEngSplitter
from RepositoryItem import RepositoryItem


class TestBrEngAmEngSplitter(TestCase):

    # оба варианта написания (брит. и амер.) имеют одну и ту же транскрипцию
    def test1(self):
        expected_result = dict()

        word = "grey (BrE)\ngray (AmE)"

        # prepare 1st part of ER data
        word_BrE = "grey"
        transcription_BrE = "[greɪ]"
        translation_BrE = "1) серый\n2) седой (о волосах)"
        morph_forms_BrE = [('k1', 'v1'), ('k2', 'v2')]
        record_BrE = RepositoryItem(word, transcription_BrE, translation_BrE)
        record_BrE.add_morphological_forms(morph_forms_BrE)
        expected_result[word_BrE] = record_BrE

        # prepare 2nd part of ER data
        word_AmE = "gray"
        transcription_AmE = "[greɪ]"
        translation_AmE = "1) серый\n2) седой (о волосах)"
        morph_forms_AmE = [('k1', 'v1'), ('k2', 'v2')]
        record_AmE = RepositoryItem(word, transcription_AmE, translation_AmE)
        record_AmE.add_morphological_forms(morph_forms_AmE)
        expected_result[word_AmE] = record_AmE

        # prepare AE data

        transcription = "[greɪ]"
        translation = "1) серый\n2) седой (о волосах)"
        test_morph_forms = [('k1', 'v1'), ('k2', 'v2')]
        test_record = RepositoryItem(word, transcription, translation)
        test_record.add_morphological_forms(test_morph_forms)

        actual_result = BrEngAmEngSplitter.split(test_record)

        for (k1, v1), (k2, v2) in zip(expected_result.items(), actual_result.items()):
            self.assertEqual(k1, k2)
            self.assertTrue(v1.compare_all_fields(v2))

    # оба варианта написания (брит. и амер.) имеют разные транкрипции
    def test2(self):
        expected_result = dict()

        word = "grey (BrE)\ngray (AmE)"

        # prepare 1st part of ER data
        word_BrE = "grey"
        transcription_BrE = "[greɪ_BR]"
        translation_BrE = "1) серый\n2) седой (о волосах)"
        morph_forms_BrE = [('k10', 'v10'), ('k20', 'v20')]
        record_BrE = RepositoryItem(word, transcription_BrE, translation_BrE)
        record_BrE.add_morphological_forms(morph_forms_BrE)
        expected_result[word_BrE] = record_BrE

        # prepare 2nd part of ER data
        word_AmE = "gray"
        transcription_AmE = "[greɪ_AM]"
        translation_AmE = "1) серый\n2) седой (о волосах)"
        morph_forms_AmE = [('k10', 'v10'), ('k20', 'v20')]
        record_AmE = RepositoryItem(word, transcription_AmE, translation_AmE)
        record_AmE.add_morphological_forms(morph_forms_AmE)
        expected_result[word_AmE] = record_AmE

        # prepare AE data
        transcription = "[greɪ_BR]\n[greɪ_AM]"
        translation = "1) серый\n2) седой (о волосах)"
        test_morph_forms = [('k10', 'v10'), ('k20', 'v20')]
        test_record = RepositoryItem(word, transcription, translation)
        test_record.add_morphological_forms(test_morph_forms)
        actual_result = BrEngAmEngSplitter.split(test_record)

        for (k1, v1), (k2, v2) in zip(expected_result.items(), actual_result.items()):
            self.assertEqual(k1, k2)
            self.assertTrue(v1.compare_all_fields(v2))
