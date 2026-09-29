from BasePosService import BasePosService
from GrammarEnums import GenderSpaCy
from SpaCyPosResolver import SpaCyPosResolver

# Словарь личных местоимений немецкого языка
personal_pronouns_dict = {
    "Nom": {
        "1Sing": "ich",
        "2Sing": "du",
        "3Sing": "er/sie/es",
        "1Plur": "wir",
        "2Plur": "ihr",
        "3Plur": "sie"
    },
    "Gen": {
        "1Sing": "meiner",
        "2Sing": "deiner",
        "3Sing": "seiner/ihrer/seiner",
        "1Plur": "unser",
        "2Plur": "euer",
        "3Plur": "ihrer"
    },
    "Dat": {
        "1Sing": "mir",
        "2Sing": "dir",
        "3Sing": "ihm/ihr/ihm",
        "1Plur": "uns",
        "2Plur": "euch",
        "3Plur": "ihnen"
    },
    "Acc": {
        "1Sing": "mich",
        "2Sing": "dich",
        "3Sing": "ihn/sie/es",
        "1Plur": "uns",
        "2Plur": "euch",
        "3Plur": "sie"
    }
}

# Словарь притяжательных местоимений немецкого языка
possessive_pronouns_dict = {
    "mein": [
        "mein", "meine", "mein", "meine",  # Nominativ
        "meines", "meiner", "meines", "meiner",  # Genitiv
        "meinem", "meiner", "meinem", "meinen",  # Dativ
        "meinen", "meine", "mein", "meine"  # Akkusativ
    ],
    "dein": [
        "dein", "deine", "dein", "deine",  # Nominativ
        "deines", "deiner", "deines", "deiner",  # Genitiv
        "deinem", "deiner", "deinem", "deinen",  # Dativ
        "deinen", "deine", "dein", "deine"  # Akkusativ
    ],
    "sein": [
        "sein", "seine", "sein", "seine",  # Nominativ
        "seines", "seiner", "seines", "seiner",  # Genitiv
        "seinem", "seiner", "seinem", "seinen",  # Dativ
        "seinen", "seine", "sein", "seine"  # Akkusativ
    ],
    "ihr": [
        "ihr", "ihre", "ihr", "ihre",  # Nominativ
        "ihres", "ihrer", "ihres", "ihrer",  # Genitiv
        "ihrem", "ihrer", "ihrem", "ihren",  # Dativ
        "ihren", "ihre", "ihr", "ihre"  # Akkusativ
    ],
    "unser": [
        "unser", "unsere", "unser", "unsere",  # Nominativ
        "unseres", "unserer", "unseres", "unserer",  # Genitiv
        "unserem", "unserer", "unserem", "unseren",  # Dativ
        "unseren", "unsere", "unser", "unsere"  # Akkusativ
    ],
    "euer": [
        "euer", "eure", "euer", "eure",  # Nominativ
        "eures", "eurer", "eures", "eurer",  # Genitiv
        "eurem", "eurer", "eurem", "euren",  # Dativ
        "euren", "eure", "euer", "eure"  # Akkusativ
    ],
    "ihr": [
        "ihr", "ihre", "ihr", "ihre",  # Nominativ
        "ihres", "ihrer", "ihres", "ihrer",  # Genitiv
        "ihrem", "ihrer", "ihrem", "ihren",  # Dativ
        "ihren", "ihre", "ihr", "ihre"  # Akkusativ
    ],
    "Ihr": [
        "Ihr", "Ihre", "Ihr", "Ihre",  # Nominativ (формы вежливого обращения)
        "Ihres", "Ihrer", "Ihres", "Ihrer",  # Genitiv
        "Ihrem", "Ihrer", "Ihrem", "Ihren",  # Dativ
        "Ihren", "Ihre", "Ihr", "Ihre"  # Akkusativ
    ]
}

interrogative_pronouns_dict = {
    "wer": [
        "wessen", "wes",  # Genitiv
        "wem",  # Dativ
        "wen"  # Akkusativ
    ]
}


