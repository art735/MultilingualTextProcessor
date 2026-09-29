import AppContext
from FilenameUtils import FilenameUtils
from OdtFileTableDao import OdtFileTableDao, TableRowsToAnkiCardsMode
from View_enums import VocabFileComboBoxEnum, PortraitFileComboBoxEnum, CurrentLanguageComboBoxEnum


# Проверяет соответствие содержимого 5-столбцового [Vocab]-файла содержимому 3-столбцового portrait-файла.
# Здесь: 3-столбцовый файл - это отполированный эталлон, а 5-столбцовый [Vocab]-файл - это то, что должно быть проверено
# на соответствие эталлону.
# Дело в том, что при учёбе 3-столбцовой версии 5-столбцового Vocab-файла неизбежно возникают различные корректировки,
# улучшения и исправления. Затем эти исправления из распечатки одновременно вносятся в электронную версию
# и 3-столбцового файла, и в оригинальный 5-столбцовый Vocab-файл.
# Однако в силу человеческого фактора иногда получается так, что исправления по ошибке вносятся неконсистентно
# в эти оба файла и нужен валидатор, который бы подстраховывал в этом вопросе.
class A060_VocabFileAgainstPortraitFileValidator:
    def __init__(self):
        self.odtFileTableDao = OdtFileTableDao()
        self.filenameUtils = FilenameUtils()

    def validate(self, vocab_lookup_selection: VocabFileComboBoxEnum,
                 portrait_lookup_selection: PortraitFileComboBoxEnum):

        # Вычитываем содержимое [Vocab]-файла(-ов) согласно выбранной на UI опции
        vocab_table_rows_as_anki_card_entities = []
        if vocab_lookup_selection == VocabFileComboBoxEnum.ALL_VOCAB_FILES:
            vocab_table_rows_as_anki_card_entities = self.odtFileTableDao.convert_table_rows_to_anki_cards(
                vocab_files=TableRowsToAnkiCardsMode.ALL_FILES, read_words=True, read_sentences=True)
        elif vocab_lookup_selection == VocabFileComboBoxEnum.LAST_VOCAB_FILE:
            vocab_table_rows_as_anki_card_entities = self.odtFileTableDao.convert_table_rows_to_anki_cards(
                vocab_files=TableRowsToAnkiCardsMode.LAST_FILE, read_words=True, read_sentences=True)

        # Определяемся со списком имён portrait-файлов
        portrait_filenames = []
        if portrait_lookup_selection == PortraitFileComboBoxEnum.ALL_PORTRAIT_FILES:
            portrait_filenames = self.filenameUtils.get_all_portrait_filenames()
        else:
            portrait_filenames.append(portrait_lookup_selection)

        non_matching_results_dict = {}
        cards_not_found_in_vocab_files = []

        # Цикл по списку имён portrait-файлов
        for portrait_filename in portrait_filenames:
            portrait_table_rows_as_anki_card_entities = (self.odtFileTableDao
            .convert_table_rows_to_anki_cards_of_single_file(
                portrait_filename, read_words=True, read_sentences=True))
            # Цикл по строкам-псевдо-карточкам в пределах одного portrait-файла
            for portrait_card in portrait_table_rows_as_anki_card_entities:
                portrait_card_front_str = ';'.join(portrait_card.front)
                # Проверяем, чтобы поле Front портретной карточки совпало с полем Front одной из vocab-карточек
                vocab_card = self._search_corresponding_vocab_card(portrait_card,
                                                                   vocab_table_rows_as_anki_card_entities)
                if vocab_card:
                    # Создаём строковое представление карточек для их дальнейшего сравнения между собой
                    portrait_card_str = portrait_card.to_str("front_transcription_back_with_comments")
                    vocab_card_str = vocab_card.to_str("front_transcription_back_with_comments")

                    non_matching_card_fields = []
                    # Если карточки не совпали - выясняем в каких именно полях
                    if vocab_card_str != portrait_card_str:
                        if portrait_card.front_comment != vocab_card.front_comment:
                            non_matching_card_fields.append('front_comment')
                        if portrait_card.transcription != vocab_card.transcription:
                            non_matching_card_fields.append('transcription')
                        if portrait_card.back != vocab_card.back:
                            non_matching_card_fields.append('back')
                        if portrait_card.back_comment != vocab_card.back_comment:
                            non_matching_card_fields.append('back_comment')

                        if len(non_matching_card_fields) > 0:
                            non_matching_results_dict[portrait_card_front_str] = ', '.join(non_matching_card_fields)
                else:
                    cards_not_found_in_vocab_files.append(portrait_card_front_str)

        output = ''
        # Если какие-то портретные карточки не нашлись в vocab-файлах - это серьёзная ошибка, такого вообще быть
        # не должно. Выводим список этих ненайдёнышей.
        if cards_not_found_in_vocab_files:
            output += f'Cards not found in vocab files:\n'
            output += '\n'.join(cards_not_found_in_vocab_files)

        if non_matching_results_dict:
            output += f'\nThe following rows in [Vocab]-file need to be corrected according to the corresponding rows in [Portrait]-file:\n'
            for card_front_str, non_matching_card_fields_str in non_matching_results_dict.items():
                output += f'{card_front_str}: {non_matching_card_fields_str}\n'

        output = output.strip()  # удаляет символы [ \t\n\r\f\v] в начале и конце строки

        if not output:
            output = 'ok'

        return output

    def _search_corresponding_vocab_card(self, portrait_card, vocab_cards):
        result = None
        for vocab_card in vocab_cards:
            if portrait_card.front == vocab_card.front:
                result = vocab_card
                break

        return result


################################################

if __name__ == '__main__':
    language = CurrentLanguageComboBoxEnum.GERMAN.value
    # language = CurrentLanguageComboBoxEnum.MODERN_GREEK.value
    # language = CurrentLanguageComboBoxEnum.ANCIENT_GREEK.value
    AppContext.switch_language(language)

    a060_VocabFileAgainstPortraitFileValidator = A060_VocabFileAgainstPortraitFileValidator()

    vocab_lookup_selection = VocabFileComboBoxEnum.ALL_VOCAB_FILES
    # portrait_lookup_selection = r'E:\Languages\Deutsch\Goethe-Institut\A1\Cc-Dd (portrait).odt'
    portrait_lookup_selection = PortraitFileComboBoxEnum.ALL_PORTRAIT_FILES

    # vocab_lookup_selection = 'Last [Vocab]-file'
    # portrait_lookup_selection = r'E:\Languages\Deutsch\Goethe-Institut\A1\Gg\Gg (portrait).odt'

    output = a060_VocabFileAgainstPortraitFileValidator.validate(vocab_lookup_selection, portrait_lookup_selection)
    print(output)
