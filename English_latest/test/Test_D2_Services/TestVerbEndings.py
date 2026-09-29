from unittest import TestCase

from Core import TranscriptionComposer

englishVocabulary_dict = {

    "work": "[wɜːk]", "read": "[riːd]", "see": "[siː]",
    "pass": "[pɑːs]", "dress": "[dres]", "teach": "[tiːʧ]",
    "wash": "[wɔʃ]", "fix": "[fɪks]", "rise": "[raɪz]",
    "place": "[pleɪs]", "change": "[ʧeɪnʤ]", "study": "['stʌdɪ]",
    "copy": "['kɔpɪ]", "play": "[pleɪ]", "buy": "[baɪ]",
    "go": "[goʊ]",

    "append": "[ə'pend]", "want": "[wɔnt]", "talk": "[tɔːk]", "employ": "[ɪm'plɔɪ]", "stop": "[stɔp]", "top": "[tɔp]",
    "play": "[pleɪ]", "mix": "[mɪks]", "prefer": "[prɪ'fɜː]", "enter": "['entə]", "create": "[krɪ'eɪt]",
    "live": "[lɪv]", "try": "[traɪ]",

    "be": "[biː]", "cry": "[kraɪ]", "have": "[hæv]", "swim": "[swɪm]", "try": "[traɪ]", "break": "[breɪk]",
    "finish": "['fɪnɪʃ]", "crouch": "[krauʧ]", "make": "[meɪk]", "take": "[teɪk]", "forgive": "[fə'gɪv]",
    "write": "[raɪt]", "agree": "[ə'griː]", "free": "[friː]", "pee": "[piː]", "fee": "[fiː]", "die": "[daɪ]",
    "lie": "[laɪ]", "tie": "[taɪ]", "carry": "['kærɪ]", "study": "['stʌdɪ]", "play": "[pleɪ]", "try": "[traɪ]",
    "say": "[seɪ]", "worry": "['wʌrɪ]", "get": "[get]", "hit": "[hɪt]", "run": "[rʌn]", "occur": "[ə'kɜː]",
    "refer": "[rɪ'fɜː]", "begin": "[bɪ'gɪn]", "stop": "[stɔp]", "forget": "[fə'get]", "open": "['oʊp(ə)n]",
    "order": "['ɔːdə]", "remember": "[rɪ'membə]", "feel": "[fiːl]", "cool": "[kuːl]", "read": "[riːd]",
    "mix": "[mɪks]", "relax": "[rɪ'læks]", "tax": "[tæks]", "snow": "[snoʊ]", "blow": "[bloʊ]", "show": "[ʃoʊ]",
    "signal": "['sɪgn(ə)l]", "travel": "['træv(ə)l]", "cancel": "['kæns(ə)l]", "signal": "['sɪgn(ə)l]",
    "travel": "['træv(ə)l]", "cancel": "['kæns(ə)l]", "compel": "[kəm'pel]", "rebel": "['reb(ə)l]",
    "compel": "[kəm'pel]", "rebel": "['reb(ə)l]", "traffic": "['træfɪk]", "mimic": "['mɪmɪk]", "panic": "['pænɪk]",
    "meet": "[miːt]"
}