class GermanPronounLemmaService(BasePosService):
    def __init__(self):
        super().__init__()
        # self.morphologyParser = MorphologyParser()
        # self.err_msg = "spaCy has incorrectly defined morphology for '{}'"
        self.spaCyPosResolver = SpaCyPosResolver()

    def get_pronoun_lemma(self, token, lemma, morph):
        result = ''
        pronominal_type = self.morphologyParser.parse(morph, "PronType")
        if not pronominal_type:  # если флаг пустой
            return result

        # приводим местоимение к нижнему регистру
        # TODO это не совсем правильно, т. к. местоимения Sie (Вы) и Ihr (Ваш) должны оставаться с большой буквы!
        token = token.lower()

        match pronominal_type:
            case 'Prs':  # Личные, притяжательные и возвратные местоимения в spaCy имеют общую особенность: PronType=Prs
                if self.spaCyPosResolver.is_personal_pronoun(morph):
                    result = self._process_personal_pronoun(token, morph)
                elif self.spaCyPosResolver.is_possessive_pronoun(morph):
                    # Если лемму возможно найти среди ключей словаря possessive_pronouns_dict, значит лемма определена
                    # библиотекой spaCy верно! В противном случае определяем лемму вручную, перебирая все значения
                    # словаря possessive_pronouns_dict.
                    if lemma in possessive_pronouns_dict:
                        result = lemma
                    else:
                        result = self._find_pronoun_lemma(token, possessive_pronouns_dict)
                        if not result:
                            result = f"Can't find lemma for possessive pronoun '{token}'"
                elif self.spaCyPosResolver.is_reflexive_pronoun(morph):
                    result = lemma
            case 'Dem':  # demonstrative pronouns [dɪˈmɒnstrətɪv ˈprəʊnaʊnz] указательные местоимения
                result = lemma
            case 'Int':  # interrogative pronouns [ˌɪntəˈrɒɡətɪv ˈprəʊnaʊnz] вопросительные местоимения
                found_lemma = self._find_pronoun_lemma(token, interrogative_pronouns_dict)
                if found_lemma:
                    result = found_lemma
                else:
                    # result = f"Can't find lemma for interrogative pronoun '{token}'"
                    result = lemma
            case 'Rel':  # relative pronouns [ˈrɛlətɪv ˈprəʊnaʊnz] относительные местоимения
                result = lemma
            case 'Recip':  # reciprocal pronouns [rɪˈsɪprəkəl ˈprəʊnaʊnz] взаимные местоимения
                result = lemma
            case 'Ind':  # indefinite pronouns [ɪnˈdɛfɪnɪt ˈprəʊnaʊnz] неопределённые местоимения
                result = self._process_indefinite_pronoun(lemma)
            case 'Art':  # article ['ɑːtɪkl] лингв. артикль
                result = lemma
            case _:
                print(f"Yet unknown pronoun type for token: '{token}' -> lemma: '{lemma}'; {morph}")

        return result

    def _process_personal_pronoun(self, token, morph):
        result = ''

        # Парсим все необходимые грамматические категории местоимения
        case = self.morphologyParser.parse(morph, 'Case')
        number = self.morphologyParser.parse(morph, 'Number')
        person = self.morphologyParser.parse(morph, 'Person')
        gender = self.morphologyParser.parse(morph, 'Gender')

        # Определяем ключ для словаря
        person_number_key = f"{person}{number}"

        if case in personal_pronouns_dict and person_number_key in personal_pronouns_dict[case]:
            pronoun = personal_pronouns_dict[case][person_number_key]
            if '/' in pronoun:
                pronoun = pronoun.split('/')

            if self._is_token_valid(token, pronoun):
                # case - Nom
                # number - такое же, как у токена
                # person - такое же, как у токена
                result = personal_pronouns_dict['Nom'][person_number_key]

                if '/' in result:
                    masc, fem, neut = result.split('/')
                    match gender:
                        case GenderSpaCy.Masc.value:
                            result = masc
                        case GenderSpaCy.Fem.value:
                            result = fem
                        case GenderSpaCy.Neut.value:
                            result = neut
            else:
                print(self.err_msg.format(token) + '. Token is invalid as a personal pronoun.')
        else:
            print(self.err_msg.format(token) + '. Token is not found in personal pronouns hard-coded dict.')

        return result

    def _is_token_valid(self, token, pronoun):
        is_valid = False
        if isinstance(pronoun, str):
            is_valid = token == pronoun
        elif isinstance(pronoun, list):
            is_valid = token in pronoun
        return is_valid

    def _process_indefinite_pronoun(self, spaCy_lemma: str):
        result = ''

        etwas = 'etwas'  # что-то, что-нибудь
        was = 'was',  # "was" как разговорный вариант слова "etwas"
        nichts = 'nichts'  # ничего
        jemand = 'jemand'  # кто-то, кто-нибудь
        niemand = 'niemand'  # никто
        man = 'man'  # кто-то, люди (неопределённый субъект)
        irgendjemand = 'irgendjemand'  # кто-то, кто-нибудь (усиленное)
        irgendetwas = 'irgendetwas'  # что-то, что-нибудь (усиленное)
        jeder = 'jeder'  # каждый
        all = 'all'  # все
        einige = 'einige'  # несколько, некоторые
        manch = 'manch'  # многие, некоторые
        etlich = 'etlich'  # несколько, многие
        wenig = 'wenig'  # немного
        viel = 'viel'  # много
        mehr = 'mehr'  # больше
        kein = 'kein'  # никакой
        anderer = 'anderer'  # другой, иной
        beide = 'beide'  # оба, обе
        paar = 'paar'  # оба, обе

        # Пришлось исхитриться и сделать словарь, чтобы можно было искать по более сокращённой форме слова (ключ
        # словаря), а в качестве value выдавать полноценную начальную форму слова.
        # На момент написания текста это всё затевалось только ради одного местоимения anderer,
        # у которого начальная форма длиннее, чем некоторые падежные формы (например, andere) и работа строки
        # "andere".startswith("anderer") дало бы False и данное местоимение никогда бы участвовало в работе алгоритма.
        indefinite_pronouns_dict = {
            etwas: etwas,
            was: etwas,
            nichts: nichts,
            jemand: jemand,
            niemand: niemand,
            man: man,
            irgendjemand: irgendjemand,
            irgendetwas: irgendetwas,
            jeder: jeder,
            all: all,
            einige: einige,
            manch: manch,
            etlich: etlich,
            wenig: wenig,
            viel: viel,
            mehr: mehr,
            kein: kein,
            anderer[:-2]: anderer,  # ключ на два символа короче, чем value, чтобы было "andere".startswith("ander"), а
            # не "andere".startswith("anderer")
            beide: beide,
            paar: paar
        }

        for k, v in indefinite_pronouns_dict.items():
            if spaCy_lemma.startswith(k):
                result = v

        return result

    def _find_pronoun_lemma(self, token, pronouns_dict):
        for lemma, forms in pronouns_dict.items():
            if token in forms:
                return lemma
        return None  # Возвращается, если форма не найдена


