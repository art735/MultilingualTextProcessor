from cltk import NLP

from GrcRegExFinder import GrcRegExFinder

grcRegExFinder = GrcRegExFinder()


def get_doc_object_tuples(input_str):
    # 1. Осуществляем препроцессинг входного текста
    preprocessed_text = InputTextPreprocessor.preprocess(input_str)

    # 2. Формируем doc-объект
    cltk_nlp = NLP(language="grc", suppress_banner=True)
    cltk_doc = cltk_nlp.analyze(text=preprocessed_text)

    # 3. Формируем массив кортежей из информации, хранящейся в doc-объекте
    tuples = []
    for token, lemma, pos, morphosyntactic_feature in zip(cltk_doc.tokens, cltk_doc.lemmata, cltk_doc.pos,
                                                          cltk_doc.morphosyntactic_features):
        # токенами могут оказаться знаки препинания, скобки и пр. Поэтому берём в работу только те токены, которые:
        # 1) точно являются греч. словами
        # 2) в составе которых есть греческие слова (маловероятная ситуация, что будут такие токены)
        guaranteed_greek_token = grcRegExFinder.search_token_for_greek_word(token)
        if len(guaranteed_greek_token):
            grammar_tuple = (token, lemma, pos, morphosyntactic_feature)
            tuples.append(grammar_tuple)

    return tuples
