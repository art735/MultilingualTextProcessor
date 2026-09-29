from VerbInfinitiveFinder import VerbInfinitiveFinder

# ChatGPT prompt: Можешь по образцу словаря для глагола müssen сгенерировать аналогичные словари
# для всех остальных немецких МОДАЛЬНЫХ глаголов

# Müssen
mussen_dict = {
    "Infinitiv": "müssen",
    "Präsens": {
        "1Sing": "muss",
        "2Sing": "musst",
        "3Sing": "muss",
        "1Plur": "müssen",
        "2Plur": "müsst",
        "3Plur": "müssen"
    },
    "Präteritum": {
        "1Sing": "musste",
        "2Sing": "musstest",
        "3Sing": "musste",
        "1Plur": "mussten",
        "2Plur": "musstet",
        "3Plur": "mussten"
    },
    "Partizip II": "gemusst",
    "Konjunktiv I": {
        "1Sing": "müsse",
        "2Sing": "müssest",
        "3Sing": "müsse",
        "1Plur": "müssen",
        "2Plur": "müsset",
        "3Plur": "müssen"
    },
    "Konjunktiv II": {
        "1Sing": "müsste",
        "2Sing": "müsstest",
        "3Sing": "müsste",
        "1Plur": "müssten",
        "2Plur": "müsstet",
        "3Plur": "müssten"
    }
}

# Können
konnen_dict = {
    "Infinitiv": "können",
    "Präsens": {
        "1Sing": "kann",
        "2Sing": "kannst",
        "3Sing": "kann",
        "1Plur": "können",
        "2Plur": "könnt",
        "3Plur": "können"
    },
    "Präteritum": {
        "1Sing": "konnte",
        "2Sing": "konntest",
        "3Sing": "konnte",
        "1Plur": "konnten",
        "2Plur": "konntet",
        "3Plur": "konnten"
    },
    "Partizip II": "gekonnt",
    "Konjunktiv I": {
        "1Sing": "könne",
        "2Sing": "könnest",
        "3Sing": "könne",
        "1Plur": "können",
        "2Plur": "könnet",
        "3Plur": "können"
    },
    "Konjunktiv II": {
        "1Sing": "könnte",
        "2Sing": "könntest",
        "3Sing": "könnte",
        "1Plur": "könnten",
        "2Plur": "könntet",
        "3Plur": "könnten"
    }
}

# Dürfen
durfen_dict = {
    "Infinitiv": "dürfen",
    "Präsens": {
        "1Sing": "darf",
        "2Sing": "darfst",
        "3Sing": "darf",
        "1Plur": "dürfen",
        "2Plur": "dürft",
        "3Plur": "dürfen"
    },
    "Präteritum": {
        "1Sing": "durfte",
        "2Sing": "durftest",
        "3Sing": "durfte",
        "1Plur": "durften",
        "2Plur": "durftet",
        "3Plur": "durften"
    },
    "Partizip II": "gedurft",
    "Konjunktiv I": {
        "1Sing": "dürfe",
        "2Sing": "dürfest",
        "3Sing": "dürfe",
        "1Plur": "dürfen",
        "2Plur": "dürfet",
        "3Plur": "dürfen"
    },
    "Konjunktiv II": {
        "1Sing": "dürfte",
        "2Sing": "dürftest",
        "3Sing": "dürfte",
        "1Plur": "dürften",
        "2Plur": "dürftet",
        "3Plur": "dürften"
    }
}

# Wollen
wollen_dict = {
    "Infinitiv": "wollen",
    "Präsens": {
        "1Sing": "will",
        "2Sing": "willst",
        "3Sing": "will",
        "1Plur": "wollen",
        "2Plur": "wollt",
        "3Plur": "wollen"
    },
    "Präteritum": {
        "1Sing": "wollte",
        "2Sing": "wolltest",
        "3Sing": "wollte",
        "1Plur": "wollten",
        "2Plur": "wolltet",
        "3Plur": "wollten"
    },
    "Partizip II": "gewollt",
    "Konjunktiv I": {
        "1Sing": "wolle",
        "2Sing": "wollest",
        "3Sing": "wolle",
        "1Plur": "wollen",
        "2Plur": "wollet",
        "3Plur": "wollen"
    },
    "Konjunktiv II": {
        "1Sing": "wollte",
        "2Sing": "wolltest",
        "3Sing": "wollte",
        "1Plur": "wollten",
        "2Plur": "wolltet",
        "3Plur": "wollten"
    }
}

