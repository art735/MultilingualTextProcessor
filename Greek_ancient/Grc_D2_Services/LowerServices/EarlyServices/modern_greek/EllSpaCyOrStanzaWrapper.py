from GrcRegExFinder import GrcRegExFinder
from GrcTextPreprocessor import GrcTextPreprocessor
from BaseSpaCyOrStanzaWrapper import BaseSpaCyOrStanzaWrapper

class EllSpaCyOrStanzaWrapper(BaseSpaCyOrStanzaWrapper):
    def __init__(self):
        # Stanza показывает большую точность при определении pos & morph для новогреческого языка по сравнению со spaCy.
        # Факт того, что Stanza лучше spaCy для определения морфологии новогреческого языка подтверждают все ключевые LLM.
        super().__init__('Stanza', 'el', GrcTextPreprocessor())
        # Для переключения на spaCy - просто раскоментировать ctor, расположенный ниже
        # super().__init__('spaCy', 'el_core_news_lg', GrcTextPreprocessor())
        self.grcRegExFinder = GrcRegExFinder()

    def get_doc_object_tuples(self, input_text, should_split_large_text_into_chunks=True):
        # Получаем из метода базового класса список готовых doc-объектов
        doc_objects = super().process(input_text, should_split_large_text_into_chunks)

        # Формируем список кортежей на основе списка doc-объектов
        tuples = []
        for doc_object in doc_objects:
            for item in doc_object:
                token = item.text
                lemma = item.lemma_
                pos = item.pos_
                morph = item.morph

                # токенами могут оказаться знаки препинания, скобки и пр. Поэтому берём в работу только те токены, которые:
                # 1) точно являются греч. словами
                # 2) в составе которых есть греческие слова (маловероятная ситуация, что будут такие токены) (в немецком
                # я отказался от этого подхода)
                guaranteed_greek_token = self.grcRegExFinder.search_token_for_greek_word(token)
                if len(guaranteed_greek_token):
                    grammar_tuple = (token, lemma, pos, morph)
                    tuples.append(grammar_tuple)

        return tuples


####################################

input_str = """
Ευτυχισμένοι Μαζί
Επεισόδιο 1
(ΓΙΑΝΝΑΚΗΣ) Σήμερα ο μπαμπάς μου παντρεύεται και θέλει να είναι όλα τέλεια.
Γι’ αυτό είναι ταραγμένος και σπαστικός.
Δεν είναι η πρώτη φορά. Αλλά είναι η πρώτη που θα το δω γιατί την προηγούμενη φορά παντρεύτηκε με τη μητέρα μου.
Που δεν είναι ώρα να θυμηθώ τώρα.
Γιατί όποτε τη θυμάμαι κλαίω και τ’ αδέρφια μου με κοροϊδεύουν.
(αναφώνημα πόνου)
Επιτρέπεται την ημέρα του γάμου μου να σιδερώνω μόνος μου πουκάμισα;
"""

input_str = "Θέλω να φάω"

# input_str = """
# Που δεν είναι ώρα να θυμηθώ τώρα.
# """

if __name__ == '__main__':
    ellSpaCyOrStanzaWrapper = EllSpaCyOrStanzaWrapper()
    doc_tuples = ellSpaCyOrStanzaWrapper.get_doc_object_tuples(input_str, True)
    for doc_tuple in doc_tuples:
        print(doc_tuple)
