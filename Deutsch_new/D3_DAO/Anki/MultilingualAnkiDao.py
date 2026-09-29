# Строка нужна для предотвращения ошибки SyntaxError: Non-UTF-8 code starting with '\xd0'
# -*- coding: utf-8 -*-
import AppContext
import beautiful_soup_helper
from AnkiCardEntity import AnkiCardEntity, AnkiField
from AnkiConnectService import AnkiConnectService
from DeuRegExFinder import DeuRegExFinder
from View_enums import CurrentLanguageComboBoxEnum

# Список агрегатных карточек, которые нужно проигнорировать в рамках валидации, которая на UI называется
# "(4) Check consistency of all [Vocab]-files".
# Логика более полной и всесторонней валидации агрегатных карточек находится в AnkiAggregateCardsValidator.py
aggregate_cards_ignored_in_consistency_validation = [
    # указываем front-поле игнорируемой карточки (front-поле - это список полос карточки)
    ['der Ort', 'der Platz', 'die Stelle'],
    ['leicht', 'VS.', 'schwer'],
    ['seit', 'VS.', 'ab'],
    ['der Eingang', 'VS.', 'der Eintritt'],
    ['das Geschäft', 'VS.', 'der Laden'],
    ['die Leute', 'VS.', 'die Menschen'],
]


class MultilingualAnkiDao:
    def __init__(self):
        self.ankiConnectService = AnkiConnectService()

    def get_regular_cards(self):
        # Название дека вычитывать каждый раз именно как локальную переменную, не делать полем класса, иначе
        # переключение между иностранными языками на UI не будет приводить к переключению названия дека
        regular_cards_deck = AppContext.get_regular_cards_deck()
        return self.get_data(regular_cards_deck)

    # Возвращает все агрегатные карточки
    def get_all_aggregate_cards(self):
        # Название дека вычитывать каждый раз именно как локальную переменную, не делать полем класса, иначе
        # переключение между иностранными языками на UI не будет приводить к переключению названия дека
        aggregate_cards_deck = AppContext.get_aggregate_cards_deck()
        return self.get_data(aggregate_cards_deck)

    # Возвращает агрегатные карточки, которые будут участвовать в UC "(4) Check consistency of all [Vocab]-files".
    # Игнорируем те карточки, перевод которых в специфическом контексте той или иной агрегатной карточки отличается
    # от общепринятого перевода этого же слова в регулярных карточках.
    def get_filtered_aggregate_cards_for_consistency_validation(self):
        all_aggregate_cards = self.get_all_aggregate_cards()
        filtered_aggregate_cards = [card for card in all_aggregate_cards
                                    if card.front not in aggregate_cards_ignored_in_consistency_validation]
        return filtered_aggregate_cards

    def get_data(self, deck_name):
        anki_data = []

        notes = self.ankiConnectService.get_notes_by_deck_name(deck_name)
        # notes = self.ankiConnectService.get_notes_by_note_type_basic_and_reversed_card_with_additional_fields()

        for note in notes:
            front: list = self._parse_note_field(AnkiField.Front.value, note)
            front_comment: list = self._parse_note_field(AnkiField.Front_comment.value, note)
            taggy: list = self._parse_note_field(AnkiField.Taggy.value, note)
            ssml: list = self._parse_note_field(AnkiField.SSML.value, note)
            transcription: list = self._parse_note_field(AnkiField.Transcription.value, note)
            grammar: list = self._parse_note_field(AnkiField.Grammar.value, note)
            back: list = self._parse_note_field(AnkiField.Back.value, note)
            back_comment: list = self._parse_note_field(AnkiField.Back_comment.value, note)

            anki_card_entity = AnkiCardEntity(front, front_comment, taggy, ssml, transcription, grammar,
                                              back, back_comment)

            anki_data.append(anki_card_entity)

            # anki_card_entity.validate_consistency()
            # if 'Wittenberg' in anki_card_entity.front:
            # print(anki_card_entity.to_str())
            # print(anki_card_entity.to_str("front_transcription_back_with_comments"))

        return anki_data

    def _parse_note_field(self, field_name: str, note):
        field_stripes = []

        # Вычитываем содержимое поля
        if field_name in note['fields']:
            field_contents = note['fields'][field_name]['value']
            field_stripes = self.parse_contents(field_contents, '<br><br>', '<br>')

        return field_stripes

    # Этот метод ещё используется для парсинга данных из OO Writer таблицы
    def parse_contents(self, field_contents, stripes_delimiter, stripe_lines_delimiter):
        field_stripes = []

        # Разбиваем содержимое поля по логическому разделителю, заменяя его на '\n'
        stripes = [stripe.replace(stripe_lines_delimiter, '\n') for stripe in field_contents.split(stripes_delimiter)]

        # Стрипаем от html-разметки каждую полосу поля
        for stripe in stripes:
            untagged_stripe = beautiful_soup_helper.strip_all_tags(stripe)

            # Замена неразрывного пробела на обычный пробел
            untagged_stripe = untagged_stripe.replace('\u00A0', ' ')
            if untagged_stripe:
                field_stripes.append(untagged_stripe)

        return field_stripes

    # def search_word(self, word_to_search, deck_name):
    #     results = []
    #     anki_data = self.get_data(deck_name)
    #
    #     # 1. Ищем сначала среди однополосных карточек
    #     for anki_entity in anki_data:
    #         if anki_entity.is_word_found_in_a_single_striped_card(word_to_search):
    #             results.append(anki_entity)
    #
    #     # 2. Если среди однополосных карточек слово не найдено, ищем его среди многополосных карточек
    #     if len(results) == 0:
    #         for anki_entity in anki_data:
    #             if anki_entity.is_word_found_in_a_multi_striped_card(word_to_search):
    #                 results.append(anki_entity)
    #
    #     return results

    def validate(self, deck_name):
        anki_data = self.get_data(deck_name)
        for anki_entity in anki_data:
            anki_entity.validate_consistency()
            anki_entity.validate_german_word_can_be_reached_for_lookup()


