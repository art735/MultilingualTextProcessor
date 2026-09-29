import GrcRegExFinder
import Utils
from GrcRegExFinder import GrcRegExFinder
from CharConstants import PIPE
from DeutschNewConstants import OO_WRITER_STRIPES_DELIMITER
from GrammarEnums import NumberSpaCy, CaseSpaCy, ConversionMode
from MorhpFormsService import MorphFormsService
from MorphologyParser import MorphologyParser
from GrcDefiniteArticleService import GrcDefiniteArticleService
from N2_NounGrammarConverter import NounGrammarConverter
from N3_DashedArticledNounsComposer import DashedArticledNounsComposer
from GrcSpaCyEngineWrapper import GrcSpaCyOrStanzaWrapper
from SpaCyPosResolver import SpaCyPosResolver
from VocabularyService import VocabularyService


class S3_TextInflectionsMaker:

    def __init__(self):
        self.token = ''
        self.token_grammaticized = ''
        self.lemma = ''
        self.pos = ''
        self.morph = ''

        self.gender = ''
        self.number = ''
        self.case = ''

        self.grcSpaCyOrStanzaWrapper = GrcSpaCyOrStanzaWrapper()
        self.vocabularyService = VocabularyService()
        self.morphFormsService = MorphFormsService()

        self.nounGrammarConverter = NounGrammarConverter()
        self.dashedArticledNounsComposer = DashedArticledNounsComposer(GrcDefiniteArticleService())

        self.grcRegExFinder = GrcRegExFinder()
        self.morphologyParser = MorphologyParser()
        self.spaCyPosResolver = SpaCyPosResolver()

        # key - token; value - pair/triplet of nouns with translation and grammar hint
        self.text_results_dict = {}

    def process_whole_text(self, input_text):

        # Проверяем все ли слова в тексте присутствуют в Excel-вокабуляре.
        # Если нет - возвращаем список слов, которые нужно добавить в вокабуляр
        missing_words = self.validate_all_words_are_present_in_vocabulary(input_text)
        if missing_words:
            output = '\n'.join(missing_words)
            return output

        # Результаты работы метода условно делятся на две категории:
        # 1. Морф. формы всего текста для вставки их в Excel
        output_1_Excel_morph_forms_results = []
        # 2. Морф. формы каждого отдельного предложения вместе с самим этим предложением
        output_2_OO_Writer_morph_forms_results = []

        # Разбиваем текст на отдельные предложения (строки, библейские стихи)
        sentences = Utils.split_by(input_text, '\n')  # взять в дальнейшую работу только непустые строки

        for sentence in sentences:
            excel_morph_forms, oo_Writer_morph_forms = self.process_sentence(sentence)
            output_1_Excel_morph_forms_results.append(excel_morph_forms)
            output_2_OO_Writer_morph_forms_results.append(oo_Writer_morph_forms)

        # Просеиваем результирующие списки от пустых результатов
        output_1_Excel_morph_forms_results = [o1 for o1 in output_1_Excel_morph_forms_results if len(o1)]
        output_2_OO_Writer_morph_forms_results = [o2 for o2 in
                                                  output_2_OO_Writer_morph_forms_results if
                                                  len(o2)]

        # 1. Вывод морф. форм всего текста для вставки их в Excel
        output_1_str = 'Morph forms to add into Excel:\n'
        if len(output_1_Excel_morph_forms_results):
            output_1_str += '\n'.join(output_1_Excel_morph_forms_results)
        else:
            output_1_str += 'No new morph forms!'

        # 2. Вывод морф. форм всего текста для вставки их в OO Writer
        output_2_str = 'Morph forms to add into OO Writer:\n'
        if len(output_2_OO_Writer_morph_forms_results):
            output_2_str += '\n\n'.join(output_2_OO_Writer_morph_forms_results)
        else:
            output_2_str += 'No new morph forms!'

        output = '\n\n'.join([output_1_str, output_2_str])
        return output

    def validate_all_words_are_present_in_vocabulary(self, input_text):
        results = []
        tuples = self.grcSpaCyOrStanzaWrapper.get_doc_object_tuples(input_text)
        for token, lemma, pos, morph in tuples:
            if not self.vocabularyService.is_word_in_vocabulary(token, lemma, True):
                result = f"Word '{token}' with lemma '{lemma}' is absent from vocabulary! Please, add it!"
                results.append(result)

        return results

    def process_sentence(self, sentence):
        # key - token; value - pair/triplet of nouns with translation and grammar hint
        # sentence_results_dict = {}

        sentence_results1 = list()
        sentence_results2 = list()

        tuples = self.grcSpaCyOrStanzaWrapper.get_doc_object_tuples(sentence)

        for self.token, self.lemma, self.pos, self.morph in tuples:
            # если слово является собственным или нарицательным существительным
            if self.spaCyPosResolver.is_noun(self.pos):
                sentence_results1, sentence_results2 = self.process_noun()
            # TODO:
            # ('ἐλέησόν', 'ἐλεέω', 'VERB', Aspect=Perf|Mood=Imp|Number=Sing|Person=2|Tense=Past|VerbForm=Fin|Voice=Act)
            # elif SpaCyPosResolver.is_verb(self.pos):
        # end of loop

        # Преобразовываем списки с результатами в строковую форму
        output1 = "\n".join(sentence_results1)
        sentence_results2_output = "\n".join(sentence_results2)

        # добавляем строку с неизвестным переводом
        sentence_with_unknown_translation = sentence + "|???"

        # В sentence_results2 хранятся морф. формы, которые будут находиться с предложением в РАЗНЫХ строках.
        # В sentence_results2_copy хранятся морф. формы, которые будут находиться с предложением в ОДНОЙ И ТОЙ ЖЕ строке.
        sentence_results2_copy = list(sentence_results2)
        sentence_results2_copy.append(sentence_with_unknown_translation)

        # Делаем merge строк в пределах каждого столбца (в механике OO Writer) и объединяем их с помощью pipe
        # в одну широкую строку, содержащую морф. формы + предложение, к которому они относятся
        col1_results = []
        col2_results = []
        for line in sentence_results2_copy:
            pieces = line.split("|")
            col1_results.append(pieces[0])
            col2_results.append(pieces[1])

        # В первом столбце между иностранными словами должно быть в среднем на 1 newline больше, чтобы они стояли ровно
        # напротив своих переводов, под каждым из которых подписан ещё и grammar_hint. Вот из-за этого grammar_hint-а
        # нужно делать на один newline больше!
        col1_results_output = (OO_WRITER_STRIPES_DELIMITER + '^^^').join(col1_results)
        col2_results_output = OO_WRITER_STRIPES_DELIMITER.join(col2_results)
        sentence_results2_copy_output = "|".join([col1_results_output, col2_results_output])

        output2 = "\n".join([sentence_results2_output, sentence_results2_copy_output])

        return output1, output2

    def process_noun(self):
        sentence_results1 = []
        sentence_results2 = []

        # 1) род (мужской, женский, средний)
        self.gender = self.morphologyParser.parse(self.morph, "Gender")
        # 2) число (единственное, двойственное, множественное)
        self.number = self.morphologyParser.parse(self.morph, "Number")
        # 3) падеж (именительный, родительный, дательный, винительный, звательный)
        self.case = self.morphologyParser.parse(self.morph, "Case")

        if self.gender and self.number and self.case:
            is_token_in_its_initial_dictionary_form = self.number == NumberSpaCy.Sing.value and self.case == CaseSpaCy.Nom.value
            # продолжаем обрабатывать токен только если он находится в отличном от начальной словарной формы состоянии
            if not is_token_in_its_initial_dictionary_form:
                token_grammar = self.nounGrammarConverter.convert(self.morph, ConversionMode.GENDER_NUMBER_CASE)
                # Одна и та же словоформа может представлять разные падежи!
                # Например, Ἰησοῦ - это и родительный, и звательный падеж!!!
                # Поэтому надо работать не просто с token, а с token_grammaticized и от него
                # тогда действительно можно требовать уникальности в 1-м столбце Excel-файла для морф. форм!
                # Ἰησοῦ (masc. sg. gen.)|ὁ Ἰησοῦς - τοῦ Ἰησοῦ|(nom. - gen.)
                # Ἰησοῦ (masc. sg. voc.)|ὁ Ἰησοῦς - Ἰησοῦ!|(nom. - voc.)
                self.token_grammaticized = f'{self.token} ({token_grammar})'

                # морф. форма обрабатываемого слова НЕ должна находиться среди:
                # 1) Excel-списка уже изученных ранее морф. форм
                # 2) словаря-поля класса text_results_dict, содержащего уже обработанные токены всех предыдущих предложений текста
                is_token_grammaticized_absent_from_excel = not self.morphFormsService.is_word_among_1st_col_words(
                    self.token_grammaticized)
                is_token_grammaticized_absent_from_text_results_dict = self.token_grammaticized not in self.text_results_dict

                if (is_token_grammaticized_absent_from_excel and
                        is_token_grammaticized_absent_from_text_results_dict):
                    # TODO: здесь идёт основная работа
                    dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(
                        self.lemma, self.token, self.pos, self.morph)
                    result1 = PIPE.join([self.token_grammaticized, dashed_nouns, grammar_hint])
                    sentence_results1.append(result1)
                    self.text_results_dict[self.token_grammaticized] = result1

                    # TODO: продолжаем работу для формирования результата по 2-й категории
                    translation = self.vocabularyService.get_word_translation(self.token, self.lemma, True)
                    # строку вида 'ὁ ἄνθρωπος – τοῦ ἀνθρώπου|(nom. – gen.)' разбиваем по пайп и берём последний элемент
                    # dashed_nouns_with_piped_pars_grammar_pieces = dashed_nouns_with_piped_pars_grammar.split('|')
                    # grammar_hint = dashed_nouns_with_piped_pars_grammar_pieces[-1]
                    translation_with_grammar_hint = "{0}^^^{1}".format(translation, grammar_hint)
                    # строка вида 'ὁ ἄνθρωπος – τοῦ ἀνθρώπου|человек^^^(nom. – gen.)'
                    result2 = dashed_nouns + "|" + translation_with_grammar_hint
                    sentence_results2.append(result2)
        else:
            if not self.gender:
                sentence_results1.append("<No 'gender (masc., fem., neut.)' info for token = > " + self.token)
            if not self.number:
                sentence_results1.append("No 'number (sg., dual, pl.)' info for token = > " + self.token)
            if not self.case:
                sentence_results1.append("No 'case (nom., gen., etc)' info for token = > " + self.token)

        return sentence_results1, sentence_results2


