import Utils
from DeuLemmaResolver import DeuLemmaResolver
from DeuSpaCyOrStanzaWrapper import DeuSpaCyOrStanzaWrapper


class TokenLemmaPosMorphDisplayer:

    def __init__(self):
        self.deuSpaCyOrStanzaWrapper = DeuSpaCyOrStanzaWrapper()
        self.deuLemmaResolver = DeuLemmaResolver()

    def display(self, input_text):
        results = []

        sentences = Utils.split_by(input_text, '\n')
        for sentence in sentences:
            results.append(f'\n{sentence}')
            tuples = self.deuSpaCyOrStanzaWrapper.get_doc_object_tuples(sentence, True)
            for token, lemma, pos, morph in tuples:
                current_word = self.deuLemmaResolver.get_single_lemma(token, lemma, pos, morph)
                current_word_displayable_morphology = (f"token = '{token}', lemma = '{current_word}', pos = '{pos}',"
                                                       f" morph = '{morph}'")
                results.append(current_word_displayable_morphology)

        output = '\n'.join(results).strip()  # удаляет символы [ \t\n\r\f\v] в начале и конце строки
        return output


########################################################

input_str = """
Auf dem Formular müssen Sie an mehreren Stellen etwas ankreuzen.
Mach bitte das Licht an!
Ein Pfund Äpfel bitte.
"""

input_str = "So, das war’s!"

if __name__ == '__main__':
    tokenLemmaPosMorphDisplayer = TokenLemmaPosMorphDisplayer()
    output = tokenLemmaPosMorphDisplayer.display(input_str)
    print(output)
