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

# --- GR-NLP-TOOLKIT ---
gr_nlp_toolkit_nlp = Pipeline("pos")
gr_nlp_toolkit_doc = gr_nlp_toolkit_nlp(sentence)

# Преобразуем токены GR-NLP-TOOLKIT в словарь для быстрого поиска по тексту
gnt_tokens_dict = {}
for token in gr_nlp_toolkit_doc.tokens:
    token_text = token.text
    pos = token.upos
    morph = token.feats

    print(f'token: {token_text}, pos: {pos}, morph: {morph}')
