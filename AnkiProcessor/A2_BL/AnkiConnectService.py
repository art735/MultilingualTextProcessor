import base64

import TimeUtils
from AnkiConnectDao import AnkiConnectDao


class AnkiConnectService:
    def __init__(self):
        self.ankiConnectDao = AnkiConnectDao()

    def get_notes_by_deck_name(self, deck_name):
        if not self._deck_exists(deck_name):
            # На практике данный exception должен подсказывать пользователю о том, что хотя Анки и запущен, но активен
            # не тот аккаунт, который пользователь подразумевает: например, для работы с немецкими карточками открыт
            # аккаунт не 'Deutsch', а какой-то другой.
            raise ValueError(
                f'Deck "{deck_name}" does not exist in the chosen Anki account. Please, open another account!')

        notes = self.find_notes_by_search_query(f'deck:"{deck_name}"')

        # notes_ids = self.ankiConnectDao.invoke_anki_connect('findNotes', query=f'deck:"{deck_name}"')
        # notes = self.ankiConnectDao.invoke_anki_connect('notesInfo', notes=notes_ids)
        return notes

    def _deck_exists(self, deck_name):
        decks = self.ankiConnectDao.invoke_anki_connect('deckNames')
        return deck_name in decks

    # Обёртка для get_notes_by_note_type, чтобы не дублировать название note type-а в разных местах проекта
    def get_notes_by_note_type_basic_and_reversed_card_with_additional_fields(self):
        notes = self.get_notes_by_note_type("Basic (and reversed card) (with additional fields)")
        return notes


    def get_notes_by_note_type(self, note_type):
        notes = self.find_notes_by_search_query(f'note:\"{note_type}\"')
        return notes

    def find_notes_by_search_query(self, search_query):
        notes_ids = self.ankiConnectDao.invoke_anki_connect('findNotes', query=search_query)
        notes = self.ankiConnectDao.invoke_anki_connect('notesInfo', notes=notes_ids)
        return notes

    def get_all_notes_from_all_decks(self):
        print("START of getting ALL notes from Anki at " + TimeUtils.get_current_timestamp())
        # Такой способ работает намного быстрее, чем старый способ, когда в начале вычитывался список всех деков,
        # а потом в цикле доставались карточки из каждого дека и складывались в общую коллекцию.
        # Прирост производительности при текущем способе: 5 сек вместо 5 мин на вычитку 6 тыс. note-ов.
        all_notes_search_query = f'note:*'
        all_notes = self.find_notes_by_search_query(all_notes_search_query)
        print("END of getting ALL notes from Anki at " + TimeUtils.get_current_timestamp())
        print("#######################")
        return all_notes

    def get_all_deck_names(self):
        all_deck_names = self.ankiConnectDao.invoke_anki_connect('deckNames')
        return all_deck_names

    # Возвращает список имён всех сабдеков, вложенных в родительский дек
    def get_all_subdeck_names(self, parent_deck_name):
        # Получаем список вообще всех деков
        all_deck_names = self.ankiConnectDao.invoke_anki_connect('deckNames')
        # Отфильтровываем список всех деков так, чтобы получить только сабдеки, начинающиеся с имени родительского дека
        subdeck_names = [deck for deck in all_deck_names if deck.startswith(f'{parent_deck_name}::')]
        return subdeck_names

    # Поиск карточек по интервалу следующего показа (due interval)
    # Например, найти все карточки, которые будут показаны не ранее, чем через 5 лет
    # Другой кейс на эту же тему: можно вычитывать все карточки, сортировать их по due interval и сбрасывать, например,
    # все карточки, старше 3-5 лет, но не менее 10% от общего числа карточек.
    def find_cards_by_due_interval(self, due_interval):
        # Вычисляем значение интервала (365 дней * 5 лет)
        # due_interval = 365 * 5
        # Формируем поисковый запрос
        search_query = f"prop:ivl>={due_interval}"
        # Выполняем поиск карточек
        result = self.find_notes_by_search_query(search_query)
        return result

    def create_deck(self, deck_name):
        self.ankiConnectDao.invoke_anki_connect('createDeck', deck=deck_name)

    def update_single_note_in_anki(self, note, note_updated_fields_dict):
        # Записываем в DAO для отправки по сети:
        # 1) id обновляемой сущности;
        # 2) название и содержимое только тех полей, которые реально обновлялись.
        note_dao_dict = {'id': note['noteId'], 'fields': note_updated_fields_dict}
        self.ankiConnectDao.invoke_anki_connect('updateNoteFields', note=note_dao_dict)

    # С помощью AnkiConnect можно обновить содержимое сразу нескольких карточек (заметок) за один запрос.
    # Для этого используется API-метод 'updateNoteFields', который принимает note (словарь с noteId и fields).
    # При обновлении сразу несколько заметок, отправляется список таких словарей.
    # Большой список карточек лучше разбивать его на отдельные порции, например, по 50-100 карточек за раз, чтобы
    # избежать нагрузки на Anki.
    def update_multiple_notes_in_anki(self, notes_to_update):
        batch_size = 100  # Размер порции карточек, отправляемых на обновление в Anki за один запрос
        for i in range(0, len(notes_to_update), batch_size):
            # Получаем список словарей, где каждый словарь содержит 'id' и 'fields' (поля для обновления).
            notes_batch = notes_to_update[i:i + batch_size]

            # Пример списка обновляемых карточек
            # notes_to_update = [
            #     {"noteId": 1234567890, "fields": {"Front": "Новый текст 1", "Back": "Обновленный ответ 1"}},
            #     {"noteId": 9876543210, "fields": {"Front": "Новый текст 2", "Back": "Обновленный ответ 2"}},
            # ]

            # Отправляем список карточек на обновление
            self.ankiConnectDao.update_multiple_notes(notes_batch)

        return

    def reset_note_cards_to_new(self, note):
        # Получаем id-шники привязанных к note карточек
        card_ids = note["cards"]
        # Сбрасываем состояние карточек в New
        self.ankiConnectDao.invoke_anki_connect('forgetCards', cards=card_ids)

    # тестовый метод
    def test_reset_note_cards_to_new(self):
        notes = self.get_notes_by_deck_name('temp')
        for note in notes:
            note_front = note['fields']['Front']['value']
            # if note_front == 'pink':
            if note_front:
                self.reset_note_cards_to_new(note)

    # Загружает новый файл в Anki через AnkiConnect
    def upload_media_file_to_anki(self, media_file_in_anki_relative_name, media_file_in_apkg_extract_dir_fullpath_name):
        with open(media_file_in_apkg_extract_dir_fullpath_name, "rb") as f:
            file_data = base64.b64encode(f.read()).decode('utf-8')

        self.ankiConnectDao.invoke_anki_connect('storeMediaFile',
                                                filename=media_file_in_anki_relative_name, data=file_data)

    # def test_upload_media(self):
    #     notes = self.get_notes_by_deck_name('temp')
    #     for note in notes:
    #         note_front = note['fields']['Front']['value']
    #         if note_front == 'cat':


####################################################################

if __name__ == '__main__':
    ankiConnectService = AnkiConnectService()

    notes = ankiConnectService.get_notes_by_deck_name('!Deutsch. !Словарь::!Goethe-Institut A1')

    # ankiConnectService.test_reset_note_cards_to_new()

    # res = ankiConnectService.find_cards_by_due_interval(365 * 5)
    # [print(r) for r in res]

    # ankiConnectService.get_note_media_files(1730116634758)

    res = ankiConnectService.get_notes_by_note_type("Basic (and reversed card) (with additional fields)")
    print(len(res))
    [print(r) for r in res]
