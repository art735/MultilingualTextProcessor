# Строка нужна для предотвращения ошибки SyntaxError: Non-UTF-8 code starting with '\xd0'
# -*- coding: utf-8 -*-
import EnWiktionaryConjugationsReader
import ModGrkVerbsConjugationsReader
from InternetToExcel import ElWiktionaryConjugationsReader


# def parse_verbs_from_Anki(input_text):
#     results = list()
#     for line in input_text.split('\n'):
#         if line:
#             (first_word, rest) = line.split(maxsplit=1)
#             rest = rest.replace('# спряжение глагола', '')
#             translation_m = re.search(r'[^a-zA-Z]+?(?=[*])', rest)
#             translation = translation_m.group().strip()
#             result = '{0}|{1}'.format(first_word, translation)
#             results.append(result)
#
#     output = '\n'.join(results)
#     return output


def format_wiktionary_to_excel_conjugations(input_text, option):
    results = list()
    for token in input_text.split('\n'):
        verb = token.strip()
        if verb:
            if option == 'moderngreekverbs.com':
                conjugation = ModGrkVerbsConjugationsReader.get_verb_conjugation(verb, True)
            elif option == 'el.wiktionary.org':
                conjugation = ElWiktionaryConjugationsReader.get_verb_conjugation(verb)
            elif option == 'en.wiktionary.org':
                conjugation = EnWiktionaryConjugationsReader.get_verb_conjugation(verb)

            results.append(conjugation)

    output = '\n\n*****\n\n'.join(results)
    return output


##################################################

# verbs = "αγαπάω  \n  ανοίγω  \n   κλείνω"
# # verbs = "αγοράζω"
# verbs = "αγαπώ"
# results = format_wiktionary_to_excel_conjugations(verbs, 'el.wiktionary.org')
# print(results)

verbs = "αγαπάω"
# results = format_wiktionary_to_excel_conjugations(verbs, 'moderngreekverbs.com')
# print(results)


# input = """
# παίρνω # спряжение глагола	I take брать, взять * * * Ενεστώτας παίρνω – παίρνουμε παίρνεις – παίρνετε παίρνει – παίρνουν Αόριστος πήρα – πήραμε πήρες – πήρατε πήρε – πήραν Συνοπτικός Μέλλοντας θα πάρω – θα πάρουμε θα πάρεις – θα πάρετε θα πάρει – θα πάρουν Perfective imperative mood Πάρε! – Πάρτε! * * * Ενεστώτας παίρνω – παίρνουμε παίρνεις – παίρνετε παίρνει – παίρνουν ?????? Ενεστώτας παίρνω – παίρνουμε παίρνεις – παίρνετε παίρνει – παίρνουν Imperfective imperative mood Παίρνε! – Παίρνετε!
# κάθομαι # спряжение глагола	I sit сидеть; садиться * * * Ενεστώτας κάθομαι – καθόμαστε κάθεσαι – κάθεστε κάθεται – κάθονται Αόριστος κάθισα – καθίσαμε κάθισες – καθίσατε κάθισε – κάθισαν Συνοπτικός Μέλλοντας θα καθίσω – θα καθίσουμε θα καθίσεις – θα καθίσετε θα καθίσει – θα καθίσουν Future Simple (colloq.) θα κάτσω – θα κάτσουμε θα κάτσεις – θα κάτσετε θα κάτσει – θα κάτσουν Προστακτική ????? * * * Ενεστώτας κάθομαι – καθόμαστε κάθεσαι – κάθεστε κάθεται – κάθονται ???????? Ενεστώτας κάθομαι – καθόμαστε κάθεσαι – κάθεστε κάθεται – κάθονται Imperative mood (убрал разделение на cont. и perfect imperative) Κάθισε! (colloq. Κάτσε!) – Καθίστε! (colloq. Κάτσετε!)
# γίνομαι # спряжение глагола	I become 1) возникать, появляться 2) осуществляться, совершаться; иметь место; состояться 3) становиться, делаться * * * Ενεστώτας γίνομαι – γινόμαστε γίνεσαι – γίνεστε γίνεται – γίνονται Αόριστος έγινα – γίναμε έγινες – γίνατε έγινε – έγιναν Συνοπτικός Μέλλοντας θα γίνω – θα γίνουμε θα γίνεις – θα γίνετε θα γίνει – θα γίνουν Perfective imperative mood Γίνε! – Γίνετε! * * * Ενεστώτας γίνομαι – γινόμαστε γίνεσαι – γίνεστε γίνεται – γίνονται ??????? Ενεστώτας γίνομαι – γινόμαστε γίνεσαι – γίνεστε γίνεται – γίνονται Imperfective imperative mood Να γίνεσαι! – Γίνεστε!
# """
# res = parse_verbs_from_Anki(input)
# print(res)
