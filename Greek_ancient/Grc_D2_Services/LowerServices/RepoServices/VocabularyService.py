from ExcelEntities.DictionaryVocabularyEntity import DictionaryVocabularyEntity
from VocabularyExcelDao import VocabularyExcelDao


class VocabularyService:
    def __init__(self):
        self.excel_vocabulary = VocabularyExcelDao()
        self.excel_vocabulary_dict = self.excel_vocabulary.get_all_sheets_data_dict()

    # Ищем слово среди морфологических форм вокабуляра (vocabulary)
    def search_word_among_morph_forms(self, word_token):
        results = []
        # Работаем не до первой совпавшей морф. формы, а проходим всё содержимое вокабуляра от начала до конца.
        # Исходим из того, что одна и та же морф. форма теоретически может встречаться в вокабуляре несколько раз
        # будучи морф. формой совершенно разных лемм.
        for vocabulary_entity in self.excel_vocabulary_dict.values():
            if word_token in vocabulary_entity.morphological_forms:
                results.append(vocabulary_entity)
        return results

    def is_word_among_morph_forms(self, word_token):
        results = self.search_word_among_morph_forms(word_token)
        if len(results):
            return True
        return False

    # Ищем слово среди лемм вокабуляра (vocabulary)
    def search_word_among_lemmas(self, word):
        results = []
        found_lemma = ''
        # if word in self.excel_vocabulary_dict:
        #     result = self.excel_vocabulary_dict[word]
        # return result
        for vocabulary_entity in self.excel_vocabulary_dict.values():
            if word in vocabulary_entity.lemmas:
                found_lemma = word
                results.append(vocabulary_entity)

        if len(results) > 1:
            raise Exception(f"Lemma '{found_lemma}' is duplicated in vocabulary!")

        return results

    def is_word_among_lemmas(self, word):
        results = self.search_word_among_lemmas(word)
        if len(results):
            return True
        return False

    ########**********************##################

    def search_word_in_vocabulary(self, word_token, word_lemma, should_search_among_morph_forms: bool):
        results = []
        if should_search_among_morph_forms:
            # Шаг №1. Ищем слово среди морф. форм (это подстраховка на случай неправильно работающего CLTK)
            results = self.search_word_among_morph_forms(word_token)

        if len(results) == 0:
            # Шаг №2. Ищем слово среди лемм вокабуляра (1-й столбец) используя ТОКЕН текста (т. е. слово "как есть")
            # Вдруг токен встретился в тексте в именит. падеже, и мы имеем шанс его найти в 1-м столбце
            results = self.search_word_among_lemmas(word_token)

            if len(results) == 0:
                # Шаг №3. Ищем слово среди лемм вокабуляра (1-й столбец) используя ЛЕММУ, которую сгенерировал CLTK
                # CLTK может неправильно определять леммы слов и этот шаг остаётся как самое последнее средство
                results = self.search_word_among_lemmas(word_lemma)

        return results

    # Выясняем не является ли слово уже выученным, т. е. не находится ли оно в вокабуляре (vocabulary)
    def is_word_in_vocabulary(self, word_token, word_lemma, should_search_among_morph_forms: bool):
        results = self.search_word_in_vocabulary(word_token, word_lemma, should_search_among_morph_forms)
        if len(results):
            return True
        return False

    def get_word_translation(self, word_token, word_lemma, should_search_among_morph_forms: bool):
        translation = ''

        found_entities = self.search_word_in_vocabulary(word_token, word_lemma, should_search_among_morph_forms)
        if len(found_entities) == 1:
            word_article: DictionaryVocabularyEntity = found_entities[0]
            translation = word_article.translation
        elif len(found_entities) > 1:
            for entity in found_entities:
                # Т. к. в вокабуляре было найдено несколько словарных статей, непонятно каким должен быть результат
                # работы метода в этом случае. Пока в качестве рабочего варианта сделал вывод строкового представления
                # всех найденных словарных статей
                translation += str(entity)

        return translation


#####################################

vocabularyService = VocabularyService()

# word_token = 'Ἠσαΐᾳ'
# word_lemma = 'ἠσαΐας'
# res = vocabularyService.is_word_in_vocabulary(word_token, word_lemma, True)
# print(res)

# word_token = 'Ἠσαΐᾳ'.lower()
# print(vocabularyService.search_word_among_morph_forms(word_token))
# print(vocabularyService.is_word_among_morph_forms(word_token))
