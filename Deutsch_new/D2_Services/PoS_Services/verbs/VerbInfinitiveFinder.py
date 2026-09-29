from BasePosService import BasePosService


class VerbInfinitiveFinder(BasePosService):
    def __init__(self, exceptional_verbs):
        super().__init__()
        self.exceptional_verbs = exceptional_verbs

    def get_verb_infinitive(self, token, morph):
        result = ''

        # Приводим входной токен (форму слова "как есть") к нижнему регистру
        token_lower = token.lower()

        # Парсим морфологию, напр. Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin
        mood = self.morphologyParser.parse(morph, "Mood")
        number = self.morphologyParser.parse(morph, "Number")
        person = self.morphologyParser.parse(morph, "Person")
        tense = self.morphologyParser.parse(morph, "Tense")

        # Определяем ключ для словаря
        person_number_key = f"{person}{number}"

        # ищем
        for verb_dict in self.exceptional_verbs:
            if mood == "Ind" and tense == "Pres":
                verb_form = verb_dict["Präsens"].get(person_number_key)
            elif mood == "Ind" and tense == "Past":
                verb_form = verb_dict["Präteritum"].get(person_number_key)
            elif mood == "Subj" and tense == "Pres":
                verb_form = verb_dict["Konjunktiv I"].get(person_number_key)
            elif mood == "Subj" and tense == "Past":
                verb_form = verb_dict["Konjunktiv II"].get(person_number_key)
            elif morph.get("VerbForm") == "Part":
                verb_form = verb_dict["Partizip II"]
            else:
                verb_form = verb_dict["Infinitiv"]

            if verb_form == token_lower:
                result = verb_dict["Infinitiv"]
                break
            # else:
            #     result = self.err_msg.format(token)

        # Иногда spaCy неправильно определяет морфологию токена, особенно для формы musst глагола müssen.
        # Поэтому если нормальный алгоритм, приведённый выше и рассчитанный на правильную морфологию от spaCy,
        # ничего не нашёл, нужно ещё попробовать поискать в словарях лемму просто прямым перебором всех значений.
        if len(result) == 0:
            for verb_dict in self.exceptional_verbs:
                is_dict_found = self._is_token_in_dict(verb_dict, token)
                if is_dict_found:
                    result = verb_dict["Infinitiv"]
                    # break # прерывает работу только внутреннего цикла, но не внешнего
                    return result

        return result

    def _is_token_in_dict(self, search_dict, search_value):
        """
        Рекурсивно ищет строковое значение в словаре любой вложенности.
        :param search_dict: Словарь, в котором производится поиск.
        :param search_value: Строка, которую нужно найти.
        """
        if not isinstance(search_dict, dict):
            return None

        # Проверяем каждый ключ и значение в словаре
        for key, value in search_dict.items():
            if isinstance(value, dict):
                # Рекурсивный вызов, если значение - это словарь
                result = self._is_token_in_dict(value, search_value)
                if result:
                    return result
            elif isinstance(value, list):
                if search_value in value:
                    return True
            elif isinstance(value, str):
                if value == search_value:
                    return True

        return None


######################################

if __name__ == '__main__':
    verbInfinitiveFinder = None
