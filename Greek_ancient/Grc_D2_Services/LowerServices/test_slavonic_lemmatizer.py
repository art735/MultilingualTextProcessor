from cltk import NLP

# 'chu' - language code for Old Church Slavonic
cltk_nlp = NLP(language="chu", suppress_banner=True)

input_text = 'в начале бе Слово'
input_text = 'ѕэни1ца џка'
input_text = 'Доброе утро! Се аз творю вся нова.'

cltk_doc = cltk_nlp.analyze(text=input_text)

for token, lemma, pos, morphosyntactic_feature in zip(cltk_doc.tokens, cltk_doc.lemmata, cltk_doc.pos,
                                                      cltk_doc.morphosyntactic_features):
    print(f'{token} --> {lemma}')
