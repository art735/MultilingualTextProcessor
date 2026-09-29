import re


def remove_in_word_second_stress(word):
    already_has_stressed_vowel = False
    word_characters_list = list()
    for character in word:
        if character in stressed_vowels:
            if not already_has_stressed_vowel:  # 1-я проходка
                word_characters_list.append(character)
                already_has_stressed_vowel = True
            else:  # 2-я проходка
                if character == 'ά':
                    word_characters_list.append('α')
                elif character == 'έ':
                    word_characters_list.append('ε')
                elif character == 'ί':
                    word_characters_list.append('ι')
                elif character == 'ύ':
                    word_characters_list.append('υ')
                elif character == 'ή':
                    word_characters_list.append('η')
                elif character == 'ό':
                    word_characters_list.append('ο')
                elif character == 'ώ':
                    word_characters_list.append('ω')
        else:
            word_characters_list.append(character)

    output_word = ''.join(word_characters_list)
    return output_word


def preprocess(sentence):
    # remove digits (verse numbering) at the beginning of each verse
    sentence = re.sub('^[0-9]*', '', sentence).strip()

    sentence = sentence.replace('·', ' ')

    sentence = sentence.replace('ἄ', 'ἄ')
    sentence = sentence.replace('ά', 'ά')
    sentence = sentence.replace('έ', 'έ')
    # sentence = sentence.replace('έ', '')
    sentence = sentence.replace('ή', 'ή')
    sentence = sentence.replace('ί', 'ί')
    sentence = sentence.replace('ΐ', 'ΐ')
    sentence = sentence.replace('ό', 'ό')
    sentence = sentence.replace('ύ', 'ύ')
    sentence = sentence.replace('ώ', 'ώ')

    return sentence


stressed_vowels = [
    'ά', 'ὰ', 'ᾶ', 'ἄ', 'ἂ', 'ἆ', 'ἅ', 'ἃ', 'ἇ',
    'ᾴ', 'ά', 'ᾲ', 'ᾷ', 'ᾄ', 'ᾂ', 'ᾆ', 'ᾅ', 'ᾃ', 'ᾇ',

    'έ', 'ὲ', 'ἔ', 'ἒ', 'ἕ', 'ἓ',

    'ή', 'ὴ', 'ῆ', 'ἤ', 'ἢ', 'ἦ', 'ἥ', 'ἣ', 'ἧ',
    'ῄ', 'ῂ', 'ῇ', 'ᾔ', 'ᾒ', 'ᾖ', 'ᾕ', 'ᾓ', 'ᾗ',

    'ί', 'ὶ', 'ῖ', 'ἴ', 'ἲ', 'ἶ', 'ἵ', 'ἳ', 'ἷ', 'ΐ', 'ῒ', 'ῗ',

    'ό', 'ὸ', 'ὄ', 'ὂ', 'ὅ', 'ὃ',

    'ύ', 'ὺ', 'ῦ', 'ὔ', 'ὒ', 'ὖ', 'ὕ', 'ὓ', 'ὗ', 'ΰ', 'ῢ', 'ῧ',

    'ώ', 'ὼ', 'ῶ', 'ὤ', 'ὢ', 'ὦ', 'ὥ', 'ὣ', 'ὧ',
    'ῴ', 'ῲ', 'ῷ', 'ᾤ', 'ᾢ', 'ᾦ', 'ᾥ', 'ᾣ', 'ᾧ'
]
