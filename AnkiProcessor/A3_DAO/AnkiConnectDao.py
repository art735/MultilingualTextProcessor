import json
import urllib.request


class AnkiConnectDao:
    def __init__(self):
        pass

    # две звёздочки распаковывают словарь с парами ключ-значение в именованные аргументы в вызове функции
    def invoke_anki_connect(self, action, **params):
        request_json = json.dumps({'action': action, 'params': params, 'version': 6}).encode('utf-8')
        response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', request_json)))
        if len(response) != 2:
            raise Exception('response has an unexpected number of fields')
        if 'error' not in response:
            raise Exception('response is missing required error field')
        if 'result' not in response:
            raise Exception('response is missing required result field')
        if response['error'] is not None:
            raise Exception(response['error'])
        return response['result']

    # Метод для массового обновления заметок. Вызывается из AnkiConnectService.update_multiple_notes_in_anki(...)
    def update_multiple_notes(self, notes_to_update):
        """
        Обновляет поля нескольких заметок за один запрос через действие 'multi'.

        :param notes: список словарей, где каждый словарь содержит 'id' (ID заметки) и 'fields' (поля для обновления)
        :return: результат выполнения запроса
        """
        actions = [
            {
                "action": "updateNoteFields",
                "params": {
                    "note": {
                        "id": note['id'],
                        "fields": note['fields']
                    }
                }
            }
            for note in notes_to_update
        ]

        # Выполняем все действия через 'multi'
        return self.invoke_anki_connect("multi", actions=actions)
