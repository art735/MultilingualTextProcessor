import re

from CharConstants import ACCENT_MARKS_REGEX_CLASS, SPACE, COMBINING_LOW_LINE

# межзубные согласные
interdental_consonants = fr'([θð])'  # умышленно обёрнуты в захватывающую группу

# альвеолярные согласные с возможным уже добавленным ранее подчёркиванием
alveolar_consonants = fr'([tdszln]{COMBINING_LOW_LINE}?)'  # умышленно обёрнуты в захватывающую группу

# словарь зубных согласных
dental_consonants_dict = {
    # зубные аналоги межзубных согласных
    "θ": "t̪", "ð": "d̪",
    # зубные аналоги альвеолярных согласных
    "t": "t̪", "d": "d̪", "s": "s̪", "z": "z̪", "l": "l̪", "n": "n̪"
}

# Искать межзубные и альвеолярные согласные на стыках слов в любом порядке их следования:
# межзубный-пробел-альвеолярный ИЛИ альвеолярный-пробел-межзубный.
# Также учитывать возможное присутствие знака ударения перед вторым словом (в отдельной захватывающей группе), причём
# квантификатор '?' стоит внутри группы (а не снаружи), т. е. сама группа является обязательной, а её содержимое - нет.
# Такое положение квантификатора важно для логики замены, где всегда будет происходить обращение к этой группе.
pattern = fr'{{}}\s({ACCENT_MARKS_REGEX_CLASS}?){{}}'
option1_regex = pattern.format(interdental_consonants, alveolar_consonants)
option2_regex = pattern.format(alveolar_consonants, interdental_consonants)


class TranscriptionAssimilationService:
    def __init__(self):
        pass

    def assimilate(self, bracketed_transcription):
        # Объединить оба регулярных выражения через ИЛИ, избавиться от цикла и производить одну замену (вместо двух)
        # мешает тот факт, что в регулярном выражении, объединённом через ИЛИ, возникает целых 4 группы, а при замене
        # нужно обращаться только к двум из них. Поэтому либо надо сильно усложнить логику 2-го параметра
        # lambda-функции, либо просто разбить регулярное выражение на две части и применять их за два прохода в цикле.
        for regex in [option1_regex, option2_regex]:
            bracketed_transcription = re.sub(regex, self._replace_match, bracketed_transcription)

        return bracketed_transcription

    def _replace_match(self, match):
        """
        Метод для обработки найденного соответствия в функции re.sub(...).
        :param match: объект re.Match
        :return: строка с заменёнными согласными
        """
        # Замена для первого согласного. Обращение к 0-му индексу захваченной строки означает, что обращаемся всегда
        # к захваченной букве и игнорируем возможно следующий за ней знак подчёркивания.
        first_consonant = dental_consonants_dict[match.group(1)[0]]
        stress_mark = match.group(2) if match.group(2) else ''  # сохраняем знак ударения (если есть)
        second_consonant = dental_consonants_dict[match.group(3)[0]]  # замена для второго согласного

        replacement = f'{first_consonant}{SPACE}{stress_mark}{second_consonant}'
        return replacement


################## Local testing environment ##########################
# На логику данного файла написаны юнит-тесты!!! #####

test_str = '[ɔn ðæt]'
test_str = '[wɪð ˈtɛnənt]'  # имеется знак ударения на стыке слов
test_str = '[ɡriːn ˈtʌm]'  # имеется знак ударения на стыке слов

if __name__ == '__main__':
    transcriptionAssimilationService = TranscriptionAssimilationService()
    print(transcriptionAssimilationService.assimilate(test_str))

    input1 = [
        "[ɔn ðæt]", "[wɪð næt]", "[ɔn ðæt wɪð næt]"
    ]

    er1 = [
        "[ɔn̪ d̪æt]", "[wɪd̪ n̪æt]", "[ɔn̪ d̪æt wɪd̪ n̪æt]"
    ]

    if all(transcriptionAssimilationService.assimilate(input_val) == er for input_val, er in zip(input1, er1)):
        print('test1 ok')
    else:
        print('test1 failed')
