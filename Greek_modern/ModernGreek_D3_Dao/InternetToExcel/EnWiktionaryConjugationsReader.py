import re

import requests
from bs4 import BeautifulSoup

import ImperativeFomatter
from HelperCode import CommonAssembler

base_url = "https://{lang}.wiktionary.org/wiki/"
pipe_delimited_pair = '{0}|{1}'


def parse_html_to_get_conjugation_tables(word):
    LANG_CODE = 'en'
    url = base_url.format(lang=LANG_CODE) + word

    response = requests.get(url)
    parser = 'html.parser'  # or lxml or html5lib
    encoding = response.encoding if 'charset' in response.headers.get('content-type', '').lower() else None

    beautiful_soup = BeautifulSoup(response.content, parser, from_encoding=encoding)
    target_divs = beautiful_soup.findAll('div', {'class': 'NavFrame'})

    # active_voice_table = None
    # passive_voice_table = None
    conjugations_table = None
    for target_div in target_divs:
        conjugations_table = target_div.find('table')
        if conjugations_table is not None:
            break

    return conjugations_table


def take_first_comma_separated_value(verb_form):
    res = verb_form
    if ',' in verb_form:
        res = verb_form.split(',')[0]

    return res


def format_as_three_piped_pairs(tense):
    res = []
    if len(tense) == 6:
        res = [pipe_delimited_pair.format(
            take_first_comma_separated_value(tense[i % 3]), take_first_comma_separated_value(tense[i]))
            for i in range(3, 6)]
    return res


def make_up_perfect_tenses(infinitive):
    perfective_aspect_present = []
    perfective_aspect_past = []
    perfective_aspect_future = []
    perfective_aspect_subjunctive = []

    if len(infinitive) > 0:
        perfective_aspect_present = [person + infinitive for person in
                                     ['έχω ', 'έχεις ', 'έχει ', 'έχουμε ', 'έχετε ', 'έχουν ']]
        perfective_aspect_past = [person + infinitive for person in
                                  ['είχα ', 'είχες ', 'είχε ', 'είχαμε ', 'είχατε ', 'είχαν ']]
        perfective_aspect_future = [person + infinitive for person in
                                    ['θα έχω ', 'θα έχεις ', 'θα έχει ', 'θα έχουμε ', 'θα έχετε ', 'θα έχουν ']]
        perfective_aspect_subjunctive = [person + infinitive for person in
                                         ['να έχω ', 'να έχεις ', 'να έχει ', 'να έχουμε ', 'να έχετε ', 'να έχουν ']]

    return perfective_aspect_present, perfective_aspect_past, perfective_aspect_future, perfective_aspect_subjunctive


