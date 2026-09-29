from unittest import TestCase

from Core import TranscriptionComposer

englishVocabulary_dict = {
    "warm": "[wɔːm]", "hot": "[hɔt]", "fast": "[fɑːst]", "nice": "[naɪs]", "narrow": "['næroʊ]", "simple": "['sɪmpl]",
    "tender": "['tendə]", "happy": "['hæpi]", "severe": "[sɪ'vɪə]",

    "small": "[smɔːl]", "hard": "[hɑːd]", "big": "[bɪg]", "hot": "[hɔt]", "slow": "[sloʊ]",
    "low": "[loʊ]", "cute": "[kjuːt]", "pale": "[peɪl]", "late": "[leɪt]", "dry": "[draɪ]",
    "busy": "['bɪzi]", "gray": "[greɪ]",

    # Двусложные прилагательные на -ow, -le, -er, -y
    "crazy": "['kreɪzi]", "pretty": "['prɪti]", "quiet": "['kwaɪət]", "simple": "['sɪmpl]", "narrow": "['næroʊ]",

    # Исключения
    "good": "[gud]", "well": "[wel]", "bad": "[bæd]", "badly": "['bædli]", "many": "['meni]", "much": "[mʌʧ]",
    "little": "['lɪtl]", "far": "[fɑː]",

    "early": "['ɜːli]", "loudly": "['laudli]", "quickly": "['kwɪkli]", "slowly": "['sloʊli]"
}


