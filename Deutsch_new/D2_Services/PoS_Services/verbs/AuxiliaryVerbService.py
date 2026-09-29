from VerbInfinitiveFinder import VerbInfinitiveFinder

# ChatGPT prompt: Можешь по образцу словаря для глагола müssen сгенерировать аналогичные словари
# для всех остальных немецких МОДАЛЬНЫХ глаголов

sein_dict = {
    "Infinitiv": "sein",
    "Präsens": {
        "1Sing": "bin",
        "2Sing": "bist",
        "3Sing": "ist",
        "1Plur": "sind",
        "2Plur": "seid",
        "3Plur": "sind"
    },
    "Präteritum": {
        "1Sing": "war",
        "2Sing": "warst",
        "3Sing": "war",
        "1Plur": "waren",
        "2Plur": "wart",
        "3Plur": "waren"
    },
    "Partizip II": "gewesen",
    "Konjunktiv I": {
        "1Sing": "sei",
        "2Sing": "seiest",
        "3Sing": "sei",
        "1Plur": " seien",
        "2Plur": "seiet",
        "3Plur": "seien"
    },
    "Konjunktiv II": {
        "1Sing": "wäre",
        "2Sing": "wärst",
        "3Sing": "wäre",
        "1Plur": " wären",
        "2Plur": "wärt",
        "3Plur": " wären"
    }
}

haben_dict = {
    "Infinitiv": "haben",
    "Präsens": {
        "1Sing": "habe",
        "2Sing": "hast",
        "3Sing": "hat",
        "1Plur": "haben",
        "2Plur": "habt",
        "3Plur": "haben"
    },
    "Präteritum": {
        "1Sing": "hatte",
        "2Sing": "hattest",
        "3Sing": "hatte",
        "1Plur": "hatten",
        "2Plur": "hattet",
        "3Plur": "hatten"
    },
    "Partizip II": "gehabt",
    "Konjunktiv I": {
        "1Sing": "habe",
        "2Sing": "habest",
        "3Sing": "habe",
        "1Plur": "haben",
        "2Plur": "habet",
        "3Plur": "haben"
    },
    "Konjunktiv II": {
        "1Sing": "hätte",
        "2Sing": "hättest",
        "3Sing": "hätte",
        "1Plur": "hätten",
        "2Plur": "hättet",
        "3Plur": "hätten"
    }
}

werden_dict = {
    "Infinitiv": "werden",
    "Präsens": {
        "1Sing": "werde",
        "2Sing": "wirst",
        "3Sing": "wird",
        "1Plur": "werden",
        "2Plur": "werdet",
        "3Plur": "werden"
    },
    "Präteritum": {
        "1Sing": "wurde",
        "2Sing": "wurdest",
        "3Sing": "wurde",
        "1Plur": "wurden",
        "2Plur": "wurdet",
        "3Plur": "wurden"
    },
    "Partizip II": "geworden",
    "Konjunktiv I": {
        "1Sing": "werde",
        "2Sing": "werdest",
        "3Sing": "werde",
        "1Plur": "werden",
        "2Plur": "werdet",
        "3Plur": "werden"
    },
    "Konjunktiv II": {
        "1Sing": "würde",
        "2Sing": "würdest",
        "3Sing": "würde",
        "1Plur": "würden",
        "2Plur": "würdet",
        "3Plur": "würden"
    }
}

# Вспомогательные глаголы (Hilfsverben) — помогают образовывать сложные формы других глаголов.
# В немецком языке к ним относятся sein, haben и werden.

# TODO не забывать добавлять новые глагольные словари в этот список!
auxiliary_verbs = [sein_dict, haben_dict, werden_dict]


class AuxiliaryVerbService(VerbInfinitiveFinder):
    def __init__(self):
        # Передаём в конструктор базового класса список словарей с формами глаголов
        super().__init__(auxiliary_verbs)

    def get_verb_infinitive(self, token, morph):
        result = super().get_verb_infinitive(token, morph)
        return result


###################################

if __name__ == '__main__':
    auxiliaryVerbService = AuxiliaryVerbService()

    # Пример использования функции с переданной морфологией
    morphology = {
        "Mood": ["Ind"],
        "Number": ["Sing"],
        "Person": ["1"],
        "Tense": ["Pres"],
        "VerbForm": ["Fin"]
    }

    # form = auxiliaryVerbService.get_verb_infinitive('bin', morphology)
    # print(form)

    # Пример поиска модального глагола с ошибочной морфологией от spaCy
    # Mood=Ind|Number=Plur|Person=1|Tense=Pres|VerbForm=Fin
    morphology = {
        "Mood": ["Ind"],
        "Number": ["Plur"],
        "Person": ["1"],
        "Tense": ["Pres"],
        "VerbForm": ["Fin"]
    }
    # form = auxiliaryVerbService.get_verb_infinitive('gewesen', morphology)
    # print(form)
