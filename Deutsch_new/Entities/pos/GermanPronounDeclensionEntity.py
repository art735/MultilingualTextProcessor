from FrontAndTranscriptionEntity import FrontAndTranscriptionEntity


class GermanPronounDeclensionEntity:
    def __init__(self):
        self.lemma = ''
        self.transcription = ''
        self.translation = ''

        self.declensions: FrontAndTranscriptionEntity = FrontAndTranscriptionEntity()

    # def declension_to_str(self, tense: FrontAndTranscriptionEntity):
    def declension_to_str(self):
        return self.declensions.to_str()
