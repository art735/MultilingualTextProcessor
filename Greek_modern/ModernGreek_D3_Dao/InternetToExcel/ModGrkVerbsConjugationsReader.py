import re

import requests
from bs4 import BeautifulSoup

import GreekToLatinTransliterater
import ImperativeFomatter
import exceptional_verbs
import αγαπάω_αγαπώ_splitter
from HelperCode import CommonAssembler

base_url = "https://moderngreekverbs.com/"


def parse_html_to_get_conjugation_tables(latin_transliteration):
    url = base_url + latin_transliteration

    response = requests.get(url)
    parser = 'html.parser'  # or lxml or html5lib
    encoding = response.encoding if 'charset' in response.headers.get('content-type', '').lower() else None

    beautiful_soup = BeautifulSoup(response.content, parser, from_encoding=encoding)
    all_tables = beautiful_soup.find_all('table')

    if len(all_tables) >= 1:
        return all_tables[0]
    else:
        return None


def format_imperative_forms(row):
    sg = row[0]
    pl = row[1]

    sg_verbs = [ImperativeFomatter.capitalize_and_add_exclamation_mark(verb) for verb in sg.split(',')]
    pl_verbs = [ImperativeFomatter.capitalize_and_add_exclamation_mark(verb) for verb in pl.split(',')]

    comma_and_space = ', '
    return comma_and_space.join(sg_verbs) + '|' + comma_and_space.join(pl_verbs)


def init_tense():
    # return ['|', '|', '|']
    return []


def format_row(row_data):
    # row_to_add = ''
    #
    # if len(row_data) == 4:
    #
    #
    # if voice == 'ACTIVE':
    #     if len(row_data) == 4:
    #         row_to_add = "{0}|{1}".format(row_data[0], row_data[1])
    #     elif len(row_data) == 2:
    #         row_to_add = row_data[0]
    # elif voice == 'PASSIVE':
    #     if len(row_data) == 4:
    #         row_to_add = "{0}|{1}".format(row_data[2], row_data[3])
    #     elif len(row_data) == 2:
    #         row_to_add = row_data[1]

    return '|'.join(row_data)


def fill_tense_with_data_rows(mood_dict, mood, tense, row_data):
    row_to_add = format_row(row_data)
    mood_dict[tense].append(row_to_add)


#######################
# Main business method
# входящий параметр 'verb' может быть написан как греческими, так и латинскими буквами
def get_verb_conjugation(verb, should_treat_ώ_ending_as_άω_ending):
    if should_treat_ώ_ending_as_άω_ending:
        if verb.endswith('ώ') and verb not in exceptional_verbs.only_omega_stressed_verbs:
            # берём корень глагола, игнорируя последнюю букву (окончание -ώ), и добавляем современное окончание -άω
            verb = verb[:-1] + 'άω'

    process_both_active_and_passive_voices = False
    if verb.endswith('ομαι') and verb not in exceptional_verbs.only_mediopassive_verbs:
        # ищем на сайте глагол по его активной форме (напр., вместо ξυρίζομαι ищем ξυρίζω)
        verb = verb[:-4] + 'ω'
        process_both_active_and_passive_voices = True

    verb_in_latin_letters_regex = r'[a-zA-Z]+'
    if re.match(verb_in_latin_letters_regex, verb):  # если входящий глагол написан латинскими символами
        latin_transliteration = verb
    else:
        latin_transliteration = GreekToLatinTransliterater.greek_to_latin(verb)

    conjugation_table = parse_html_to_get_conjugation_tables(latin_transliteration)

    if conjugation_table is None:
        return "NO CONJUGATIONS FOR VERB {0} ({1})".format(verb, latin_transliteration)

    ###############################################################

    active_voice_rows = []
    passive_voice_rows = []

    all_rows = conjugation_table.find_all('tr')
    header_row = [re.sub(r'\n', '', th.get_text()) for th in all_rows[0].find_all('th')]
    is_passive_voice_exists_in_table = False
    if 'Passive' in header_row:
        is_passive_voice_exists_in_table = True

    for i in range(2, len(all_rows)):  # 0-й и 1-й элементы списка - это шапка таблицы; пропускаем их
        row = all_rows[i]
        row_headers = [re.sub(r'\n', '', th.get_text()) for th in row.find_all('th')]
        row_data = [re.sub(r'\s\s+', ' ', td.get_text().split('\n')[0]) for td in row.find_all('td')]

        # если строка содержит 4 элемента, значит в таблице присутствуют и активный, и пассивный залоги
        if len(row_data) == 4:
            active_voice_rows.append((row_headers, row_data[:2]))  # two first elements
            passive_voice_rows.append((row_headers, row_data[-2:]))  # two last elements
        # если строка содержит только 2 элемента, это может быть истрактовано двояко:
        # 1) либо таблица содержит и активный, и пассивный залоги, но в рамках каждого из них произошло объединение
        # 2-х соседних ячеек (как в строке с инфинитивом, например)
        # 2) либо же таблица содержит только активный залог
        # Вот поэтому нужен специальный флаг, который подскажет как трактовать данную ситуацию
        elif len(row_data) == 2:
            if is_passive_voice_exists_in_table:
                active_voice_rows.append((row_headers, row_data[0]))
                passive_voice_rows.append((row_headers, row_data[1]))
            else:
                active_voice_rows.append((row_headers, row_data))
        elif len(row_data) == 1:
            active_voice_rows.append((row_headers, row_data[0]))

    ############################################################

    if process_both_active_and_passive_voices:
        results = [process_single_voice(active_voice_rows), process_single_voice(passive_voice_rows)]
        output = '\n\n+ + +\n\n'.join(results)
    else:
        output = process_single_voice(active_voice_rows)

    return output


