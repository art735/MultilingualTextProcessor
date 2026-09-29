from unittest import TestCase

from Core import TranscriberCoreEngine
from RepositoryItem import RepositoryItem

# в словаре все слова должны быть с маленькой буквы (даже собственные имена существительные!)
englishVocabulary_dict = {
    # примеры притяжательных существительных из справочника Израилевича, Качаловой
    "girl": RepositoryItem("girl", "[gɜːl]", ""),
    "Jack".lower(): RepositoryItem("Jack", "[ʤæk]", ""),
    "horse": RepositoryItem("horse", "[hɔːs]", ""),
    "boy": RepositoryItem("boy", "[bɔɪ]", ""),
    "worker": RepositoryItem("worker", "['wɜːkə]", ""),
    "child": RepositoryItem("child", "[ʧaɪld]", "", [("children", "['ʧɪldr(ə)n]")]),
    "workman": RepositoryItem("workman", "['wɜːkmən]", "", [("workmen", "['wɜːkmən]")]),
    "commander-in-chief": RepositoryItem("commander-in-chief", "[kəˌmɑːndər ɪn 'tʃiːf]", ""),
    "brother-in-law": RepositoryItem("brother-in-law", "['brʌð(ə)(r)ɪnˌlɔː]", ""),
    "Helen".lower(): RepositoryItem("Helen", "['helən]", ""),
    "student": RepositoryItem("student", "['st(j)uːd(ə)nt]", ""),
    "Moscow".lower(): RepositoryItem("Moscow", "['mɔskəu]", ""),
    "Neva".lower(): RepositoryItem("Neva", "['neɪvə]", ""),

    # примеры притяжательных существительных с веб-странички https://grammarway.com/ru/possessive-case
    "Charles".lower(): RepositoryItem("Charles", "[ʧɑːlz]", ""),
    "man": RepositoryItem("man", "[mæn]", "", [("men", "[men]")]),
    "child": RepositoryItem("child", "[ʧaɪld]", "", [("children", "['ʧɪldr(ə)n]")]),
    "mum": RepositoryItem("mum", "[mʌm]", ""),
    "Jack".lower(): RepositoryItem("Jack", "[ʤæk]", ""),
    "Richard".lower(): RepositoryItem("Richard", "['rɪʧəd]", ""),
    "Tim".lower(): RepositoryItem("Tim", "[tɪm]", ""),
    "Kelly".lower(): RepositoryItem("Kelly", "['keli]", ""),
    "Shakespeare".lower(): RepositoryItem("Shakespeare", "['ʃeɪkspɪə]", ""),
    "Kate".lower(): RepositoryItem("Kate", "[keɪt]", ""),
    "Florida".lower(): RepositoryItem("Florida", "['flɔrɪdə]", ""),
    "God".lower(): RepositoryItem("God", "[gɔd]", ""),
    "Valentine".lower(): RepositoryItem("Valentine", "['væləntaɪn]", ""),
    "people": RepositoryItem("people", "['piːpl]", ""),
    "brother": RepositoryItem("brother", "['brʌðə]", ""),
    "brother-in-law": RepositoryItem("brother-in-law", "['brʌð(ə)(r)ɪnˌlɔː]", ""),
    "friend": RepositoryItem("friend", "[frend]", ""),
    "mother": RepositoryItem("mother", "['mʌðə]", ""),
    "great": RepositoryItem("great", "[greɪt]", ""),
    "dog": RepositoryItem("dog", "[dɔg]", ""),
    "player": RepositoryItem("player", "['pleɪə]", ""),
    "actress": RepositoryItem("actress", "['æktrəs]", ""),
    "James".lower(): RepositoryItem("James", "[ʤeɪmz]", ""),
    "appearance": RepositoryItem("appearance", "[ə'pɪər(ə)ns]", ""),
    "conscience": RepositoryItem("conscience", "['kɔnʃ(ə)ns]", ""),
    "goodness": RepositoryItem("goodness", "['gudnəs]", ""),
    "witness": RepositoryItem("witness", "['wɪtnəs]", ""),
    "father": RepositoryItem("father", "['fɑːðə]", ""),
    "baker": RepositoryItem("baker", "['beɪkə]", ""),
    "dentist": RepositoryItem("dentist", "['dentɪst]", ""),
    "company": RepositoryItem("company", "['kʌmpəni]", ""),
    "nation": RepositoryItem("nation", "['neɪʃ(ə)n]", ""),
    "ship": RepositoryItem("ship", "[ʃɪp]", ""),
    "plane": RepositoryItem("plane", "[pleɪn]", ""),
    "car": RepositoryItem("car", "[kɑː]", ""),
    "moon": RepositoryItem("moon", "[muːn]", ""),
    "sun": RepositoryItem("sun", "[sʌn]", ""),
    "forest": RepositoryItem("forest", "['fɔrɪst]", ""),
    "yesterday": RepositoryItem("yesterday", "['jestədeɪ]", ""),
    "month": RepositoryItem("month", "[mʌnθ]", ""),
    "cent": RepositoryItem("cent", "[sent]", ""),
    "dollar": RepositoryItem("dollar", "['dɔlə]", ""),
    "mile": RepositoryItem("mile", "['maɪl]", ""),
    "time": RepositoryItem("time", "[taɪm]", ""),
    "full-time": RepositoryItem("full-time", "[ˌful'taɪm]", ""),
    "stone": RepositoryItem("stone", "[stoʊn]", ""),
    "death": RepositoryItem("death", "[deθ]", ""),
    "mind": RepositoryItem("mind", "[maɪnd]", ""),
    "harm": RepositoryItem("harm", "[hɑːm]", ""),
    "one": RepositoryItem("one", "[wʌn]", ""),
    "one-third": RepositoryItem("one-third", "[wʌn θɜːd]", ""),
    "wit": RepositoryItem("wit", "[wɪt]", ""),
    "arm": RepositoryItem("arm", "[ɑːm]", ""),
    "finger": RepositoryItem("finger", "['fɪŋgə]", ""),
    "needle": RepositoryItem("needle", "['niːdl]", ""),
    "pin": RepositoryItem("pin", "[pɪn]", ""),
    "cow": RepositoryItem("cow", "[kau]", ""),
    "soldier": RepositoryItem("soldier", "['soʊlʤə]", ""),
    "sheep": RepositoryItem("sheep", "[ʃiːp]", ""),
    "veteran": RepositoryItem("veteran", "['vet(ə)r(ə)n]", ""),
    "USA".lower(): RepositoryItem("USA", "[ˌjuː es 'eɪ]", "")
}