class TestVerbEndings(TestCase):

    def test_presentSimpleForms(self):
        words = ["works", "reads", "sees", "passes", "dresses", "teaches", "washes",
                 "fixes", "rises", "places", "changes", "studies", "copies", "plays", "buys", "goes"]
        expected_results = ["[wɜːks]", "[riːdz]", "[siːz]", "['pɑːsɪz]", "['dresɪz]", "['tiːʧɪz]", "['wɔʃɪz]",
                            "['fɪksɪz]", "['raɪzɪz]", "['pleɪsɪz]", "['ʧeɪnʤɪz]", "['stʌdɪz]", "['kɔpɪz]", "[pleɪz]",
                            "[baɪz]", "[goʊz]"]
        words_lemmas = ["work", "read", "see", "pass", "dress", "teach", "wash", "fix", "rise", "place", "change",
                        "study", "copy", "play", "buy", "go"]
        for word, word_lemma, expected_result in zip(words, words_lemmas, expected_results):
            unbracketed_result = TranscriptionComposer.compose_verb_transcription(word, word_lemma,
                                                                                  englishVocabulary_dict[word_lemma])
            actual_result = "[{0}]".format(unbracketed_result.strip())
            self.assertEqual(expected_result, actual_result)

    def test_pastSimple_and_pastParticiple_Forms(self):

        # Глаголы, транскрипция которых оканчивается на звуки [d] и [t]
        words = ["appended", "wanted"]
        expected_results = ["[ə'pendɪd]", "['wɔntɪd]"]
        words_lemmas = ["append", "want"]
        for word, word_lemma, expected_result in zip(words, words_lemmas, expected_results):
            unbracketed_result = TranscriptionComposer.compose_verb_transcription(word, word_lemma,
                                                                                  englishVocabulary_dict[word_lemma])
            actual_result = "[{0}]".format(unbracketed_result.strip())
            self.assertEqual(expected_result, actual_result)

        words = ["talked", "employed", "stopped", "topped", "played", "mixed", "preferred", "entered", "created",
                 "lived", "tried"]
        expected_results = ["[tɔːkt]", "[ɪm'plɔɪd]", "[stɔpt]", "[tɔpt]", "[pleɪd]", "[mɪkst]", "[prɪ'fɜːd]",
                            "['entəd]", "[krɪ'eɪtɪd]", "[lɪvd]", "[traɪd]"]
        words_lemmas = ["talk", "employ", "stop", "top", "play", "mix", "prefer", "enter", "create", "live", "try"]
        for word, word_lemma, expected_result in zip(words, words_lemmas, expected_results):
            unbracketed_result = TranscriptionComposer.compose_verb_transcription(word, word_lemma,
                                                                                  englishVocabulary_dict[word_lemma])
            actual_result = "[{0}]".format(unbracketed_result.strip())
            self.assertEqual(expected_result, actual_result)

    def test_participleI_forms(self):
        words = ["being", "crying", "having", "swimming", "trying", "breaking", "finishing", "crouching", "making",
                 "taking", "forgiving", "writing", "agreeing", "freeing", "peeing", "feeing", "dying", "lying",
                 "tying", "carrying", "studying", "playing", "trying", "saying", "worrying", "getting", "hitting",
                 "running", "occurring", "referring", "beginning", "stopping", "forgetting", "opening", "ordering",
                 "remembering", "feeling", "cooling", "reading", "mixing", "relaxing", "taxing", "snowing",
                 "blowing", "showing", "signalling", "travelling", "cancelling", "signaling", "traveling", "canceling",
                 "compelling", "rebelling", "compelling", "rebelling", "trafficking", "mimicking", "panicking",
                 "meeting"]

        expected_results = ["['biːɪŋ]", "['kraɪɪŋ]", "['hævɪŋ]", "['swɪmɪŋ]", "['traɪɪŋ]", "['breɪkɪŋ]", "['fɪnɪʃɪŋ]",
                            "['krauʧɪŋ]", "['meɪkɪŋ]", "['teɪkɪŋ]", "[fə'gɪvɪŋ]", "['raɪtɪŋ]", "[ə'griːɪŋ]",
                            "['friːɪŋ]", "['piːɪŋ]", "['fiːɪŋ]", "['daɪɪŋ]", "['laɪɪŋ]", "['taɪɪŋ]", "['kærɪɪŋ]",
                            "['stʌdɪɪŋ]", "['pleɪɪŋ]", "['traɪɪŋ]", "['seɪɪŋ]", "['wʌrɪɪŋ]", "['getɪŋ]", "['hɪtɪŋ]",
                            "['rʌnɪŋ]", "[ə'kɜːɪŋ]", "[rɪ'fɜːɪŋ]", "[bɪ'gɪnɪŋ]", "['stɔpɪŋ]", "[fə'getɪŋ]",
                            "['oʊp(ə)nɪŋ]", "['ɔːdəɪŋ]", "[rɪ'membəɪŋ]", "['fiːlɪŋ]", "['kuːlɪŋ]", "['riːdɪŋ]",
                            "['mɪksɪŋ]", "[rɪ'læksɪŋ]", "['tæksɪŋ]", "['snoʊɪŋ]", "['bloʊɪŋ]", "['ʃoʊɪŋ]",
                            "['sɪgn(ə)lɪŋ]", "['træv(ə)lɪŋ]", "['kæns(ə)lɪŋ]", "['sɪgn(ə)lɪŋ]", "['træv(ə)lɪŋ]",
                            "['kæns(ə)lɪŋ]", "[kəm'pelɪŋ]", "['reb(ə)lɪŋ]", "[kəm'pelɪŋ]", "['reb(ə)lɪŋ]",
                            "['træfɪkɪŋ]", "['mɪmɪkɪŋ]", "['pænɪkɪŋ]", "['miːtɪŋ]"]

        words_lemmas = ["be", "cry", "have", "swim", "try", "break", "finish", "crouch", "make", "take", "forgive",
                        "write", "agree", "free", "pee", "fee", "die", "lie", "tie", "carry", "study", "play", "try",
                        "say",
                        "worry", "get", "hit", "run", "occur", "refer", "begin", "stop", "forget", "open", "order",
                        "remember",
                        "feel", "cool", "read", "mix", "relax", "tax", "snow", "blow", "show", "signal", "travel",
                        "cancel",
                        "signal", "travel", "cancel", "compel", "rebel", "compel", "rebel", "traffic", "mimic", "panic",
                        "meet"]

        for word, word_lemma, expected_result in zip(words, words_lemmas, expected_results):
            unbracketed_result = TranscriptionComposer.compose_verb_transcription(word, word_lemma,
                                                                                  englishVocabulary_dict[word_lemma])
            actual_result = "[{0}]".format(unbracketed_result.strip())
            self.assertEqual(expected_result, actual_result)
