from GrammarEnums import GenderSpaCy, NumberSpaCy, CaseSpaCy, GenderAbbr, NumberAbbr, CaseAbbr, ConversionMode, \
    str_to_enum
from MorphologyParser import MorphologyParser


# Статическая функция для генерации строки с сокращениями
def format_grammar_string(gender, number, case):
    return f'{gender.value} {number.value} {case.value}'


# трёхмерный ассоциативный массив
grammar_dict = {
    GenderSpaCy.Masc.value: {
        NumberSpaCy.Sing.value: {
            CaseSpaCy.Nom.value: format_grammar_string(GenderAbbr.masc, NumberAbbr.sg, CaseAbbr.nom),
            CaseSpaCy.Gen.value: format_grammar_string(GenderAbbr.masc, NumberAbbr.sg, CaseAbbr.gen),
            CaseSpaCy.Dat.value: format_grammar_string(GenderAbbr.masc, NumberAbbr.sg, CaseAbbr.dat),
            CaseSpaCy.Acc.value: format_grammar_string(GenderAbbr.masc, NumberAbbr.sg, CaseAbbr.acc),
            CaseSpaCy.Voc.value: format_grammar_string(GenderAbbr.masc, NumberAbbr.sg, CaseAbbr.voc),
        },
        NumberSpaCy.Dual.value: {
            CaseSpaCy.Nom.value: format_grammar_string(GenderAbbr.masc, NumberAbbr.du, CaseAbbr.nom),
            CaseSpaCy.Gen.value: format_grammar_string(GenderAbbr.masc, NumberAbbr.du, CaseAbbr.gen),
            CaseSpaCy.Dat.value: format_grammar_string(GenderAbbr.masc, NumberAbbr.du, CaseAbbr.dat),
            CaseSpaCy.Acc.value: format_grammar_string(GenderAbbr.masc, NumberAbbr.du, CaseAbbr.acc),
            CaseSpaCy.Voc.value: format_grammar_string(GenderAbbr.masc, NumberAbbr.du, CaseAbbr.voc),
        },
        NumberSpaCy.Plur.value: {
            CaseSpaCy.Nom.value: format_grammar_string(GenderAbbr.masc, NumberAbbr.pl, CaseAbbr.nom),
            CaseSpaCy.Gen.value: format_grammar_string(GenderAbbr.masc, NumberAbbr.pl, CaseAbbr.gen),
            CaseSpaCy.Dat.value: format_grammar_string(GenderAbbr.masc, NumberAbbr.pl, CaseAbbr.dat),
            CaseSpaCy.Acc.value: format_grammar_string(GenderAbbr.masc, NumberAbbr.pl, CaseAbbr.acc),
            CaseSpaCy.Voc.value: format_grammar_string(GenderAbbr.masc, NumberAbbr.pl, CaseAbbr.voc),
        }
    },
    GenderSpaCy.Fem.value: {
        NumberSpaCy.Sing.value: {
            CaseSpaCy.Nom.value: format_grammar_string(GenderAbbr.fem, NumberAbbr.sg, CaseAbbr.nom),
            CaseSpaCy.Gen.value: format_grammar_string(GenderAbbr.fem, NumberAbbr.sg, CaseAbbr.gen),
            CaseSpaCy.Dat.value: format_grammar_string(GenderAbbr.fem, NumberAbbr.sg, CaseAbbr.dat),
            CaseSpaCy.Acc.value: format_grammar_string(GenderAbbr.fem, NumberAbbr.sg, CaseAbbr.acc),
            CaseSpaCy.Voc.value: format_grammar_string(GenderAbbr.fem, NumberAbbr.sg, CaseAbbr.voc),
        },
        NumberSpaCy.Dual.value: {
            CaseSpaCy.Nom.value: format_grammar_string(GenderAbbr.fem, NumberAbbr.du, CaseAbbr.nom),
            CaseSpaCy.Gen.value: format_grammar_string(GenderAbbr.fem, NumberAbbr.du, CaseAbbr.gen),
            CaseSpaCy.Dat.value: format_grammar_string(GenderAbbr.fem, NumberAbbr.du, CaseAbbr.dat),
            CaseSpaCy.Acc.value: format_grammar_string(GenderAbbr.fem, NumberAbbr.du, CaseAbbr.acc),
            CaseSpaCy.Voc.value: format_grammar_string(GenderAbbr.fem, NumberAbbr.du, CaseAbbr.voc),
        },
        NumberSpaCy.Plur.value: {
            CaseSpaCy.Nom.value: format_grammar_string(GenderAbbr.fem, NumberAbbr.pl, CaseAbbr.nom),
            CaseSpaCy.Gen.value: format_grammar_string(GenderAbbr.fem, NumberAbbr.pl, CaseAbbr.gen),
            CaseSpaCy.Dat.value: format_grammar_string(GenderAbbr.fem, NumberAbbr.pl, CaseAbbr.dat),
            CaseSpaCy.Acc.value: format_grammar_string(GenderAbbr.fem, NumberAbbr.pl, CaseAbbr.acc),
            CaseSpaCy.Voc.value: format_grammar_string(GenderAbbr.fem, NumberAbbr.pl, CaseAbbr.voc),
        }
    },
    GenderSpaCy.Neut.value: {
        NumberSpaCy.Sing.value: {
            CaseSpaCy.Nom.value: format_grammar_string(GenderAbbr.neut, NumberAbbr.sg, CaseAbbr.nom),
            CaseSpaCy.Gen.value: format_grammar_string(GenderAbbr.neut, NumberAbbr.sg, CaseAbbr.gen),
            CaseSpaCy.Dat.value: format_grammar_string(GenderAbbr.neut, NumberAbbr.sg, CaseAbbr.dat),
            CaseSpaCy.Acc.value: format_grammar_string(GenderAbbr.neut, NumberAbbr.sg, CaseAbbr.acc),
            CaseSpaCy.Voc.value: format_grammar_string(GenderAbbr.neut, NumberAbbr.sg, CaseAbbr.voc),
        },
        NumberSpaCy.Dual.value: {
            CaseSpaCy.Nom.value: format_grammar_string(GenderAbbr.neut, NumberAbbr.du, CaseAbbr.nom),
            CaseSpaCy.Gen.value: format_grammar_string(GenderAbbr.neut, NumberAbbr.du, CaseAbbr.gen),
            CaseSpaCy.Dat.value: format_grammar_string(GenderAbbr.neut, NumberAbbr.du, CaseAbbr.dat),
            CaseSpaCy.Acc.value: format_grammar_string(GenderAbbr.neut, NumberAbbr.du, CaseAbbr.acc),
            CaseSpaCy.Voc.value: format_grammar_string(GenderAbbr.neut, NumberAbbr.du, CaseAbbr.voc),
        },
        NumberSpaCy.Plur.value: {
            CaseSpaCy.Nom.value: format_grammar_string(GenderAbbr.neut, NumberAbbr.pl, CaseAbbr.nom),
            CaseSpaCy.Gen.value: format_grammar_string(GenderAbbr.neut, NumberAbbr.pl, CaseAbbr.gen),
            CaseSpaCy.Dat.value: format_grammar_string(GenderAbbr.neut, NumberAbbr.pl, CaseAbbr.dat),
            CaseSpaCy.Acc.value: format_grammar_string(GenderAbbr.neut, NumberAbbr.pl, CaseAbbr.acc),
            CaseSpaCy.Voc.value: format_grammar_string(GenderAbbr.neut, NumberAbbr.pl, CaseAbbr.voc),
        }
    }
}


