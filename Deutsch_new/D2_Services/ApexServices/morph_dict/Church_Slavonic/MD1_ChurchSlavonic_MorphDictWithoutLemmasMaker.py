import unicodedata

import AppContext
from View_enums import CurrentLanguageComboBoxEnum

llm_prompt = """
\n\nТы – эксперт по морфологии и лемматизации церковнославянского языка Елизаветинской эпохи (Российская империя, 18-19 вв.).

Твоя задача: для каждого токена определить правильную лемму и pos-тег (в формате UPOS).

Формат входного текста:

Предложение1:
новый токен11
новый токен12
новый токен13
...
новый токен1n

<пустая строка как разделитель предложений>

Предложение2:
новый токен21
новый токен22
новый токен23
...
новый токен2n

Ты должен сформировать ответ в строго следующем формате:

Предложение1:
новый токен11|лемма11|pos11
новый токен12|лемма12|pos12
новый токен13|лемма13|pos13
...
новый токен1n|лемма1n|pos1n

<пустая строка как разделитель предложений>

Предложение2:
новый токен21|лемма21|pos21
новый токен22|лемма22|pos22
новый токен23|лемма23|pos23
...
новый токен2n|лемма2n|pos2n

Вывод должен быть оформлен так, чтобы кластер «предложение и список его токен|лемма|pos-строк» отделялся бы
пустой строкой от аналогичных кластеров на базе других предложений с их токен|лемма|pos-строками.
Если вслед за предложением нет списка токен|лемма|pos-строк, то выводить его всё равно нужно, точно также отделяя
его пустой строкой от предыдущего и последующего кластеров.

Теперь обработай следующие входные данные:

"""