############################################

morph_dict = {
    "Case": ["Dat"],
    "Number": ["Sing"],
    "Person": ["2"],
    "PronType": ["Prs"]
}
# res = pronounLemmaService.get_pronoun_lemma('dir', '', morph_dict)
# print(res)


spaCy_lemma = "weniger"
morph_dict = {
    "PronType": ["Ind"]
}
# res = pronounService.get_pronoun_lemma('', spaCy_lemma, morph_dict)
# print(res)

spaCy_lemma = "andere"
morph_dict = {
    "PronType": ["Ind"]
}
# res = pronounLemmaService.get_pronoun_lemma('', spaCy_lemma, morph_dict)
# print(res)

morph_dict = {
    "Case": ["Acc"],
    "Gender": ["Masc"],
    "Number": ["Sing"],
    "PronType": ["Int"]
}
# res = pronounLemmaService.get_pronoun_lemma('dir', '', morph_dict)
# print(res)


if __name__ == '__main__':
    germanPronounLemmaService = GermanPronounLemmaService()

    res = germanPronounLemmaService.get_pronoun_lemma('wem', 'wem', morph_dict)
    res = germanPronounLemmaService.get_pronoun_lemma('wen', 'wen', morph_dict)
    res = germanPronounLemmaService.get_pronoun_lemma('sie', 'sie',
                                                      {"Case": ["Acc"], "Number": ["Sing"], "Person": ["3"],
                                                       "PronType": ["Prs"]})
    print(res)