##########################################################################################

# text = "τοῦ εὐαγγελίου"

# Данное слово имеет формы единственного, двойственного и множественного числа!
# Именительный	ὀφθαλμός|ὀφθαλμώ|ὀφθαλμοί
# Родительный	ὀφθαλμοῦ|ὀφθαλμῶν|ὀφθαλμῶν
# Дательный	    ὀφθαλμῷ|ὀφθαλμώ|ὀφθαλμοῖς
# Винительный	ὀφθαλμόν|ὀφθαλμώ|ὀφθαλμούς
# Звательный	ὀφθαλμέ|ὀφθαλμώ|ὀφθαλμοί

# text = "ὀφθαλμώ τοῦ ἀνθρώπου"  # глаза человека; данную фразу CLTK pos-тэггирует неверно, не распознаёт двойственное число
text = "ἀδελφῶν"
text = "ἀνθρώποις"
text = "μαθητάς"
text = "λόγος"
text = """
πρόσωπον
προσώπου
προσώπῳ

πρόσωπον
προσώπου
προσώπῳ
"""

text = "# 1Ἀρχὴ τοῦ εὐαγγελίου Ἰησοῦ Χριστοῦ [υἱοῦ θεοῦ]."
# text = "Ἰησοῦ"

# text = """
# # 1Ἀρχὴ τοῦ εὐαγγελίου Ἰησοῦ Χριστοῦ [υἱοῦ θεοῦ].
# # 2Ἀρχὴ τοῦ εὐαγγελίου Ἰησοῦ Χριστοῦ [υἱοῦ θεοῦ].
# # 3Ἀρχὴ τοῦ εὐαγγελίου Ἰησοῦ Χριστοῦ [υἱοῦ θεοῦ].
# """

