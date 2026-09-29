class SlashContainingCellSplitter:
    def __init__(self):
        pass

    def split_by_slash(self, word_transcription_tuples):
        validation_messages = self._validate_consistency_of_slash_containing_tuples(word_transcription_tuples)
        # Если имеются валидационные сообщения (свидетельствующие об ошибках форматирования slashed-separated слов),
        # тогда будет выброшено исключение со списком таких ошибок и работа программы будет невозможна без устранения
        # этих ошибок
        if validation_messages:
            raise ValueError('\n'.join(validation_messages))

        results = []
        for word, transcription in word_transcription_tuples:
            if '/' in word:
                word_slashed_parts = word.split('/')
                transcription_slashed_parts = transcription.split('/')
                for word_slashed_part, transcription_slashed_part in zip(word_slashed_parts,
                                                                         transcription_slashed_parts):
                    results.append(tuple([word_slashed_part.strip(), transcription_slashed_part.strip()]))
            else:
                results.append(tuple([word, transcription]))

        return results

    def _validate_consistency_of_slash_containing_tuples(self, tuples_from_all_sheets):
        validation_messages = []
        for word, transcription in tuples_from_all_sheets:
            # Если word содержит слеш с учётом того, что имеется список исключений допустимости слеша в слове
            # if '/' in word and any(sub not in word for sub in ['sie/Sie ']):
            if '/' in word:
                word_slashed_parts = word.split('/')
                transcription_slashed_parts = transcription.split('/')
                if len(word_slashed_parts) != len(transcription_slashed_parts):
                    validation_messages.append(
                        f"Excel word '{word}' and its transcription have mismatching number of slashes!")

                # Количество пробелов в каждой slashed part должно быть одинаковым. На практике это чаще всего означает,
                # что у существительного с обеих сторон от слеша должен присутствовать артикль.
                # Должно быть так: "die Worte / die Wörter", но никак не "die Worte / Wörter"
                # Подсчёт количества пробелов с использованием трюка сохранения каждого результата в set
                space_counts_set = {word_slashed_part.strip().count(' ') for word_slashed_part in word_slashed_parts}
                # при len(space_counts_set) == 1 все строки имеют одинаковое количество пробелов
                if len(space_counts_set) != 1:
                    validation_messages.append(
                        f"Excel word '{word}' has mismatching number of spaces in its slash-separated parts!")

        return validation_messages


############################################

valid_tuples = [
    ("des Hofs / des Hofes", "[hoːfs] / [ˈhoːfəs]"),
    ("die Worte / die Wörter", "[ˈvɔʁtə] / [ˈvœʁtɐ]")
]

buggy_tuples = [
    ("des Hofs / des Hofes", "[hoːfs]"),  # намеренная ошибка в транскрипции: отсутствует слеш и 2-я часть
    ("die Worte / Wörter", "[ˈvɔʁtə] / [ˈvœʁtɐ]")  # намеренная ошибка в слове: отсутствует артикль после слеша
]

if __name__ == '__main__':
    slashContainingCellSplitter = SlashContainingCellSplitter()

    results = slashContainingCellSplitter.split_by_slash(valid_tuples)
    for r in results:
        print(r)

    results = slashContainingCellSplitter.split_by_slash(buggy_tuples)
    for r in results:
        print(r)
