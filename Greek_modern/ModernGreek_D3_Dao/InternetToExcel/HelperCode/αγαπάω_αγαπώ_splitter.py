import re

from HelperCode import CommonAssembler

# any_greek_letter_regex = r'[\u0370-\u03ff\u1f00-\u1fff]'
# greek_word = r'{0}+'.format(any_greek_letter_regex)

pipe_delimited_pair = '{0}|{1}'
modern_ancient_delimiter = ','


def disassemble_into_tenses(input_text):
    tenses = input_text.split('\n\n')

    all_present_tenses = tenses[0]
    all_past_tenses = tenses[1]
    all_future_tenses = tenses[2]
    all_subjunctive_tenses = tenses[3]
    imperatives = tenses[4]
    infinitive = tenses[5]

    present_tenses_1st_person, present_tenses_2nd_person, present_tenses_3rd_person = all_present_tenses.split('\n')
    past_tenses_1st_person, past_tenses_2nd_person, past_tenses_3rd_person = all_past_tenses.split('\n')
    future_tenses_1st_person, future_tenses_2nd_person, future_tenses_3rd_person = all_future_tenses.split('\n')
    subjunctive_tenses_1st_person, subjunctive_tenses_2nd_person, subjunctive_tenses_3rd_person = all_subjunctive_tenses.split(
        '\n')

    # PRESENT TENSES
    aoristic_aspect_present = []
    imperfective_aspect_present = []
    perfective_aspect_present = []

    for e in [present_tenses_1st_person, present_tenses_2nd_person, present_tenses_3rd_person]:
        aoristic, imperfective, perfective = e.split('||')
        aoristic_aspect_present.append(aoristic)
        imperfective_aspect_present.append(imperfective)
        perfective_aspect_present.append(perfective)

    # PAST TENSES
    aoristic_aspect_past = []
    imperfective_aspect_past = []
    perfective_aspect_past = []

    for e in [past_tenses_1st_person, past_tenses_2nd_person, past_tenses_3rd_person]:
        aoristic, imperfective, perfective = e.split('||')
        aoristic_aspect_past.append(aoristic)
        imperfective_aspect_past.append(imperfective)
        perfective_aspect_past.append(perfective)

    # FUTURE TENSES
    aoristic_aspect_future = []
    imperfective_aspect_future = []
    perfective_aspect_future = []

    for e in [future_tenses_1st_person, future_tenses_2nd_person, future_tenses_3rd_person]:
        aoristic, imperfective, perfective = e.split('||')
        aoristic_aspect_future.append(aoristic)
        imperfective_aspect_future.append(imperfective)
        perfective_aspect_future.append(perfective)

    # SUBJUNCTIVE TENSES
    aoristic_aspect_subjunctive = []
    imperfective_aspect_subjunctive = []
    perfective_aspect_subjunctive = []

    for e in [subjunctive_tenses_1st_person, subjunctive_tenses_2nd_person, subjunctive_tenses_3rd_person]:
        aoristic, imperfective, perfective = e.split('||')
        aoristic_aspect_subjunctive.append(aoristic)
        imperfective_aspect_subjunctive.append(imperfective)
        perfective_aspect_subjunctive.append(perfective)

    # IMPERATIVES
    all_found_delimiters = re.findall(r'\|\|', imperatives)
    no_of_delimiters = len(all_found_delimiters)
    if no_of_delimiters == 1:
        aoristic_aspect_imperative, imperfective_aspect_imperative = imperatives.split('||')
        perfective_aspect_imperative = ''
    elif no_of_delimiters == 2:
        aoristic_aspect_imperative, imperfective_aspect_imperative, perfective_aspect_imperative = imperatives.split(
            '||')

    return [aoristic_aspect_present, imperfective_aspect_present, perfective_aspect_present,
            aoristic_aspect_past, imperfective_aspect_past, perfective_aspect_past,
            aoristic_aspect_future, imperfective_aspect_future, perfective_aspect_future,
            aoristic_aspect_subjunctive, imperfective_aspect_subjunctive, perfective_aspect_subjunctive,
            aoristic_aspect_imperative, imperfective_aspect_imperative, perfective_aspect_imperative, infinitive]


def separate_single_row_modern_and_ancient_forms(row):
    sg, pl = row.split('|')
    # sg_forms = re.findall(greek_word, sg)
    # pl_forms = re.findall(greek_word, pl)
    sg_forms = [form.strip() for form in sg.split(modern_ancient_delimiter)]
    pl_forms = [form.strip() for form in pl.split(modern_ancient_delimiter)]

    modern_form = pipe_delimited_pair.format(sg_forms[0], pl_forms[0])
    # бывают ситуации, когда одна ячейка таблицы содержит более 2-х форм спряжений,
    # например: αγαπούσαν(ε), αγάπαγαν, αγαπάγανε
    # в этом случае первую форму считаем относящейся к modern_form, а остальные – к ancient_form
    # если это не так, вручную затем можно будет подправить в самом Excel, главное здесь не потерять все имеющиеся формы
    # и хоть куда-то их временно определить при парсинге Internet-таблицы
    ancient_form = pipe_delimited_pair.format(', '.join(sg_forms[1:]), ', '.join(pl_forms[1:]))
    return modern_form, ancient_form


