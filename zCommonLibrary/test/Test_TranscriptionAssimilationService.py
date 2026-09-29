from unittest import TestCase

from TranscriptionAssimilationService import TranscriptionAssimilationService


# ChatGPT-4o prompt
# Сгенерируй пары английских слов и их транскрипции так, чтобы транскрипция 1-го слова заканчивалась на один символов из regex-группы [θð], а транскрипция 2-го слова начиналась на один из символов regex-группы [tdszln].

# Сгенерируй все возможные комбинации таких слов для двух случаев:
# 1) транскрипция 2-го слова НЕ начинается со знака ударения;
# 2) транскрипция 2-го слова начинается! со знака ударения.


class Test_TranscriptionAssimilationService(TestCase):

    def setUp(self):
        self.transcriptionAssimilationService = TranscriptionAssimilationService()

    # θ + no stress + [tdszln]
    def test11(self):
        # bath time
        input_str = "[bæθ taɪm]"
        expected_result = "[bæt̪ t̪aɪm]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

        # faith day
        input_str = "[feɪθ deɪ]"
        expected_result = "[feɪt̪ d̪eɪ]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

        # death sun
        input_str = "[dɛθ sʌn]"
        expected_result = "[dɛt̪ s̪ʌn]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

        # breath zone
        input_str = "[brɛθ zoʊn]"
        expected_result = "[brɛt̪ z̪oʊn]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

        # teeth line
        input_str = "[tiːθ laɪn]"
        expected_result = "[tiːt̪ l̪aɪn]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

        # stealth net
        input_str = "[stɛlθ nɛt]"
        expected_result = "[stɛlt̪ n̪ɛt]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

    # θ + stress + [tdszln]
    def test12(self):
        # bath table
        input_str = "[bæθ ˈteɪbl]"
        expected_result = "[bæt̪ ˈt̪eɪbl]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

        # faith danger
        input_str = "[feɪθ ˈdeɪndʒə]"
        expected_result = "[feɪt̪ ˈd̪eɪndʒə]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

        # death simple
        input_str = "[dɛθ ˈsɪmpl]"
        expected_result = "[dɛt̪ ˈs̪ɪmpl]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

        # breath zebra
        input_str = "[brɛθ ˈzebrə]"
        expected_result = "[brɛt̪ ˈz̪ebrə]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

        # teeth lemon
        input_str = "[tiːθ ˈlemən]"
        expected_result = "[tiːt̪ ˈl̪emən]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

        # breath nature
        input_str = "[breθ ˈneɪtʃə]"
        expected_result = "[bret̪ ˈn̪eɪtʃə]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

    # ð + no stress + [tdszln]
    def test21(self):
        # with time
        input_str = "[wɪð taɪm]"
        expected_result = "[wɪd̪ t̪aɪm]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

        # with day
        input_str = "[wɪð deɪ]"
        expected_result = "[wɪd̪ d̪eɪ]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

        # with sun
        input_str = "[wɪð sʌn]"
        expected_result = "[wɪd̪ s̪ʌn]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

        # with zone
        input_str = "[wɪð zoʊn]"
        expected_result = "[wɪd̪ z̪oʊn]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

        # with line
        input_str = "[wɪð laɪn]"
        expected_result = "[wɪd̪ l̪aɪn]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

        # with net
        input_str = "[wɪð nɛt]"
        expected_result = "[wɪd̪ n̪ɛt]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

    # ð + stress + [tdszln]
    def test22(self):
        # with table
        input_str = "[wɪð ˈteɪbl]"
        expected_result = "[wɪd̪ ˈt̪eɪbl]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

        # with danger
        input_str = "[wɪð ˈdeɪndʒə]"
        expected_result = "[wɪd̪ ˈd̪eɪndʒə]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

        # with simple
        input_str = "[wɪð ˈsɪmpl]"
        expected_result = "[wɪd̪ ˈs̪ɪmpl]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

        # with zebra
        input_str = "[wɪð ˈzebrə]"
        expected_result = "[wɪd̪ ˈz̪ebrə]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

        # with lemon
        input_str = "[wɪð ˈlemən]"
        expected_result = "[wɪd̪ ˈl̪emən]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

        # with nature
        input_str = "[wɪð ˈneɪtʃə]"
        expected_result = "[wɪd̪ ˈn̪eɪtʃə]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

    # выборочные сценарии [tdszln] + [θð] (с ударениями и без)
    def test3(self):
        # cat theory
        input_str = "[kæt ˈθɪəri]"
        expected_result = "[kæt̪ ˈt̪ɪəri]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

        # bid though
        input_str = "[bɪd ðoʊ]"
        expected_result = "[bɪd̪ d̪oʊ]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

        # cats theory
        input_str = "[kæts ˈθɪəri]"
        expected_result = "[kæts̪ ˈt̪ɪəri]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

        # bells thorn
        input_str = "[bɛlz θɔrn]"
        expected_result = "[bɛlz̪ t̪ɔrn]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

        # bell that
        input_str = "[bɛl ˈðæt]"
        expected_result = "[bɛl̪ ˈd̪æt]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

        # green thread
        input_str = "[ɡriːn θrɛd]"
        expected_result = "[ɡriːn̪ t̪rɛd]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

        # holds this
        input_str = "[hoʊldz ðɪs]"
        expected_result = "[hoʊldz̪ d̪ɪs]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

        # cats theta
        input_str = "[kæts ˈθeɪtə]"
        expected_result = "[kæts̪ ˈt̪eɪtə]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

        # green thumb
        input_str = "[ɡriːn ˈθʌm]"
        expected_result = "[ɡriːn̪ ˈt̪ʌm]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

        # holds they
        input_str = "[hoʊldz ˈðeɪ]"
        expected_result = "[hoʊldz̪ ˈd̪eɪ]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)

        # friends thirsty
        input_str = "[frɛndz ˈθɜːsti]"
        expected_result = "[frɛndz̪ ˈt̪ɜːsti]"
        actual_result = self.transcriptionAssimilationService.assimilate(input_str)
        self.assertEqual(expected_result, actual_result)
