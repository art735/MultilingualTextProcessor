import ast

from MorphDictToStrConverter import MorphDictToStrConverter


class MD2_LlmLemmasIntoMorphDictIntegrator:
    def __init__(self):
        self.morphDictToStrConverter = MorphDictToStrConverter()

    def integrate_llm_lemmas_into_orig_dict(self, orig_dict_plus_llm_output):
        # 1. Ковертируем информацию из входной строки в два словаря и валидируем их консистентность между собой
        orig_dict, llm_dict = self._extract_two_dicts(orig_dict_plus_llm_output)

        # 2. Формируем результирующий словарь с полноценными кортежами, добавляя к существующей в orig_dict информации
        # ещё и леммы, т. е. (token, pos, morph) -> (token, LEMMA, pos, morph)
        result_dict = {}
        for sentence in orig_dict.keys():
            orig_dict_tuples = orig_dict[sentence]
            llm_dict_tuples = llm_dict[sentence]

            new_tuples = []
            for (token, pos, morph), (llm_token, llm_lemma) in zip(orig_dict_tuples, llm_dict_tuples):

                # На всякий случай проверим идентичность токенов
                if token != llm_token:
                    raise ValueError(
                        f"Несовпадающие токены в предложении:'{sentence}'\n"
                        f"orig_dict token = '{token}'\n"
                        f"llm_dict token = '{llm_token}'"
                    )

                # Интегрируем lemma в кортежи
                new_tuples.append((token, llm_lemma, pos, morph))
            result_dict[sentence] = new_tuples

        result_dict_str = self.morphDictToStrConverter.morph_dict_to_str(result_dict)
        return result_dict_str

    # Входной текст состоит из строкового представления orig_dict и под ним идут в столбик обычным текстом его же ключи
    # с расположенными под ними token|лемма-строками.
    # Задача: распарсить входную строку так, чтобы на выходе получилось два полноценных Python-словаря.
    def _extract_two_dicts(self, big_text: str):
        # 1. Отделяем верхний/оригинальный словарь по балансу фигурных скобок
        orig_dict_str, rest = self._extract_orig_dict(big_text)

        # 2. Конвертируем текст верхнего/оригинального словаря в Python-объект
        orig_dict = self._parse_dict_text(orig_dict_str)

        # 3. Парсим вторую/нижнюю часть в словарь {sentence: [(token, lemma)...]}
        llm_dict = {}
        blocks = rest.split("\n\n")  # предложения разделены пустой строкой
        for block in blocks:
            sentence, pairs = self._parse_token_lemma_block(block)
            if sentence:
                llm_dict[sentence] = pairs

        # 4. Валидируем словари на соответствие ключей и токенов
        self._validate_dicts(orig_dict, llm_dict)

        return orig_dict, llm_dict

    # Работает надёжно даже если:
    # 1) внутри словаря есть вложенные {}
    # 2) в морфологических тегах случайно появятся фигурные скобки
    # 3) в блоке токенов/лемм встречаются {...}
    # 4) LLM генерирует мусор или формат внизу меняется
    # Потому что определение конца словаря делается строго по балансу скобок — единственно правильный способ.
    def _extract_orig_dict(self, text: str):
        """
        Извлекает верхний словарь из текста по балансу {}.
        Возвращает:
            dict_text — строка словаря
            rest_text — остаток после словаря
        """
        # Находим первую '{'
        try:
            start = text.index("{")
        except ValueError:
            raise ValueError("В тексте нет открывающей фигурной скобки '{'")

        depth = 0
        end = None

        # Идём по символам, считая баланс
        for i, ch in enumerate(text[start:], start=start):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break

        if end is None:
            raise ValueError("Не удалось найти корректную закрывающую '}' для словаря")

        dict_text = text[start:end]
        rest_text = text[end:].strip()

        return dict_text, rest_text

    def _parse_dict_text(self, dict_text: str):
        """
        Пробует распарсить текст словаря сначала как JSON, затем как Python-словарь.
        """
        # try:
        #     return json.loads(dict_text)
        # except Exception:
        #     pass

        try:
            return ast.literal_eval(dict_text)
        except Exception as e:
            raise ValueError(f"Не удалось распарсить словарь: {e}")

    def _parse_token_lemma_block(self, block: str):
        """
        Превращает блок:
            предложение
            токен|лемма
            токен|лемма
        в структуру (sentence, [(token, lemma)...]).
        """
        lines = [l.strip() for l in block.splitlines() if l.strip()]
        if not lines:
            return None, []

        sentence = lines[0]
        pairs = []
        for line in lines[1:]:
            if "|" in line:
                token, lemma = line.split("|", 1)
                pairs.append((token.strip(), lemma.strip()))

        return sentence, pairs

    def _validate_dicts(self, orig_dict, llm_dict):
        """
        Проверяет:
        1) порядок и кол-во ключей
        2) порядок и кол-во токенов внутри значений
        """

        # Превращаем в списки, поскольку порядок важен
        keys_orig_dict = list(orig_dict.keys())
        keys_llm_dict = list(llm_dict.keys())

        # --- 1) Проверяем порядок ключей ---
        if keys_orig_dict != keys_llm_dict:
            raise ValueError(
                "Порядок или состав ключей в словарях orig_dict и llm_dict не совпадает! Возможное решение: добавить пустую строку-разделитель перед одним из предложений.\n"
                f"orig_dict:  {keys_orig_dict}\n"
                f"llm_dict: {keys_llm_dict}"
            )

        # --- 2) Проверяем последовательность токенов внутри каждого ключа ---
        for sentence in keys_orig_dict:
            tokens_orig_dict = [t[0] for t in orig_dict[sentence]]
            tokens_llm_dict = [t[0] for t in llm_dict[sentence]]

            if tokens_orig_dict != tokens_llm_dict:
                raise ValueError(
                    f"Несоответствие токенов в следующем предложении: '{sentence}'\n"
                    f"Токены orig_dict: {tokens_orig_dict}\n"
                    f"Токены llm_dict: {tokens_llm_dict}"
                )

        return True