def separate_whole_tense_modern_and_ancient_forms(tense_conjugations):
    modern_forms = []
    ancient_forms = []

    for i in range(0, len(tense_conjugations)):
        row = tense_conjugations[i]
        if modern_ancient_delimiter in row:  # если в строке присутствует разделитель
            modern_form, ancient_form = separate_single_row_modern_and_ancient_forms(row)
            modern_forms.append(modern_form)
            ancient_forms.append(ancient_form)
        else:
            modern_forms.append(row)
            ancient_forms.append(row)

    return modern_forms, ancient_forms


def print_tense_before_and_after_split(initial_forms, modern_forms, ancient_forms):
    for person_line in initial_forms:
        print(person_line)
    print()
    for person_line in modern_forms:
        print(person_line)
    print()
    for person_line in ancient_forms:
        print(person_line)


# Main business method!!!
def split_into_two_separate_paradigms(input_text):
    # Stage 1. Disassemble before processing
    [aoristic_aspect_present, imperfective_aspect_present, perfective_aspect_present,
     aoristic_aspect_past, imperfective_aspect_past, perfective_aspect_past,
     aoristic_aspect_future, imperfective_aspect_future, perfective_aspect_future,
     aoristic_aspect_subjunctive, imperfective_aspect_subjunctive, perfective_aspect_subjunctive,
     aoristic_aspect_imperative, imperfective_aspect_imperative, perfective_aspect_imperative,
     infinitive] = disassemble_into_tenses(input_text)

    # Stage 2. Distinguishing between ancient -ώ and modern -άω forms

    # for person_line in aoristic_aspect_imperative:
    #     print(person_line)

    # print(imperfective_aspect_imperative)

    # Present Simple & Present Continuous
    aoristic_aspect_present_modern_forms, aoristic_aspect_present_ancient_forms = \
        separate_whole_tense_modern_and_ancient_forms(aoristic_aspect_present)

    imperfective_aspect_present_modern_forms = aoristic_aspect_present_modern_forms
    imperfective_aspect_present_ancient_forms = aoristic_aspect_present_ancient_forms

    # print_tense_before_and_after_split(aoristic_aspect_present, aoristic_aspect_present_modern_forms,
    #                                    aoristic_aspect_present_ancient_forms)

    # Past Continuous
    imperfective_aspect_past_ousa_forms, imperfective_aspect_past_colloquial_forms = \
        separate_whole_tense_modern_and_ancient_forms(imperfective_aspect_past)

    # print_tense_before_and_after_split(imperfective_aspect_past, imperfective_aspect_past_ousa_forms,
    #                                    imperfective_aspect_past_colloquial_forms)

    # Future Continuous
    imperfective_aspect_future_modern_forms, imperfective_aspect_future_ancient_forms = \
        separate_whole_tense_modern_and_ancient_forms(imperfective_aspect_future)

    # print_tense_before_and_after_split(imperfective_aspect_future, imperfective_aspect_future_modern_forms,
    #                                    imperfective_aspect_future_ancient_forms)

    # Subjunctive imperfective
    imperfective_aspect_subjunctive_modern_forms, imperfective_aspect_subjunctive_ancient_forms = \
        separate_whole_tense_modern_and_ancient_forms(imperfective_aspect_subjunctive)

    # print_tense_before_and_after_split(imperfective_aspect_subjunctive, imperfective_aspect_subjunctive_modern_forms,
    #                                    imperfective_aspect_subjunctive_ancient_forms)

    # Stage 3. Assemble after processing
    output_ancient = CommonAssembler.assemble_conjugation_table(aoristic_aspect_present_ancient_forms,
                                                                imperfective_aspect_present_ancient_forms,
                                                                perfective_aspect_present,
                                                                aoristic_aspect_past,
                                                                imperfective_aspect_past_ousa_forms,
                                                                perfective_aspect_past,
                                                                # Past Cont.: здесь использую только -ousa форму
                                                                aoristic_aspect_future,
                                                                imperfective_aspect_future_ancient_forms,
                                                                perfective_aspect_future,
                                                                aoristic_aspect_subjunctive,
                                                                imperfective_aspect_subjunctive_ancient_forms,
                                                                perfective_aspect_subjunctive,
                                                                aoristic_aspect_imperative,
                                                                imperfective_aspect_imperative,
                                                                perfective_aspect_imperative, infinitive)

    output_modern = CommonAssembler.assemble_conjugation_table(aoristic_aspect_present_modern_forms,
                                                               imperfective_aspect_present_modern_forms,
                                                               perfective_aspect_present,
                                                               aoristic_aspect_past, imperfective_aspect_past,
                                                               perfective_aspect_past,
                                                               # Past Cont.: здесь использую обе формы, как они указаны в таблице
                                                               aoristic_aspect_future,
                                                               imperfective_aspect_future_modern_forms,
                                                               perfective_aspect_future,
                                                               aoristic_aspect_subjunctive,
                                                               imperfective_aspect_subjunctive_modern_forms,
                                                               perfective_aspect_subjunctive,
                                                               aoristic_aspect_imperative,
                                                               imperfective_aspect_imperative,
                                                               perfective_aspect_imperative, infinitive)

    output = output_modern + '\n\n# # #\n\n' + output_ancient
    return output


