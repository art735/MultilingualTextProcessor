import VowelPreprocessor
from EBibleLexiconService import EBibleLexiconService
from ProcessingLemmaEntity import ProcessingLemmaEntity
from GrcSpaCyEngineWrapper import GrcSpaCyOrStanzaWrapper
from VocabularyService import VocabularyService

# https://github.com/tonyjurg/Philo_Opificio_Mundi/blob/main/parse_NLP.ipynb

table_heading = '# | TOKEN | LEMMA | VERDICT\n__________________________________________________'


class S1_TextLemmasFinder:

    def __init__(self):
        self.grcSpaCyOrStanzaWrapper = GrcSpaCyOrStanzaWrapper()
        self.vocabularyService = VocabularyService()
        self.eBibleLexiconService = EBibleLexiconService()

        # Содержит все недублирующиеся объекты типа ProcessingLemmaEntity.
        # Корректная работа множества регулируется переопределёнными методами __eq__ & __hash__
        # На момент написания комментария __eq__ & __hash__ были переопределены на основании полей "token-lemma-verdict"
        # Это значит, что объекты, у которых значения в этих полях совпадают, в множество results_set не попадают, т. к.
        # простым языком слова текста, представленные в коде объектами, уже обрабатывались
        self.results_set = set()
        self.counter = 0

    # Главная отправная точка: какой бы вид не имели входные данные (изолированное слово или целый текст (чисто
    # греческий или мешанина из разных языков)), они должны целиком попадать на вход spaCy-лемматайзера,
    # который зная весь контекст, определит леммы каждого слова и дальше результаты его работы можно будет
    # сравнивать с леммами из 'eBible lexicon.xls'.
    # Но подстраиваться нужно именно под spaCy (под тот факт, что он должен отработать с максимально широким
    # текстовым контекстом для как можно более точного результата лемматизации).

    # Цель данного метода обслуживать два базовых use case-а:
    # UC#1. Происходит работа над уроком из учебника: здесь на вход метода поступает текст урока "как есть", т. е.
    # в виде мешанины из слов урока на разных языках (русском и греческом, английском и греческом).
    # spaCy-движок спокойно воспринимает эту разноязыкую мешанину и выполняет лемматизацию.

    # UC#2. Происходит работа над текстом, о котором заранее известно, что это чисто греческий текст без посторонних
    # примесей. Это случай, например, чтения Евангелия или чтения текста из того же учебника греч. языка, но теперь
    # уже изолированно от другой (не греческой информации) этого же урока. В этом случае мы рассчитываем и надеемся,
    # что лемматизация произойдёт точнее, чем в случае, когда на вход поступали отдельные изолированные слова,
    # лишённые контекста.
    def find_lemmas(self, input_str):

        hundred_percent_match_results = []
        lemmas_not_equal_results = []
        spaCy_only_results = []
        eBibleLexicon_only_results = []
        not_found_results = []

        # tuples = CltkEngineWrapper.get_doc_object_tuples(input_str)
        tuples = self.grcSpaCyOrStanzaWrapper.get_doc_object_tuples(input_str)

        for token, lemma, *rest in tuples:
            # Только если слово отсутствует в вокабуляре, имеет смысл работать с ним дальше:
            if not self.vocabularyService.is_word_in_vocabulary(token, lemma, True):
                # Ищем лемму неизвестного слова в файле 'eBible lexicon (dictionary).xls'
                eBibleLexicon_lemmas = []
                eBibleLexicon_lemmas_str = ''
                # Если в token присутствует 2-е ударение (как в слове ἄγγελόν из фразы "ἄγγελόν μου"),
                # нужно удалить это 2-е ударение перед поиском в eBibleLexicon, но в то же время в некоторых
                # других словоформах (например, ἐλέησόν) eBibleLexicon хранит форму слова с двумя ударениями!
                # Поэтому нужно пробовать оба варианта: сначала искать в eBibleLexicon слово "как есть" (даже если
                # у него два ударения), а затем удалять 2-е ударение и искать ещё раз форму слова без него!

                # 1. Поиск в eBibleLexicon по токену "как есть" (с возможным 2-м ударением)
                eBibleLexicon_entities_set1 = self.eBibleLexiconService.look_up(token)

                # 2. Поиск в eBibleLexicon по токену, очищенному от 2-го доп. ударения
                token_without_2nd_stress = VowelPreprocessor.remove_in_word_second_stress(token)
                eBibleLexicon_entities_set2 = self.eBibleLexiconService.look_up(token_without_2nd_stress)

                # 3. Объединение результатов двух поисков в один общий set
                eBibleLexicon_entities_set = eBibleLexicon_entities_set1 | eBibleLexicon_entities_set2

                if eBibleLexicon_entities_set:  # если слово найдено в 'eBible lexicon.xls'
                    eBibleLexicon_lemmas = [eBibleLexicon_entity.lemma
                                            for eBibleLexicon_entity in eBibleLexicon_entities_set]
                    eBibleLexicon_lemmas_str = ", ".join(eBibleLexicon_lemmas)

                # Сравниваем две полученные из разных источников леммы, т. е.:
                # 1) лемму, полученную от движка spaCy
                # 2) лемму, вычитанную из файла 'eBible lexicon (dictionary).xls'
                if lemma and eBibleLexicon_lemmas_str:
                    if lemma in eBibleLexicon_lemmas:
                        verdict = "100%"
                        res = self.format_result(token, lemma, verdict)
                        hundred_percent_match_results.append(res)
                    else:
                        verdict = "spaCy – " + lemma + "; " + "eBibleLexicon – " + eBibleLexicon_lemmas_str
                        res = self.format_result(token, "???", verdict)
                        lemmas_not_equal_results.append(res)
                elif lemma and not eBibleLexicon_lemmas_str:
                    verdict = "spaCy only"
                    res = self.format_result(token, lemma, verdict)
                    spaCy_only_results.append(res)
                elif not lemma and eBibleLexicon_lemmas_str:
                    verdict = "eBibleLexicon only"
                    res = self.format_result(token, eBibleLexicon_lemmas_str, verdict)
                    eBibleLexicon_only_results.append(res)
                else:
                    verdict = "not found"
                    res = self.format_result(token, "???", verdict)
                    not_found_results.append(res)
            # end of loop

        output_results = []
        is_table_heading_already_added = False
        for results in [not_found_results, lemmas_not_equal_results, spaCy_only_results, eBibleLexicon_only_results,
                        hundred_percent_match_results]:
            output_res = "\n".join([r for r in results if r])
            if output_res:
                if not is_table_heading_already_added:
                    # table_heading = (('{} | {} | {} | {}'
                    #                  '\n__________________________________________________').
                    #                  format('#', 'TOKEN', 'LEMMA', 'VERDICT'))
                    output_results.append(table_heading)
                    is_table_heading_already_added = True
                output_results.append(output_res)

        if output_results:
            output = "\n- - -\n".join(output_results)
        else:
            output = "No new lemmas found!"
        return output

    def format_result(self, token, lemma, comment):
        out = ''
        processing_lemma_entity = ProcessingLemmaEntity(token, lemma, comment)
        # Отфильтровываем здесь одинаковые сущности (см. методы __eq__ & __hash__ внутри сущности)
        if processing_lemma_entity not in self.results_set:
            self.counter += 1  # увеличиваем глобальный счётчик на 1
            processing_lemma_entity.counter = self.counter
            self.results_set.add(processing_lemma_entity)
            out = str(processing_lemma_entity)

        return out


