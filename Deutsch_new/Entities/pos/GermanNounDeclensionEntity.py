class GermanNounDeclensionEntity:
    def __init__(self):
        self.word: str = ''
        self.transcription: str = ''
        self.translation: str = ''

        # словарь падежных форм слова и их транскрипций; key - падежная форма слова, value - транскрипция
        self.declensions_dict = dict()

    def find_transcription(self, articled_noun_form):
        transcription = ''
        if articled_noun_form == self.word:
            transcription = self.transcription
        elif articled_noun_form in self.declensions_dict:
            transcription = self.declensions_dict[articled_noun_form]
        return transcription

    def __str__(self):
        translation_str = self.translation.replace('\n', '^^^')
        first_line = f'{self.word}|{self.transcription}|{translation_str}\n'
        second_line = f'\t{self.declensions_dict}\n'
        return first_line + second_line
