import re

personal_pronouns_with_transcriptions_dict = {
    "ich": "[ɪç]",
    "du": "[duː]",
    "er/sie/es": "[eːɐ/ziː/ɛs̯]",  # Это визуальный обман, что перед закрывающей скобкой есть пробел, его там нет!
    "wir": "[viːɐ̯]",
    "ihr": "[iːɐ̯]",
    "sie/Sie": "[ziː/ziː]"
}


def add_personal_pronoun_to_transcription(word, transcription):
    output = transcription
    for key, val in personal_pronouns_with_transcriptions_dict.items():
        if word.startswith(key):
            output = "[{0} {1}]".format(val[1:-1].strip(), transcription[1:-1].strip())
            break
    return output


def strip_personal_pronoun_before_verb(raw_verb):
    piped_personal_pronouns = '|'.join(personal_pronouns_with_transcriptions_dict.keys())
    bare_verb = re.sub(fr'^((dass\s)?({piped_personal_pronouns}))\s', '', raw_verb)
    return bare_verb


# На момент написания метода, планировалось его использование только при парсинге Excel-файла
def strip_personal_pronoun_after_imperative_verb_form(raw_verb):
    bare_verb = re.sub(r'\s(\(du\)|\(ihr\))$', '', raw_verb)
    return bare_verb


def strip_all_possible_personal_pronouns_around_verb(raw_verb):
    bare_verb = raw_verb
    bare_verb = strip_personal_pronoun_before_verb(bare_verb)
    bare_verb = strip_personal_pronoun_after_imperative_verb_form(bare_verb)
    return bare_verb


###############################################

if __name__ == '__main__':
    input1 = [
        'ich gelte', 'wir gelten',
        'du giltst', 'ihr geltet',
        'er/sie/es gilt', 'sie/Sie gelten',

        'gilt (du)', 'geltet (ihr)'
    ]

    er1 = [
        'gelte', 'gelten',
        'giltst', 'geltet',
        'gilt', 'gelten',

        'gilt', 'geltet'
    ]

    if all(strip_all_possible_personal_pronouns_around_verb(input_val) == er for input_val, er in zip(input1, er1)):
        print('test1 ok')
    else:
        print('test1 failed')

    # ---

    input2 = [
        'dass ich teilnehme', 'dass wir teilnehmen',
        'dass du teilnimmst', 'dass ihr teilnehmt',
        'dass er/sie/es teilnimmt', 'dass sie/Sie teilnehmen'
    ]

    er2 = [
        'teilnehme', 'teilnehmen',
        'teilnimmst', 'teilnehmt',
        'teilnimmt', 'teilnehmen'
    ]

    if all(strip_all_possible_personal_pronouns_around_verb(input_val) == er for input_val, er in zip(input1, er1)):
        print('test2 ok')
    else:
        print('test2 failed')
