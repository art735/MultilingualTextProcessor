from itertools import chain

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
        # поддержания общей архитектуры передачи зависимостей через ctor
        self.morphDictToStrConverter = MorphDictToStrConverter()

    def process(self, text_sentences):

        all_morph_dict_files_merged_dict = self.morphDictService.read_and_merge_morph_dicts_from_all_files()
        # сквозной список всех кортежей
        tuples_from_all_morph_dict_files = list(chain.from_iterable(all_morph_dict_files_merged_dict.values()))

        result_dict = {}

        # `splitlines()` надёжнее, чем `text_sentences.split('\n')`, т. к. splitlines() корректно работает с разными
        # вариантами перевода строк (\n, \r\n и т. д.).
        for sentence in (s.strip() for s in text_sentences.splitlines() if s.strip()):

            # Уровень 1: встречалось ли ранее само предложение?
            #        ↓
            #      да → вообще не добавляем предложение
            #      нет → добавляем предложение
            #
            # Уровень 2: какие токены этого предложения нужны внутри него?
            #        ↓
            #   только те токены, которые не встречались ранее (учитывая и связанный с ними POS)

            # Если предложение ранее встречалось, игнорируем его и переходим к следующему предложению
            if sentence in result_dict or sentence in all_morph_dict_files_merged_dict:
                continue

            sentence_with_tuples = {sentence: []}

            tuples = self.spaCyOrStanzaWrapper.get_doc_object_tuples(sentence)

            # current_lemma здесь намеренно игнорируется с помощью _, т. к. она здесь нигде не используется
            for current_token, _, current_pos, current_morph in tuples:

                # Если токен представляет собой знак пунктуации, игнорируем его
                if current_pos == 'PUNCT':
                    continue

                # Приводим токен к нужному регистру в зависимости
                # от языка и POS.
                current_token = self._normalize_token_case(
                    current_token,
                    current_pos,
                    AppContext.get_current_language()
                )

                # Берём в дальнейшую работу только такие токены, которые не встречались ранее:
                # 1) ни в списке токенов текущего предложения
                # 2) ни в словаре result_dict (текущая сессия)
                # 3) ни в других morph_dict-файлах (предыдущие сессии)

                # Сравнение токенов выполняется без учёта регистра как подстраховка на случай, когда регистр токена
                # в словаре был подправлен вручную как исправление ошибки работы Stanza (теоретически она может
                # неверно определить POS слова: посчитать слово PROPN, когда оно таким не является или же наоборот
                # не заметить настоящее PROPN и присвоить ему NOUN и т. д.).
                # POS должен совпадать.

                # Token check #1. Есть ли токен в списке токенов текущего предложения. Если да, то пропукаем его.
                is_token_absent_from_current_sentence = self._is_token_pos_absent(
                    current_token,
                    current_pos,
                    sentence_with_tuples[sentence]  # токены текущего предложения
                )
                if not is_token_absent_from_current_sentence:
                    continue

                # Token check #2. Есть ли токен в result_dict (текущая сессия). Если да, то пропукаем его.
                is_token_absent_from_result_dict = all(
                    self._is_token_pos_absent(
                        current_token,
                        current_pos,
                        sentence_tuples
                    )
                    for sentence_tuples in result_dict.values()
                )
                if not is_token_absent_from_result_dict:
                    continue

                # Token check #3. Есть ли токен в других morph_dict-файлах (предыдущие сессии). Если да, то пропукаем его.
                is_token_absent_from_morph_dict_files = self._is_token_pos_absent(
                        current_token,
                        current_pos,
                        tuples_from_all_morph_dict_files
                    )
                if not is_token_absent_from_morph_dict_files:
                    continue

                # В данной точке кода очевидно, что токена нет во всех существующих наборах данных, поэтому добавляем
                # его в результирующий набор.
                new_tup = (current_token, current_pos, current_morph)
                sentence_with_tuples[sentence].append(new_tup)
                # end of loop over tuples

            # update() добавляет новые ключи в конец словаря, сохраняя их порядок
            result_dict.update(sentence_with_tuples)
            # end of loop over sentences

        result_dict_str = self.morphDictToStrConverter.morph_dict_to_str(result_dict)
        result = f'{llm_prompt}\n{result_dict_str}'.strip()
        return result

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

    @staticmethod
    def _is_token_pos_absent(token, pos, morph_dict_tuples):
        """
        Проверяет, отсутствует ли в переданном наборе токенов
        токен с таким же POS.

        Сравнение токенов выполняется без учёта регистра.
        Это необходимо, например, для:
            The / the
            Μαρία / μαρία

        POS при этом должен совпадать.
        """

        # casefold() предназначен для регистронезависимого сравнения строк и работает корректнее lower() для некоторых языков.
        # Сравниваем здесь токены без учёта регистра, это универсальный способ для всех языков.

        # any() отвечает на вопрос: Есть ли хотя бы один такой элемент?
        # Тогда: not any(...) читается как: Нет ни одного такого элемента.
        # Это практически дословно соответствует названию функции _is_token_pos_absent().
        # И семантически not any(...) здесь лучше чем all()

        # В данный метод передаются кортежи двух разных форматов:
        # 1) кортежи в result_dict: (existing_token, existing_pos, morph)
        # 2) кортежи из morph_diсt-файлов: (existing_token, EXISTING_LEMMA, existing_pos, morph)
        # Из кортежей обоих типов нужно взять только existing_token и existing_pos, поэтому применяется синтаксис *_ для existing_lemma
        return not any(
            token.casefold() == existing_token.casefold() and pos == existing_pos
            for existing_token, *_, existing_pos, _ in morph_dict_tuples
        )


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