#####################################################################################################

# text = "# 1Ἀρχὴ τοῦ εὐαγγελίου Ἰησοῦ Χριστοῦ [υἱοῦ θεοῦ]."
# text = "Ἀρχὴ τοῦ εὐαγγελίου Ἰησοῦ Χριστοῦ [υἱοῦ θεοῦ]."

# text = """
# Урок 01
#
# 1. Алфавит
#
# Греческий алфавит состоит из 24 букв.
#
# Ἀρχὴ
#
# Примечания к алфавиту:
# τοῦ εὐαγγελίου
# 1. Прописные буквы употребляются в начале только такого предложения, которое начинается с красной строки или представляет собой прямую речь, а также в собственных именах, географических названиях, названиях народов.
# Ἰησοῦ Χριστοῦ
# 2. В квадратных скобках здесь и далее даётся транскрипция, т. е. передача звучания слова русскими буквами.
# [υἱοῦ θεοῦ]
# 3. Буква Γ γ (гамма) перед γ, κ, ξ, χ произносится как [н], например:
#
# перед γ:
# ἄγγελος
# [ангелос]
# """

# text = """
# εὐαγγέλιον
# εὐαγγελίου
#
# ἰησοῦς
# ἰησοῦ
#
# χριστός
# χριστοῦ
# """

# text = "# 1Ἀρχὴ τοῦ εὐαγγελίου Ἰησοῦ Χριστοῦ [υἱοῦ θεοῦ]."

text = """
1Ἀρχὴ τοῦ εὐαγγελίου Ἰησοῦ Χριστοῦ [υἱοῦ θεοῦ].

2Καθὼς γέγραπται ἐν τῷ Ἠσαΐᾳ τῷ προφήτῃ·ἰδοὺ ἀποστέλλω τὸν ἄγγελόν μου πρὸ προσώπου σου, ὃς κατασκευάσει τὴν ὁδόν σου·
"""

text = """
# 1Ἀρχὴ τοῦ εὐαγγελίου Ἰησοῦ Χριστοῦ [υἱοῦ θεοῦ].
Κύριε Ἰησοῦ Χριστέ, ἐλέησόν με!
"""

# text = "ἐλέησόν με"

if __name__ == '__main__':
    s1_TextLemmasFinder = S1_TextLemmasFinder()
    res = s1_TextLemmasFinder.find_lemmas(text)
    print(res)
