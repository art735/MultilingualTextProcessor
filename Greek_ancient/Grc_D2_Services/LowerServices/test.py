from cltk import NLP
from cltk.morphology.universal_dependencies_features import Gender

# cltk.morphology.universal_dependencies_features.Case
from LowerServices import LemmaExtractor

NEWLINE = '\n'


def preprocess(text):
    # results = []
    # lines = [s for s in text.split(NEWLINE) if len(s)]  # взять в дальнейшую работу только непустые строки
    # for line in lines:
    #     stripped = re.sub(r'^([ὁἡ]|τό)\s', r'', line)  # strip definite article at the beginning of the word
    #     stripped = re.sub(r'\d+', r'', stripped)  # strip digits/numbers
    #     truncated = stripped.split(',')[0]  # если словарная статья содержит запятую(-ые), взять только то, что находится до первой запятой
    #     unspaced = truncated.split(' ')[0]  # если оставшаяся часть содержит пробел, взять только то, что находится до пробела
    #     results.append(unspaced)
    # output = " ".join(results)
    # return output
    return LemmaExtractor.extract(text)


def abc(text):
    # newlined_res = process_text(text)
    # listed_res = " ".join(newlined_res.split("\n"))
    # print(listed_res)
    preprocessed_text = preprocess(text)

    cltk_nlp = NLP(language="grc")
    cltk_doc = cltk_nlp.analyze(text=preprocessed_text)
    print(cltk_doc.lemmata)
    print(cltk_doc.pos)

    # print(cltk_doc.tokens[:5])
    # print(cltk_doc.lemmata[:5])
    print(cltk_doc.morphosyntactic_features)
    # print(cltk_doc.pos[:5])
    # print(cltk_doc.sentences_tokens)

    # Для каждого урока из учебника / стиха Евангелия делать:
    # 1) словарь новых слов
    # 2) словарь новых морфологий: пара "слово в начальной форме - конкретная форма из данного предложения"
    #
    res = []
    for lemma, pos, morphosyntactic_feature in zip(cltk_doc.lemmata, cltk_doc.pos, cltk_doc.morphosyntactic_features):
        if pos in ['NOUN', 'PROPN']:  # если слово является существительным
            if Gender in morphosyntactic_feature.features:
                gender = morphosyntactic_feature.features[Gender][0]
                if gender == Gender.masculine:
                    res.append("ὁ " + lemma)
                elif gender == Gender.feminine:
                    res.append("ἡ " + lemma)
                elif gender == Gender.neuter:
                    res.append("τὸ " + lemma)
            else:
                res.append("<CLTK doesn't have 'gender' info> " + lemma)
        else:
            res.append(lemma)

    # print(res)
    output = '\n'.join(res)
    return output


#############################################

# text = "1Ἀρχὴ τοῦ εὐαγγελίου Ἰησοῦ Χριστοῦ [υἱοῦ θεοῦ]."

str = """
ἡ ἔρημος

"""

res = abc(str)
print(res)
