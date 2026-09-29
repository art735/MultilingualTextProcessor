# Строка нужна для предотвращения ошибки SyntaxError: Non-UTF-8 code starting with '\xd0'
# -*- coding: utf-8 -*-

import re

import beautiful_soup_helper
import exceptional_verbs
from AnkiConnectService import AnkiConnectService


def parse_front_field(field_data):
    result = field_data

    # Разбивать содержимое поля Front по <br><br>, брать 1-й токен и стрипать его от любых тегов
    pieces = field_data.split('<br><br>')
    if len(pieces) > 0:
        result = beautiful_soup_helper.strip_all_tags(pieces[0])

    return result


def parse_back_field(field_data):
    translation = field_data

    pieces = field_data.split('<br><br>')
    if len(pieces) > 0:
        for piece in pieces:

            # Заменяем <br> на ^^^, чтобы затем в OO Writer превратить их в \n
            piece = re.sub(r'<br>', '^^^', piece)

            # Очищаем от всех html-тегов
            piece = beautiful_soup_helper.strip_all_tags(piece)

            # re.match is anchored at the start ^pattern. Ensures the string begins with the pattern
            # VS.
            # re.fullmatch is anchored at the start and end of the pattern ^pattern$.
            # Ensures the full string matches the pattern

            # выкусываем регулярным выражением русский перевод глагола: он содержит русские буквы (большие и маленькие),
            # некоторые знаки пунктуации, цифры, круглые скобки и пробел
            if re.match(r'[А-Яа-я0-9\(\),;\s]+', piece):  # re.match оказался более уместен, чем re.fullmatch
                translation = piece
                break

    return translation


def process_single_note(note, ignored_fields):
    verb = ''
    translation = ''

    for field_name, value in note['fields'].items():
        if field_name not in ignored_fields:  # некоторые поля не нужно обрабатывать, например Audio
            if field_name == 'Front':
                verb = parse_front_field(value['value'])
            elif field_name == 'Back':
                translation = parse_back_field(value['value'])

    return verb, translation


def process_specially_ended_verbs(verb_translation_dict):
    # убедиться, что у глаголов, заканчивающихся на -ώ или -άω, есть соотв. hint в переводе
    stressed_omega_hint = '^^^(-ώ)'
    ao_hint = '^^^(-άω)'

    additional_verb_translation_dict = {}
    for verb, translation in verb_translation_dict.items():
        # для глаголов на -ώ пробуем добавить более современный аналог на -άω
        if verb.endswith('ώ') and verb not in exceptional_verbs.only_omega_stressed_verbs:
            # обновляем translation существующего в словаре глагола
            if not translation.endswith(stressed_omega_hint):
                translation += stressed_omega_hint
                verb_translation_dict[verb] = translation

            # берём корень глагола, игнорируя последнюю букву (окончание -ώ), и добавляем современное окончание -άω
            # не для всех глаголов так можно делать; неподходящие варианты потом нужно будет удалить вручную из словаря
            verb_άω = verb[:-1] + 'άω'
            if verb_άω not in verb_translation_dict:
                # просто подстраховка; вообще-то translation глагола на -ώ на данном этапе всегда должен иметь хинт в виде '^^^(-ώ)'
                if translation.endswith(stressed_omega_hint):
                    translation = translation.replace(stressed_omega_hint, ao_hint)
                else:
                    translation += ao_hint
                additional_verb_translation_dict[verb_άω] = translation
        # для медиопассивных глаголов на -ομαι добавляем активную форму на -ω
        # не для всех глаголов так можно делать; неподходящие варианты потом нужно будет удалить вручную из словаря
        elif verb.endswith('ομαι') and verb not in exceptional_verbs.only_mediopassive_verbs:
            active_voice_counterpart = verb[:-4] + 'ω'
            if active_voice_counterpart not in verb_translation_dict:
                additional_verb_translation_dict[active_voice_counterpart] = '???'

    # merge two dicts (starting from Python 3.9)
    verb_translation_dict = verb_translation_dict | additional_verb_translation_dict
    return verb_translation_dict


# MAIN BUSINESS METHOD
def read_verbs(notes, ignored_fields):
    # Step 1
    verb_translation_dict = {}
    for i in range(0, len(notes)):
        note = notes[i]
        verb, translation = process_single_note(note, ignored_fields)
        verb_translation_dict[verb] = translation

    # Step 2
    final_verb_translation_dict = process_specially_ended_verbs(verb_translation_dict)

    # Step 3
    results = []
    for verb, translation in sorted(final_verb_translation_dict.items()):
        results.append(verb + '|' + translation)

    return results


#######################################

ankiConnectService = AnkiConnectService()

notes = ankiConnectService.get_notes_by_deck_name('Languages. Greek. Verbs (raw)')
ignored_fields = ['Audio']

res = read_verbs(notes, ignored_fields)
for r in res:
    print(r)

# test = """1) управлять&nbsp;(<i>автомашиной и т. п.</i>)<br>2) вести&nbsp;(<i>куда-л.</i>)<br>3) направлять, указывать; руководить, быть во главе<br>4) водить, вести&nbsp;(<i>кого-л.</i>)<br><br>* * *<br><br>Ενεστώτας<br><br>οδηγώ – οδηγούμε<br>οδη<u>γεί</u>ς – οδη<u>γεί</u>τε<br>οδη<u>γεί</u> – οδηγούν<br><br>Αόριστος<br><br>οδή<u>γη</u>σα – οδη<u>γή</u>σαμε<br>οδή<u>γη</u>σες – οδη<u>γή</u>σατε<br>οδή<u>γη</u>σε – οδή<u>γη</u>σαν<br><br>Συνοπτικός Μέλλοντας<br><br>θα οδη<u>γή</u>σω – θα οδη<u>γή</u>σουμε<br>θα οδη<u>γή</u>σεις – θα οδη<u>γή</u>σετε<br>θα οδη<u>γή</u>σει – θα οδη<u>γή</u>σουν<br><br><b>Perfective imperative mood</b><br>Οδή<u>γη</u>σε! – Οδη<u>γή</u>στε!<br><br>* * *<br><br>Ενεστώτας<br><br>οδηγώ – οδηγούμε<br>οδη<u>γεί</u>ς – οδη<u>γεί</u>τε<br>οδη<u>γεί</u>&nbsp;– οδηγούν<br><br>?????<br><br>Ενεστώτας<br><br>οδηγώ – οδηγούμε<br>οδη<u>γεί</u>ς – οδη<u>γεί</u>τε<br>οδη<u>γεί</u>&nbsp;– οδηγούν<br><br>Προστακτική<br>?????"""
# res = parse_back_field(test)
# print(res)


# if re.match(r'[а-я]+', 'брать'):
#     print('Success!')
