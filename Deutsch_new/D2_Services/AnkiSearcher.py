from AnkiCardEntity import AnkiCardEntity


def search_for_anki_card(word_to_search, cards):
    found_card: AnkiCardEntity = None
    for card in cards:
        if card.is_word_found(word_to_search, should_split_by_space=False):
            found_card = card
            break

    return found_card

# смотреть тест-кейсы в MultilingualAnkiService