# text = """
# 1Ἀρχὴ τοῦ εὐαγγελίου Ἰησοῦ Χριστοῦ [υἱοῦ θεοῦ].
# 2Καθὼς γέγραπται ἐν τῷ Ἠσαΐᾳ τῷ προφήτῃ·ἰδοὺ ἀποστέλλω τὸν ἄγγελόν μου πρὸ προσώπου σου, ὃς κατασκευάσει τὴν ὁδόν σου·
# """

# text = """
# 1Ἀρχὴ τοῦ εὐαγγελίου Ἰησοῦ Χριστοῦ [υἱοῦ θεοῦ].
# 2Καθὼς γέγραπται ἐν τῷ Ἠσαΐᾳ τῷ προφήτῃ·ἰδοὺ ἀποστέλλω τὸν ἄγγελόν μου πρὸ προσώπου σου, ὃς κατασκευάσει τὴν ὁδόν σου·
# 1Ἀρχὴ τοῦ εὐαγγελίου Ἰησοῦ Χριστοῦ [υἱοῦ θεοῦ].
# """

# text = "1Ἀρχὴ"

# text = """
# # 1Ἀρχὴ τοῦ εὐαγγελίου Ἰησοῦ Χριστοῦ [υἱοῦ θεοῦ].
# # 2Καθὼς γέγραπται ἐν τῷ Ἠσαΐᾳ τῷ προφήτῃ·ἰδοὺ ἀποστέλλω τὸν ἄγγελόν μου πρὸ προσώπου σου, ὃς κατασκευάσει τὴν ὁδόν σου·
# """

# text = """
# # 1Ἀρχὴ τοῦ εὐαγγελίου Ἰησοῦ Χριστοῦ [υἱοῦ θεοῦ].
# Κύριε Ἰησοῦ Χριστέ, ἐλέησόν με!
# """

text = """
Κύριε Ἰησοῦ Χριστέ, ἐλέησόν με!
"""

if __name__ == '__main__':
    s3_TextInflectionsMaker = S3_TextInflectionsMaker()
    res = s3_TextInflectionsMaker.process_whole_text(text)
    print(res)
