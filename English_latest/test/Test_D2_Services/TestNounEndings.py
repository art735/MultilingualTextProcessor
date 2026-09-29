from unittest import TestCase

from Core import TranscriptionComposer

englishVocabulary_dict = {
    "room": "[ruːm]", "pencil": "['pens(ə)l]", "chair": "[ʧeə]",
    "shoe": "[ʃuː]",
    "book": "[buk]", "map": "[mæp]",
    "bus": "[bʌs]", "class": "[klɑːs]", "dish": "[dɪʃ]", "inch": "[ɪnʧ]", "box": "[bɔks]",
    "horse": "[hɔːs]", "place": "[pleɪs]", "prize": "[praɪz]", "judge": "['ʤʌʤ]",
    "city": "['sɪtɪ]", "army": "['ɑːmɪ]", "factory": "['fækt(ə)rɪ]",
    "day": "[deɪ]", "boy": "[bɔɪ]", "toy": "[tɔɪ]", "key": "[kiː]",
    "cargo": "['kɑːgoʊ]", "hero": "['hɪəroʊ]", "tomato": "[tə'mɑːtoʊ]",
    "piano": "[pɪ'ænoʊ]", "photo": "['foʊtoʊ]",
    "leaf": "[liːf]", "wolf": "[wulf]", "knife": "[naɪf]", "wife": "[waɪf]",
    "chief": "[ʧiːf]", "handkerchief": "['hæŋkəʧiːf]", "roof": "[ruːf]", "safe": "[seɪf]", "wharf": "[wɔːf]"
}


