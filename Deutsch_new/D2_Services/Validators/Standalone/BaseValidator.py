from AnkiConnectService import AnkiConnectService


# ignored_tokens = ['–']

class BaseValidator:
    ignored_lines = ['- - -', 'VS.']

    def __init__(self):
        self.ankiConnectService = AnkiConnectService()
        # self.aggregate_cards_deck_name = '!Deutsch. Агрегаты'
        # self.regular_cards_deck_name = '!Deutsch. !Словарь'
        # self.regular_cards_deck_name = 'temp'

    # Validation UC#1. Самый первый шаг в валидациях - это запустить AnkiRunner для замены в карточках всех неправильных
    # последовательностей символов на правильные
    def validate_uc1_anki_runner_base(self, deck_name):
        notes = self.ankiConnectService.get_notes_by_deck_name(deck_name)
        # MethodExecutionTimeLogger.run(lambda: AnkiCardsAppearanceProcessor.process(notes, Mode.SEARCH_ONLY))
        # MethodExecutionTimeLogger.run(lambda: AnkiCardsAppearanceProcessor.process(notes, Mode.FIND_AND_REPLACE))

    # Validation UC#2. Валидировать, что каждая карточка содержит одинаковое количество полос в ключевых полях
    def validate_uc2_main_card_fields_pieces_consistency_base(self, cards):
        for card in cards:
            card.validate_consistency()

    def _print_dict_with_results(self, results_dict):
        # Сначала сортируем словарь по ключам
        sorted_dict = dict(sorted(results_dict.items()))

        # Затем сортируем списки значений внутри каждого ключа
        for key in sorted_dict:
            sorted_dict[key] = sorted(sorted_dict[key])

        dict_items_list = list(sorted_dict.items())

        # Перебираем элементы коллекций с помощью индексов, чтобы сделать красивый вывод
        for i in range(len(dict_items_list)):
            aggregate_card_ready_token, vals = dict_items_list[i]
            print(f"'{aggregate_card_ready_token}': [")
            for j in range(len(vals)):
                val = vals[j]
                if j < len(vals) - 1:
                    print(f'\t"{val}",')
                elif i < len(dict_items_list) - 1:
                    print(f'\t"{val}"\n],\n')
                else:
                    print(f'\t"{val}"\n]')
