from FrontAndTranscriptionEntity import FrontAndTranscriptionEntity


class GermanVerbConjugationEntity:
    def __init__(self):
        self.infinitive: str = ''
        self.transcription: str = ''
        self.translation: str = ''

        self.präsens: FrontAndTranscriptionEntity = FrontAndTranscriptionEntity()
        self.präteritum: FrontAndTranscriptionEntity = FrontAndTranscriptionEntity()

        self.konjunktiv_I: FrontAndTranscriptionEntity = FrontAndTranscriptionEntity()
        self.konjunktiv_II: FrontAndTranscriptionEntity = FrontAndTranscriptionEntity()

        # TODO Оставить partizip_I изолированной формой или сделать infinitive_partizip_I ???
        self.partizip_I = FrontAndTranscriptionEntity()
        self.infinitiv_partizip_II = FrontAndTranscriptionEntity()

        self.imperativ: FrontAndTranscriptionEntity = FrontAndTranscriptionEntity()

    # Пример использования в вызывающем коде:
    # print("Präsens:\n", german_verb.conjugation_to_str(german_verb.präsens))
    def conjugation_to_str(self, tense: FrontAndTranscriptionEntity):
        return tense.to_str()