class TestAdjectiveAdverbEndings(TestCase):

    def test1(self):
        word_tuples = [("warmer", "warmest"), ("hotter", "hottest"), ("faster", "fastest"), ("nicer", "nicest"),
                       ("narrower", "narrowest"), ("simpler", "simplest"), ("tenderer", "tenderest"),
                       ("happier", "happiest"), ("severer", "severest")]
        expected_result_tuples = [("['wɔːmə]", "['wɔːmɪst]"), ("['hɔtə]", "['hɔtɪst]"), ("['fɑːstə]", "['fɑːstɪst]"),
                                  ("['naɪsə]", "['naɪsɪst]"), ("['næroʊə]", "['næroʊɪst]"),
                                  ("['sɪmplə]", "['sɪmplɪst]"), ("['tendərə]", "['tendərɪst]"),
                                  ("['hæpiə]", "['hæpiɪst]"), ("[sɪ'vɪərə]", "[sɪ'vɪərɪst]")]
        words_lemmas = ["warm", "hot", "fast", "nice", "narrow", "simple", "tender", "happy", "severe"]
        for word_tuple, word_lemma, expected_result_tuple in zip(word_tuples, words_lemmas, expected_result_tuples):
            for word, expected_result in zip(word_tuple, expected_result_tuple):
                unbracketed_result = TranscriptionComposer.compose_adjective_adverb_transcription(word,
                                                                                                  englishVocabulary_dict[
                                                                                                      word_lemma])
                actual_result = "[{0}]".format(unbracketed_result.strip())
                self.assertEqual(expected_result, actual_result)

    # Односложные прилагательные и наречия
    def test2(self):
        word_tuples = [("smaller", "smallest"), ("harder", "hardest"), ("bigger", "biggest"), ("hotter", "hottest"),
                       ("slower", "slowest"), ("lower", "lowest"), ("cuter", "cutest"), ("paler", "palest"),
                       ("later", "latest"), ("drier", "driest"), ("busier", "busiest"), ("grayer", "grayest")]
        expected_result_tuples = [("['smɔːlə]", "['smɔːlɪst]"), ("['hɑːdə]", "['hɑːdɪst]"), ("['bɪgə]", "['bɪgɪst]"),
                                  ("['hɔtə]", "['hɔtɪst]"), ("['sloʊə]", "['sloʊɪst]"), ("['loʊə]", "['loʊɪst]"),
                                  ("['kjuːtə]", "['kjuːtɪst]"), ("['peɪlə]", "['peɪlɪst]"), ("['leɪtə]", "['leɪtɪst]"),
                                  ("['draɪə]", "['draɪɪst]"), ("['bɪziə]", "['bɪziɪst]"), ("['greɪə]", "['greɪɪst]")]
        words_lemmas = ["small", "hard", "big", "hot", "slow", "low", "cute", "pale", "late", "dry", "busy", "gray"]
        for word_tuple, word_lemma, expected_result_tuple in zip(word_tuples, words_lemmas, expected_result_tuples):
            for word, expected_result in zip(word_tuple, expected_result_tuple):
                unbracketed_result = TranscriptionComposer.compose_adjective_adverb_transcription(word,
                                                                                                  englishVocabulary_dict[
                                                                                                      word_lemma])
                actual_result = "[{0}]".format(unbracketed_result.strip())
                self.assertEqual(expected_result, actual_result)

    # Двусложные прилагательные на -ow, -le, -er, -y
    def test3(self):
        word_tuples = [("crazier", "craziest"), ("prettier", "prettiest"), ("quieter", "quietest"),
                       ("simpler", "simplest"), ("narrower", "narrowest")]

        expected_result_tuples = [("['kreɪziə]", "['kreɪziɪst]"), ("['prɪtiə]", "['prɪtiɪst]"),
                                  ("['kwaɪətə]", "['kwaɪətɪst]"), ("['sɪmplə]", "['sɪmplɪst]"),
                                  ("['næroʊə]", "['næroʊɪst]")]

        words_lemmas = ["crazy", "pretty", "quiet", "simple", "narrow"]
        for word_tuple, word_lemma, expected_result_tuple in zip(word_tuples, words_lemmas, expected_result_tuples):
            for word, expected_result in zip(word_tuple, expected_result_tuple):
                unbracketed_result = TranscriptionComposer.compose_adjective_adverb_transcription(word,
                                                                                                  englishVocabulary_dict[
                                                                                                      word_lemma])
                actual_result = "[{0}]".format(unbracketed_result.strip())
                self.assertEqual(expected_result, actual_result)

    # Исключения. Данный тест не нужен и неправилен. Тестируемая ситуация никогда не возникнет
    # Слова-исключения всегда явно добавляются в словарь и ситуация никогда не дойдёт до прибавления суффиксов.
    # def test4(self):
    #     word_tuples = [("better", "best"), ("better", "best"), ("worse", "worst"), ("worse", "worst"),
    #                    ("more", "most"), ("more", "most"), ("less", "least"), ("farther", "farthest"),
    #                    ("further", "furthest")]
    #
    #     expected_result_tuples = [("['betə]", "[best]"), ("['betə]", "[best]"), ("[wɜːs]", "[wɜːst]"),
    #                               ("[wɜːs]", "[wɜːst]"), ("[mɔː]", "[məust]"), ("[mɔː]", "[məust]"),
    #                               ("[les]", "[liːst]"), ("['fɑːðə]", "['fɑːðɪst]"), ("['fɜːðə]", "['fɜːðɪst]")]
    #
    #     words_lemmas = ["good", "well", "bad", "badly", "many", "much", "little", "far", "far"]
    #     for word_tuple, word_lemma, expected_result_tuple in zip(word_tuples, words_lemmas, expected_result_tuples):
    #         for word, expected_result in zip(word_tuple, expected_result_tuple):
    #             unbracketed_result = AdjectiveProcessor.compose_transcription(word, englishVocabulary_dict[word_lemma])
    #             actual_result = "[{0}]".format(unbracketed_result.strip())
    #             self.assertEqual(expected_result, actual_result)

    def test5(self):
        word_tuples = [("earlier", "earliest"), ("loudlier", "loudliest"), ("quicker", "quickest"),
                       ("slower", "slowest")]

        expected_result_tuples = [("['ɜːliə]", "['ɜːliɪst]"), ("['laudliə]", "['laudliɪst]"),
                                  ("['kwɪkliə]", "['kwɪkliɪst]"), ("['sloʊliə]", "['sloʊliɪst]")]

        words_lemmas = ["early", "loudly", "quickly", "slowly"]
        for word_tuple, word_lemma, expected_result_tuple in zip(word_tuples, words_lemmas, expected_result_tuples):
            for word, expected_result in zip(word_tuple, expected_result_tuple):
                unbracketed_result = TranscriptionComposer.compose_adjective_adverb_transcription(word,
                                                                                                  englishVocabulary_dict[
                                                                                                      word_lemma])
                actual_result = "[{0}]".format(unbracketed_result.strip())
                self.assertEqual(expected_result, actual_result)
