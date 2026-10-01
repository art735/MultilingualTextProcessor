import AppContext
from MorphDictToStrConverter import MorphDictToStrConverter
from View_enums import CurrentLanguageComboBoxEnum

llm_prompt = """
\n\nТы – эксперт по морфологии и лемматизации иностранных языков.

Твоя задача: для каждого токена определить правильную лемму слова на предоставленном иностранном языке.

Тебе даётся Python-словарь, ключами которого являются предложения иностранного языка,
а значениями - список (token, pos, morph) некоторых слов этого предложения, где:
- token: точная словоформа
- pos: часть речи, предсказанная внешним парсером (может быть ошибочной)
- morph: морфологические признаки, предсказанные внешним парсером (могут быть ошибочными).

Правила:
1. Всегда отдавай приоритет фактической словоформе токена.
2. Рассматривай POS и MORPH только как ориентировочные подсказки.
   - Если они противоречат форме, игнорируй их.
3. Используй свои знания морфологии, чтобы определить:
   - является ли токен глаголом, существительным, прилагательным, частицей, местоимением, наречием и т. д.;
   - возможную парадигму словоизменения;
   - корректную лемму, от которой могла произойти данная форма.
4. Если форма морфологически неоднозначна, используй контекст для разрешения.
5. Если контекст отсутствует, выбирай лемму, наиболее совместимую с морфологией и наиболее распространённую.
6. Не давай объяснений, если они явно не запрошены.
7. Выводи результат строго в следующем текстовом формате:

предложение1
токен11|лемма11
токен12|лемма12
...
токен_1n|лемма_1n

предложение2
токен21|лемма21
токен22|лемма22
...
токен_2n|лемма_2n

и т. д.

Вывод должен быть оформлен так, чтобы кластер «предложение и список его токен|лемма-строк» отделялся бы пустой строкой
от аналогичных кластеров на базе других предложений с их токен|лемма-строками.

Теперь обработай следующий Python-словарь:
"""


