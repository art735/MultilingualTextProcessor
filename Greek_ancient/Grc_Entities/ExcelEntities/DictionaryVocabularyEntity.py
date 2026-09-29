import re


class DictionaryVocabularyEntity:
    def __init__(self, lemmas_str, morphological_forms_str, word_article, translation):
        # TODO добавить в присвоении каждому полю вызов метода strip() (для удаления случайных пробелов) ???
        # lemmas_str - это список лемм через запятую из 1-го столбца одной и той же словарной статьи
        # программа должна допускать возможность существования и обработки нескольких лемм для одного и того же слова:
        # это связано как с историческими особенностями древнегреческого языка (отличие в написании слова в разных
        # диалектах), так и с особенностями работы CLTK, которая, например, для имени "Иоанн" даёт лемму Ιωάν(ν)ης.
        # Получается, что для корректной работы алгоритмов приложения у этого слова должен быть
        # следующий список лемм: Ιωάν(ν)ης, Ιωάνης, Ιωάννης
        self.lemmas_str: str = lemmas_str.lower()
        self.lemmas: list = [lemma.strip().lower() for lemma in lemmas_str.split(',') if len(lemma)]

        self.morphological_forms_str: str = morphological_forms_str
        self.morphological_forms: list = self.parse_morphological_forms(morphological_forms_str)

        self.word_article: str = word_article
        self.translation: str = re.sub(r'\n', r'^^^', str(translation))

    def parse_morphological_forms(self, morphological_forms_str):
        result = list()
        for comma_separated_piece in morphological_forms_str.split(','):
            # single_morph_record = self.process_single_morph_record(comma_separated_piece)
            result.append(comma_separated_piece)
        return result

    def __str__(self):
        return f'{self.lemmas_str}|{self.morphological_forms_str}|{self.word_article}|{self.translation}'

    def __hash__(self):
        return hash(self.lemmas_str)

    def __eq__(self, other):
        return (
                self.__class__ == other.__class__ and
                self.lemmas_str == other.lemmas_str
        )