# данный метод обрабатывает вычитанную таблицу спряжений отедельно для активного, и отдельного для пассивного залогов
def process_single_voice(particular_voice_rows):
    imperfective_aspect_present = init_tense()
    imperfective_aspect_past = init_tense()
    imperfective_aspect_future = init_tense()
    imperfective_aspect_subjunctive = init_tense()
    imperfective_aspect_imperative = '|'
    pres_participles = '|'

    aoristic_aspect_present = init_tense()
    aoristic_aspect_past = init_tense()
    aoristic_aspect_future = init_tense()
    aoristic_aspect_subjunctive = init_tense()
    aoristic_aspect_imperative = '|'
    infinitive = ""

    perfective_aspect_present = init_tense()
    perfective_aspect_past = init_tense()
    perfective_aspect_future = init_tense()
    perfective_aspect_subjunctive = init_tense()
    perfective_aspect_imperative = ''  # вроде бы нет таких форм в новогреческом, хотя в wiktionary для нек-рых глаголов есть!
    perf_participles = '|'

    # INDICATIVE MOOD
    indicative_mood_dict = {
        'Present': imperfective_aspect_present,
        'Imperfect': imperfective_aspect_past,
        'FutureContinuous': imperfective_aspect_future,

        # '': aoristic_aspect_present,
        'Aorist': aoristic_aspect_past,
        'SimpFut': aoristic_aspect_future,

        'Perfect': perfective_aspect_present,
        'Pluperfect': perfective_aspect_past,
        'FutPerf': perfective_aspect_future
    }

    # SUBJUNCTIVE MOOD
    subjunctive_mood_dict = {
        'Present': imperfective_aspect_subjunctive,
        'Aorist': aoristic_aspect_subjunctive,
        'Perf': perfective_aspect_subjunctive,
    }

    # IMPERATIVE MOOD
    # imperative_mood_dict = {
    # 'Pres': imperfective_aspect_imperative,
    # 'Aorist': aoristic_aspect_imperative
    # }

    participles_dict = {
        'Pres': pres_participles,
        'Perf': perf_participles
    }

    moods = ['INDICATIVE', 'SUBJUNCTIVE', 'Imperative', 'Participle', 'Infin']
    tenses = ['Present', 'Imperfect', 'Aorist', 'Perfect', 'Pluperfect', 'FutureContinuous',
              'SimpFut', 'FutPerf', 'Perf', 'Pres']

    current_mood = ''
    current_tense = ''

    for row_headers, row_data in particular_voice_rows:
        # define current MOOD and TENSE
        # если список содержит 2 элемента, то 1-й из них mood, 2-й - tense
        if len(row_headers) == 2:
            if row_headers[0] in moods:
                current_mood = row_headers[0]
            if row_headers[1] in tenses:
                current_tense = row_headers[1]
        # если список содержит 1 элемент, то это новый tense, а mood остаётся прежним
        elif len(row_headers) == 1:
            if row_headers[0] in tenses:
                current_tense = row_headers[0]

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # главная работа по наполнению current_tense-коллекций данными!
        if current_mood == 'INDICATIVE':
            fill_tense_with_data_rows(indicative_mood_dict, current_mood, current_tense, row_data)
        elif current_mood == 'SUBJUNCTIVE':
            fill_tense_with_data_rows(subjunctive_mood_dict, current_mood, current_tense, row_data)
        elif current_mood == 'Imperative':
            if current_tense == 'Pres':
                imperfective_aspect_imperative = format_imperative_forms(row_data)
            elif current_tense == 'Aorist':
                aoristic_aspect_imperative = format_imperative_forms(row_data)
        # причастия парсятся, но пока в Excel не сохраняются;
        # нужно разобраться подробнее с их структурой и количеством возможных вариантов
        elif current_mood == 'Participle':
            if current_tense == 'Pres':
                pres_participles = format_row(row_data)
            elif current_tense == 'Perf':
                perf_participles = format_row(row_data)
        elif current_mood == 'Infin':
            infinitive = row_data

    # loop end

    aoristic_aspect_present = imperfective_aspect_present

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

    # Define whether 'αγαπάω_αγαπώ_splitter' should be used
    if len(aoristic_aspect_present) > 0:
        first_person = aoristic_aspect_present[0]
        if '|' in first_person:
            sg, pl = first_person.split('|')
            if ', ' in sg:
                sg_1, sg_2 = sg.split(', ')
                if sg_1.endswith('άω') and sg_2.endswith('ώ'):
                    output = αγαπάω_αγαπώ_splitter.split_into_two_separate_paradigms(output)

    return output


############################

# verb_to_lookup = 'είμαι'
# verb_to_lookup = 'exw'
# verb_to_lookup = 'αρέσω'
# verb_to_lookup = 'δοκιμάζω'
# verb_to_lookup = 'αργώ'
# verb_to_lookup = 'αγοράζω'
# verb_to_lookup = 'αγαπάω'
# verb_to_lookup = 'ζητώ'
# verb_to_lookup = 'θυμάμαι'
# verb_to_lookup = 'ξυρίζομαι'
verb_to_lookup = 'κάθομαι'
# verb_to_lookup = 'ανατέλλω'
# verb_to_lookup = 'κλείνω'
# output = get_verb_conjugation(verb_to_lookup, True)
# print(output)
