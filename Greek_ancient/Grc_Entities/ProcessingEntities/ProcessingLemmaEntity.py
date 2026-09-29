class ProcessingLemmaEntity:

    # ctor перегружен: может принимать 3 и 4 параметра:
    # 1) если передаём 3 параметра, то поле counter инициализируется значением 0
    # 2) если передаём 4 параметра, то поле counter инициализируется переданным в ctor значением
    def __init__(self, token, lemma, verdict, counter=0):
        self.counter: int = int(counter)
        self.token: str = token
        self.lemma: str = lemma
        self.verdict: str = verdict

    def is_lemma_ambivalent_and_offered_by_eBibleLexicon(self):
        # 4 | ἰησοῦ | ἰησοῦς | CLTK – ἰασός; eBibleLexicon – ἰησοῦς (здесь через запятую теоретически возможны ещё варианты)
        result = False
        if 'spaCy' in self.verdict and 'eBibleLexicon' in self.verdict:
            # парсим verdict, чтобы узнать, какой движок предлагал какие леммы
            verdict_parts = self.verdict.split(';')
            eBibleLexicon_part = verdict_parts[1]
            eBibleLexicon_comma_separated_lemmas_str = eBibleLexicon_part.split('–')[1].strip()
            eBibleLexicon_lemmas = [ebl.strip() for ebl in eBibleLexicon_comma_separated_lemmas_str.split(',')]

            # если на первом шаге при конфликте мнений CLTK и eBibleLexicon выбор пользователем был сделан всё же
            # в пользу eBibleLexicon (в пользу одной из лемм, предлагавшихся eBibleLexicon; в большинстве случаев
            # eBibleLexicon будет предлагать только одну лемму, но в теории их может быть несколько через запятую)
            if self.lemma in eBibleLexicon_lemmas:
                result = True
        return result

    def __str__(self):
        # "<3" означает выравнивание по левому краю, ширина вывода равна 3
        # В Четвероевангелии длина самого длинного токена составляет 18 символов, а самой длинной леммы - 17.
        # Выберем ширину вывода для токена/леммы = 15, это значение не удовлетворяет максимально возможной длине
        # токена/леммы, но с другой стороны делает вывод более компактным для большинства слов
        # return f'{self.counter:<3} | {self.token:<15} | {self.lemma:<15} | {self.verdict}'
        return f'{self.counter} | {self.token} | {self.lemma} | {self.verdict}'

    # бизнес-ключом данной сущности на первом этапе работы программы ('Find text lemmas') решил выбрать тройку значений "token-lemma-verdict"
    # 1) чисто token не решился сделать бизнес-ключом, потому что предполагаю, что один и тот же token может одновременно
    # быть словоформой совершенно разных слов и ошибочность работы CLTK-токенайзера это не раз показывала
    # 2) чисто lemma здесь тоже не решился сделать бизнес-ключом, потому что не факт, что лемма была выбрана правильно,
    # а в некоторых конфликтных ситуациях между CLTK и eBibleLexicon лемма вообще помечается как ??? и остаётся на
    # выбор пользователя вручную
    # На 2-м этапе работы программы работы программы всё внимание будет уделено полю lemma, возможно через отдельный словарь
    # {lemma: ProcessingLemmaEntity} так что на 2-м этапе, возможно, методы __eq__ & __hash__ не будут играть никакой роли,
    # т. к. они нужны только в том случае, если объект ProcessingLemmaEntity будет КЛЮЧОМ словаря, но не его значением.

    def __eq__(self, other):
        if isinstance(other, ProcessingLemmaEntity):
            return (self.token, self.lemma, self.verdict) == (other.token, other.lemma, other.verdict)
        return False

    def __hash__(self):
        return hash((self.token, self.lemma, self.verdict))
