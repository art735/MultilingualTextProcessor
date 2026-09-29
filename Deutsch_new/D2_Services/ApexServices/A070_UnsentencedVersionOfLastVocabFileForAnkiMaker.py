import AppContext
from OdtFileTableDao import OdtFileTableDao, TableRowsToAnkiCardsMode
from View_enums import CurrentLanguageComboBoxEnum


class A070_UnsentencedVersionOfLastVocabFileForAnkiMaker:

    def __init__(self):
        self.odtFileTableDao = OdtFileTableDao()

    def print_vocabulary(self):
        table_rows_as_anki_card_entities = self.odtFileTableDao.convert_table_rows_to_anki_cards(
            vocab_files=TableRowsToAnkiCardsMode.LAST_FILE)

        results = []
        for table_row_as_anki_card_entity in table_rows_as_anki_card_entities:
            result = table_row_as_anki_card_entity.to_str(format_type="front_transcription_back_with_comments")
            results.append(result)

        output = '\n'.join(results)
        return output


##################################################################

if __name__ == '__main__':
    language = CurrentLanguageComboBoxEnum.GERMAN.value
    # language = CurrentLanguageComboBoxEnum.MODERN_GREEK.value
    # language = CurrentLanguageComboBoxEnum.ANCIENT_GREEK.value
    AppContext.switch_language(language)

    a070_UnsentencedVersionOfLastVocabFileForAnkiMaker = A070_UnsentencedVersionOfLastVocabFileForAnkiMaker()
    res = a070_UnsentencedVersionOfLastVocabFileForAnkiMaker.print_vocabulary()
    print(res)
