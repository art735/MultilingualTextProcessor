from AuxiliaryVerbService import AuxiliaryVerbService
from DeterminerService import DeterminerService
from DeuDefiniteArticleService import DeuDefiniteArticleService
from ExcelService import ExcelService
from GermanPronounLemmaService import GermanPronounLemmaService
from GermanVerbLemmaService import GermanVerbLemmaService
from ModalVerbService import ModalVerbService
from MorphologyParser import MorphologyParser
from SpaCyPosResolver import SpaCyPosResolver


# осенью 2024 - зимой 2025 обрабатывал материалы уровня A1 из Гёте-методички следующими версиями библиотек:
# spaCy: 3.7.5
# de_dep_news_trf: 3.7.2

class DeuLemmaResolver:

    def __init__(self):
        self.excelService = ExcelService()
        self.spaCyPosResolver = SpaCyPosResolver()
        self.germanPronounLemmaService = GermanPronounLemmaService()
        self.determinerService = DeterminerService()
        self.deuDefiniteArticleService = DeuDefiniteArticleService()
        self.auxiliaryVerbService = AuxiliaryVerbService()
        self.modalVerbService = ModalVerbService()
        self.germanVerbLemmaService = GermanVerbLemmaService()

        self.morphologyParser = MorphologyParser()

    # TODO: добавить флажок, который бы задавал режим работы метода:
    #  1) более подробный для работы на 1-м этапе с выводом всех "not found" ошибок от всех сервисов (PronounService, VerbService и т. п.).
    #  2) без подробностей с выводом леммы "как есть" (в худшем случае с выводом того варианта леммы, который нашла
    #  spaCy) для тех сервисов следующих этапов, которые вызывают данный метод как один из шагов своей работы
    def get_single_lemma(self, token, lemma, pos, morph):

        # excelService = ExcelService()  # инициализируем каждый раз заново при вызове метода
        # с переходом на инжекцию ExcelService через ctor не понял как инициализировать этот сервис каждый раз при
        # вызове метода

        # Для каждого иностранного языка должен быть .xls-файл, который, среди прочего, содержал бы список игнорируемых
        # токенов. Например, это может быть отдельный лист с названием "ignored_tokens".
        if self.excelService.is_token_ignored(token):  # TODO: сделать lang-зависимым
            return None

        # В первую очередь ищем леммы в ручном hard-coded словаре, который содержит те токены и их соответствующие
        # леммы, которые spaCy не может корректно определить (корректно по токену найти правильную лемму).
        manual_lemma = self.excelService.search_among_excel_manual_lemmas(token)
        if manual_lemma:
            return manual_lemma

        if self.spaCyPosResolver.is_noun(pos):
            # Если token начинается с маленькой буквы, то делаем первую букву заглавной, т. к. немецкие существительные
            # должны начинаться с большой буквы.
            if token[0].islower():
                token = token.capitalize()
                lemma = lemma.capitalize()
        # Слова, не являющиеся существительными, приводим к нижнему регистру
        else:
            token = token.lower()
            lemma = lemma.lower()

        # В самом худшем случае лемма просто останется сама собой под псевдонимом current_word.
        # Псевдоним введён потому, что леммам-существительным добавляются артикли и получившаяся конструкция
        # в строгом смысле слова леммой уже считаться не может.
        current_word = lemma

        # Определяем является ли слово местоимением не по pos-тегу 'PRON', а именно по ключу "PronType"
        # в словаре morph. Неопределённое местоимение может быть помечено в spaCy одним из шести pos-тегов
        # (NOUN, ADJ, NUM, PRON, ADV, DET), но при этом pos-тег не будет влиять на определение
        # начальной формы (леммы) неопределённого местоимения (если верить ChatGPT-4omni, August 2024).
        # Поэтому первейший критерий, по которому определяем часть речи - это, как ни странно, не pos-тег,
        # а характерные поля объекта morph. В частности для выяснения является ли слово местоимением,
        # проверяем поле "PronType" объекта morph и не обращаем внимания на pos-тег.

        # pronominal_type = self.morphologyParser.parse(morph, "PronType")
        # if pronominal_type:
        # Проверка на принадлежность слова к местоимениям должна идти самой первой (по порядку) проверкой, потому что
        # здесь проверяется не pos (который может быть любым и это может ввести в заблуждение), а morph!
        if self.spaCyPosResolver.is_pronoun(morph):
            current_word = self.germanPronounLemmaService.get_pronoun_lemma(token, lemma, morph)
            current_word = self._post_process_lemma_search_result(lemma, current_word,
                                                                  'not found by PronounService')

        # determiner [dɪ'tɜːmɪnə] лингв. определяющее слово, определитель, детерминатив
        # Детерминативами в spaCy считаются, например, артикли, некоторые виды местоимений и т. д.
        # elif pos == 'DET':
        elif self.spaCyPosResolver.is_determiner(pos):
            current_word = self.determinerService.get_lemma(lemma, morph)
            current_word = self._post_process_lemma_search_result(lemma, current_word,
                                                                  'not found by DeterminerService')

        # Если слово является нарицательным существительным (pos = 'NOUN'), добавляем ему артикль.
        # Для собственных имён существительных (pos == 'PROPN') в методе add_definite_article_to_lemma есть отдельная
        # ветка (артикль добавляется только словам-исключениям).
        # elif pos == 'NOUN':
        elif self.spaCyPosResolver.is_noun(pos):
            current_word = self.deuDefiniteArticleService.add_definite_article_to_lemma(lemma, pos, morph)

        # aux-глаголами в терминологии spaCy считаются вспомогательные глаголы sein, haben и werden и модальные глаголы
        elif self.spaCyPosResolver.is_aux(pos):
            # Сначала ищем среди hard-coded словарей вспомогательных глаголов и если там ничего не будет найдено,
            # будем искать среди hard-coded словарей модальных глаголов
            current_word = self.auxiliaryVerbService.get_verb_infinitive(token, morph)
            if not current_word:  # если не нашли среди вспомогательных глаголов, ищем среди модальных глагол
                current_word = self.modalVerbService.get_verb_infinitive(token, morph)
                if not current_word:  # если не нашли и среди модальных глаголов, выводим сообщение о странности такой ситуации
                    current_word = self._post_process_lemma_search_result(
                        lemma, current_word,
                        'not found among hard-coded dictionaries of AUXILIARY and MODAL verbs')

        # spaCy плохо умеет определять леммы (инфинитивы) глаголов. Пользуемся данными из "Deutsch Lexikon (!Popov).xls" для определения
        # леммы глагола.
        elif self.spaCyPosResolver.is_verb(pos):
            current_word = self.germanVerbLemmaService.find_verb_lemma(token)
            if not current_word:
                # current_word = f"{lemma} (no verb form '{token}' in 'Deutsch Lexikon (!Popov).xls')"
                current_word = lemma

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

    def _post_process_lemma_search_result(self, lemma, current_word, message):
        result = current_word
        if len(current_word) == 0:
            result = f"spaCy lemma: '{lemma}'; {message}"
        return result


#################################################

if __name__ == '__main__':
    deuLemmaResolver = DeuLemmaResolver()
    res = deuLemmaResolver.get_single_lemma('Morgen', 'Morgen', 'NOUN',
                                             {'Case': ['Nom'], 'Gender': ['Masc'], 'Number': ['Sing']})
    print(res)
