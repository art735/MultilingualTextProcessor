from BaseSpaCyOrStanzaWrapper import BaseSpaCyOrStanzaWrapper
from DeuRegExFinder import DeuRegExFinder
from DeuTextPreprocessor import DeuTextPreprocessor


class DeuSpaCyOrStanzaWrapper(BaseSpaCyOrStanzaWrapper):
    def __init__(self):
        super().__init__('spaCy', 'de_dep_news_trf', DeuTextPreprocessor())
        self.deuRegExFinder = DeuRegExFinder()

    def get_doc_object_tuples(self, input_text, should_split_large_text_into_chunks=False):

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
                # 1) точно являются немецкими словами
                # 2) в составе которых есть немецкие слова (маловероятная ситуация, что будут такие токены) (это неверно!)
                # guaranteed_german_token = self.deuRegExFinder.search_token_for_german_word(token)
                # if len(guaranteed_german_token):
                #     grammar_tuple = (token, lemma, pos, morph)
                #     tuples.append(grammar_tuple)

                if self.deuRegExFinder.is_token_a_canonical_word(token):
                    grammar_tuple = (token, lemma, pos, morph)
                    tuples.append(grammar_tuple)

        return tuples


####################################

input_str = "1Das ist ein Test-Text mit deutschen Wörtern wie Fußgängerübergang und E-Mail2."
# input_str = "Ab morgen muss ich arbeiten."
# input_str = "Wann kann ich den Schrank bei dir abholen?"
# input_str = "Ich sehe ihn auf der Straße"
input_str = "Ich sehe meine Straße"

input_str = """
Ab morgen muss ich arbeiten.
Ich bin oft im Büro, aber nur für wenige Stunden.
Wir fahren um zwölf Uhr ab.
Vor der Abfahrt rufe ich an.
Ich muss meine Schlüssel abgeben.
Wann kann ich den Schrank bei dir abholen?
Wir müssen noch meinen Bruder abholen.
Da ist ein Brief für dich ohne Absender.
Achtung! Das dürfen Sie nicht tun.
Können Sie mir seine Adresse sagen?
"""

input_str = "Ich musste gestern lange arbeiten."
input_str = "(sich) anmelden"
input_str = 'Wo geht’s hier bitte zur Autobahn?'

input_str = """
Wort
gruppen
liste
"""

input_str = 'Alles Gute!'
input_str = 'Hast du alles?'
input_str = 'Fahren Sie an der nächsten Straße nach rechts.'
input_str = 'willst du diese Jacke?'
input_str = 'du willst  diese Jacke?'
input_str = 'Auf dem Formular müssen Sie an mehreren Stellen etwas ankreuzen.'
input_str = 'Nein, ich möchte die andere.'
input_str = 'Wo geht’s hier bitte zur Autobahn?'

if __name__ == '__main__':
    deuSpaCyOrStanzaWrapper = DeuSpaCyOrStanzaWrapper()
    doc_tuples = deuSpaCyOrStanzaWrapper.get_doc_object_tuples(input_str, True)
    [print(doc_tuple) for doc_tuple in doc_tuples]
