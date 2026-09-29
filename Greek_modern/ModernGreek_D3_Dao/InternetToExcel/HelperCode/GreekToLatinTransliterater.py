def greek_to_latin(greek_text):
    greek_to_latin_dict = {
        'α': 'a', 'Α': 'A',
        'ά': 'a', 'Ά': 'A',

        'β': 'b', 'Β': 'B',
        'γ': 'g', 'Γ': 'G',
        'δ': 'd', 'Δ': 'D',

        'ε': 'e', 'Ε': 'E',
        'έ': 'e', 'Έ': 'E',

        'ζ': 'z', 'Ζ': 'Z',

        'η': 'i', 'Η': 'I',
        'ή': 'i', 'Ή': 'I',

        'θ': 'th', 'Θ': 'TH',

        'ι': 'i', 'Ι': 'I',
        'ί': 'i', 'Ί': 'I',

        'κ': 'k', 'Κ': 'K',
        'λ': 'l', 'Λ': 'L',
        'μ': 'm', 'Μ': 'M',
        'ν': 'n', 'Ν': 'N',
        'ξ': 'ks', 'Ξ': 'KS',

        'ο': 'o', 'Ο': 'O',
        'ό': 'o', 'Ό': 'O',

        'π': 'p', 'Π': 'P',
        'ρ': 'r', 'Ρ': 'R',
        'σ': 's', 'Σ': 'S',
        'τ': 't', 'Τ': 'T',

        'υ': 'u', 'Υ': 'U',
        'ύ': 'u', 'Ύ': 'U',

        # 'φ': 'ph', 'Φ': 'PH',
        'φ': 'f', 'Φ': 'F',
        # 'χ': 'ch', 'Χ': 'CH',
        'χ': 'x', 'Χ': 'X',
        'ψ': 'ps', 'Ψ': 'PS',

        'ω': 'o', 'Ω': 'O',
        'ώ': 'o', 'Ώ': 'O'
    }

    latin_text = ''
    for greek_char in greek_text:
        if greek_char in greek_to_latin_dict:
            latin_text += greek_to_latin_dict.get(greek_char)

    return latin_text