#############################################################

if __name__ == '__main__':
    language = CurrentLanguageComboBoxEnum.GERMAN.value
    # language = CurrentLanguageComboBoxEnum.MODERN_GREEK.value
    # language = CurrentLanguageComboBoxEnum.ANCIENT_GREEK.value
    AppContext.switch_language(language)

    multilingualAnkiDao = MultilingualAnkiDao()

    # regular_cards = multilingualAnkiDao.get_regular_cards()
    # [print(card) for card in regular_cards]

    aggregate_cards = multilingualAnkiDao.get_all_aggregate_cards()
    [print(card) for card in aggregate_cards]


    anki_deck_name = '!A_Словари::!Words (new)'
    anki_deck_name = '!A_Словари'
    # anki_deck_name = 'temp'
    # anki_deck_name = 'CyberBionic Systematics'

    # deck_data = germanWordsFromAnkiDao.get_data(deck_name)
    # for dd in deck_data:
    # print(dd)
    # print(dd.to_str())
    # print(dd.to_str("front_transcription_back_with_comments"))
    # print(dd.to_str("front_back"))

    # germanWordsFromAnkiDao.validate(deck_name)

    word_to_search = 'Ur-'
    # word_to_search = 'bedanken'
    # word_to_search = 'Alex'
    # res = germanWordsFromAnkiDao.search_word(word_to_search)

    # TODO вернуться к этому варианту валидации
    # res = germanWordsFromAnkiDao.validate_all_parts_of_complex_words_are_present_in_other_cards()
    # for r in res:
    #     print(f'{r}\n')

    # germanWordsFromAnkiDao.validate_elements_of_aggregate_cards_can_be_found_among_single_striped_cards()
    # for r in res:
    #     print(f'{r}\n')
