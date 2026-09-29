from GrammarEnums import NumberSpaCy, CaseSpaCy, ConversionMode
from MorphologyParser import MorphologyParser
from GrcDefiniteArticleService import GrcDefiniteArticleService
from N2_NounGrammarConverter import NounGrammarConverter


class DashedArticledNounsComposer:

    # В конструктор передаётся греческий или немецкий nounDefiniteArticleService
    def __init__(self, nounDefiniteArticleService):
        self.nounDefiniteArticleService = nounDefiniteArticleService
        self.nounGrammarConverter = NounGrammarConverter()
        self.morphologyParser = MorphologyParser()

    # параметр noun_declension_entity - объект типа GermanNounDeclensionEntity, который нужен в контексте работы с
    # немецким языком и не нужен в контексте работы с греческим.
    def compose(self, lemma: str, token: str, pos: str, morph, noun_declension_entity=None):
        # инициализация переменных, хранящих возвращаемые значения метода
        dashed_nouns = ''
        grammar_hint = ''
        info_msg = ''

        dashed_pair_of_nouns = '{0} – {1}'
        dashed_pair_of_grammar = f'({dashed_pair_of_nouns})'  # (nom. – gen.), (sg. – du.), (sg. – pl.)

        dashed_triplet_of_nouns = '{0} – {1} – {2}'
        dashed_triplet_of_grammar = '(sg. – {0} nom. – {0} {1})'  # (sg. - du. nom. - du. gen.), (sg. - pl. nom. - pl. acc.)

        yet_unknown_form = '???'

        case = self.morphologyParser.parse(morph, "Case")
        number = self.morphologyParser.parse(morph, "Number")
        # gender = self.morphologyParser.parse(morph, "Gender")

        articled_lemma = self.nounDefiniteArticleService.add_definite_article_to_lemma(lemma, pos, morph)
        articled_token = self.nounDefiniteArticleService.add_definite_article_to_token(token, pos, morph)

        # условие, когда dashed-кластер будет состоять из двух существительных (а не трёх!)
        if ((number == NumberSpaCy.Sing.value and case != CaseSpaCy.Nom.value) or
                (number in [NumberSpaCy.Dual.value, NumberSpaCy.Plur.value] and case == CaseSpaCy.Nom.value)):

            # формируем пару (а не тройку) существительных
            dashed_nouns = dashed_pair_of_nouns.format(articled_lemma, articled_token)

            # формируем грамматику для пары (а не тройки) существительных
            match number:
                case NumberSpaCy.Sing.value:
                    lemma_grammar = 'nom.'
                    token_grammar = self.nounGrammarConverter.convert(morph, ConversionMode.CASE_ONLY)
                case NumberSpaCy.Dual.value:
                    lemma_grammar = 'sg.'
                    token_grammar = 'du.'
                case NumberSpaCy.Plur.value:
                    lemma_grammar = 'sg.'
                    token_grammar = 'pl.'
                case _:
                    lemma_grammar = 'unknown'
                    token_grammar = 'unknown'

            grammar_hint = dashed_pair_of_grammar.format(lemma_grammar, token_grammar)
            # result = dashed_nouns + "|" + grammar_hint
        # в остальных случаях форматируем существительные как ТРОЙКИ значений
        elif number in [NumberSpaCy.Dual.value, NumberSpaCy.Plur.value] and case != CaseSpaCy.Nom.value:
            middle_form_abbr_number = ''
            match number:
                case NumberSpaCy.Dual.value:
                    middle_form_spacy_number = NumberSpaCy.Dual.value
                    middle_form_abbr_number = 'du.'
                case NumberSpaCy.Plur.value:
                    middle_form_spacy_number = NumberSpaCy.Plur.value
                    middle_form_abbr_number = 'pl.'

            # Формируем морф.-объект для middle_form
            middle_form_morph = {}
            middle_form_morph['Number'] = [middle_form_spacy_number]
            middle_form_morph['Case'] = ['Nom']
            middle_form_morph['Gender'] = morph.get('Gender')
            if noun_declension_entity:  # вариант для немецкого языка
                # iter() создаёт итератор по items(), а next() берёт первый элемент.
                # Хронологически в declensions_dict первой добавляется именно форма pl_nom (см. GermanNounDeclensionDao)
                pl_nom_word, pl_nom_transcription = next(iter(noun_declension_entity.declensions_dict.items()))
                articled_middle_form = pl_nom_word
            else:  # вариант для греческого языка
                articled_middle_form = self.nounDefiniteArticleService.add_definite_article_to_token(yet_unknown_form,
                                                                                                     pos,
                                                                                                     middle_form_morph)

            dashed_nouns = dashed_triplet_of_nouns.format(articled_lemma, articled_middle_form, articled_token)

            token_grammar = self.nounGrammarConverter.convert(morph, ConversionMode.CASE_ONLY)
            grammar_hint = dashed_triplet_of_grammar.format(middle_form_abbr_number, token_grammar)
            # result = dashed_nouns + "|" + grammar_hint
        elif number == NumberSpaCy.Sing.value and case == CaseSpaCy.Nom.value:
            info_msg = f"Word '{token}' is in its initial dictionary form (sg. nom.)"
        else:
            info_msg = f"Some strange grammatical number/case situation for token = > '{token}'"

        return dashed_nouns, grammar_hint, info_msg


#########################################

composer = DashedArticledNounsComposer(GrcDefiniteArticleService())

# res = composer.compose('ἄνθρωπος', 'ἀνθρώπου', GenderSpaCy.Masc.value, NumberSpaCy.Sing.value, CaseSpaCy.Gen.value)
# print(res)

# res = composer.compose('ἄνθρωπος', 'ἀνθρώπων', GenderSpaCy.Masc.value, NumberSpaCy.Plur.value, CaseSpaCy.Gen.value)
# print(res)

# res = composer.compose('ὀφθαλμός', 'ὀφθαλμοῖν', GenderSpaCy.Masc.value, NumberSpaCy.Dual.value, CaseSpaCy.Dat.value)
# print(res)

# res = composer.compose('ἄνθρωπος', 'ἄνθρωπος', GenderSpaCy.Masc.value, NumberSpaCy.Sing.value, CaseSpaCy.Nom.value)
# print(res)