# Конвертирует род/число/падеж существительного из CLTK-представления в общепринятые сокращения
class NounGrammarConverter:
    def __init__(self):
        self.morphologyParser = MorphologyParser()

    def convert(self, morph, conversion_mode: ConversionMode):
        result = ''

        # 1) род (мужской, женский, средний)
        gender = self.morphologyParser.parse(morph, "Gender")
        # 2) число (единственное, двойственное, множественное)
        number = self.morphologyParser.parse(morph, "Number")
        # 3) падеж (именительный, родительный, дательный, винительный, звательный)
        case = self.morphologyParser.parse(morph, "Case")

        # if type(gender) is str and type(number) is str and type(case) is str:
        #     gender, number, case = self.convert_gender_number_case_to_enum(gender, number, case)
        if gender in grammar_dict and number in grammar_dict[gender] and case in grammar_dict[gender][number]:
            match conversion_mode:
                case conversion_mode.GENDER_NUMBER_CASE:
                    result = grammar_dict[gender][number][case]
                case conversion_mode.NUMBER_CASE:
                    full_str = grammar_dict[gender][number][case]
                    pieces = full_str.split()
                    if len(pieces) == 3:  # три элемента: род, число, падеж
                        number = pieces[1]
                        case = pieces[2]
                        result = f'{number} {case}'
                case conversion_mode.CASE_ONLY:
                    full_str = grammar_dict[gender][number][case]
                    pieces = full_str.split()
                    if len(pieces) == 3:  # три элемента: род, число, падеж
                        result = pieces[-1]
                case _:  # дифолтная ветка не является обязательной
                    result = ''

        return result

    def convert_gender_number_case_to_enum(self, gender_str, number_str, case_str):
        gender = str_to_enum(GenderSpaCy, gender_str)
        number = str_to_enum(NumberSpaCy, number_str)
        case = str_to_enum(CaseSpaCy, case_str)
        return gender, number, case


###############################################################################

nounGrammarConverter = NounGrammarConverter()

# morph = {'Gender': ['Masc'], 'Number': ['Sing'], 'Case': ['Nom']}
# print(nounGrammarConverter.convert(morph, ConversionMode.GENDER_NUMBER_CASE))

# morph = {'Gender': ['Fem'], 'Number': ['Dual'], 'Case': ['Gen']}
# print(nounGrammarConverter.convert(morph, ConversionMode.NUMBER_CASE))

# morph = {'Gender': ['Neut'], 'Number': ['Plur'], 'Case': ['Voc']}
# print(nounGrammarConverter.convert(morph, ConversionMode.CASE_ONLY))
