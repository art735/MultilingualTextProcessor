from unittest import TestCase

from Core import TranscriberCoreEngine
from RepositoryItem import RepositoryItem

# vocabulary_dict = ExcelDaoEnglishVocabulary.get_EnglishVocabulary_dict()

vocabulary_dict = {
    "these": RepositoryItem("these", "[ðiːz]", "мн. от this – эти"),
    "record": RepositoryItem("record", "['rekɔːd]", "запись"),
    "to record": RepositoryItem("to record", "[rɪ'kɔːd]", "записывать"),
    "to record": RepositoryItem("to record", "[rɪ'kɔːd]", "записывать"),
    "to be": RepositoryItem("to be", "[biː]", "быть; существовать", [("am", "[æm]"), ("is", "[ɪz]"), ("are", "[ɑː(r)]"),
                                                                     ("was", "[wɔz]"), ("been", "[biːn]"),
                                                                     ("were", "[wɜː]")]),
    "a": RepositoryItem("a", "[ə]", "неопределённый артикль"),

    "close": RepositoryItem("close", "[kləuz]", "конец"),
    "close (adj.)": RepositoryItem("close (adj.)", "[kləus]", "закрытый",
                                   [("closer", "['kləusə]"), ("closest", "['kləusɪst]")]),
    "close (adv.)": RepositoryItem("close (adv.)", "[kləus]", "близко, около; рядом",
                                   [("closer", "['kləusə]"), ("closest", "['kləusɪst]")]),
    "to close": RepositoryItem("to close", "[kləuz]", "закрывать(ся)"),
    "to": RepositoryItem("to", "[tuː]", "определённый артикль"),

    "the": RepositoryItem("the", "[ðiː]", "к, в (выражает движение к какой-л. точке)"),
    "closer": RepositoryItem("closer", "['kləuzə]", "закрыватель"),
    "to come": RepositoryItem("to come", "[kʌm]", "приходить, приезжать"),
}


class TestTranscriberCoreEngine(TestCase):

    def test1(self):
        sentence = "These records are recording a record!"
        expected_result = "[ðiːz 'rekɔːdz ɑː(r) rɪ'kɔːdɪŋ ə 'rekɔːd]"
        sentenceUnknownWords, sentenceTranscription = TranscriberCoreEngine.transcribe(sentence, vocabulary_dict)
        self.assertEqual(expected_result, sentenceTranscription)

    def test2(self):
        sentence = "A close close is closing to a close."
        expected_result = "[ə kləus kləuz ɪz 'kləuzɪŋ tuː ə kləuz]"
        sentenceUnknownWords, sentenceTranscription = TranscriberCoreEngine.transcribe(sentence, vocabulary_dict)
        self.assertEqual(expected_result, sentenceTranscription)

    def test3(self):
        sentence = "The closest closer is coming closer."
        expected_result = "[ðiː 'kləusɪst 'kləuzə ɪz 'kʌmɪŋ 'kləusə]"
        sentenceUnknownWords, sentenceTranscription = TranscriberCoreEngine.transcribe(sentence, vocabulary_dict)
        self.assertEqual(expected_result, sentenceTranscription)
