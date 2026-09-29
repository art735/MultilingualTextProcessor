import stanza

# sentence = "Η Ιταλία κέρδισε την Αγγλία στον τελικό του Euro 2020."
sentence = "Η Ιταλία κέρδισε την Αγγλία στον τελικό του Euro 2020."
# sentence = "Ο Γιώργος είναι ψηλότερος από τον Νίκο."
# sentence = "Η Μαρία τρέχει πιο γρήγορα από εμένα."

sentence = "Θέλω να φάω"

# --- Stanza ---
# stanza_nlp = stanza.Pipeline('el', processors='tokenize,lemma', use_gpu=False)
stanza_nlp = stanza.Pipeline('el', processors='tokenize,mwt,pos,lemma', use_gpu=False)
stanza_doc = stanza_nlp(sentence)

# --- Совмещение результатов ---
for stanza_token in stanza_doc.sentences[0].words:
    token = stanza_token.text
    lemma = stanza_token.lemma
    pos = stanza_token.upos               # UPOS
    morph = stanza_token.feats            # Морфологические признаки

    print(f'word: {token}, lemma: {lemma}, pos: {pos}, morph: {morph}')

