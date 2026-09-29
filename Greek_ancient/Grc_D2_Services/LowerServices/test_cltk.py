import re

from cltk import NLP

import RecognizedNewmansDictionaryFormatter


# # from cltk.stem.lemma import LemmaReplacer
# # from cltk.corpus.utils.formatter import assemble_tlg_author_filepaths
#
# # Create a lemmatizer object for Ancient Greek
# lemmatizer = LemmaReplacer('greek')
#
# # Example text
# text = "Ἐν ἀρχῇ ἦν ὁ λόγος..."
#
# # Lemmatize the text
# lemmatized_text = lemmatizer.lemmatize(text)
#
# # Print the lemmatized text
# print(lemmatized_text)


# https://github.com/cltk/cltk/blob/master/notebooks/CLTK%20Demonstration.ipynb

# выкусывает из общего текста с цифрами, точками, скобками и разными другими посторонними символами только греческие слова
def preprocess(original_text):
    matches = re.findall(RecognizedNewmansDictionaryFormatter.greek_word, original_text)
    print(matches)
    return ' '.join(matches)


cltk_nlp = NLP(language="grc")

# forms = cltk_nlp.inflect("ὀφθαλμός", upos='NOUN')
# print(forms)
