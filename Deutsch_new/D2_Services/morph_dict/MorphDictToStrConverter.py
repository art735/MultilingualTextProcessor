class MorphDictToStrConverter:

    # MORPH_DICT EXAMPLE:
    # {
    #    "Σκηνή": [
    #	     ("Σκηνή", "σκηνή", "NOUN", "Gender=Fem|Number=Sing|Case=Nom")
    #    ],
    #    "Ευτυχισμένοι Μαζί": [
    #        ("Ευτυχισμένοι", "ευτυχισμένος", "ADJ", "Gender=Masc|Number=Plur|Case=Nom"),
    #        ("Μαζί", "μαζί", "ADV", "_")
    #    ],
    #    "Επεισόδιο 1": [
    #        ("Επεισόδιο", "επεισόδιο", "NOUN", "Gender=Neut|Number=Sing|Case=Nom"),
    #        ("1", "1", "NUM", "_")
    #    ]
    # }
    def morph_dict_to_str(self, morph_dict):
        entries = []
        for sentence, tuples in morph_dict.items():
            entry_first_line = f'\t"{sentence}": ['
            tuples_str = ',\n'.join(self._tup_to_str(tup) for tup in tuples)
            entry_last_line = '\t]'
            entry_str = '\n'.join([entry_first_line, tuples_str, entry_last_line])
            entries.append(entry_str)

        entries_str = ',\n'.join(entries)
        morph_dict_str = "{\n" + entries_str + "\n}"
        return morph_dict_str

    # ("Σκηνή", "σκηνή", "NOUN", "Gender=Fem|Number=Sing|Case=Nom")
    def _tup_to_str(self, tup):
        comma_separated_quoted_elements = ', '.join(f'"{t}"' for t in tup)
        tup_str = f'\t\t({comma_separated_quoted_elements})'
        return tup_str


########################################

test_dict = {
    "1. Sie ist sehr freundlich und hilfsbereit.": [
        ("Sie", "sie", "PRON", "Case=Nom|Gender=Fem|Number=Sing|Person=3|PronType=Prs"),
        ("ist", "sein", "AUX", "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin"),
        ("sehr", "sehr", "ADV", ""),
        ("freundlich", "freundlich", "ADV", "Degree=Pos"),
        ("und", "und", "CCONJ", ""),
        ("hilfsbereit", "hilfsbereit", "ADV", "Degree=Pos")
    ],
    "2. Gestern haben sie einen neuen Hund adoptiert.": [
        ("Gestern", "gestern", "ADV", ""),
        ("haben", "haben", "AUX", "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin"),
        ("sie", "sie", "PRON", "Case=Nom|Number=Plur|Person=3|PronType=Prs"),
        ("einen", "ein", "DET", "Case=Acc|Definite=Ind|Gender=Masc|Number=Sing|PronType=Art"),
        ("neuen", "neu", "ADJ", "Case=Acc|Degree=Pos|Gender=Masc|Number=Sing"),
        ("Hund", "Hund", "NOUN", "Case=Acc|Gender=Masc|Number=Sing"),
        ("adoptiert", "adoptieren", "VERB", "VerbForm=Part")
    ]
}

if __name__ == '__main__':
    morphDictToStrConverter = MorphDictToStrConverter()
    res = morphDictToStrConverter.morph_dict_to_str(test_dict)
    # С помощью Text Diff Viewer сравнивать input и output: если всё работает правильно, разницы быть не должно.
    # Разница может быть только в том, что в исходном словаре для отступов используются пробелы вместо табуляции.
    print(res)
