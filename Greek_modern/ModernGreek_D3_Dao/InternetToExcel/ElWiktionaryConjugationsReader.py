import requests
from bs4 import BeautifulSoup

import ImperativeFomatter
from HelperCode import CommonAssembler

base_url = "https://{lang}.wiktionary.org/wiki/"
pipe_delimited_pair = '{0}|{1}'


def parse_html_to_get_conjugation_tables(word):
    lang_code = 'el'
    url = base_url.format(lang=lang_code) + word

    response = requests.get(url)
    parser = 'html.parser'  # or lxml or html5lib
    encoding = response.encoding if 'charset' in response.headers.get('content-type', '').lower() else None

    beautiful_soup = BeautifulSoup(response.content, parser, from_encoding=encoding)
    # all_inflection_tables = beautiful_soup.find_all("table")
    # active_voice_table = all_inflection_tables[1]

    # table_div = beautiful_soup.find('div', id="NavFrame1")
    # table_div = beautiful_soup.findAll('div', {'id': 'NavFrame1'})
    target_divs = beautiful_soup.findAll('div', {'class': 'NavFrame'})

    active_voice_table = None
    passive_voice_table = None
    for target_div in target_divs:
        if 'Ενεργητική φωνή' in target_div.text:
            active_voice_table = target_div.find('table')
        elif 'Παθητική φωνή' in target_div.text:
            passive_voice_table = target_div.find('table')

    return active_voice_table, passive_voice_table


def format_as_three_piped_pairs(tense):
    result = []
    if len(tense) == 6:
        result = [pipe_delimited_pair.format(tense[i % 3], tense[i]) for i in range(3, 6)]
    return result


