import stanza
from gr_nlp_toolkit import Pipeline

# sentence = "Η Ιταλία κέρδισε την Αγγλία στον τελικό του Euro 2020."
sentence = "Η Ιταλία κέρδισε την Αγγλία στον τελικό του Euro 2020."
sentence = "Ο Γιώργος είναι ψηλότερος από τον Νίκο."
sentence = "Η Μαρία τρέχει πιο γρήγορα από εμένα."
sentence = "Η Μαρία τρέχει πιο γρήγορα από εμένα."

sentence = """
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

sentence = "Θέλω να φάω"

# --- Stanza ---
stanza_nlp = stanza.Pipeline('el', processors='tokenize,mwt,pos,lemma', use_gpu=False)
stanza_doc = stanza_nlp(sentence)

# --- GR-NLP-TOOLKIT ---
gr_nlp_toolkit_nlp = Pipeline("pos")
gr_nlp_toolkit_doc = gr_nlp_toolkit_nlp(sentence)

# Преобразуем токены GR-NLP-TOOLKIT в словарь для быстрого поиска по тексту
gnt_tokens_dict = {}
for token in gr_nlp_toolkit_doc.tokens:
    text_norm = token.text.strip().lower()
    gnt_tokens_dict.setdefault(text_norm, []).append(token)

# Функция безопасного извлечения токена GR-NLP по тексту
def find_matching_gnt_token(word_text):
    key = word_text.strip().lower()
    if key in gnt_tokens_dict and gnt_tokens_dict[key]:
        return gnt_tokens_dict[key].pop(0)  # берём первый и удаляем, чтобы не дублировать
    return None

# --- Совмещение результатов ---
for stanza_token in stanza_doc.sentences[0].words:
    gnt_token = find_matching_gnt_token(stanza_token.text)

    # если совпадения нет, просто используем данные Stanza
    if not gnt_token:
        morph = stanza_token.feats
    else:
        # Для прилагательных — морфология от Stanza, иначе — от GR-NLP-TOOLKIT
        if stanza_token.upos == "ADJ":
            morph = stanza_token.feats
        else:
            morph = getattr(gnt_token, "feats", stanza_token.feats)

    print(f'word: {stanza_token.text}, lemma: {stanza_token.lemma}, morph: {morph}')
