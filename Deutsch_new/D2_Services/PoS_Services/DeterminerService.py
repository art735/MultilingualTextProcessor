from BasePosService import BasePosService


class DeterminerService(BasePosService):

    def __init__(self):
        super().__init__()

    def get_lemma(self, spaCy_lemma, morph):
        result = ''

        # pronominal_type = self.morphologyParser.parse(morph, "PronType")
        #
        # match pronominal_type:
        #     case 'Ind':  # indefinite pronoun
        #         result = self._process_indefinite_pronoun(spaCy_lemma)

        return result


################################################

if __name__ == '__main__':
    determinerService = DeterminerService()
