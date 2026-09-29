class MorphFormVocabularyEntity:
    def __init__(self, token_grammaticized, morph_forms_dashed_sequence, grammatical_hint_under_translation):
        # TODO добавить в присвоении каждому полю вызов метода strip() (для удаления случайных пробелов) ???

        # Ἰησοῦ (sg. gen.)|ὁ Ἰησοῦς - τοῦ Ἰησοῦ|(nom. - gen.)
        # Ἰησοῦ (sg. voc.)|ὁ Ἰησοῦς - Ἰησοῦ!|(nom. - voc.)
        # просто token, например Ἰησοῦ, не может быть уникальным ключом,
        # а token_grammaticized, например Ἰησοῦ (sg. gen.) или Ἰησοῦ (sg. voc.) - может и будет!
        self.token_grammaticized: str = token_grammaticized  # добавить вызов метода .lower() ???, а вызов .strip() ???
        self.morph_forms_dashed_sequence: str = morph_forms_dashed_sequence
        self.grammatical_hint_under_translation: str = grammatical_hint_under_translation

    # def to_pipe_separated_str(self):
    #     morphological_forms_str = ", ".join([str(entity) for entity in self.morphological_forms])
    #
    #     return "{0}|{1}|{2}|{3}|{4}".format(self.lemma, self.lemma_occurrences_count,
    #                                          morphological_forms_str, self.full_word_article, self.translation)

    def __str__(self):
        return f'{self.token_grammaticized}|{self.morph_forms_dashed_sequence}|{self.grammatical_hint_under_translation}'

    def __hash__(self):
        return hash(self.token_grammaticized)

    def __eq__(self, other):
        return (
                self.__class__ == other.__class__ and
                self.token_grammaticized == other.token_grammaticized
        )
