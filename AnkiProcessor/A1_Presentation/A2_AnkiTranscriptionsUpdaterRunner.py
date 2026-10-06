from A2_AnkiTranscriptionsUpdater import AnkiTranscriptionsUpdater
from user_enums import Mode

if __name__ == '__main__':
    ankiTranscriptionsUpdater = AnkiTranscriptionsUpdater()

    # !!! DEUTSCH
    # Step 1. Запускаем с mode=Mode.SEARCH_ONLY, чтобы увидеть форматирование каких транскрипций будет сломано при
    # последующем запуске с флагом mode=Mode.FIND_AND_REPLACE. Фиксировать в Notepad++ список этих транскрипций,
    # чтобы потом вручную восстановить их форматирование.
    # ankiTranscriptionsUpdater.update_transcriptions_in_particular_language_decks('deu', Mode.SEARCH_ONLY)
    # Step 2. Запускаем с mode=Mode.FIND_AND_REPLACE
    ankiTranscriptionsUpdater.update_transcriptions_in_particular_language_decks('deu', Mode.FIND_AND_REPLACE)

    # !!! ENGLISH
    # Step 1. Запускаем с mode=Mode.SEARCH_ONLY, чтобы увидеть форматирование каких транскрипций будет сломано при
    # последующем запуске с флагом mode=Mode.FIND_AND_REPLACE. Фиксировать в Notepad++ список этих транскрипций,
    # чтобы потом вручную восстановить их форматирование.
    # ankiTranscriptionsUpdater.update_transcriptions_in_particular_language_decks('eng', Mode.SEARCH_ONLY)
    # Step 2. Запускаем с mode=Mode.FIND_AND_REPLACE
    ankiTranscriptionsUpdater.update_transcriptions_in_particular_language_decks('eng', Mode.FIND_AND_REPLACE)

    # !!! ITALIAN
    # Step 1. Запускаем с mode=Mode.SEARCH_ONLY, чтобы увидеть форматирование каких транскрипций будет сломано при
    # последующем запуске с флагом mode=Mode.FIND_AND_REPLACE. Фиксировать в Notepad++ список этих транскрипций,
    # чтобы потом вручную восстановить их форматирование.
    # ankiTranscriptionsUpdater.update_transcriptions_in_particular_language_decks('ita', Mode.SEARCH_ONLY)
    # Step 2. Запускаем с mode=Mode.FIND_AND_REPLACE
    ankiTranscriptionsUpdater.update_transcriptions_in_particular_language_decks('ita', Mode.FIND_AND_REPLACE)
