my_dict = {
    'VERB': 1151,
    'NOUN': 1113,
    'ADJ': 341,
    'ADV': 159,
    'PROPN': 122,
    'ADP': 57,
    'NUM': 23,
    'PRON': 21,
    'SCONJ': 17,
    'X': 13,
    'INTJ': 9,
    'CCONJ': 7,
    'DET': 4,
    'AUX': 2
}

if 'NOUN' in my_dict and 'PROPN' in my_dict:
    noun_propn_merged_key = 'NOUN + PROPN'
    noun_propn_merged_value = my_dict['NOUN'] + my_dict['PROPN']

    del my_dict['NOUN']
    del my_dict['PROPN']

    my_dict[noun_propn_merged_key] = noun_propn_merged_value

    my_dict = dict(sorted(my_dict.items(), key=lambda item: item[1], reverse=True))

    print(my_dict)
