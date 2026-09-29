from AuxiliaryVerbService import AuxiliaryVerbService
from DeterminerService import DeterminerService
from EllDefiniteArticleService import EllDefiniteArticleService
from ExcelService import ExcelService
from DeuDefiniteArticleService import DeuDefiniteArticleService
from GermanPronounLemmaService import GermanPronounLemmaService
from GermanVerbLemmaService import GermanVerbLemmaService
from ModalVerbService import ModalVerbService
from MorphologyParser import MorphologyParser
from SpaCyPosResolver import SpaCyPosResolver


# осенью 2024 - зимой 2025 обрабатывал материалы уровня A1 из Гёте-методички следующими версиями библиотек:
# spaCy: 3.7.5
# de_dep_news_trf: 3.7.2

class EllLemmaResolver:

    def __init__(self):
        self.excelService = ExcelService()
        self.spaCyPosResolver = SpaCyPosResolver()
        self.ellDefiniteArticleService = EllDefiniteArticleService()
        # self.germanPronounLemmaService = GermanPronounLemmaService()
        # self.determinerService = DeterminerService()
        # self.auxiliaryVerbService = AuxiliaryVerbService()
        # self.modalVerbService = ModalVerbService()
        # self.germanVerbLemmaService = GermanVerbLemmaService()
        #
        # self.morphologyParser = MorphologyParser()

    def get_single_lemma(self, token, lemma, pos, morph):

        # excelService = ExcelService()  # инициализируем каждый раз заново при вызове метода
        # с переходом на инжекцию ExcelService через ctor не понял как инициализировать этот сервис каждый раз при
        # вызове метода

        # Для каждого иностранного языка должен быть .xls-файл, который, среди прочего, содержал бы список игнорируемых
        # токенов. Например, это может быть отдельный лист с названием "ignored_tokens".
        if self.excelService.is_token_ignored(token):
            return None

        # В первую очередь ищем леммы в ручном hard-coded словаре, который содержит те токены и их соответствующие
        # леммы, которые spaCy не может корректно определить (корректно по токену найти правильную лемму).
        manual_lemma = self.excelService.search_among_excel_manual_lemmas(token)
        if manual_lemma:
            return manual_lemma

        # Если слово не является собственным именем существительным и начинается с большой буквы, делаем его
        # с маленькой буквы
        if not self.spaCyPosResolver.is_proper_noun(pos) and token[0].isupper():
            token = token.lower()
            lemma = lemma.lower()

        # В самом худшем случае лемма просто останется сама собой под псевдонимом current_word.
        # Псевдоним введён потому, что леммам-существительным добавляются артикли и получившаяся конструкция
        # в строгом смысле слова леммой уже считаться не может.
        current_word = lemma

        if self.spaCyPosResolver.is_noun(pos):
            current_word = self.ellDefiniteArticleService.add_definite_article_to_lemma(lemma, pos, morph)

        # Для прилагательных добавляем "ADJ", чтобы на следующих этапах с помощью этой метки добавить им окончания
        # в поле Front_comment
        if self.spaCyPosResolver.is_adjective(pos):
            current_word = f'{current_word}|ADJ'

        # Снова ищем current_word среди manual_lemmas и в случае успеха возвращаем костыль из Excel
        # В частности, данный подход нужен для слов erste, zweite, etc. для которых spaCy считает леммой формы erster,
        # zweiter, etc., а у меня в [Vocab]-словарике они выписаны в слабом склонении: erste, zweite, etc.
        # Поэтому здесь нужен симбиоз обоих подходов: сначала spaCy находит свой вариант леммы, а потом я её в Excel
        # подменяю на нужный мне вариант.
        # "Jacken im ersten, Jeans im zweiten Stock."
        manual_lemma = self.excelService.search_among_excel_manual_lemmas(current_word)
        if manual_lemma:
            current_word = manual_lemma

        return current_word

    # def _post_process_lemma_search_result(self, lemma, current_word, message):
    #     result = current_word
    #     if len(current_word) == 0:
    #         result = f"spaCy lemma: '{lemma}'; {message}"
    #     return result


#################################################

if __name__ == '__main__':
    ellLemmaResolver = EllLemmaResolver()
    res = ellLemmaResolver.get_single_lemma('νομός', 'νομός', 'NOUN',
                                            {'Case': ['Nom'], 'Gender': ['Masc'], 'Number': ['Sing']})
    print(res)
