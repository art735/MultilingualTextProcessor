import GermanPronounHelper
import ExcelDaoUtils

verbs_worksheet_indices = [[0, 1], [4, 5], [6, 7], [9, 10], [11, 12],
                           [14, 15], [16, 17], [18, 19],  # Partizip I & Partizip II
                           [18, 19]
                           ]  # zu-infinitive


def get_tuples(verbs_worksheet):
    bare_verbs_worksheet_tuples = []
    verbs_worksheet_tuples = ExcelDaoUtils.getWorksheetData(verbs_worksheet, verbs_worksheet_indices)
    for raw_verb, transcription in verbs_worksheet_tuples:
        tup = tuple([GermanPronounHelper.strip_all_possible_personal_pronouns_around_verb(raw_verb), transcription])
        bare_verbs_worksheet_tuples.append(tup)

    return bare_verbs_worksheet_tuples