# Main business method
def get_verb_conjugation(word):
    active_voice_table, passive_voice_table = parse_html_to_get_conjugation_tables(word)

    if active_voice_table is None:
        return "NO CONJUGATIONS FOR VERB " + word

    # active_voice_table_body = active_voice_table.find('tbody')

    all_rows = active_voice_table.find_all('tr')
    data = list()
    for row in all_rows:
        columns = row.find_all('td')
        # заменяет <br/>, находящийся в середине текста ячейки, на ", "
        columns = [column.get_text(separator=", ").strip() for column in columns]
        data.append([column for column in columns if column])  # Get rid of empty values

    # # el.wiktionary.org не содержит спряжений некоторых глаголов, заканчивающихся на -ώ (напр., αγαπώ).
    # # Спряжения для таких глаголов нужно искать с альтернативным окончанием на -άω (напр., αγαπάω)
    # # Тем не менее, таблица <table> на страничке с глаголов на -ώ присутствует и содержит после парсинга одну строку
    # # поэтому проверяем, чтобы размер списка вычитанных данных не содержит даже 2-х строк,
    # # досрочно завершаем работу функции
    # if len(data) < 2:
    #     return "NO CONJUGATIONS FOR VERB " + word

    # for d in data:
    #     print(d)

    IMPERFECTIVE_ASPECT_INDEX = 0
    AORISTIC_ASPECT_INDEX = 1
    PERFECTIVE_ASPECT_INDEX = 2

    imperfective_aspect_present = []
    imperfective_aspect_past = []
    imperfective_aspect_future = []
    imperfective_aspect_subjunctive = []
    imperfective_aspect_imperative_dict = {}
    # participle = ""

    # aoristic_aspect_present = [] - данного времени в таблице нет, оно совпадает с imperfective_aspect_present
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

    current_aspect_index = 0
    for row in data:
        if current_aspect_index == IMPERFECTIVE_ASPECT_INDEX:
            if len(row) > 0:
                if row[0] == "α' ενικ.":
                    imperfective_aspect_present.append(row[1])
                    imperfective_aspect_past.append(row[2])
                    imperfective_aspect_future.append(row[3])
                    imperfective_aspect_subjunctive.append(row[4])
                    participle = row[5]
                elif row[0] == "β' ενικ.":
                    imperfective_aspect_present.append(row[1])
                    imperfective_aspect_past.append(row[2])
                    imperfective_aspect_future.append(row[3])
                    imperfective_aspect_subjunctive.append(row[4])
                    if len(row) == 6:
                        imperfective_aspect_imperative_dict['sg'] = row[5]
                elif row[0] == "γ' ενικ.":
                    imperfective_aspect_present.append(row[1])
                    imperfective_aspect_past.append(row[2])
                    imperfective_aspect_future.append(row[3])
                    imperfective_aspect_subjunctive.append(row[4])
                elif row[0] == "α' πληθ.":
                    imperfective_aspect_present.append(row[1])
                    imperfective_aspect_past.append(row[2])
                    imperfective_aspect_future.append(row[3])
                    imperfective_aspect_subjunctive.append(row[4])
                elif row[0] == "β' πληθ.":
                    imperfective_aspect_present.append(row[1])
                    imperfective_aspect_past.append(row[2])
                    imperfective_aspect_future.append(row[3])
                    imperfective_aspect_subjunctive.append(row[4])
                    if len(row) == 6:
                        imperfective_aspect_imperative_dict['pl'] = row[5]
                elif row[0] == "γ' πληθ.":
                    imperfective_aspect_present.append(row[1])
                    imperfective_aspect_past.append(row[2])
                    imperfective_aspect_future.append(row[3])
                    imperfective_aspect_subjunctive.append(row[4])
                    current_aspect_index = current_aspect_index + 1  # переходим к следующему аспекту

        elif current_aspect_index == AORISTIC_ASPECT_INDEX:
            if len(row) > 0:
                if row[0] == "α' ενικ.":
                    aoristic_aspect_past.append(row[1])
                    aoristic_aspect_future.append(row[2])
                    aoristic_aspect_subjunctive.append(row[3])
                    infinitive = row[4]
                elif row[0] == "β' ενικ.":
                    aoristic_aspect_past.append(row[1])
                    aoristic_aspect_future.append(row[2])
                    aoristic_aspect_subjunctive.append(row[3])
                    aoristic_aspect_imperative_dict['sg'] = row[4]
                elif row[0] == "γ' ενικ.":
                    aoristic_aspect_past.append(row[1])
                    aoristic_aspect_future.append(row[2])
                    aoristic_aspect_subjunctive.append(row[3])
                elif row[0] == "α' πληθ.":
                    aoristic_aspect_past.append(row[1])
                    aoristic_aspect_future.append(row[2])
                    aoristic_aspect_subjunctive.append(row[3])
                elif row[0] == "β' πληθ.":
                    aoristic_aspect_past.append(row[1])
                    aoristic_aspect_future.append(row[2])
                    aoristic_aspect_subjunctive.append(row[3])
                    aoristic_aspect_imperative_dict['pl'] = row[4]
                elif row[0] == "γ' πληθ.":
                    aoristic_aspect_past.append(row[1])
                    aoristic_aspect_future.append(row[2])
                    aoristic_aspect_subjunctive.append(row[3])
                    current_aspect_index = current_aspect_index + 1  # переходим к следующему аспекту

        elif current_aspect_index == PERFECTIVE_ASPECT_INDEX:
            if len(row) > 0:
                if row[0] == "α' ενικ.":
                    perfective_aspect_present.append(row[1])
                    perfective_aspect_past.append(row[2])
                    perfective_aspect_future.append(row[3])
                    perfective_aspect_subjunctive.append(row[4])
                elif row[0] == "β' ενικ.":
                    perfective_aspect_present.append(row[1])
                    perfective_aspect_past.append(row[2])
                    perfective_aspect_future.append(row[3])
                    perfective_aspect_subjunctive.append(row[4])
                    if len(row) == 6:
                        perfective_aspect_imperative_dict['sg'] = row[5]
                elif row[0] == "γ' ενικ.":
                    perfective_aspect_present.append(row[1])
                    perfective_aspect_past.append(row[2])
                    perfective_aspect_future.append(row[3])
                    perfective_aspect_subjunctive.append(row[4])
                elif row[0] == "α' πληθ.":
                    perfective_aspect_present.append(row[1])
                    perfective_aspect_past.append(row[2])
                    perfective_aspect_future.append(row[3])
                    perfective_aspect_subjunctive.append(row[4])
                elif row[0] == "β' πληθ.":
                    perfective_aspect_present.append(row[1])
                    perfective_aspect_past.append(row[2])
                    perfective_aspect_future.append(row[3])
                    perfective_aspect_subjunctive.append(row[4])
                    if len(row) == 6:
                        perfective_aspect_imperative_dict['pl'] = row[5]
                elif row[0] == "γ' πληθ.":
                    perfective_aspect_present.append(row[1])
                    perfective_aspect_past.append(row[2])
                    perfective_aspect_future.append(row[3])
                    perfective_aspect_subjunctive.append(row[4])
                    current_aspect_index = current_aspect_index + 1  # переходим к следующему аспекту

    # oo_writer_pattern = "{0}|{1}||{2}|{3}||{4}|{5}"

    # PRESENT TENSES
    imperfective_aspect_present = format_as_three_piped_pairs(imperfective_aspect_present)
    aoristic_aspect_present = imperfective_aspect_present
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

# verb_to_lookup = 'ζητώ'
verb_to_lookup = 'επιθυμώ'
# verb_to_lookup = 'αγοράζω'
# verb_to_lookup = 'αγαπάω'
# verb_to_lookup = 'ανοίγω'
# verb_to_lookup = 'κλείνω'
output = get_verb_conjugation(verb_to_lookup)
print(output)
