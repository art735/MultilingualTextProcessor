import AppContext
from OdtFileTableDao import OdtFileTableDao, TableRowsToAnkiCardsMode
from View_enums import CurrentLanguageComboBoxEnum


# Делает из 5-столбцового Vocab-файла 3-столбцовую версию для печати и учёбы, перемещая комментарии из 2-го и 5-го
# столбцов (front_comment и back_comment) в 1-й и 3-й соответственно
class A050_Printable3ColVersionOfLastVocabFileComposer:

    def __init__(self):
        self.odtFileTableDao = OdtFileTableDao()

    def compose_3col_version(self):
        table_rows_as_anki_card_entities = self.odtFileTableDao.convert_table_rows_to_anki_cards(
            vocab_files=TableRowsToAnkiCardsMode.LAST_FILE, read_words=True, read_sentences=True,
            ignore_empty_rows=False)

        results = []
        for table_row_as_anki_card_entity in table_rows_as_anki_card_entities:
            entity_str = table_row_as_anki_card_entity.to_str(format_type="front_transcription_back_with_comments")
            front, front_comment, transcription, back, back_comment = entity_str.split('|')

            col1st = front
            if front_comment:
                # двойной слеш в комментарии уже присутствует
                col1st += '^^^^^' + front_comment

            col2nd = transcription

            col3rd = back
            if back_comment:
                col3rd += '^^^^^* * *^^^^^' + back_comment

            result = col1st + '|' + col2nd + '|' + col3rd
            results.append(result)

        output = '\n'.join(results)
        return output


################################################

if __name__ == '__main__':
    language = CurrentLanguageComboBoxEnum.GERMAN.value
    # language = CurrentLanguageComboBoxEnum.MODERN_GREEK.value
    # language = CurrentLanguageComboBoxEnum.ANCIENT_GREEK.value
    AppContext.switch_language(language)

    a050_Printable3ColVersionOfLastVocabFileComposer = A050_Printable3ColVersionOfLastVocabFileComposer()
    res = a050_Printable3ColVersionOfLastVocabFileComposer.compose_3col_version()
    print(res)
