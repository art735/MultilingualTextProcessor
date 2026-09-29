double_pipe_delimiter = '||'


def _join_single_values(aoristic_aspect_value, imperfective_aspect_value, perfective_aspect_value):
    if aoristic_aspect_value == '':
        aoristic_aspect_value = '|'
    if imperfective_aspect_value == '':
        imperfective_aspect_value = '|'
    if perfective_aspect_value == '':
        perfective_aspect_value = '|'

    out = double_pipe_delimiter.join([aoristic_aspect_value, imperfective_aspect_value, perfective_aspect_value])
    return out


def _join_tenses(aoristic_aspect_tense, imperfective_aspect_tense, perfective_aspect_tense, index):
    if len(aoristic_aspect_tense) == 0:
        aoristic_aspect_tense = ['|', '|', '|']
    if len(imperfective_aspect_tense) == 0:
        imperfective_aspect_tense = ['|', '|', '|']
    if len(perfective_aspect_tense) == 0:
        perfective_aspect_tense = ['|', '|', '|']

    aoristic_aspect_value = aoristic_aspect_tense[index]
    imperfective_aspect_value = imperfective_aspect_tense[index]
    perfective_aspect_value = perfective_aspect_tense[index]

    return _join_single_values(aoristic_aspect_value, imperfective_aspect_value, perfective_aspect_value)


def assemble_conjugation_table(aoristic_aspect_present, imperfective_aspect_present, perfective_aspect_present,
                               aoristic_aspect_past, imperfective_aspect_past, perfective_aspect_past,
                               aoristic_aspect_future, imperfective_aspect_future, perfective_aspect_future,
                               aoristic_aspect_subjunctive, imperfective_aspect_subjunctive,
                               perfective_aspect_subjunctive,
                               aoristic_aspect_imperative, imperfective_aspect_imperative, perfective_aspect_imperative,
                               infinitive):
    # PRESENT TENSES
    present_tenses_1st_person = _join_tenses(
        aoristic_aspect_present, imperfective_aspect_present, perfective_aspect_present, 0)

    present_tenses_2nd_person = _join_tenses(
        aoristic_aspect_present, imperfective_aspect_present, perfective_aspect_present, 1)

    present_tenses_3rd_person = _join_tenses(
        aoristic_aspect_present, imperfective_aspect_present, perfective_aspect_present, 2)

    # PAST TENSES
    past_tenses_1st_person = _join_tenses(
        aoristic_aspect_past, imperfective_aspect_past, perfective_aspect_past, 0)

    past_tenses_2nd_person = _join_tenses(
        aoristic_aspect_past, imperfective_aspect_past, perfective_aspect_past, 1)

    past_tenses_3rd_person = _join_tenses(
        aoristic_aspect_past, imperfective_aspect_past, perfective_aspect_past, 2)

    # FUTURE TENSES
    future_tenses_1st_person = _join_tenses(
        aoristic_aspect_future, imperfective_aspect_future, perfective_aspect_future, 0)

    future_tenses_2nd_person = _join_tenses(
        aoristic_aspect_future, imperfective_aspect_future, perfective_aspect_future, 1)

    future_tenses_3rd_person = _join_tenses(
        aoristic_aspect_future, imperfective_aspect_future, perfective_aspect_future, 2)

    # SUBJUNCTIVE
    subjunctive_1st_person = _join_tenses(
        aoristic_aspect_subjunctive, imperfective_aspect_subjunctive, perfective_aspect_subjunctive, 0)

    subjunctive_2nd_person = _join_tenses(
        aoristic_aspect_subjunctive, imperfective_aspect_subjunctive, perfective_aspect_subjunctive, 1)

    subjunctive_3rd_person = _join_tenses(
        aoristic_aspect_subjunctive, imperfective_aspect_subjunctive, perfective_aspect_subjunctive, 2)

    # IMPERATIVE
    imperatives = _join_single_values(
        aoristic_aspect_imperative, imperfective_aspect_imperative, perfective_aspect_imperative)

    # PUTTING IT ALL TOGETHER
    all_present_tenses = '\n'.join([present_tenses_1st_person, present_tenses_2nd_person, present_tenses_3rd_person])
    all_past_tenses = '\n'.join([past_tenses_1st_person, past_tenses_2nd_person, past_tenses_3rd_person])
    all_future_tenses = '\n'.join([future_tenses_1st_person, future_tenses_2nd_person, future_tenses_3rd_person])
    all_subjunctive_tenses = '\n'.join([subjunctive_1st_person, subjunctive_2nd_person, subjunctive_3rd_person])

    output = '\n\n'.join([all_present_tenses, all_past_tenses, all_future_tenses, all_subjunctive_tenses, imperatives,
                          infinitive])
    return output