################################################


input_str = """αγαπάω, αγαπώ|αγαπάμε, αγαπούμε||αγαπάω, αγαπώ|αγαπάμε, αγαπούμε||έχω αγαπήσει|έχουμε αγαπήσει
αγαπάς|αγαπάτε||αγαπάς|αγαπάτε||έχεις αγαπήσει|έχετε αγαπήσει
αγαπάει, αγαπά|αγαπάν(ε), αγαπούν(ε)||αγαπάει, αγαπά|αγαπάν(ε), αγαπούν(ε)||έχει αγαπήσει|έχουν αγαπήσει

αγάπησα|αγαπήσαμε||αγαπούσα, αγάπαγα|αγαπούσαμε, αγαπάγαμε||είχα αγαπήσει|είχαμε αγαπήσει
αγάπησες|αγαπήσατε||αγαπούσες, αγάπαγες|αγαπούσατε, αγαπάγατε||είχες αγαπήσει|είχατε αγαπήσει
αγάπησε|αγάπησαν, αγαπήσαν(ε)||αγαπούσε, αγάπαγε|αγαπούσαν(ε), αγάπαγαν, αγαπάγανε||είχε αγαπήσει|είχαν αγαπήσει

θα αγαπήσω|θα αγαπήσουμε, θα αγαπήσομε||θα αγαπάω, θα αγαπώ|θα αγαπάμε, θα αγαπούμε||θα έχω αγαπήσει|θα έχουμε αγαπήσει
θα αγαπήσεις|θα αγαπήσετε||θα αγαπάς|θα αγαπάτε||θα έχεις αγαπήσει|θα έχετε αγαπήσει
θα αγαπήσει|θα αγαπήσουν(ε)||θα αγαπάει, θα αγαπά|θα αγαπάν(ε), θα αγαπούν(ε)||θα έχει αγαπήσει|θα έχουν αγαπήσει

να αγαπήσω|να αγαπήσουμε, να αγαπήσομε||να αγαπάω, να αγαπώ|να αγαπάμε, να αγαπούμε||να έχω αγαπήσει|να έχουμε αγαπήσει
να αγαπήσεις|να αγαπήσετε||να αγαπάς|να αγαπάτε||να έχεις αγαπήσει|να έχετε αγαπήσει
να αγαπήσει|να αγαπήσουν(ε)||να αγαπάει, να αγαπά|να αγαπάν(ε), να αγαπούν(ε)||να έχει αγαπήσει|να έχουν αγαπήσει

αγάπησε, αγάπα|αγαπήστε||αγάπα, αγάπαγε|αγαπάτε

αγαπήσει"""

input_str = """τρώω, τρώγω|τρώμε, τρώγομε, τρώγουμε||τρώω, τρώγω|τρώμε, τρώγομε, τρώγουμε||έχω φάει|έχουμε φάει
τρως, τρώγεις|τρώτε, τρώγετε||τρως, τρώγεις|τρώτε, τρώγετε||έχεις φάει|έχετε φάει
τρώει, τρώγει|τρώνε, τρων, τρώγουν(ε)||τρώει, τρώγει|τρώνε, τρων, τρώγουν(ε)||έχει φάει|έχουν φάει

έφαγα|φάγαμε||έτρωγα|τρώγαμε||είχα φάει|είχαμε φάει
έφαγες|φάγατε||έτρωγες|τρώγατε||είχες φάει|είχατε φάει
έφαγε|έφαγαν, φάγαν(ε)||έτρωγε|έτρωγαν, τρώγαν(ε)||είχε φάει|είχαν φάει

θα φάω|θα φάμε||θα τρώω, θα τρώγω|θα τρώμε, θα τρώγουμε, θα τρώγομε||θα έχω φάει|θα έχουμε φάει
θα φας|θα φάτε||θα τρως, θα τρώγεις|θα τρωτε, θα τρώγετε||θα έχεις φάει|θα έχετε φάει
θα φάει|θα φάνε, θα φάν||θα τρώει|θα τρώνε, θα τρων, θα τρώγουν(ε)||θα έχει φάει|θα έχουν φάει

να φαω|να φάμε||να τρώω, να τρώγω|να τρώμε, να τρώγουμε, να τρώγομε||να έχω φάει|να έχουμε φάει
να φας|να φάτε||να τρως|να τρώτε||να έχεις φάει|να έχετε φάει
να φάει|να φάνε, να φαν||να τρώει|να τρώνε, να τρων, να τρώγουν(ε)||να έχει φάει|να έχουν φάει

Φάε!|Φάτε!||Τρώγε!|Τρώτε!, Τρώγετε!|||

φάει"""

res = split_into_two_separate_paradigms(input_str)
print(res)
