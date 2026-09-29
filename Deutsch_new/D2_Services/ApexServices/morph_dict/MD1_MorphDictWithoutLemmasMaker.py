import AppContext
from MorphDictToStrConverter import MorphDictToStrConverter
from View_enums import CurrentLanguageComboBoxEnum

llm_prompt = """
Ты – эксперт по морфологии и лемматизации новогреческого языка.

Твоя задача: для каждого токена определить правильную лемму слова в новогреческом языке.

Тебе предоставляется Python-словарь, ключами которого являются греческие предложения, а значениями - список (token, pos, morph) некоторых слов этого предложения.
- token: точная словоформа
- pos: часть речи, предсказанная внешним парсером (может быть ошибочной)
- morph: морфологические признаки, предсказанные внешним парсером (могут быть ошибочными)

Правила:
1. Всегда отдавай приоритет фактической греческой словоформе токена.
2. Рассматривай POS и MORPH только как ориентировочные подсказки.
   - Если они противоречат форме, игнорируй их.
3. Используй свои знания морфологии новогреческого языка, чтобы определить:
   - является ли токен глаголом, существительным, прилагательным, частицей, местоимением, наречием и т. д.;
   - возможную парадигму словоизменения;
   - корректную лемму, от которой могла произойти данная форма.
4. Если форма морфологически неоднозначна, используй контекст для разрешения.
5. Если контекст отсутствует, выбирай лемму, наиболее совместимую с морфологией и наиболее распространённую.
6. Не давай объяснений, если они явно не запрошены.
7. Выводи результат строго в следующем формате JSON:

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

Вывод должен быть оформлен так, чтобы кластер «предложение и список его токен|лемма-строк» отделялся бы пустой строкой от аналогичных кластеров на базе других предложений с их токен|лемма-строками

Теперь обработай следующий Python-словарь:
"""

class MD1_MorphDictWithoutLemmasMaker:
    def __init__(self):

        from BusinessObjectFactory import BusinessObjectFactory

        language = CurrentLanguageComboBoxEnum.MODERN_GREEK.value
        AppContext.switch_language(language)

        morphDictService = BusinessObjectFactory.get_MorphDictService()
        self.token_pos_tuples_from_all_morph_dict_files = morphDictService.read_and_merge_morph_dicts_from_all_files()

        self.ellSpaCyOrStanzaWrapper = BusinessObjectFactory.get_spaCyOrStanzaWrapper()


    # def _get_token_pos_tuples_from_all_morph_dict_files(self):
    #     from BusinessObjectFactory import BusinessObjectFactory
    #
    #     language = CurrentLanguageComboBoxEnum.MODERN_GREEK.value
    #     AppContext.switch_language(language)
    #
    #     morphDictService = BusinessObjectFactory.get_MorphDictService()
    #
    #     token_pos_tuples_from_all_morph_dict_files = morphDictService.read_and_merge_morph_dicts_from_all_files()
    #     return token_pos_tuples_from_all_morph_dict_files

    def process(self, text_sentences):
        result_dict = {}
        for sentence in text_sentences.strip().split('\n'):
            tuples = self.ellSpaCyOrStanzaWrapper.get_doc_object_tuples(sentence)
            for current_token, current_lemma, current_pos, current_morph in tuples:

                # Если токен представляет собой знак пунктуации, игнорируем его
                if current_pos == 'PUNCT':
                    continue

                # Если токен не является именем собственным, приводим его к нижнему регистру
                if current_pos != 'PROPN':
                    current_token = current_token.lower()

                # Берём в дальнейшую работу только такие токены, которые не встречались ранее:
                # 1) ни в словаре result_dict (текущая сессия)
                # 2) ни в других morph_dict-файлах (предыдущие сессии)
                is_token_absent_from_result_dict = not any(
                    current_token == token and current_pos == pos
                    for tuples in result_dict.values()
                    for token, pos, morph in tuples
                )

                if is_token_absent_from_result_dict:
                    # TODO: прогнать алгоритм 2 раза подряд (сохранив после 1-го раза результаты в morph_dict-файл),
                    #  чтобы убедиться, что 2-й прогон формирует пустой словарь, т. к. все кортежи уже и так есть в
                    #  существующих (последнем) morph_dict-файле.
                    # Проверить отсутствие токена во всех предыдущих morph_dict-файлах (при условии, что у них и POS-теги совпадают)
                    if (current_token, current_pos) not in self.token_pos_tuples_from_all_morph_dict_files:
                        new_tup = (current_token, current_pos, current_morph)
                        if sentence not in result_dict:
                            result_dict[sentence] = []
                        result_dict[sentence].append(new_tup)

        morphDictToStrConverter = MorphDictToStrConverter()
        result_dict_str = morphDictToStrConverter.morph_dict_to_str(result_dict)

        result = f'{llm_prompt}\n{result_dict_str}'.strip()
        # result = f'{result_dict_str}'
        return result

####################################################################

text = """
Ο ήλιος λάμπει σήμερα.
Πίνω έναν καφέ στο μπαλκόνι.
Το λεωφορείο έφτασε αργά.
Η Μαρία διαβάζει ένα βιβλίο.
"""

if __name__ == '__main__':
    md1_MorphDictWithoutLemmasMaker = MD1_MorphDictWithoutLemmasMaker()
    res = md1_MorphDictWithoutLemmasMaker.process(text)
    print(res)
