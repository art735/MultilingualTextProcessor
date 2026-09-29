from GermanExcelForAnkiDao import GermanExcelForAnkiDao

SEPARATOR = "\n\n********************\n\n"


class ExcelToAnkiVerbService:
    def __init__(self):
        self.germanExcelForAnkiDao = GermanExcelForAnkiDao()

    def get_forms_for_verbs(self, input_text):
        return self._get_verb_forms(input_text, self.germanExcelForAnkiDao.get_verbs_for_anki)

    def get_forms_for_awesome_tts(self, input_text):
        return self._get_verb_forms(input_text, self.germanExcelForAnkiDao.get_verbs_for_awesome_tts)

    def _get_verb_forms(self, input, callback):
        found_verbs = []

        verbs_dict = callback()

        verbs_to_search = input.split()

        for verb in verbs_to_search:
            if verb in verbs_dict:
                found_verbs.append(verbs_dict[verb])
            else:
                message = f"!!! Verb '{verb}' not found in Excel !!!".format(verb)
                found_verbs.append(message)

        output = SEPARATOR.join(found_verbs)
        return output


###################################

input_str = "sein     heißen \n\n\n\n wohnen   \n"
input_str = "arbeiten"
input_str = " aaa  sein  "
input_str = "schreiben"
input_str = "gelten"  # слово из другой Excel-книги: Politik

if __name__ == '__main__':
    excelToAnkiVerbService = ExcelToAnkiVerbService()

    # res = excelToAnkiVerbService.get_forms_for_verbs(input_str)
    # print(res)

    res = excelToAnkiVerbService.get_forms_for_awesome_tts(input_str)
    print(res)
