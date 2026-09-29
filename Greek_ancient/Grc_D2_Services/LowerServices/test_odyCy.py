import spacy

text = 'Κύριε Ιησού Χριστέ, ελέησόν με!'

nlp = spacy.load('grc_odycy_joint_trf')
doc = nlp(text)
print([token.lemma_ for token in doc])

# doc = CltkDocObjectProvider.get_cltk_doc_object(text)
# print(doc.lemmata)
