import re

import GrcRegExFinder
from GrcRegExFinder import GrcRegExFinder

COMMA = ','
SPACE = ' '


# main entity
class EBibleLexiconEntity:
    def __init__(self, lemma, lemma_occurrences_count, morphological_forms_str, word_article, translation):

        self.grcRegExFinder = GrcRegExFinder()

        # TODO добавить в присвоении каждому полю вызов метода strip() (для удаления случайных пробелов) ???
        # self.word = word.lower()
        # self.word_case_backup = word # сохранить первоначальный регистр букв слова: Charles (с большой буквы); USA (все буквы большие)
        self.lemma: str = lemma.lower()  # слово "как есть" с сохранением первоначального регистра букв
        # если пользователь забыл вбить кол-во раз, кот. лемма встречалась, нужно сделать так, чтобы код не падал
        # если в ячейке значение пустое, считать, что лемма встречалась -1 раз
        # self.lemma_occurrences_count: int = int(lemma_occurrences_count) if len(str(lemma_occurrences_count)) else -1
        self.lemma_occurrences_count: int = int(lemma_occurrences_count)
        self.morphological_forms: list[InternalMorphFormEntity] = self.parse_morphological_forms(
            morphological_forms_str)
        self.word_article: str = word_article
        self.translation: str = re.sub(r'\n', r'^^^', str(translation))

    def parse_morphological_forms(self, morphological_forms_str):
        result = list()
        # Сюда приходит строка вида ἀγανακτεῖν 1, ἀγανακτοῦντες 1, ἀγανακτῶν 1, ἠγανάκτησαν 3, ἠγανάκτησεν 1
        for comma_separated_piece in morphological_forms_str.split(','):
            single_morph_record = self.process_single_morph_record(comma_separated_piece)
            result.append(single_morph_record)

        return result

    def process_single_morph_record(self, morph_record):
        # формат данных в файле "eBible lexicon.xls": здесь для каждой морфологической формы указано количество раз,
        # которые она встречается в Библии
        result = InternalMorphFormEntity()
        # Сюда приходит строка вида 'ἀγανακτεῖν 1'
        if SPACE in morph_record:  # формат
            morph_pieces = [csp.strip() for csp in morph_record.split(SPACE) if csp]
            if len(morph_pieces) == 2:
                morph_word = morph_pieces[0]
                morph_word_count = morph_pieces[1]
                if self.grcRegExFinder.is_greek_word(morph_word) and morph_word_count.isdigit():
                    result = InternalMorphFormEntity(morph_word, morph_word_count)

        return result

    def has_entity_given_morph_form(self, mf_to_find):
        for mf in self.morphological_forms:
            if mf.morph_word == mf_to_find:
                return True
        return False

    def __str__(self):
        morphological_forms_str = ", ".join([str(mf) for mf in self.morphological_forms if len(mf.morph_word)])
        return f'{self.lemma}|{morphological_forms_str}|{self.word_article}|{self.translation}'

    def __hash__(self):
        return hash(self.lemma)

    def __eq__(self, other):
        return (
                self.__class__ == other.__class__ and
                self.lemma == other.lemma
        )


###########################################################################

class InternalMorphFormEntity:
    def __init__(self, morph_word=None, morph_word_count=None):
        # Логика для конструктора без параметров
        if morph_word is None and morph_word_count is None:
            self.morph_word = ''
            self.morph_word_count = 0
        # Логика для конструктора с двумя параметрами
        else:
            self.morph_word: str = morph_word.lower()
            self.morph_word_count: int = morph_word_count

    def __str__(self):
        return f'{self.morph_word} {self.morph_word_count}'

    def __hash__(self):
        return hash(self.morph_word)

    def __eq__(self, other):
        return (
                self.__class__ == other.__class__ and
                self.morph_word == other.morph_word
        )
