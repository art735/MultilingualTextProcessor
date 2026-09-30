from DeuRegExFinder import DeuRegExFinder
from DeuTextPreprocessor import DeuTextPreprocessor
from GrcRegExFinder import GrcRegExFinder
from GrcTextPreprocessor import GrcTextPreprocessor
from BaseSpaCyOrStanzaWrapper import BaseSpaCyOrStanzaWrapper

class EngSpaCyOrStanzaWrapper(BaseSpaCyOrStanzaWrapper):
    def __init__(self):
        # Stanza показывает большую точность при определении pos & morph для английского языка по сравнению со spaCy.
        # Факт того, что Stanza лучше spaCy для определения морфологии английского языка подтверждают все ключевые AI-чаты.
        # Переиспользуем для английского языка text processor из немецкого языка.
        super().__init__('Stanza', 'en', DeuTextPreprocessor())
        # Для переключения на spaCy - просто раскомментировать ctor, расположенный ниже
        # super().__init__('spaCy', 'el_core_news_lg', GrcTextPreprocessor())

        # Переиспользуем для английского языка те же регулярные выражения, что и для немецкого. У обоих языков
        # используется латинская письменность и в этом плане работа с ними идентична.
        self.engRegExFinder = DeuRegExFinder()

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
                # 1) точно являются английскими словами
                # 2) в составе которых есть английские слова (маловероятная ситуация, что будут такие токены) (это неверно!)
                # guaranteed_german_token = self.deuRegExFinder.search_token_for_german_word(token)
                # if len(guaranteed_german_token):
                #     grammar_tuple = (token, lemma, pos, morph)
                #     tuples.append(grammar_tuple)

                if self.engRegExFinder.is_token_a_canonical_word(token):
                    grammar_tuple = (token, lemma, pos, morph)
                    tuples.append(grammar_tuple)

        return tuples


####################################

input_str = """
The children were running quickly through the fields.
The leaves were falling quickly from the highest trees.
"""

if __name__ == '__main__':
    engSpaCyOrStanzaWrapper = EngSpaCyOrStanzaWrapper()
    doc_tuples = engSpaCyOrStanzaWrapper.get_doc_object_tuples(input_str, True)
    for doc_tuple in doc_tuples:
        print(doc_tuple)