class MD1_ChurchSlavonic_MorphDictWithoutLemmasMaker:

    def __init__(self, morphDictService):
        self.morphDictService = morphDictService

    def process(self, text_sentences):
        """
        Формирует входные данные для LLM.

        Правила обработки:

        1. Существующий morph_dict используется только для определения уже
           встречавшихся token.
        2. POS, lemma и morph полностью игнорируются при дедупликации.
        3. Если token уже встречался в morph_dict-файлах, он пропускается.
        4. Если token уже встречался в рамках текущего вызова process(),
           он пропускается.
        5. Пунктуация не является token и не попадает в результат.
        6. Каждое предложение добавляется в результат всегда, даже если
           после фильтрации в нём не осталось ни одного token.
        """

        # Все ранее сохранённые morph_dict.
        all_morph_dict_files_merged_dict = (
            self.morphDictService.read_and_merge_morph_dicts_from_all_files()
        )

        # ------------------------------------------------------------------
        # Token, которые уже встречались в существующих morph_dict-файлах.
        #
        # В старом варианте ключ строился как (token, POS).
        # Теперь POS полностью исключён: ключом является только token.
        # ------------------------------------------------------------------
        seen_tokens_from_all_morph_dicts = {
            self._token_key(sentence_tuple[0])
            for sentence_tuples in all_morph_dict_files_merged_dict.values()
            for sentence_tuple in sentence_tuples
            if sentence_tuple
        }

        # Token, которые уже встретились внутри текущего process().
        seen_tokens_from_current_session = set()

        result_dict = {}

        # Каждая непустая строка входа считается отдельным предложением.
        # Это соответствует текущему контракту process(text_sentences).
        for sentence in (s.strip() for s in text_sentences.splitlines() if s.strip()):

            # Уровень 1: встречалось ли ранее данное предложение?
            #
            # Если предложение уже есть либо в morph_dict-файлах,
            # либо уже было добавлено в текущий result_dict,
            # полностью пропускаем его.
            if sentence in result_dict or sentence in all_morph_dict_files_merged_dict:
                continue

            # --------------------------------------------------------------
            # Ручная токенизация.
            # Stanza / spaCy больше не нужны.
            # --------------------------------------------------------------
            tokens = self._tokenize_sentence(sentence)

            for token in tokens:

                # Нормализованный ключ нужен только для поиска совпадений.
                # Сам token в результат передаётся в исходном написании.
                token_key = self._token_key(token)

                # ----------------------------------------------------------
                # Token уже встречался:
                #
                #   1) либо в существующих morph_dict;
                #   2) либо ранее в текущем process().
                #
                # В обоих случаях token больше не нужен.
                # ----------------------------------------------------------
                if (
                    token_key in seen_tokens_from_all_morph_dicts
                    or token_key in seen_tokens_from_current_session
                ):
                    continue

                # Новый token берём в работу.
                # setdefault() создаст для sentence пустой список, если ключа ещё нет, и сразу добавит в него token.
                result_dict.setdefault(sentence, []).append(token)

                # Фиксируем его как уже использованный в текущей сессии.
                seen_tokens_from_current_session.add(token_key)

        return self._build_llm_input(result_dict)

    @staticmethod
    def _token_key(token):
        """
        Возвращает нормализованный ключ token для дедупликации.

        Используется только для сравнения.
        В LLM при этом передаётся исходное написание token.

        casefold() обеспечивает регистронезависимое Unicode-сравнение.
        """

        return token.casefold()

    @staticmethod
    def _tokenize_sentence(sentence):
        """
        Ручная токенизация предложения.

        Token представляет собой последовательность букв/цифр Unicode
        с возможными комбинируемыми знаками.

        Пунктуация и пробелы разделяют token и не попадают в результат.

        Внутренний апостроф ' / ’ сохраняется внутри token, если после него
        продолжается последовательность букв/цифр.

        Например:

            "Сло́во, и Сло́во."

        превращается в:

            ["Сло́во", "и", "Сло́во"]

        Дефис рассматривается как разделитель.
        """

        # Приводим предложение к нижнему регистру.
        sentence = sentence.lower()

        tokens = []
        current_token = []

        def is_token_char(char):
            category = unicodedata.category(char)

            return (
                char.isalpha()
                or char.isdigit()
                or category in {"Mn", "Mc", "Me"}
            )

        def flush_current_token():
            if current_token:
                tokens.append("".join(current_token))
                current_token.clear()

        length = len(sentence)

        for index, char in enumerate(sentence):

            # Обычная буква, цифра или комбинируемый диакритический знак.
            if is_token_char(char):
                current_token.append(char)
                continue

            # Апостроф внутри слова:
            #
            # "..." + "'" + "..."
            #
            # сохраняем как часть token, только если после него
            # действительно продолжается token.
            if (
                char in {"'", "’"}
                and current_token
                and index + 1 < length
                and is_token_char(sentence[index + 1])
            ):
                current_token.append(char)
                continue

            # Пробел, запятая, точка, двоеточие, точка с запятой,
            # скобки, кавычки, тире, дефис и т. п.
            flush_current_token()

        flush_current_token()

        return tokens

    @staticmethod
    def _build_llm_input(result_dict):
        """
        Формирует текст, который будет добавлен после llm_prompt.

        Каждый кластер имеет вид:

            предложение:
            token1
            token2
            token3

        Между кластерами всегда одна пустая строка.

        Если у предложения нет новых token, остаётся только:

            предложение:
        """

        clusters = []

        for sentence, tokens in result_dict.items():

            cluster_lines = [f"{sentence}:"]

            # Если tokens == [], это специально оставляет только строку
            # с предложением, что соответствует требованиям llm_prompt.
            cluster_lines.extend(tokens)

            clusters.append("\n".join(cluster_lines))

        result_dict_str = "\n\n".join(clusters)

        return f"{llm_prompt}\n{result_dict_str}".strip()


############################################################################


text = """
Въ нача́ле бѣ́ Сло́во.
И Сло́во бѣ́ къ Бо́гу.
"""

text = """
Псалом 1

1 Блаже́н муж, и́же не и́де на сове́т нечести́вых и на пути́ гре́шных не ста, и на седа́лищи губи́телей не се́де,
2 но в зако́не Госпо́дни во́ля eго́, и в зако́не Его́ поучи́тся день и нощь.
3 И бу́дет я́ко дре́во насажде́нное при исхо́дищих вод, е́же плод свой даст во вре́мя свое́, и лист eго́ не отпаде́т, и вся, ели́ка а́ще твори́т, успе́ет.
4 Не та́ко нечести́вии, не та́ко, но я́ко прах, eго́же возмета́ет ветр от лица́ земли́.
5 Сего́ ра́ди не воскре́снут нечести́вии на суд, ниже́ гре́шницы в сове́т пра́ведных.
6 Я́ко весть Госпо́дь путь пра́ведных, и путь нечести́вых поги́бнет.
"""


if __name__ == "__main__":
    from BusinessObjectFactory import BusinessObjectFactory
    language = CurrentLanguageComboBoxEnum.CHURCH_SLAVONIC.value
    AppContext.switch_language(language)

    md1_MorphDictWithoutLemmasMaker = BusinessObjectFactory.create_md1_ChurchSlavonic_MorphDictWithoutLemmasMaker()
    res = md1_MorphDictWithoutLemmasMaker.process(text)

    print(res)