###############################################################################

orig_dict_plus_llm_output_test_str = """
{
	"Ο ήλιος λάμπει σήμερα.": [
		("ήλιος", "PROPN", "Case=Nom|Gender=Masc|Number=Sing"),
		("λάμπει", "VERB", "Aspect=Imp|Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act"),
		("σήμερα", "ADV", "")
	],
	"Πίνω έναν καφέ στο μπαλκόνι.": [
		("πίνω", "VERB", "Aspect=Imp|Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act"),
		("έναν", "DET", "Case=Acc|Definite=Ind|Gender=Masc|Number=Sing|PronType=Art"),
		("καφέ", "NOUN", "Case=Acc|Gender=Masc|Number=Sing"),
		("σ", "ADP", ""),
		("μπαλκόνι", "NOUN", "Case=Acc|Gender=Neut|Number=Sing")
	],
	"Το λεωφορείο έφτασε αργά.": [
		("λεωφορείο", "NOUN", "Case=Nom|Gender=Neut|Number=Sing"),
		("έφτασε", "VERB", "Aspect=Perf|Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act"),
		("αργά", "ADV", "")
	],
	"Η Μαρία διαβάζει ένα βιβλίο.": [
		("μαρία", "NOUN", "Case=Nom|Gender=Fem|Number=Sing"),
		("διαβάζει", "VERB", "Aspect=Imp|Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act"),
		("βιβλίο", "NOUN", "Case=Acc|Gender=Neut|Number=Sing")
	]
}

Ο ήλιος λάμπει σήμερα.
ήλιος|ήλιος
λάμπει|λάμπω
σήμερα|σήμερα

Πίνω έναν καφέ στο μπαλκόνι.
πίνω|πίνω
έναν|ένας
καφέ|καφές
σ|σε
μπαλκόνι|μπαλκόνι

Το λεωφορείο έφτασε αργά.
λεωφορείο|λεωφορείο
έφτασε|φτάνω
αργά|αργά

Η Μαρία διαβάζει ένα βιβλίο.
μαρία|Μαρία
διαβάζει|διαβάζω
βιβλίο|βιβλίο
"""

if __name__ == '__main__':
    md2_LlmLemmasIntoMorphDictIntegrator = MD2_LlmLemmasIntoMorphDictIntegrator()
    res = md2_LlmLemmasIntoMorphDictIntegrator.integrate_llm_lemmas_into_orig_dict(orig_dict_plus_llm_output_test_str)
    print(res)
