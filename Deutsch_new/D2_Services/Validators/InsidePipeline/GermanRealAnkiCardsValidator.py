from AnkiRegularCardsValidator import AnkiRegularCardsValidator
from MultilingualAnkiDao import MultilingualAnkiDao


class GermanRealAnkiCardsValidator:
    error_msg = "Inconsistent words {0} (in 'Transcription' and 'Back' fields):\n\n{1}"

    def __init__(self, anki_regular_cards, anki_aggregate_cards):
        self.anki_regular_cards = anki_regular_cards
        self.anki_aggregate_cards = anki_aggregate_cards
        self.multilingualAnkiDao = MultilingualAnkiDao()

    def validate(self, should_split_by_space_flag):
        # 1. Валидируем регулярные карточки
        output1_regular_cards = self._validate_regular_cards(should_split_by_space_flag)

        # 2. Валидируем агрегатные карточки (при условии, что валидация регулярных карточек прошла успешно)
        # Нет смысла валидировать агрегатные карточки, если валидация регулярых карточек прошла неуспешно потому, что
        # эти же самые неконсистентные регулярные карточки могут встречаться в агрегатных карточках.
        output2_aggregate_cards = ''
        if not output1_regular_cards:
            output2_aggregate_cards = self._validate_aggregate_cards()

        # 3. Валидируем сумму регулярных и агрегатных карточек (при условии, что валидация агрегатных карточек
        # прошла успешно)
        output3_regular_plus_aggregate_cards = ''
        if not output1_regular_cards and not output2_aggregate_cards:
            output3_regular_plus_aggregate_cards = self._validate_regular_plus_aggregate_cards()

        output = '\n\n* * *\n\n'.join([out for out in [output1_regular_cards, output2_aggregate_cards,
                                                       output3_regular_plus_aggregate_cards] if out])
        return output

    def _validate_regular_cards(self, should_split_by_space_flag):
        # 1. Валидируем регулярные карточки на lack и excess
        ankiRegularCardsValidator = AnkiRegularCardsValidator(self.anki_regular_cards)
        lack_results_set, excess_results_set, printable_output = \
            ankiRegularCardsValidator.find_regular_cards_lack_and_excess_sets(should_split_by_space_flag)

        # 2. Валидируем регулярные карточки на консистентность
        output_consistency = ankiRegularCardsValidator.find_inconsistent_translations_of_the_same_word()
        if output_consistency:
            output_consistency = self.error_msg.format('among Anki regular cards', output_consistency)

        # .strip() удаляет символы [ \t\n\r\f\v] в начале и конце строки
        output_regular_cards = '\n\n* * *\n\n'.join(
            [out for out in [printable_output.strip(), output_consistency] if out])
        return output_regular_cards

    def _validate_aggregate_cards(self):
        output_aggregate_cards = ''

        ankiRegularCardsValidator = AnkiRegularCardsValidator(self.anki_aggregate_cards)
        output_consistency = ankiRegularCardsValidator.find_inconsistent_translations_of_the_same_word()
        if output_consistency:
            output_aggregate_cards += self.error_msg.format('among Anki aggregate cards', output_consistency)

        return output_aggregate_cards

    def _validate_regular_plus_aggregate_cards(self):
        output_regular_plus_aggregate_cards = ''

        ankiRegularCardsValidator = AnkiRegularCardsValidator(self.anki_regular_cards + self.anki_aggregate_cards)
        output_consistency = ankiRegularCardsValidator.find_inconsistent_translations_of_the_same_word()
        if output_consistency:
            output_regular_plus_aggregate_cards += self.error_msg.format('among Anki (regular + aggregate) cards',
                                                                         output_consistency)

        return output_regular_plus_aggregate_cards


##############################################

if __name__ == '__main__':
    multilingualAnkiDao = MultilingualAnkiDao()
    anki_regular_cards_test = multilingualAnkiDao.get_regular_cards()
    anki_aggregate_cards_test = multilingualAnkiDao.get_filtered_aggregate_cards_for_consistency_validation()
    germanRealAnkiCardsValidator = GermanRealAnkiCardsValidator(anki_regular_cards_test, anki_aggregate_cards_test)
    res = germanRealAnkiCardsValidator.validate(should_split_by_space_flag=False)
    if not res:
        res = 'ok'
    print(res)
