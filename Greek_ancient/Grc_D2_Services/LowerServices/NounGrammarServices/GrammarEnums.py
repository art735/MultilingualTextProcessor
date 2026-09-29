from enum import Enum


# Флажки, сигнализирующие о том, какое кол-во информации конвертировать
class ConversionMode(Enum):
    GENDER_NUMBER_CASE = 1  # convert all three grammatical categories: gender, number, case
    NUMBER_CASE = 2  # convert two grammatical categories: number and case
    CASE_ONLY = 3  # convert only one grammatical category: case (падеж)


# Принятые мной сокращения для РОДА существительных
class GenderAbbr(Enum):
    masc = "masc."
    fem = "fem."
    neut = "neut."


# Строковые значения библиотеки spaCy для РОДА существительных, завёрнутые мной в enum
class GenderSpaCy(Enum):
    Masc = "Masc"
    Fem = "Fem"
    Neut = "Neut"
    Com = "Com"


# Принятые мной сокращения для ЧИСЛА существительных
class NumberAbbr(Enum):
    sg = "sg."
    du = "du."
    pl = "pl."


# Строковые значения библиотеки spaCy для ЧИСЛА существительных, завёрнутые мной в enum
class NumberSpaCy(Enum):
    Sing = "Sing"
    Dual = "Dual"
    Plur = "Plur"


# Принятые мной сокращения для ПАДЕЖА существительных
class CaseAbbr(Enum):
    nom = "nom."
    gen = "gen."
    dat = "dat."
    acc = "acc."
    voc = "voc."


# Строковые значения библиотеки spaCy для ПАДЕЖА существительных, завёрнутые мной в enum
class CaseSpaCy(Enum):
    Nom = "Nom"
    Gen = "Gen"
    Dat = "Dat"
    Acc = "Acc"
    Voc = "Voc"


# Функция для конвертации строки в enum
def str_to_enum(enum_class, enum_str):
    try:
        return enum_class[enum_str]
    except KeyError:
        raise ValueError(f"'{enum_str}' is not a valid name for {enum_class.__name__}")