# Sollen
sollen_dict = {
    "Infinitiv": "sollen",
    "Präsens": {
        "1Sing": "soll",
        "2Sing": "sollst",
        "3Sing": "soll",
        "1Plur": "sollen",
        "2Plur": "sollt",
        "3Plur": "sollen"
    },
    "Präteritum": {
        "1Sing": "sollte",
        "2Sing": "solltest",
        "3Sing": "sollte",
        "1Plur": "sollten",
        "2Plur": "solltet",
        "3Plur": "sollten"
    },
    "Partizip II": "gesollt",
    "Konjunktiv I": {
        "1Sing": "solle",
        "2Sing": "sollest",
        "3Sing": "solle",
        "1Plur": "sollen",
        "2Plur": "sollet",
        "3Plur": "sollen"
    },
    "Konjunktiv II": {
        "1Sing": "sollte",
        "2Sing": "solltest",
        "3Sing": "sollte",
        "1Plur": "sollten",
        "2Plur": "solltet",
        "3Plur": "sollten"
    }
}

# Mögen
mogen_dict = {
    "Infinitiv": "mögen",
    "Präsens": {
        "1Sing": "mag",
        "2Sing": "magst",
        "3Sing": "mag",
        "1Plur": "mögen",
        "2Plur": "mögt",
        "3Plur": "mögen"
    },
    "Präteritum": {
        "1Sing": "mochte",
        "2Sing": "mochtest",
        "3Sing": "mochte",
        "1Plur": "mochten",
        "2Plur": "mochtet",
        "3Plur": "mochten"
    },
    "Partizip II": "gemocht",
    "Konjunktiv I": {
        "1Sing": "möge",
        "2Sing": "mögest",
        "3Sing": "möge",
        "1Plur": "mögen",
        "2Plur": "möget",
        "3Plur": "mögen"
    },
    "Konjunktiv II": {
        "1Sing": "möchte",
        "2Sing": "möchtest",
        "3Sing": "möchte",
        "1Plur": "möchten",
        "2Plur": "möchtet",
        "3Plur": "möchten"
    }
}

# Модальные глаголы (Modalverben) — выражают отношение говорящего к действию (желание, необходимость, возможность).
# Примеры: können, müssen, dürfen, sollen, wollen, mögen.

# TODO не забывать добавлять новые глагольные словари в этот список!
modal_verbs = [mussen_dict, konnen_dict, durfen_dict, wollen_dict, sollen_dict, mogen_dict]


class ModalVerbService(VerbInfinitiveFinder):
    def __init__(self):
        # Передаём в конструктор базового класса список словарей с формами глаголов
        super().__init__(modal_verbs)

    def get_verb_infinitive(self, token, morph):
        result = super().get_verb_infinitive(token, morph)
        return result


###################################

if __name__ == '__main__':
    modalVerbService = ModalVerbService()

    # Пример использования функции с переданной морфологией
    morphology = {
        "Mood": ["Ind"],
        "Number": ["Sing"],
        "Person": ["1"],
        "Tense": ["Pres"],
        "VerbForm": ["Fin"]
    }

    # form = modalVerbService.get_verb_infinitive('muss', morphology)
    # print(form)

    # form = modalVerbService.get_verb_infinitive('kann', morphology)
    # print(form)

    # Пример поиска модального глагола с ошибочной морфологией от spaCy для формы musst (на самом деле 2-е л. ед. ч.)
    # Mood=Ind|Number=Plur|Person=1|Tense=Pres|VerbForm=Fin
    morphology = {
        "Mood": ["Ind"],
        "Number": ["Plur"],
        "Person": ["1"],
        "Tense": ["Pres"],
        "VerbForm": ["Fin"]
    }
    # form = modalVerbService.get_verb_infinitive('musst', morphology)
    # print(form)
