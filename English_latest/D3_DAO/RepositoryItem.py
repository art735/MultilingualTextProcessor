import re

TRANSCRIPTION_FIELD_NAME = 'transcription'
TRANSLATION_FIELD_NAME = 'translation'
MORPHOLOGICAL_FORMS_FIELD_NAME = 'morphological_forms'


class RepositoryItem:
    def __init__(self, word, transcription, translation, morphological_forms=None):
        # TODO добавить в присвоении каждому поля вызов метода strip() (для удаления случайных пробелов) ???
        # self.word = word.lower()
        # self.word_case_backup = word # сохранить первоначальный регистр букв слова: Charles (с большой буквы); USA (все буквы большие)
        self.word = word  # слово "как есть" с сохранением первоначального регистра букв
        self.transcription = transcription
        self.translation = translation

        if morphological_forms:
            self.morphological_forms = morphological_forms
        else:
            self.morphological_forms = []

    def add_morphological_forms(self, morphological_tuples):
        for morphological_tuple in morphological_tuples:
            self.add_morphological_form(morphological_tuple)

    def add_morphological_form(self, morphological_tuple):
        # не пропускать в словарь пустые кортежи ('', '')
        if any(morphological_tuple):  # If the iterable object is empty, the any() function will return False.
            self.morphological_forms.append(morphological_tuple)

    def convert_morphological_forms_to_str(self):
        string_tuples = list()
        for tup in self.morphological_forms:
            tup_str = "{0} {1}".format(tup[0], tup[1])
            string_tuples.append(tup_str)

        result = '; '.join(string_tuples)
        return result.strip()

    def __str__(self):
        # pieces = [self.word_case_backup, self.transcription, re.sub(r'\n', '^^^', self.translation)]
        word_str = re.sub(r'\n', '^^^', self.word) if '\n' in self.word else self.word
        transcription_str = re.sub(r'\n', '^^^',
                                   self.transcription) if '\n' in self.transcription else self.transcription
        translation_str = re.sub(r'\n', '^^^', self.translation) if '\n' in self.translation else self.translation

        pieces = [word_str, transcription_str, translation_str]
        morph_forms_str = self.convert_morphological_forms_to_str()
        if len(morph_forms_str) > 0:
            pieces.append(morph_forms_str)

        return "*".join(pieces)

    def __hash__(self):
        return hash(self.word)

    def __eq__(self, other):
        return (
                self.__class__ == other.__class__ and
                self.word == other.word
        )

    # equals сравнивает только по одному полю, а данный метод в юнит-тестах сравнивает все поля!
    def compare_all_fields(self, other):
        return self.word == other.word and \
            self.transcription == other.transcription and \
            self.translation == other.translation and \
            self.morphological_forms == other.morphological_forms

###############################################

# item = RepositoryItem("child", "child".isupper(), "[ʧaɪld]", "ребёнок", [("children", "['ʧɪldr(ə)n]")])
# print(item)