class MD1_MorphDictWithoutLemmasMaker:

    def __init__(self, morphDictService, spaCyOrStanzaWrapper):
        self.morphDictService = morphDictService
        self.spaCyOrStanzaWrapper = spaCyOrStanzaWrapper
        # простой утилитный класс, пока не стал его передавать через DI, хотя ChatGPT советует так сделать для
        # поддержания единообразной архитектуры передачи зависимостей через ctor
        self.morphDictToStrConverter = MorphDictToStrConverter()

    def process(self, text_sentences):

        # новое предложение?
        #    │
        #    ├─ нет → skip
        #    │
        #    └─ да
        #        │
        #        └─ каждый token + POS
        #              │
        #              ├─ уже в текущем предложении → skip
        #              ├─ уже в текущей сессии    → skip
        #              ├─ уже в старых morph_dict → skip
        #              └─ иначе → добавить
        #        │
        #        └─ предложение добавить ВСЕГДА

        all_morph_dict_files_merged_dict = self.morphDictService.read_and_merge_morph_dicts_from_all_files()

        # Множество уникальных пар (token, POS), уже встречавшихся в предыдущих morph_dict-файлах.
        # Внешние фигурные скобки { ... } в данном случае означают именно set, а не dict, потому что внутри нет
        # конструкции key: value. Это множество (set), создаваемое через генераторное выражение для множества (set comprehension).
        seen_token_pos_from_all_morph_dicts = {
            self._token_pos_key(existing_token, existing_pos)
            for sentence_tuples in all_morph_dict_files_merged_dict.values()
            for existing_token, *_, existing_pos, _ in sentence_tuples
        }

        result_dict = {}

        # Множество уникальных пар (token, POS), уже добавленных в текущий result_dict.
        # Используем именно set() (а не list) для хранения уже встречавшихся пар (token, POS),
        # чтобы проверять наличие токена за O(1) в среднем вместо последовательного перебора всех ранее сохранённых
        # кортежей. Это существенно ускоряет поиск дубликатов при большом количестве токенов.
        seen_token_pos_from_current_session = set()

        # `splitlines()` надёжнее, чем `text_sentences.split('\n')`, т. к. splitlines()
        # корректно работает с разными вариантами перевода строк (\n, \r\n и т. д.).
        for sentence in (s.strip() for s in text_sentences.splitlines() if s.strip()):

            # Уровень 1: встречалось ли ранее данное предложение?
            #
            # Если предложение уже есть либо в morph_dict-файлах,
            # либо уже было добавлено в текущий result_dict,
            # полностью пропускаем его.
            if sentence in result_dict or sentence in all_morph_dict_files_merged_dict:
                continue

            # Список кортежей (token, POS, morph) текущего предложения
            sentence_tuples = []

            # Множество уникальных пар (token, POS), уже добавленных в текущее предложение.
            seen_token_pos_from_current_sentence = set()

            tuples = self.spaCyOrStanzaWrapper.get_doc_object_tuples(sentence)

            # current_lemma здесь намеренно игнорируется с помощью _, т. к. она здесь нигде не используется.
            for current_token, _, current_pos, current_morph in tuples:

                # Если токен представляет собой знак пунктуации,
                # игнорируем его.
                if current_pos == 'PUNCT':
                    continue

                # Приводим токен к нужному регистру в зависимости от языка и POS.
                current_token = self._normalize_token_case(
                    current_token,
                    current_pos,
                    AppContext.get_current_language()
                )

                # Единый ключ для всех проверок token + POS.
                #
                # casefold() вызывается внутри _token_pos_key(), поэтому в остальных местах программы повторять
                # current_token.casefold() / existing_token.casefold() не нужно.
                token_pos_key = self._token_pos_key(
                    current_token,
                    current_pos
                )

                # Поиск через оператор in внутри set() работает за O(1), что намного эффективнее, чем искать в списках.

                # Token check #1. Есть ли такой token + POS в текущем предложении? Если да, то пропускаем его.
                if token_pos_key in seen_token_pos_from_current_sentence:
                    continue

                # Token check #2. Есть ли такой token + POS в result_dict текущей сессии? Если да, то пропускаем его.
                if token_pos_key in seen_token_pos_from_current_session:
                    continue

                # Token check #3. Есть ли такой token + POS в предыдущих morph_dict-файлах? Если да, то пропускаем его.
                if token_pos_key in seen_token_pos_from_all_morph_dicts:
                    continue

                # В данной точке кода очевидно, что token + POS отсутствует во всех существующих наборах данных
                # (текущего предложения, текущей сессии и во всех morph_dict-файлах). Значит добавляем его в результаты.
                new_tup = (current_token, current_pos, current_morph)
                sentence_tuples.append(new_tup)

                # Фиксируем токен как уже использованный и в текущем предложении, и в текущей сессии.
                seen_token_pos_from_current_sentence.add(token_pos_key)
                # Обязательно нужно добавлять token_pos_key и в результат текущей сессии, т. к. по завершении
                # внутреннего цикла все накопленные пары текущего предложения будут очищены.
                seen_token_pos_from_current_session.add(token_pos_key)

            # Предложение добавляется в результат НЕЗАВИСИМО от того, имеет ли оно хотя бы один новый токен.
            result_dict[sentence] = sentence_tuples

        result_dict_str = self.morphDictToStrConverter.morph_dict_to_str(result_dict)
        result = f'{llm_prompt}\n{result_dict_str}'.strip()

        return result

    @staticmethod
    def _token_pos_key(token, pos):
        """
        Создаёт единый нормализованный ключ для сравнения token + POS.

        Хорошее решение для централизации casefold().
        Регистронезависимое сравнение токенов всегда выполняется через casefold() именно здесь,
        поэтому в остальных местах программы не требуется повторять вызов метода casefold() при сравнении токенов,
        что с одной стороны исключает дублирование этой логики, а с другой - риск забыть вызывать casefold(),
        что может привести к неконсистентному сравнению.
        """
        return token.casefold(), pos

    @staticmethod
    def _normalize_token_case(token, pos, language):
        """
        Приводит токен к нижнему регистру с учётом языка и POS.

        Немецкий:
            PROPN и NOUN сохраняют исходный регистр.

        Остальные языки:
            PROPN сохраняет исходный регистр.
            Все остальные токены приводятся к нижнему регистру.
        """

        if language == CurrentLanguageComboBoxEnum.GERMAN.value:
            if pos in {'PROPN', 'NOUN'}:
                return token
        else:
            if pos == 'PROPN':
                return token

        return token.lower()


####################################################################

text = """
Ο ήλιος λάμπει σήμερα.
Πίνω έναν καφέ στο μπαλκόνι.
Το λεωφορείο έφτασε αργά.
Η Μαρία διαβάζει ένα βιβλίο.
"""

# text = """
# Sie ist sehr freundlich und hilfsbereit.
# Gestern haben sie einen neuen Hund adoptiert.
# """

text = """
The children were running quickly through the fields.
The children were running through the fields quickly.
The leaves were falling quickly from the highest trees.
The leaves were falling from the highest trees quickly.
"""

if __name__ == '__main__':
    from BusinessObjectFactory import BusinessObjectFactory

    # language = CurrentLanguageComboBoxEnum.GERMAN.value
    # language = CurrentLanguageComboBoxEnum.MODERN_GREEK.value
    language = CurrentLanguageComboBoxEnum.ENGLISH.value
    # language = CurrentLanguageComboBoxEnum.ANCIENT_GREEK.value

    AppContext.switch_language(language)

    md1_MorphDictWithoutLemmasMaker = BusinessObjectFactory.create_md1_MorphDictWithoutLemmasMaker()
    res = md1_MorphDictWithoutLemmasMaker.process(text)

    # если вдруг вывод "пустой", убедиться, что язык входного текста соответствует языку, который выбран в комбобоксе
    print(res)
