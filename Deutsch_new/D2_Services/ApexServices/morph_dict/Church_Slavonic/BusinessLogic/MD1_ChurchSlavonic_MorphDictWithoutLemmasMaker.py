import AppContext

from ChurchSlavonicTextNormalizer import ChurchSlavonicTextNormalizer
from ChurchSlavonicTokenizer import ChurchSlavonicTokenizer
from View_enums import CurrentLanguageComboBoxEnum

llm_prompt = """
\n\nТы – эксперт по морфологии и лемматизации церковнославянского языка Елизаветинской эпохи (Российская империя, XVIII век).

Твоя задача: для каждого токена определить правильную лемму и pos-тег (в формате UPOS).

Правила лемматизации:
- причастия нужно приводить к инфинитиву глагола (наиболее распространённая практика современных NLP),
- местоименные формы — к именительному падежу мужского рода.

Правила написания лемм:
1. УДАРЕНИЯ: леммы должны иметь ударения (кроме односложных слов);
2. СОВРЕМЕННАЯ ОРФОГРАФИЯ:
2.1) не используй бездумно буву «ѣ» вместо «е» (возможно есть слова, где нужна именно «ѣ», но этих слов меньшинство, а для большинства случаев используй обычную русскую букву «е»)
2.2) не ставь просто так твёрдый знак в конце слов, заканчивающихся на согласный.

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
        self.tokenizer = ChurchSlavonicTokenizer()

    def process(self, text_sentences):
        """
        Формирует входные данные для LLM.

        Весь входной текст сначала нормализуется через
        ChurchSlavonicTextNormalizer.

        После этого:

        1. Уже встречавшиеся token из morph_dict пропускаются.
        2. Уже встречавшиеся token текущей сессии пропускаются.
        3. POS не участвует в дедупликации.
        4. Каждое предложение сохраняется в result_dict.
        """

        # ==============================================================
        # 1. Нормализуем весь исходный текст.
        # ==============================================================
        normalized_text = ChurchSlavonicTextNormalizer.normalize_text(text_sentences)

        # ==============================================================
        # 2. Читаем существующие morph_dict.
        # ==============================================================
        all_morph_dict_files_merged_dict = self.morphDictService.read_and_merge_morph_dicts_from_all_files()

        # ==============================================================
        # 3. Собираем уже известные tokens.
        #
        # Для сравнения используется тот же нормализатор, что и для входного текста.
        # ==============================================================
        seen_tokens_from_all_morph_dicts = {
            self._token_key(sentence_tuple[0])
            for sentence_tuples in all_morph_dict_files_merged_dict.values()
            for sentence_tuple in sentence_tuples
            if sentence_tuple
        }

        # ==============================================================
        # 4. Tokens текущей сессии.
        # ==============================================================
        seen_tokens_from_current_session = set()

        result_dict = {}

        # ==============================================================
        # 5. Обрабатываем уже нормализованный текст.
        # ==============================================================
        for raw_sentence in normalized_text.splitlines():

            sentence = raw_sentence.strip()

            if not sentence:
                continue

            # ----------------------------------------------------------
            # Предложение должно быть представлено в result_dict
            # даже тогда, когда в нём нет новых tokens.
            # ----------------------------------------------------------
            result_dict.setdefault(sentence, [])

            tokens = self.tokenizer.tokenize(sentence)
            for token in tokens:

                token_key = self._token_key(token)

                # ------------------------------------------------------
                # Token уже встречался?
                # ------------------------------------------------------
                if (
                    token_key in seen_tokens_from_all_morph_dicts
                    or token_key in seen_tokens_from_current_session
                ):
                    continue

                # ------------------------------------------------------
                # Новый token.
                # ------------------------------------------------------
                result_dict[sentence].append(token)

                # ------------------------------------------------------
                # Запоминаем token как уже использованный.
                # ------------------------------------------------------
                seen_tokens_from_current_session.add(token_key)

        return self._build_llm_input(result_dict)

    @staticmethod
    def _token_key(token):
        """
        Канонический ключ для дедупликации token.

        Вся логика нормализации token находится
        в ChurchSlavonicTextNormalizer.
        """

        return (
            ChurchSlavonicTextNormalizer
            .normalize_token_key(token)
        )

    @staticmethod
    def _build_llm_input(result_dict):
        """
        Формирует вход для LLM.
        """

        clusters = []

        for sentence, tokens in result_dict.items():

            cluster_lines = [f"{sentence}:"]

            cluster_lines.extend(tokens)

            clusters.append(
                "\n".join(cluster_lines)
            )

        result_dict_str = "\n\n".join(clusters)

        return (
            f"{llm_prompt}\n"
            f"{result_dict_str}"
        ).strip()


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
