import EnglishConstants


def _assemble_transcription(bare_word_lemma_transcription, ending):
    word_stress = ""  # empty by default
    if (EnglishConstants.STRESS_SYMBOL not in bare_word_lemma_transcription) and \
            any(ending_vowel in ending for ending_vowel in
                EnglishConstants.ENDINGS_VOWELS):  # проверить, что прибавляемое окончание содержит один из набора гласных
        # the following endings contain I_SOUND: IZ_ENDING, ID_ENDING, ING_ENDING
        # the following endings contain schwa sound: ER_ENDING
        word_stress = EnglishConstants.STRESS_SYMBOL
    transcription = word_stress + bare_word_lemma_transcription + ending
    return transcription


def _strip_square_brackets(word_lemma_transcription):
    if word_lemma_transcription.startswith('[') and word_lemma_transcription.endswith(']'):
        bare_word_lemma_transcription = word_lemma_transcription[1:-1]
    else:
        bare_word_lemma_transcription = word_lemma_transcription
    return bare_word_lemma_transcription


def compose_adjective_adverb_transcription(word, word_lemma_transcription):
    result = ""
    bare_word_lemma_transcription = _strip_square_brackets(word_lemma_transcription)

    if word.endswith('er'):  # comparative degree
        if bare_word_lemma_transcription[-1] == EnglishConstants.SCHWA:
            result = _assemble_transcription(bare_word_lemma_transcription, 'r' + EnglishConstants.ER_ENDING)
        else:
            result = _assemble_transcription(bare_word_lemma_transcription, EnglishConstants.ER_ENDING)
    elif word.endswith('est'):  # superlative degree
        if bare_word_lemma_transcription[-1] == EnglishConstants.SCHWA:
            result = _assemble_transcription(bare_word_lemma_transcription, 'r' + EnglishConstants.EST_ENDING)
        else:
            result = _assemble_transcription(bare_word_lemma_transcription, EnglishConstants.EST_ENDING)

    return result


def compose_noun_transcription(word, word_lemma, word_lemma_transcription):
    result = ""
    bare_word_lemma_transcription = _strip_square_brackets(word_lemma_transcription)
    word_ending = word.replace(word_lemma, '')

    # лесенка if-elif-...-else от самого конкретного и длинного окончания к самому общему и короткому
    if word.endswith('ves'):
        result = _assemble_transcription(bare_word_lemma_transcription[:-1] + "v", EnglishConstants.Z_ENDING)
    elif word.endswith('fes'):  # safe -> safes
        result = _assemble_transcription(bare_word_lemma_transcription, EnglishConstants.S_ENDING)
    elif word.endswith('ies'):
        result = _assemble_transcription(bare_word_lemma_transcription, EnglishConstants.Z_ENDING)
    elif word.endswith('es'):
        if bare_word_lemma_transcription[-1] in EnglishConstants.IZ_ENDING_PRODUCING_CONSONANTS:
            result = _assemble_transcription(bare_word_lemma_transcription, EnglishConstants.IZ_ENDING)
        # elif re.search('[o]$', word_lemma):
        elif word_lemma.endswith('o'):
            result = _assemble_transcription(bare_word_lemma_transcription, EnglishConstants.Z_ENDING)
        elif word_ending == 's':  # shoe -> shoes
            result = _assemble_transcription(bare_word_lemma_transcription, EnglishConstants.Z_ENDING)
    elif word.endswith('s'):
        if bare_word_lemma_transcription[-1] in EnglishConstants.unvoiced_consonants:
            result = _assemble_transcription(bare_word_lemma_transcription, EnglishConstants.S_ENDING)
        else:
            result = _assemble_transcription(bare_word_lemma_transcription, EnglishConstants.Z_ENDING)

    return result


def compose_noun_possessive_case_transcription(previous_word_transcription, pos_tag):
    result = ""
    bare_prev_word_transcription = _strip_square_brackets(previous_word_transcription)

    if pos_tag == 'POS':
        if bare_prev_word_transcription[-1] in EnglishConstants.IZ_ENDING_PRODUCING_CONSONANTS:
            result = _assemble_transcription(bare_prev_word_transcription, EnglishConstants.IZ_ENDING)
        elif bare_prev_word_transcription[-1] in EnglishConstants.unvoiced_consonants:
            result = _assemble_transcription(bare_prev_word_transcription, EnglishConstants.S_ENDING)
        else:
            result = _assemble_transcription(bare_prev_word_transcription, EnglishConstants.Z_ENDING)

    return result


def compose_verb_transcription(word, word_lemma, word_lemma_transcription):
    result = ""
    bare_word_lemma_transcription = _strip_square_brackets(word_lemma_transcription)
    # word_ending = word.replace(word_lemma, '')
    # word = re.sub(r'^to\s', '', word) # удалить частицу to

    # правила обработки окончаний глаголов 3-л. ед.ч. наст. вр. такие же, как и сущ. мн.ч.
    if word.endswith('s'):
        result = compose_noun_transcription(word, word_lemma, word_lemma_transcription)
    # правила обработки окончаний глаголов в форме Past Simple и Participle II
    elif word.endswith('ed'):
        if bare_word_lemma_transcription[
            -1] in EnglishConstants.ID_ENDING_PRODUCING_CONSONANTS:  # транскрипция глагола заканчивается на звуки [d] или [t]
            result = _assemble_transcription(bare_word_lemma_transcription, EnglishConstants.ID_ENDING)
        elif bare_word_lemma_transcription[-1] in EnglishConstants.unvoiced_consonants:
            # транскрипция глагола заканчивается на глухой согласный
            result = _assemble_transcription(bare_word_lemma_transcription, EnglishConstants.T_ENDING)
        else:
            # транскрипция глагола по остаточному принципу заканчивается на звонкий согласный или гласный
            result = _assemble_transcription(bare_word_lemma_transcription, EnglishConstants.D_ENDING)
    # правила обработки окончаний глаголов в форме Participle I
    elif word.endswith('ing'):
        result = _assemble_transcription(bare_word_lemma_transcription, EnglishConstants.ING_ENDING)

    return result