# Main business method
def get_verb_conjugation(word):
    conjugations_table = parse_html_to_get_conjugation_tables(word)

    if conjugations_table is None:
        return "NO CONJUGATIONS FOR VERB " + word

    all_rows = conjugations_table.find_all('tr')
    tabular_data = list()
    for row in all_rows:
        row_data = row.find_all('td')
        # заменяет <br/>, находящийся в середине текста ячейки, на ", "
        row_data = [rd.get_text(separator=", ").strip() for rd in row_data]
        tabular_data.append([rd for rd in row_data if rd])  # Get rid of empty values

    # for d in tabular_data:
    #     print(d)

    NON_PAST_TENSES_MODE = False
    PAST_TENSES_MODE = False
    IMPERATIVES_MODE = False

    imperfective_aspect_present = []
    imperfective_aspect_past = []
    imperfective_aspect_future = []
    imperfective_aspect_subjunctive = []
    imperfective_aspect_imperative_dict = {}
    # participle = ""

    aoristic_aspect_present = []
    aoristic_aspect_past = []
    aoristic_aspect_future = []
    aoristic_aspect_subjunctive = []
    aoristic_aspect_imperative_dict = {}
    infinitive = ""

    perfective_aspect_present = []
    perfective_aspect_past = []
    perfective_aspect_future = []
    perfective_aspect_subjunctive = []
    perfective_aspect_imperative_dict = {}

    for i in range(2, len(tabular_data)):
        row = tabular_data[i]
        if len(row) == 0:
            continue

        if 'Non-past tenses' in row[0]:
            NON_PAST_TENSES_MODE = True
            continue
        elif 'Past tenses' in row[0]:
            PAST_TENSES_MODE = True
            continue
        elif 'Imperative' in row[0]:
            IMPERATIVES_MODE = True
            continue

        if NON_PAST_TENSES_MODE and len(imperfective_aspect_present) < 6:
            if re.match(r'[123].*?(sg|pl).*?', row[0]):
                imperfective_aspect_present.append(row[1].strip(','))
                imperfective_aspect_future.append('θα ' + row[1].strip(','))
                imperfective_aspect_subjunctive.append('να ' + row[1].strip(','))

                aoristic_aspect_present.append(row[1].strip(','))
                aoristic_aspect_future.append('θα ' + row[2].strip(','))
                aoristic_aspect_subjunctive.append('να ' + row[2].strip(','))

        elif PAST_TENSES_MODE and len(imperfective_aspect_past) < 6:
            if re.match(r'[123].*?(sg|pl).*?', row[0]):
                imperfective_aspect_past.append(row[1].strip(','))
                aoristic_aspect_past.append(row[2].strip(','))

        elif IMPERATIVES_MODE and len(imperfective_aspect_imperative_dict.items()) < 2:
            if re.match(r'[2].*?sg.*?', row[0]):
                imperfective_aspect_imperative_dict['sg'] = row[1].strip(',')
                aoristic_aspect_imperative_dict['sg'] = row[2].strip(',')
            elif re.match(r'[2].*?pl.*?', row[0]):
                imperfective_aspect_imperative_dict['pl'] = row[1].strip(',')
                aoristic_aspect_imperative_dict['pl'] = row[2].strip(',')

        elif 'Nonfinite form' in row[0]:
            infinitive = row[1].strip(',')
    # loop end

    perfective_aspect_present, perfective_aspect_past, perfective_aspect_future, perfective_aspect_subjunctive = make_up_perfect_tenses(
        infinitive)

    # PRESENT TENSES
    imperfective_aspect_present = format_as_three_piped_pairs(imperfective_aspect_present)
    aoristic_aspect_present = format_as_three_piped_pairs(aoristic_aspect_present)
    perfective_aspect_present = format_as_three_piped_pairs(perfective_aspect_present)

    # PAST TENSES
    aoristic_aspect_past = format_as_three_piped_pairs(aoristic_aspect_past)
    imperfective_aspect_past = format_as_three_piped_pairs(imperfective_aspect_past)
    perfective_aspect_past = format_as_three_piped_pairs(perfective_aspect_past)

    # FUTURE TENSES
    aoristic_aspect_future = format_as_three_piped_pairs(aoristic_aspect_future)
    imperfective_aspect_future = format_as_three_piped_pairs(imperfective_aspect_future)
    perfective_aspect_future = format_as_three_piped_pairs(perfective_aspect_future)

    # SUBJUNCTIVE
    aoristic_aspect_subjunctive = format_as_three_piped_pairs(aoristic_aspect_subjunctive)
    imperfective_aspect_subjunctive = format_as_three_piped_pairs(imperfective_aspect_subjunctive)
    perfective_aspect_subjunctive = format_as_three_piped_pairs(perfective_aspect_subjunctive)

    # IMPERATIVE
    aoristic_aspect_imperative = pipe_delimited_pair.format(
        ImperativeFomatter.capitalize_and_add_exclamation_mark(
            aoristic_aspect_imperative_dict['sg']) if 'sg' in aoristic_aspect_imperative_dict else '',
        ImperativeFomatter.capitalize_and_add_exclamation_mark(
            aoristic_aspect_imperative_dict['pl']) if 'pl' in aoristic_aspect_imperative_dict else ''
    )

    imperfective_aspect_imperative = pipe_delimited_pair.format(
        ImperativeFomatter.capitalize_and_add_exclamation_mark(
            imperfective_aspect_imperative_dict['sg']) if 'sg' in imperfective_aspect_imperative_dict else '',
        ImperativeFomatter.capitalize_and_add_exclamation_mark(
            imperfective_aspect_imperative_dict['pl']) if 'pl' in imperfective_aspect_imperative_dict else ''
    )

    perfective_aspect_imperative = pipe_delimited_pair.format(
        ImperativeFomatter.capitalize_and_add_exclamation_mark(
            perfective_aspect_imperative_dict['sg']) if 'sg' in perfective_aspect_imperative_dict else '',
        ImperativeFomatter.capitalize_and_add_exclamation_mark(
            perfective_aspect_imperative_dict['pl']) if 'pl' in perfective_aspect_imperative_dict else ''
    )

    output = CommonAssembler.assemble_conjugation_table(aoristic_aspect_present, imperfective_aspect_present,
                                                        perfective_aspect_present,
                                                        aoristic_aspect_past, imperfective_aspect_past,
                                                        perfective_aspect_past,
                                                        aoristic_aspect_future, imperfective_aspect_future,
                                                        perfective_aspect_future,
                                                        aoristic_aspect_subjunctive, imperfective_aspect_subjunctive,
                                                        perfective_aspect_subjunctive,
                                                        aoristic_aspect_imperative, imperfective_aspect_imperative,
                                                        perfective_aspect_imperative, infinitive)

    return output


############################

# verb_to_lookup = 'είμαι'
# verb_to_lookup = 'exw'
verb_to_lookup = 'θυμάμαι'
# verb_to_lookup = 'αγοράζω'
# verb_to_lookup = 'αγαπάω'
# verb_to_lookup = 'ανοίγω'
# verb_to_lookup = 'κλείνω'
# output = get_verb_conjugation(verb_to_lookup)
# print(output)
