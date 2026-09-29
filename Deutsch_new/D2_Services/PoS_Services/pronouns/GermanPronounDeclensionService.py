from GermanPronounDeclensionDao import GermanPronounDeclensionDao


class GermanPronounDeclensionService:

    def __init__(self):
        self.germanPronounDeclensionDao = GermanPronounDeclensionDao()
        self.pronoun_entities = self.germanPronounDeclensionDao.convert_excel_rows_to_entities()

    def get_pronoun_declension(self, pronoun_lemma):

        if pronoun_lemma == 'sie':
            fr1, tr1 = self._get_pronoun_declension_inner('sie (sg.)')
            fr2, tr2 = self._get_pronoun_declension_inner('sie (pl.)')
            front = '^^^^^'.join([fr1, fr2])
            transcription = '^^^^^'.join([tr1, tr2])
        else:
            front, transcription = self._get_pronoun_declension_inner(pronoun_lemma)

        return front, transcription

    def _get_pronoun_declension_inner(self, pronoun_lemma):
        front = f"!!! Declension of pronoun_entity '{pronoun_lemma}' is not found !!!"
        transcription = ''

        for pronoun_entity in self.pronoun_entities:
            if pronoun_entity.lemma == pronoun_lemma:
                front, transcription = pronoun_entity.declension_to_str().split('|')
                return front, transcription

        return front, transcription


####################################

if __name__ == '__main__':
    germanPronounDeclensionService = GermanPronounDeclensionService()

    # pronoun = 'ich'
    # pronoun = 'mein'
    # pronoun = 'jeder'
    pronoun = 'sie'

    front, transcription = germanPronounDeclensionService.get_pronoun_declension(pronoun)
    # print(front)
    # print(transcription)
    res = front + "|" + transcription
    print(res)
