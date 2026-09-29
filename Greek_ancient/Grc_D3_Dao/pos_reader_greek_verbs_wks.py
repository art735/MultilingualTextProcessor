import ExcelDaoUtils


# def _stripPersonalPronouns(tuples):
#     result = list()
#     for raw_verb, transcription in tuples:
#         bare_verb = re.sub(r'^((dass\s)?(ich|du|er|er/sie/es|wir|ihr|sie))\s', '', raw_verb)
#         bare_verb = re.sub(r'\s(\(du\)|\(ihr\))$', '', bare_verb)
#         result.append(tuple([bare_verb, transcription]))
#     return result


def get_tuples(verbs_worksheet):
    verbs_worksheet_indices = [[0, 1],  # greek verbs and its russian traslation
                               [3, 4],  # aoristic aspect
                               [6, 7],  # imperfective aspect
                               [9, 10]  # perfective aspect
                               ]

    verbs_worksheet_tuples = ExcelDaoUtils.getWorksheetData(verbs_worksheet, verbs_worksheet_indices)
    # bare_verbs_worksheet_tuples = _stripPersonalPronouns(verbs_worksheet_tuples)
    return verbs_worksheet_tuples
