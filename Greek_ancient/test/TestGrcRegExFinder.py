from unittest import TestCase

from GrcRegExFinder import GrcRegExFinder


class TestGrcRegExFinder(TestCase):

    def setUp(self):
        self.grcRegExFinder = GrcRegExFinder()

    def test_is_token_a_greek_word(self):
        token = "1Ἀρχὴ"
        self.assertFalse(self.grcRegExFinder.is_greek_word(token))

        token = "Ἀρχὴ1"
        self.assertFalse(self.grcRegExFinder.is_greek_word(token))

        token = "Ἀρχὴ"
        self.assertTrue(self.grcRegExFinder.is_greek_word(token))

        token = "Ἀρχὴ τοῦ εὐαγγελίου Ἰησοῦ Χριστοῦ"
        self.assertFalse(self.grcRegExFinder.is_greek_word(token))

        token = "ἈρχὴτοῦεὐαγγελίουἸησοῦΧριστοῦ"
        self.assertTrue(self.grcRegExFinder.is_greek_word(token))

        token = "-"
        self.assertFalse(self.grcRegExFinder.is_greek_word(token))

        token = "--"
        self.assertFalse(self.grcRegExFinder.is_greek_word(token))

        token = "VS_02_2803"
        self.assertFalse(self.grcRegExFinder.is_greek_word(token))
