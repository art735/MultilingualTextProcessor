import re

import AppContext
from CharConstants import PIPE
from MorphologyParser import MorphologyParser
from MultilingualExcelDao import MultilingualExcelDao
from SpaCyPosResolver import SpaCyPosResolver

# Базовый класс для работы с определённым артиклем
class BaseDefiniteArticleService:
    def __init__(self, lang_code: str, definite_articles_dict: dict):
        self.lang_code = lang_code
        self.definite_articles_dict = definite_articles_dict
        self.multilingualExcelDao = MultilingualExcelDao(lang_code)
        self.morphologyParser = MorphologyParser()
        self.spaCyPosResolver = SpaCyPosResolver()

    def add_definite_article_to_lemma(self, lemma: str, pos: str, morph):
        # Чтобы не потерять lemma в перипетиях алгоритма, сразу записываем её в result и в худшем случае её же
        # и вернём в качестве результата.
        result = lemma

        # Самое первое действие здесь - это проверить, не содержится ли token в Excel-листе manual_lemmas, т. к.
        # spaCy может неправильно лемматизировать и определить морфологию некоторых слов. И если это так, то просто
        # возвращаем hard-coded лемму для соответствующего токена.
        manual_lemmas_dict = self.multilingualExcelDao.get_manual_lemmas_dict()
        if lemma in manual_lemmas_dict:
            result = manual_lemmas_dict[lemma]
            return result

        # Ветка для работы с СОБСТВЕННЫМ именем существительным (только для немецкого языка)
        if AppContext.is_language_german(self.lang_code) and self.spaCyPosResolver.is_proper_noun(pos):
            # В первую очередь ищем СОБСТВЕННОЕ имя существительное среди специального списка исключений.
            # Если оно нашло себя в этом списке, возвращаем результат с артиклем, в противном случае - без артикля.
            search_res = self._search_among_exceptional_proper_nouns_with_articles(lemma)
            if search_res:
                result = search_res
                return result

        # Искать артикль для леммы - это значит искать артикль всегда имея в виду только именительный падеж.
        # Род существительного остаётся без изменения.
        # Число существительного в spaCy имеет некоторую логическую связь с Gender, см. ниже.
        gender = self.morphologyParser.parse(morph, "Gender")
        number = self._resolve_number(gender, morph)
        new_morph = {"Case": ["Nom"], "Gender": [gender], "Number": [number]}
        result = self.add_definite_article_to_token(lemma, pos, new_morph)
        return result

    def _resolve_number(self, gender, morph):
        # Если поле Gender не пустое, значит форма ед. ч. для слова существует и для поиска артикля именно для леммы
        # нужно передавать number='Sing'.
        # Если же поле Gender - пустое, значит форма ед. ч. для слова не существует, и слово употребляется только во
        # мн. ч. В этом случае передаём тот Number, кот. пришёл от spaCy.
        if gender:
            number = 'Sing'
        else:
            number = self.morphologyParser.parse(morph, "Number")
        return number

    def add_definite_article_to_token(self, token: str, pos: str, morph):
        # Чтобы не потерять token в перипетиях алгоритма, сразу записываем его в result и в худшем случае его же
        # и вернём в качестве результата.
        result = token
        definite_article = ''
        error_msg = ''

        # Только для немецкого языка: если token начинается с маленькой буквы, то делаем первую букву заглавной, т. к.
        # немецкие существительные должны начинаться с большой буквы.
        if AppContext.is_language_german(self.lang_code) and token[0].islower():
            token = token.capitalize()

        # Парсим морфологию, напр.:
        # - для сущ. в ед.ч.: Case=Nom|Gender=Neut|Number=Sing
        # - для сущ. во мн.ч.: Case=Nom|Number=Plur (для Plur-сущ. морфология в SpaCy обычно не указывается)
        case = self.morphologyParser.parse(morph, "Case")
        gender = self.morphologyParser.parse(morph, "Gender")
        number = self.morphologyParser.parse(morph, "Number")

        # Если слово в принципе имеет форму ед. ч., значит поле Gender не пустое.
        if gender:
            try:
                definite_article = self.definite_articles_dict[gender][number][case]
            except KeyError:
                result = f"Can't find appropriate definite article for word '{token}' with morph = '{morph}'"
        # Если же поле Gender - пустое, значит форма ед. ч. для слова не существует, и слово употребляется только во
        # мн. ч. Пробуем найти соответствующий артикль используя только number и case.
        else:
            for gender, number_case_dict in self.definite_articles_dict.items():
                if number in number_case_dict and case in number_case_dict[number]:
                    definite_article = number_case_dict[number][case]
                    break

        # if case and number:
        #     if number == 'Sing':
        #         # Определяем ключ для вложенного словаря
        #         number_gender_key = f"{number}_{gender}"
        #         definite_article = DefiniteArticles.de_definite_articles_dict.get(case).get(number_gender_key)
        #     elif number == 'Plur':  # для сущ. во мн.ч. spaCy, скорей всего, не укажет поле 'Gender' в морфологии
        #         definite_article = DefiniteArticles.de_definite_articles_dict.get(case).get('Plur')
        #     else:
        #         result = f"Can't find appropriate definite article for word '{token}' with number = '{number}'"

        if definite_article:
            result = f'{definite_article} {token}'

        return result

    def starts_with_definite_article(self, token):
        starts_with_definite_article_regex = self._get_starts_with_definite_article_regex()
        result = bool(re.search(starts_with_definite_article_regex, token))
        return result

    def not_starts_with_definite_article(self, token):
        result = not self.starts_with_definite_article(token)
        return result

    # Удаляет определённый артикль перед словом
    def strip_definite_article(self, articled_noun):
        starts_with_definite_article_regex = self._get_starts_with_definite_article_regex()
        bare_noun = re.sub(f'{starts_with_definite_article_regex}', '', articled_noun)
        return bare_noun

    def _get_starts_with_definite_article_regex(self):
        article_forms_set = self._get_all_article_forms()

        # Piped-артикли нужно обязательно обернуть в non-capturing group, иначе пайпы будут работать неправильно в том
        # регулярном выражении, в которое будет встроено данное регулярное выражение: пайпы разобьют его на отдельные
        # части и всё будет работать неправильно.
        piped_definite_articles = f'(?:{PIPE.join(article_forms_set)})'

        # Формула регулярного выражения для захвата определённого артикля:
        # - возможный пробел(ы) перед артиклем из-за погрешностей копирования/вставки слова в ячейку Excel
        # - возможная открывающая круглая скобка (для немецких артиклей перед географическими названиями, фамилиями и т. д.)
        # - piped последовательность определённых артиклей
        # - возможная закрывающая круглая скобка
        # - один или более пробел (между артиклем и словом)
        starts_with_definite_article_regex = fr'^\s*\(?{piped_definite_articles}\)?\s+'
        return starts_with_definite_article_regex

    def _get_all_article_forms(self):
        article_forms_set = {
            article
            for gender in self.definite_articles_dict.values()
            for number in gender.values()
            for article in number.values()
        }
        # print(article_forms_set)
        return article_forms_set
