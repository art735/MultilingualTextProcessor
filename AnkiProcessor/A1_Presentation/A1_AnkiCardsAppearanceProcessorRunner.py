# Suppress the following warning:
# C:\Program Files (x86)\Python39-32\lib\site-packages\bs4\__init__.py:435: MarkupResemblesLocatorWarning:
# The input looks more like a filename than markup. You may want to open this file and pass the filehandle into Beautiful Soup.
# warnings.filterwarnings("ignore", category=UserWarning, module='bs4')


from A1_AnkiCardsAppearanceProcessor import AnkiCardsAppearanceProcessor
import MethodExecutionTimeLogger
from AnkiConnectService import AnkiConnectService

from user_enums import Mode

ankiConnectService = AnkiConnectService()

# notes = ankiConnectService.get_notes_by_deck_name('Languages. Greek Modern')
# notes = ankiConnectService.get_notes_by_deck_name('Languages. Greek Modern::raw')
notes = ankiConnectService.get_notes_by_deck_name('temp')
# notes = ankiConnectService.get_notes_by_deck_name('!Deutsch. !Словарь::new2')
# notes = ankiConnectService.get_notes_by_deck_name('Italian')
# notes = ankiConnectService.get_notes_by_deck_name('Languages. Greek. !Словарь')
# notes = ankiConnectService.get_notes_by_deck_name('!Deutsch. !Словарь::!Deutsch. Goethe-Institut')
# notes = ankiConnectService.get_notes_by_deck_name('Goethe A1')

# notes = ankiConnectService.get_all_notes_from_all_decks()

# notes = ankiConnectService.get_notes_by_note_type_basic_and_reversed_card_with_additional_fields()

if __name__ == '__main__':
    ankiCardsAppearanceProcessor = AnkiCardsAppearanceProcessor()

    # TODO после того, как форматирование всех карточек в колоде "English (new)" будет отработано,
    # TODO выполнить этот метод с включенным флажком для колоды "English", карточки там сильно разломаны
    # MethodExecutionTimeLogger.run(lambda: ankiCardsAppearanceProcessor.process(notes, Mode.FIND_AND_REPLACE, strip_all_tags_except_br_and_img_tags=True))
    MethodExecutionTimeLogger.run(lambda: ankiCardsAppearanceProcessor.process(notes, Mode.FIND_AND_REPLACE))
