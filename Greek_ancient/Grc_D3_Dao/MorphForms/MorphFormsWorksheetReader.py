from Base.BaseWorksheetReader import BaseWorksheetReader
from ExcelEntities.MorphFormVocabularyEntity import MorphFormVocabularyEntity


class MorphFormsWorksheetReader(BaseWorksheetReader):

    def __init__(self):
        columns_dict = {
            0: 'KEY_MORPH_FORM_COLUMN_INDEX',
            1: 'MORPH_FORMS_DASHED_SEQUENCE',
            2: 'GRAMMATICAL_HINT_UNDER_TRANSLATION'
        }
        super().__init__(columns_dict)

    def get_data_from_worksheet(self, worksheet):
        sheet_data = super().get_data_from_worksheet(worksheet)

        # KEY - lemma
        # VALUE - all the consecutive Excel rows related to KEY
        result = []
        for row in sheet_data:
            token_grammaticized = row[0]
            morph_forms_dashed_sequence = row[1]
            grammatical_hint_under_translation = row[2]
            result.append(MorphFormVocabularyEntity(token_grammaticized, morph_forms_dashed_sequence,
                                                    grammatical_hint_under_translation))

        return result
