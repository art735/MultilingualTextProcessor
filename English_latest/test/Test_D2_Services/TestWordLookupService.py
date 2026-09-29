from unittest import TestCase

import WordLookupService
from EnglishConstants import NEWLINE
from RepositoryItem import RepositoryItem

englishVocabulary_dict = {

    "close": RepositoryItem("close", "[kləuz]", "конец"),
    "close (adj.)": RepositoryItem("close (adj.)", "[kləus]", "закрытый",
                                   [("closer", "['kləusə]"), ("closest", "['kləusɪst]")]),
    "close (adv.)": RepositoryItem("close (adv.)", "[kləus]", "близко",
                                   [("closer", "['kləusə]"), ("closest", "['kləusɪst]")]),
    "to close": RepositoryItem("to close", "[kləuz]", "закрывать(ся)"),
    "closer": RepositoryItem("closer", "['kləuzə]", "закрыватель"),

}


class TestWordLookupService(TestCase):

    def test_close(self):
        expected_result_items = ["VOCABULARY:",
                                 "close*[kləuz]*конец",
                                 "close (adj.)*[kləus]*закрытый*closer ['kləusə]; closest ['kləusɪst]",
                                 "close (adv.)*[kləus]*близко, около; рядом*closer ['kləusə]; closest ['kləusɪst]",
                                 "to close*[kləuz]*закрывать(ся)"]
        expected_result = NEWLINE.join(expected_result_items)
        actual_result = WordLookupService.look_up("close")
        self.assertEqual(expected_result, actual_result)

    def test_closer(self):
        expected_result_items = ["VOCABULARY:",
                                 "close (adj.)*[kləus]*закрытый*closer ['kləusə]; closest ['kləusɪst]",
                                 "close (adv.)*[kləus]*близко, около; рядом*closer ['kləusə]; closest ['kləusɪst]",
                                 "closer*['kləuzə]*закрыватель"]
        expected_result = NEWLINE.join(expected_result_items)
        actual_result = WordLookupService.look_up("closer")
        self.assertEqual(expected_result, actual_result)
