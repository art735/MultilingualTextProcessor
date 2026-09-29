voiced_consonants = ['b', 'd', 'g', 'z', 'ʒ', 'ʤ', 'v', 'ð', 'h', 'm', 'n', 'ŋ', 'r', 'l', 'w',
                     'j']  # 'j' - точно звонкий звук!
unvoiced_consonants = ['p', 't', 'k', 's', 'ʃ', 'ʧ', 'f', 'θ']

I_SOUND = 'ɪ'

# May be useful in regexp-s
# voiced_consonants_str = "".join(voiced_consonants_list)
# unvoiced_consonants_str = "".join(unvoiced_consonants_list)

# print(voiced_consonants_str)
# print(unvoiced_consonants_str)

IZ_ENDING_PRODUCING_CONSONANTS = ['z', 's', 'ʒ', 'ʃ', 'ʤ', 'ʧ']
IZ_ENDING = 'ɪz'
S_ENDING = 's'
Z_ENDING = 'z'

ID_ENDING_PRODUCING_CONSONANTS = ['d', 't']
ID_ENDING = 'ɪd'
T_ENDING = 't'
D_ENDING = 'd'

ING_ENDING = 'ɪŋ'

# окончания степеней сравнения прилагательных
ER_ENDING = 'ə'
EST_ENDING = 'ɪst'

SCHWA = 'ə'

# список гласных, которые встречаются в грамматических суффиксах/окончаниях, прибавляемых сущ., прил., глаг.
ENDINGS_VOWELS = ['ɪ', 'ə']

STRESS_SYMBOL = "'"

NEWLINE = '\n'
DOUBLE_NEWLINE = '\n\n'

# STRAIGHT_APOSTROPHE = "'"
# CURLY_APOSTROPHE = "’"
