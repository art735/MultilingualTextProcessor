import re

import ExcelDaoUtils


def _stripSuperlativeAdjectives(tuples):
    result = list()
    for raw_adjective, transcription in tuples:
        bare_adjective = re.sub(r'^am\s', '', raw_adjective)
        result.append(tuple([bare_adjective, transcription]))
    return result


def get_tuples(adjectives_worksheet):
    adjectives_worksheet_indices = [[0, 1], [4, 5], [6, 7],
                                    [9, 10], [11, 12], [13, 14], [15, 16],  # der Positiv
                                    [18, 19], [20, 21], [22, 23], [24, 25],  # der Komparativ
                                    [27, 28], [29, 30], [31, 32], [33, 34]  # der Superlativ
                                    ]
    adjectives_worksheet_tuples = ExcelDaoUtils.getWorksheetData(adjectives_worksheet, adjectives_worksheet_indices)
    bare_adjectives_worksheet_tuples = _stripSuperlativeAdjectives(adjectives_worksheet_tuples)
    return bare_adjectives_worksheet_tuples
