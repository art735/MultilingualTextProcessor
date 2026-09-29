from typing import List

import AnkiSearcher
from AnkiCardEntity import AnkiCardEntity
from MultilingualAnkiDao import MultilingualAnkiDao


class MultilingualAnkiService:

    def __init__(self):
        self.multilingualAnkiDao = MultilingualAnkiDao()

        # Основная коллекция регулярных карточек
        # self.main_regular_cards_deck_name = '!Deutsch. !Словарь'
        self.main_regular_cards: List[AnkiCardEntity] = self.multilingualAnkiDao.get_regular_cards()

        # Коллекция регулярных карточек текущего студента / курса / учебника
        # self.student_regular_cards_deck_name = '!Deutsch. Goethe-Institut'
        # self.student_regular_cards: List[AnkiCardEntity] = self.germanWordsFromAnkiDao.get_data(self.student_regular_cards_deck_name)

    # Ищет word_to_search среди основной коллекции регулярных карточек, а именно среди однополосных карточек и
    # последних полос многополосных карточек
    def search_among_main_regular_cards(self, word_to_search):
        result = AnkiSearcher.search_for_anki_card(word_to_search, self.main_regular_cards)
        return result


###################################

if __name__ == '__main__':

    multilingualAnkiService = MultilingualAnkiService()

    word_to_search = 'wissen'
    word_to_search = 'die Freundschaft'

    word_to_search = 'die Aktiengesellschaft'
    # word_to_search = 'die U-Bahn'
    # TODO: валидировать, что транскрипция в таких словах тоже имеет правильный формат!
    # TODO: BRD снова вернуть в карточку с Bundesrepublic

    # res = ankiCardsService.search_among_main_regular_cards(word_to_search)
    # print(res)

    input1 = [
        # die Deutsche Demokratische Republik (DDR)
        'die Deutsche Demokratische Republik', 'die DDR',

        # die Bundesrepublik Deutschland (BRD)
        'die Bundesrepublik Deutschland', 'die BRD',

        # die Untergrundbahn (U-Bahn)
        'die Untergrundbahn', 'die U-Bahn',

        # das Direktschaltgetriebe (DSG)
        'das Direktschaltgetriebe', 'das DSG',

        # die Volkshochschule (VHS)
        'die Volkshochschule', 'die VHS',

        # der Büstenhalter (BH)
        'der Büstenhalter', 'der BH',

        # die Aktiengesellschaft (AG)
        'die Aktiengesellschaft', 'die AG',
    ]

    er1 = [
        # die Deutsche Demokratische Republik
        ['deutsch', 'demokratisch', 'die Republik', 'die Deutsche Demokratische Republik (DDR)'],
        # die DDR
        ['deutsch', 'demokratisch', 'die Republik', 'die Deutsche Demokratische Republik (DDR)'],

        # die Bundesrepublik Deutschland
        ['die Bundesrepublik', 'Deutschland', 'die Bundesrepublik Deutschland (BRD)'],
        # die BRD
        ['die Bundesrepublik', 'Deutschland', 'die Bundesrepublik Deutschland (BRD)'],

        # die Untergrundbahn'
        ['der Untergrund', 'die Bahn', 'die Untergrundbahn (U-Bahn)'],
        # die U-Bahn'
        ['der Untergrund', 'die Bahn', 'die Untergrundbahn (U-Bahn)'],

        # das Direktschaltgetriebe
        ['direkt', 'die Schaltung', 'das Getriebe', 'das Direktschaltgetriebe (DSG)'],
        # das DSG
        ['direkt', 'die Schaltung', 'das Getriebe', 'das Direktschaltgetriebe (DSG)'],

        # die Volkshochschule
        ['das Volk', 'die Hochschule', 'die Volkshochschule (VHS)'],
        # die VHS
        ['das Volk', 'die Hochschule', 'die Volkshochschule (VHS)'],

        # der Büstenhalter
        ['die Büste', 'der Halter', 'der Büstenhalter (BH)'],
        # der BH
        ['die Büste', 'der Halter', 'der Büstenhalter (BH)'],

        # die Aktiengesellschaft
        ['die Aktie', 'die Gesellschaft', 'die Aktiengesellschaft (AG)'],
        # die AG
        ['die Aktie', 'die Gesellschaft', 'die Aktiengesellschaft (AG)']
    ]

    if all(multilingualAnkiService.search_among_main_regular_cards(input_val).front == er for input_val, er in
           zip(input1, er1)):
        print('test1 ok')
    else:
        print('test1 failed')
