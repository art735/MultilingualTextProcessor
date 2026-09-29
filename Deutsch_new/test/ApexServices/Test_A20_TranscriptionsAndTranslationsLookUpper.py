from unittest import TestCase

from A020_TranscriptionsAndTranslationsLookUpper import A020_TranscriptionsAndTranslationsLookUpper
from MultilingualAnkiService import MultilingualAnkiService
from OdtCopyPasteTableDao import OdtCopyPasteTableDao


class Test_A20_TranscriptionsAndTranslationsLookUpper(TestCase):

    # Выполняется один раз при загрузке модуля Test_A20_TranscriptionsAndTranslationsLookUpper
    # def setUpClass(self):

    # Выполняется перед каждым тестом
    def setUp(self):
        self.odtCopyPasteTableDao = OdtCopyPasteTableDao()
        self.ankiCardsService = MultilingualAnkiService()
        self.a020_TranscriptionsAndTranslationsLookUpper = A020_TranscriptionsAndTranslationsLookUpper(
            self.odtCopyPasteTableDao,
            self.ankiCardsService)

    def test_look_up(self):
        # Тестировать, что метод, встретив сложное/составное слово, во-первых, нашёл его среди главной коллекции
        # регулярных карточек, а, во-вторых, не найдя его среди студенческой коллекции регулярных карточек и среди слов,
        # стоящих выше по таблице, разбил его на составные части и поместил их выше себя по таблице
        # TODO: когда студенческая коллекция станет содержать слова ab- и/или holen, данный тест начнёт падать.
        #  нужно как-то замокать обращение к Анки-коллекциям регулярных карточек.
        input_str = '<table><thead><tr><td>abholen</td></tr></thead></table>'
        expected_result = ['ab-', 'holen', 'ab-^^^^^holen^^^^^abholen']

        # self.ankiCardsServiceMock.search_among_main_regular_cards.return_value = None
        # self.ankiCardsServiceMock.search_among_student_regular_cards.return_value = None

        look_up_result = self.a020_TranscriptionsAndTranslationsLookUpper.look_up(input_str)
        actual_result = []
        for line in look_up_result.split('\n'):
            if line:
                first_col_word = line.split('|')[0]
                actual_result.append(first_col_word)
        self.assertEquals(expected_result, actual_result)
