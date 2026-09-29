import AppContext
from AnkiCardEntity import AnkiCardEntity
from MultilingualAnkiDao import MultilingualAnkiDao
from View_enums import CurrentLanguageComboBoxEnum


class A080_DuplicatesAfterImportToAnkiRevealer:

    # def __init__(self):
    #     regular_cards = []

    # TODO: Запускать данный метод как отдельный step процесса (после импорта слов в Анки) + как валидационный
    #  метод перед самым началом работы на 1-м этапе

    def reveal_duplicates(self):

        # Вычитываем из Анки регулярные карточки
        multilingualAnkiDao = MultilingualAnkiDao()
        # TODO сделать конфигурационный / property файл с путями к Excel-файлам и названиями деков
        # regular_cards_deck_name = AnkiRegularCardsValidator.regular_cards_deck_name
        regular_cards = multilingualAnkiDao.get_regular_cards()

        # exact_duplicates - это карточки у которых совпадает поле Front и остальные текстовые поля (мультимедийные
        # поля в проверке не участвуют)
        exact_duplicates = set()
        # partial_duplicates_dict - это карточки у которых совпадает поле Front, но имеются отличия в других текстовых
        # полях
        partial_duplicates_dict = {}

        for i in range(0, len(regular_cards)):
            regular_card: AnkiCardEntity = regular_cards[i]
            regular_card_front_str = ';'.join(regular_card.front)

            for j in range(0, len(regular_cards)):
                if i != j:
                    other_regular_card: AnkiCardEntity = regular_cards[j]
                    other_regular_card_front_str = ';'.join(other_regular_card.front)

                    if regular_card_front_str == other_regular_card_front_str:
                        # Если у карточек совпадают ВСЕ поля, они считаются ПОЛНЫМИ/ТОЧНЫМИ дубликатами
                        if str(regular_card) == str(other_regular_card):
                            exact_duplicates.add(regular_card_front_str)
                        # Если у карточек совпадают не все поля, они считаются ЧАСТИЧНЫМИ дубликатами
                        else:
                            non_matching_card_fields = []
                            if regular_card.front_comment != other_regular_card.front_comment:
                                non_matching_card_fields.append('front_comment')

                            if regular_card.taggy != other_regular_card.taggy:
                                non_matching_card_fields.append('taggy')

                            if regular_card.ssml != other_regular_card.ssml:
                                non_matching_card_fields.append('ssml')

                            if regular_card.transcription != other_regular_card.transcription:
                                non_matching_card_fields.append('transcription')

                            if regular_card.grammar != other_regular_card.grammar:
                                non_matching_card_fields.append('grammar')

                            if regular_card.back != other_regular_card.back:
                                non_matching_card_fields.append('back')

                            if regular_card.back_comment != other_regular_card.back_comment:
                                non_matching_card_fields.append('back_comment')

                            if len(non_matching_card_fields) > 0:
                                partial_duplicates_dict[regular_card_front_str] = ', '.join(non_matching_card_fields)

        output = ''
        if exact_duplicates:
            output += 'EXACT DUPLICATES:\n'
            for card in sorted(exact_duplicates):
                output += f'{card}\n'

        if partial_duplicates_dict:
            output += '\nPARTIAL DUPLICATES:\n'
            for card_front_str, non_matching_card_fields_str in sorted(partial_duplicates_dict.items()):
                output += f'{card_front_str}: {non_matching_card_fields_str}\n'

        if not output:
            output += 'No duplicates found!'

        return output


###################################

if __name__ == '__main__':
    language = CurrentLanguageComboBoxEnum.GERMAN.value
    # language = CurrentLanguageComboBoxEnum.MODERN_GREEK.value
    # language = CurrentLanguageComboBoxEnum.ANCIENT_GREEK.value
    AppContext.switch_language(language)

    a080_DuplicatesAfterImportToAnkiRevealer = A080_DuplicatesAfterImportToAnkiRevealer()
    res = a080_DuplicatesAfterImportToAnkiRevealer.reveal_duplicates()
    print(res)