class TestNounPossessiveCase(TestCase):

    # примеры притяжательных существительных из справочника Израилевича, Качаловой
    def test1(self):
        words = ["girl's", "Jack's", "horse's", "boys'", "workers'", "children's", "workmen's",
                 "commander-in-chief's", "brother-in-law's", "Helen's", "student's", "Moscow's", "Neva's"]

        expected_results = ["[gɜːlz]", "[ʤæks]", "['hɔːsɪz]", "[bɔɪz]", "['wɜːkəz]", "['ʧɪldr(ə)nz]", "['wɜːkmənz]",
                            "[kəˌmɑːndər ɪn 'tʃiːfs]", "['brʌð(ə)(r)ɪnˌlɔːz]", "['helənz]", "['st(j)uːd(ə)nts]",
                            "['mɔskəuz]", "['neɪvəz]"]

        for word, expected_result in zip(words, expected_results):
            sentenceUnknownWords, actual_result = TranscriberCoreEngine.transcribe(word, englishVocabulary_dict)
            self.assertEqual(expected_result, actual_result)

    # примеры притяжательных существительных с веб-странички https://grammarway.com/ru/possessive-case
    def test21(self):
        words = ["mum's", "Charles'", "girls'", "Jack's", "men's", "people's", "children's", "Richard's", "Tim's",
                 "Kelly's", "Shakespeare's", "brother's", "friend's", "mother's", "Great's", "dogs'", "players'"]

        expected_results = ["[mʌmz]", "['ʧɑːlzɪz]", "[gɜːlz]", "[ʤæks]", "[menz]", "['piːplz]", "['ʧɪldr(ə)nz]",
                            "['rɪʧədz]", "[tɪmz]", "['keliz]", "['ʃeɪkspɪəz]", "['brʌðəz]", "[frendz]", "['mʌðəz]",
                            "[greɪts]", "[dɔgz]", "['pleɪəz]"]

        for word, expected_result in zip(words, expected_results):
            sentenceUnknownWords, actual_result = TranscriberCoreEngine.transcribe(word, englishVocabulary_dict)
            self.assertEqual(expected_result, actual_result)

    def test22(self):
        words = ["James'", "James's"]  # в зависимости от автора учебника грамматики возможны оба варианта
        expected_results = ["['ʤeɪmzɪz]", "['ʤeɪmzɪz]"]
        for word, expected_result in zip(words, expected_results):
            sentenceUnknownWords, actual_result = TranscriberCoreEngine.transcribe(word, englishVocabulary_dict)
            self.assertEqual(expected_result, actual_result)

    def test23(self):
        words = ["witness's", "father's", "Kate's", "baker's", "dentist's",
                 "company's", "nation's", "Florida's", "ship's", "plane's",
                 "car's", "moon's", "sun's", "forest's", "yesterday's", "months'", "cent's", "dollars'", "mile's",
                 "God's", "time's", "stone's", "death's", "mind's", "harm's", "one's", "wit's", "arm's", "finger's",
                 "needle's", "pin's", "cow's", "soldier's", "sheep's", "veterans'", "Valentine's", "USA's"]

        expected_results = ["['wɪtnəsɪz]", "['fɑːðəz]", "[keɪts]",
                            "['beɪkəz]", "['dentɪsts]", "['kʌmpəniz]", "['neɪʃ(ə)nz]", "['flɔrɪdəz]", "[ʃɪps]",
                            "[pleɪnz]", "[kɑːz]", "[muːnz]", "[sʌnz]", "['fɔrɪsts]", "['jestədeɪz]", "[mʌnθs]",
                            "[sents]", "['dɔləz]", "['maɪlz]", "[gɔdz]", "[taɪmz]", "[stoʊnz]", "[deθs]", "[maɪndz]",
                            "[hɑːmz]", "[wʌnz]", "[wɪts]", "[ɑːmz]", "['fɪŋgəz]", "['niːdlz]", "[pɪnz]", "[kauz]",
                            "['soʊlʤəz]", "[ʃiːps]", "['vet(ə)r(ə)nz]", "['væləntaɪnz]", "[ˌjuː es 'eɪz]"]
        for word, expected_result in zip(words, expected_results):
            sentenceUnknownWords, actual_result = TranscriberCoreEngine.transcribe(word, englishVocabulary_dict)
            self.assertEqual(expected_result, actual_result)