class TestNounEndings(TestCase):

    # Тест мн. ч. 'обычных' существительных (которые не имеют специальных окончаний)
    def test1(self):

        # Существительные, которые в ед.ч. оканчиваются на звонкий согласный
        words = ["rooms", "pencils", "chairs"]
        expected_results = ["[ruːmz]", "['pens(ə)lz]", "[ʧeəz]"]
        words_lemmas = ["room", "pencil", "chair"]
        for word, word_lemma, expected_result in zip(words, words_lemmas, expected_results):
            unbracketed_result = TranscriptionComposer.compose_noun_transcription(word, word_lemma,
                                                                                  englishVocabulary_dict[word_lemma])
            actual_result = "[{0}]".format(unbracketed_result.strip())
            self.assertEqual(expected_result, actual_result)

        # Существительные, которые в ед.ч. оканчиваются на гласный
        words = ["shoes"]
        expected_results = ["[ʃuːz]"]
        words_lemmas = ["shoe"]
        for word, word_lemma, expected_result in zip(words, words_lemmas, expected_results):
            unbracketed_result = TranscriptionComposer.compose_noun_transcription(word, word_lemma,
                                                                                  englishVocabulary_dict[word_lemma])
            actual_result = "[{0}]".format(unbracketed_result.strip())
            self.assertEqual(expected_result, actual_result)

        # Существительные, которые в ед.ч. оканчиваются на глухой согласный
        words = ["books", "maps"]
        expected_results = ["[buks]", "[mæps]"]
        words_lemmas = ["book", "map"]
        for word, word_lemma, expected_result in zip(words, words_lemmas, expected_results):
            unbracketed_result = TranscriptionComposer.compose_noun_transcription(word, word_lemma,
                                                                                  englishVocabulary_dict[word_lemma])
            actual_result = "[{0}]".format(unbracketed_result.strip())
            self.assertEqual(expected_result, actual_result)

    # Тест мн. ч. существительных, оканчивающихся в ед. ч. на -s, -ss, -sh, -ch, x
    def test2(self):
        words = ["buses", "classes", "dishes", "inches", "boxes"]
        expected_results = ["['bʌsɪz]", "['klɑːsɪz]", "['dɪʃɪz]", "['ɪnʧɪz]", "['bɔksɪz]"]
        words_lemmas = ["bus", "class", "dish", "inch", "box"]

        for word, word_lemma, expected_result in zip(words, words_lemmas, expected_results):
            unbracketed_result = TranscriptionComposer.compose_noun_transcription(word, word_lemma,
                                                                                  englishVocabulary_dict[word_lemma])
            actual_result = "[{0}]".format(unbracketed_result.strip())
            self.assertEqual(expected_result, actual_result)

    # Тест мн. ч. существительных, оканчивающихся в ед. ч. на -se, -ce, -ze, -ge
    def test3(self):
        words = ["horses", "places", "prizes", "judges"]
        expected_results = ["['hɔːsɪz]", "['pleɪsɪz]", "['praɪzɪz]", "['ʤʌʤɪz]"]
        words_lemmas = ["horse", "place", "prize", "judge"]
        for word, word_lemma, expected_result in zip(words, words_lemmas, expected_results):
            unbracketed_result = TranscriptionComposer.compose_noun_transcription(word, word_lemma,
                                                                                  englishVocabulary_dict[word_lemma])
            actual_result = "[{0}]".format(unbracketed_result.strip())
            self.assertEqual(expected_result, actual_result)

    # Тест мн. ч. существительных, оканчивающихся в ед. ч. на -y
    def test4(self):

        # Существительные, которые в ед.ч. оканчиваются на согласную + y
        words = ["cities", "armies", "factories"]
        expected_results = ["['sɪtɪz]", "['ɑːmɪz]", "['fækt(ə)rɪz]"]
        words_lemmas = ["city", "army", "factory"]
        for word, word_lemma, expected_result in zip(words, words_lemmas, expected_results):
            unbracketed_result = TranscriptionComposer.compose_noun_transcription(word, word_lemma,
                                                                                  englishVocabulary_dict[word_lemma])
            actual_result = "[{0}]".format(unbracketed_result.strip())
            self.assertEqual(expected_result, actual_result)

        # Существительные, которые в ед.ч. оканчиваются на гласную + y
        words = ["days", "boys", "toys", "keys"]
        expected_results = ["[deɪz]", "[bɔɪz]", "[tɔɪz]", "[kiːz]"]
        words_lemmas = ["day", "boy", "toy", "key"]
        for word, word_lemma, expected_result in zip(words, words_lemmas, expected_results):
            unbracketed_result = TranscriptionComposer.compose_noun_transcription(word, word_lemma,
                                                                                  englishVocabulary_dict[word_lemma])
            actual_result = "[{0}]".format(unbracketed_result.strip())
            self.assertEqual(expected_result, actual_result)

    # Тест мн. ч. существительных, оканчивающихся в ед. ч. на -o
    def test5(self):

        # -o + es
        words = ["cargoes", "heroes", "tomatoes"]
        expected_results = ["['kɑːgoʊz]", "['hɪəroʊz]", "[tə'mɑːtoʊz]"]
        words_lemmas = ["cargo", "hero", "tomato"]
        for word, word_lemma, expected_result in zip(words, words_lemmas, expected_results):
            unbracketed_result = TranscriptionComposer.compose_noun_transcription(word, word_lemma,
                                                                                  englishVocabulary_dict[word_lemma])
            actual_result = "[{0}]".format(unbracketed_result.strip())
            self.assertEqual(expected_result, actual_result)

        # -o + s
        words = ["pianos", "photos"]
        expected_results = ["[pɪ'ænoʊz]", "['foʊtoʊz]"]
        words_lemmas = ["piano", "photo"]
        for word, word_lemma, expected_result in zip(words, words_lemmas, expected_results):
            unbracketed_result = TranscriptionComposer.compose_noun_transcription(word, word_lemma,
                                                                                  englishVocabulary_dict[word_lemma])
            actual_result = "[{0}]".format(unbracketed_result.strip())
            self.assertEqual(expected_result, actual_result)

    # Тест мн. ч. существительных, оканчивающихся в ед. ч. на -f
    def test6(self):

        # -f + es
        words = ["leaves", "wolves"]
        expected_results = ["[liːvz]", "[wulvz]"]
        words_lemmas = ["leaf", "wolf"]
        for word, word_lemma, expected_result in zip(words, words_lemmas, expected_results):
            unbracketed_result = TranscriptionComposer.compose_noun_transcription(word, word_lemma,
                                                                                  englishVocabulary_dict[word_lemma])
            actual_result = "[{0}]".format(unbracketed_result.strip())
            self.assertEqual(expected_result, actual_result)

        # -fe + es
        words = ["knives", "wives"]
        expected_results = ["[naɪvz]", "[waɪvz]"]
        words_lemmas = ["knife", "wife"]
        for word, word_lemma, expected_result in zip(words, words_lemmas, expected_results):
            unbracketed_result = TranscriptionComposer.compose_noun_transcription(word, word_lemma,
                                                                                  englishVocabulary_dict[word_lemma])
            actual_result = "[{0}]".format(unbracketed_result.strip())
            self.assertEqual(expected_result, actual_result)

        # -f(e) + s
        words = ["chiefs", "handkerchiefs", "roofs", "safes"]
        expected_results = ["[ʧiːfs]", "['hæŋkəʧiːfs]", "[ruːfs]", "[seɪfs]"]
        words_lemmas = ["chief", "handkerchief", "roof", "safe"]
        for word, word_lemma, expected_result in zip(words, words_lemmas, expected_results):
            unbracketed_result = TranscriptionComposer.compose_noun_transcription(word, word_lemma,
                                                                                  englishVocabulary_dict[word_lemma])
            actual_result = "[{0}]".format(unbracketed_result.strip())
            self.assertEqual(expected_result, actual_result)

        # -f(e) + s (слова с 2-мя вариантами мн. ч.)
        words = ["wharfs", "wharves"]
        expected_results = ["[wɔːfs]", "[wɔːvz]"]
        words_lemmas = ["wharf", "wharf"]
        for word, word_lemma, expected_result in zip(words, words_lemmas, expected_results):
            unbracketed_result = TranscriptionComposer.compose_noun_transcription(word, word_lemma,
                                                                                  englishVocabulary_dict[word_lemma])
            actual_result = "[{0}]".format(unbracketed_result.strip())
            self.assertEqual(expected_result, actual_result)
