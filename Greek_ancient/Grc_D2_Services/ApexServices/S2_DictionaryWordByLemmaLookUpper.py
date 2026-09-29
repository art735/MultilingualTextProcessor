from DictionaryService import DictionaryService
from LowerServices.GrcConstants import NEWLINE
from ProcessingLemmaService import ProcessingLemmaService
from VocabularyService import VocabularyService


class S2_DictionaryWordByLemmaLookUpper:
    def __init__(self):
        self.dictionaryService = DictionaryService()
        self.vocabularyService = VocabularyService()
        self.processingLemmaService = ProcessingLemmaService()

    def look_up(self, input_lines):
        results = []

        # Временный словарь
        lemma_counter_dict = {}  # key - lemma; value - counter

        entities, incorrectly_formatted_lines = self.processingLemmaService.parse_input_lines(input_lines)

        for entity in entities:
            # res = ''

            # в результатах работы метода дублируем два поля из 1-го этапа, чтобы было супер понятно с какой строкой
            # выполнялась работа и какой результат был достигнут
            res_first_part = f'{entity.counter}|{entity.lemma}||'

            # работаем позитивно только с той леммой, которая ещё не встречалась
            if entity.lemma not in lemma_counter_dict:
                # Запоминаем во временный словарь пару {лемма:счётчик}, с которой работаем
                lemma_counter_dict[entity.lemma] = entity.counter
                dictionary_entity = self.dictionaryService.look_up_by_lemma(entity.lemma)

                # Амбивалентная (двусмысленная) лемма - это лемма, по которой на первом шаге
                # мнения CLTK и eBible разошлись и пользователь должен выбрать вручную один из этих двух вариантов.
                # Если победил вариант леммы от eBibleLexicon (а не CLTK), то словоформу нужно включить в vocabulary
                if entity.is_lemma_ambivalent_and_offered_by_eBibleLexicon():
                    # если в vocabulary такая словарная статья уже есть, ...
                    if self.vocabularyService.is_word_among_lemmas(entity.lemma):
                        # ... но у неё ещё нет такой словоформы - нужно об этом сообщить!"
                        if not self.vocabularyService.is_word_among_morph_forms(entity.token):
                            res = f"Token '{entity.token}' should be added to morph forms of the existing vocabulary article under lemma '{entity.lemma}'"
                        else:  # в vocabulary такая словарная статья уже есть и, более того, среди её морф. форм уже есть рассматриваемый токен
                            res = ''
                    # значит в vocabulary ещё нет такой словарной статьи, во 2-ю позицию/колонку (морфологические формы) прописываем токен
                    else:
                        # res_dictionary_part = dictionary_entity.to_str_using_outer_morph_form(entity.token)
                        res_dictionary_part = str(dictionary_entity)
                        res = res_first_part + res_dictionary_part
                else:
                    # res = f'{entity.counter}|{entity.lemma}||{dictionary_entity}'
                    res_dictionary_part = str(dictionary_entity)
                    res = res_first_part + res_dictionary_part
            else:  # иначе говорим о том, что лемма уже встречалась в такой-то строке
                lemma_counter = lemma_counter_dict[entity.lemma]
                res = res_first_part + f"Такая лемма уже обработана в строке № {lemma_counter}"

            if len(res):
                results.append(res)
        # end of loop

        output = NEWLINE.join(results)

        if len(incorrectly_formatted_lines) > 1:
            wrong_lines_output = NEWLINE.join(incorrectly_formatted_lines)
            output += wrong_lines_output

        if len(output) == 0:
            output = "Nothing to process!"

        return output


######################################################################

# input_lines = """
# 1|ἀρχὴ|ἀρχή|100%
# 2|τοῦ|ὁ|100%
# 3|εὐαγγελίου|εὐαγγέλιον|100%
# 4|ἰησοῦ|ἰησοῦς|100%
# 5|χριστοῦ|χριστός|100%
# 6|υἱοῦ|υἱός|100%
# 7|θεοῦ|θεός|100%
# 8|ἄγγελος|ἄγγελος|100%
# """

# input_lines = """
# 4|ἰησοῦ|ἰησοῦς|100%
#
# 1|ἀρχὴ|ἀρχή|100%
#
# 3|εὐαγγελίου|εὐαγγέλιον|100%
# 2|τοῦ|ὁ|100%
#
# 7|θεοῦ|θεός|100%
# 8|ἄγγελος|ἄγγελος|100%
# 5|χριστοῦ|χριστός|100%
# 6|υἱοῦ|υἱός|100%
# """

# input_lines = """
# 1|ἀρχὴ|ἀρχή|100%
# 2|τοῦ|ὁ
# τοῦἀρχή
# """

# input_lines = """
# 1|εὐαγγέλιον|εὐαγγέλιον|100%
# 2|εὐαγγελίου|εὐαγγέλιον|100%
# 3|ἰησοῦς|ἰησοῦς|100%
# 4|ἰησοῦ|ἰησοῦς|100%
# 5|χριστός|χριστός|100%
# 6|χριστοῦ|χριστός|100%
# """
#
# input_lines = """
# 3|ἰησοῦς|ἰησοῦς|100%
# 1|εὐαγγέλιον|εὐαγγέλιον|100%
# 2|εὐαγγελίου|εὐαγγέλιον|100%
# 5|χριστός|χριστός|100%
# 4|ἰησοῦ|ἰησοῦς|100%
# 6|χριστοῦ|χριστός|100%
# """

# input_lines = """
# 3|ἰησοῦς|ἰησοῦς
# 1|εὐαγγέλιον2|εὐαγγέλιον|100%
# 2|εὐαγγελίου|εὐαγγέλιον|100%
# χριστός|χριστός|100%
# 4|ἰησοῦ|ἰησοῦς|100%
# 6|χριστοῦ|χριστός|100%
# """

input_lines = """
6|χριστοῦ|χριστός|100%
2|εὐαγγελίου|εὐαγγέλιον|100%
5|χριστός|χριστός|100%

"""

# input_lines = """
# 4 | ἰησοῦ | ἰησοῦς | CLTK – ἰασός; eBibleLexicon – ἰησοῦς
# """

# input_lines = """
# 1Ἀρχὴ τοῦ εὐαγγελίου Ἰησοῦ Χριστοῦ [υἱοῦ θεοῦ].
# 2Καθὼς γέγραπται ἐν τῷ Ἠσαΐᾳ τῷ προφήτῃ·ἰδοὺ ἀποστέλλω τὸν ἄγγελόν μου πρὸ προσώπου σου, ὃς κατασκευάσει τὴν ὁδόν σου·
# """

input_lines = """
# | TOKEN | LEMMA | VERDICT
__________________________________________________
- - -
1 | ἀρχὴ | ἀρχή | 100%
2 | τοῦ | ὁ | 100%
3 | εὐαγγελίου | εὐαγγέλιον | 100%
4 | ἰησοῦ | ἰησοῦς | 100%
5 | χριστοῦ | χριστός | 100%
6 | υἱοῦ | υἱός | 100%
7 | θεοῦ | θεός | 100%
8 | κύριε | κύριος | 100%
9 | χριστέ | χριστός | 100%
10 | ἐλέησόν | ἐλεέω | 100%
11 | με | ἐγώ | 100%
"""

if __name__ == '__main__':
    s2_DictionaryWordByLemmaLookUpper = S2_DictionaryWordByLemmaLookUpper()
    out = s2_DictionaryWordByLemmaLookUpper.look_up(input_lines)
    print(out)
