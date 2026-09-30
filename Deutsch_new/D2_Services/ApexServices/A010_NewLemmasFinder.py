import re
from collections import Counter

import AppContext
from CharConstants import SPACE
from MorphDictService import MorphDictService
from OdtFilesService import OdtFilesService
from View_enums import CurrentLanguageComboBoxEnum


# осенью 2024 - зимой 2025 обрабатывал материалы уровня A1 из Гёте-методички следующими версиями библиотек:
# spaCy: 3.7.5
# немецкий язык - de_dep_news_trf: 3.7.2 (spaCy >=3.7.0,<3.8.0)
# древнегреческий язык - grc_odycy_joint_trf: 0.7.0 (spaCy >=3.7.4,<3.8.0)

# Вывод: для работы обоих _trf-библиотек (de_dep_news_trf и grc_odycy_joint_trf) нужна версия spaCy < 3.8.0, которую
# можно установить следующей командой pip install "spacy<3.8.0", а лучше прописать все пакеты в файле requirements.txt и
# устанавливать их все одновременно с учётом совместимости версий пакетов (и версий их зависимостей) между собой.
# "spacy<3.8.0" - это spaCy 3.7.5 в моём случае.


class A010_NewLemmasFinder:
    def __init__(self, morphDictService: MorphDictService, lemmaResolver):
        self.morphDictService = morphDictService
        self.lemmaResolver = lemmaResolver

        # Каждый раз переинициализируем данный сервис в методе-обработчике нажатия на кнопку "Process".
        # Нужен именно как поле класса (а не просто локальная переменная), т. к. используется в нескольких методах
        # данного класса.
        # self.odtFilesService = None

        # Глобальный частотный словарь
        # self.results_freq_dict = None

    # Работа с флагом "output_format_as_freq_dict" доступна только при вызове данного метода из другого кода,
    # к UI данный флаг никак не привязан, чтобы не перегружать UI лишними компонентами и логикой их обработки для
    # такого довольно редкого сценария как составление частотного словаря.
    def find_new_lemmas(self, input_text,
                        morph_dict_policy_read_from_last_file=True,
                        morph_dict_policy_generate_on_the_fly=False,
                        line_by_line_mode=True,
                        include_sentences_with_new_lemmas_in_the_output=True,
                        include_even_sentences_without_new_lemmas_in_the_output=False,
                        whole_text_mode=False,  # по умолчанию метод воспринимает входной текст как единое целое
                        output_format_as_freq_dict=False):

        if line_by_line_mode and whole_text_mode:
            raise ValueError("'line_by_line_mode' and 'whole_text_mode' can't be True simultaneously!")
        elif not line_by_line_mode and not whole_text_mode:
            raise ValueError("Either 'line_by_line_mode' or 'whole_text_mode' should be True!")

        # Глобальный частотный словарь. Инициализируется спец. объектом Counter из модуля collections для большего
        # удобства работы с ним: Counter автоматически создаёт запись для нового ключа с нулевым значением, а затем
        # увеличивает его на 1. Кроме этого, Counter хранит порядок вставки ключей в словарь!
        # Обнуляем глобальный словарь при каждом входе в метод
        self.results_freq_dict = Counter()

        # Каждый раз переинициализируем данный сервис, потому что в конструкторе он только единожды (при инициализации
        # объекта) вычитывает содержимое [Vocab]-файлов. А поскольку это содержимое может меняться в процессе работы
        # над материалом, нужно чтобы при каждом нажатии на кнопку "Process" актуальные данные подтягивались из
        # [Vocab]-файлов без перезапуска программы.
        self.odtFilesService = OdtFilesService()

        # Make sure odtFilesService_factory is callable
        # if callable(self.odtFilesService_factory):
        #     self.odtFilesService = self.odtFilesService_factory()
        # else:
        #     # If it's already an instance, just use it
        #     self.odtFilesService = self.odtFilesService_factory

        input_text = input_text.strip()  # Убирает по краям строки пробел и следующие символы [\t\n\r\v\f]

        # UI lookup 'Morph_dict policy'
        if morph_dict_policy_read_from_last_file:
            morph_dict = self.morphDictService.read_morph_dict_from_last_file()
        elif morph_dict_policy_generate_on_the_fly:
            # Если включена радио-кнопка "Whole text mode", заменяем в исходном тексте '\n' на пробелы, чтобы spaCy
            # воспринял входной текст как единое целое и обработал его за один раз.
            if whole_text_mode:
                input_text = re.sub(r'\n+', SPACE, input_text)
            morph_dict = self.morphDictService.generate_morph_dict_on_the_fly(input_text)
        else:
            raise ValueError("Either 'morph_dict_policy_read_from_last_file' or 'morph_dict_policy_generate_on_the_fly'"
                             " should be True!")

        # 'text_unit' - это или отдельное предложение, или весь текст целиком в зависимости от состояния флагов
        for text_unit, tuples in morph_dict.items():
            # В результате работы метода глобальный словарь self.results_freq_dict заполняется леммами новых слов.
            # Метод возвращает True, если в предложении были обнаружены новые леммы и только в этом случае
            # само предложение можно добавлять в результирующий набор (при разрешении соответствующего флага).
            is_at_least_one_new_word = self._process_tuples_of_single_text_unit(tuples)
            if line_by_line_mode:  # если на UI выставлена соответствующая радио-кнопка
                # Здесь добавляем в частотный словарь и само предложение (если на это есть разрешение соотв. флага
                # на UI), причём на всякий случай считаем частоту его появления. В большинстве случаев это должна
                # быть 1.
                if include_sentences_with_new_lemmas_in_the_output and is_at_least_one_new_word:
                    # Такая лаконичная запись возможна благодаря тому, что глобальный частотный словарь
                    # self.results_freq_dict инициализирован объектом Counter из модуля collections.
                    self.results_freq_dict[text_unit] += 1
                # Если установлен флаг, разрешающий добавлять даже предложения, не содержащие новых лемм, добавляем
                # эти предложения в результирующий набор. А такой флаг автоматически сбрасывается при выключении
                # флага "include_sentences_with_new_lemmas_in_the_output" (эта логика реализована в контроллере).
                elif include_even_sentences_without_new_lemmas_in_the_output:
                    self.results_freq_dict[text_unit] += 1

            # для переключателя 'whole_text_mode' никаких доп. действий не требуется: частотный словарь уже и так
            # заполнен леммами новых слов, а весь входной текст по определению и так не нужно включать в результаты.

        # Формируем вывод результатов работы на экран
        if output_format_as_freq_dict:
            output = '\n'.join([f'{lemma}: {counter}' for lemma, counter in self.results_freq_dict.items()])
        else:  # ветка для формирования "обычного" формата вывода
            output = '\n'.join(self.results_freq_dict.keys())  # Counter хранит порядок вставки ключей в словарь!

        # # Обычное слово выводим на экран с одним newline-символом
        # if line not in input_sentences:
        #     output += f'{line}\n'
        # # Предложение выводим на экран с двумя newline-символами после него (т. е. визуально с одной пустой
        # # строкой после него)
        # else:
        #     output += f'{line}\n\n'

        # Удаляем лишние newline-символы по краям строки
        output = output.strip()  # Убирает по краям строки пробел и следующие символы [\t\n\r\v\f]

        if not output:
            output = "No new lemmas!"

        return output

    # В названии метода специально использована абстрактная фраза "single_text_unit", т. к. в зависимости от значений
    # флагов вызывающего метода find_new_lemmas() под "text_unit" может пониматься как отдельное предложение,
    # так и весь текст целиком.
    def _process_tuples_of_single_text_unit(self, tuples):
        is_at_least_one_new_word = False
        for token, lemma, pos, morph in tuples:

            # в самом худшем случае current_word - это lemma от spaCy, которая не претерпела никаких трансформаций
            current_word = self.lemmaResolver.get_single_lemma(token, lemma, pos, morph)

            # current_word будет None, если token будет обнаружен среди списка ignored_tokens
            if current_word is None:
                continue

            # Только если слово отсутствует в вокабуляре, имеет смысл работать с ним дальше.
            if self.odtFilesService.is_word_absent_from_vocabulary(current_word):
                # Считаем слово новым только в том случае, если его нет ни в вокабуляре, ни в частотном словаре.
                # Если же в вокабуляре его нет, а в частотный словарь оно уже попало из предыдущих предложений текущей
                # сессии, но оно уже считается как бы выученным и не влияет на включение флага.
                if current_word not in self.results_freq_dict:  # не объединять через AND с предыдущим условием, это будет логическая ошибка!
                    is_at_least_one_new_word = True

                # Такая лаконичная запись возможна благодаря тому, что глобальный частотный словарь
                # self.results_freq_dict инициализирован объектом Counter из модуля collections.
                # Counter автоматически создаёт запись для нового ключа с нулевым значением, а затем увеличивает его
                # на 1. Кроме этого, Counter хранит порядок вставки ключей в словарь!
                # Основная задача метода - заполнять глобальный частотный словарь self.results_freq_dict
                self.results_freq_dict[current_word] += 1

        return is_at_least_one_new_word


#############################################################

# resources_dir = r'E:\Languages\[Git repo] MultilingualTextProcessor\resources'
# input_str = FileContentsReader.get_file_text(fr'{resources_dir}\German\all_text.txt')

# input_str = "1Das ist ein Test-Text mit deutschen Wörtern wie Fußgängerübergang und E-Mail2."
# input_str = """
# Ab morgen muss ich arbeiten.
# Ich bin oft im Büro, aber nur für wenige Stunden.
# Wir fahren um zwölf Uhr ab.
# """

# input_str = 'Die Eltern bringen ihre Kinder zur Schule.'
# input_str = 'Alles Gute!'
# input_str = 'Hast du alles?'
# input_str = 'Hast du?'
# input_str = 'Er hat Zeit, also muss er uns helfen.'
# input_str = 'Willst du diese Jacke?'

input_str = """
Auf dem Formular müssen Sie an mehreren Stellen etwas ankreuzen.
Mach bitte das Licht an!
Ein Pfund Äpfel bitte.
Guten Appetit!
Wie heißt das auf Deutsch?
Zieh die Schuhe aus, bitte!
"""

input_str = """
Auf dem Formular müssen Sie an mehreren Stellen etwas ankreuzen.
"""

input_str = 'Viele meiner Verwandten, z.B. meine beiden Brüder, arbeiten auch hier.'
input_str = 'Nimm noch ein paar Brote für die Fahrt mit.'
input_str = 'Deine Tasche kannst du dorthin stellen.'
input_str = 'Kannst du mich zum Flughafen bringen?'

input_str = """
Wir treffen uns in Halle B.
"""

input_str = """
Herzlichen Glückwunsch zum Geburtstag!
Herzlichen Glückwunsch zum Geburtstag!
"""

input_str = 'VS.'
input_str = 'Hallo Inge! Wie geht’s?'
input_str = 'Sind die Möbel neu?'
input_str = 'Familie Kurz bekommt ein Baby.'
input_str = 'Sie wohnt am Anfang der Straße.'

# sie в значении ОНА и ОНИ
input_str = """
1. Sie ist sehr freundlich und hilfsbereit.
2. Gestern haben sie einen neuen Hund adoptiert.
"""

input_str = 'Σήμερα ο μπαμπάς μου παντρεύεται και θέλει να είναι όλα τέλεια.'

input_str = """
Ευτυχισμένοι Μαζί
Επεισόδιο 1
(ΓΙΑΝΝΑΚΗΣ) Σήμερα ο μπαμπάς μου παντρεύεται και θέλει να είναι όλα τέλεια.
Γι’ αυτό είναι ταραγμένος και σπαστικός.
Δεν είναι η πρώτη φορά παντρεύεται, αλλά είναι η πρώτη που θα το δω γιατί την προηγούμενη φορά παντρεύτηκε τη μητέρα μου.
Που δεν είναι ώρα να θυμηθώ τώρα.
Γιατί όποτε τη θυμάμαι κλαίω και τ’ αδέρφια μου με κοροϊδεύουν.
"""

if __name__ == '__main__':
    from BusinessObjectFactory import BusinessObjectFactory

    # language = CurrentLanguageComboBoxEnum.GERMAN.value
    language = CurrentLanguageComboBoxEnum.MODERN_GREEK.value
    # language = CurrentLanguageComboBoxEnum.ANCIENT_GREEK.value
    AppContext.switch_language(language)  # выбор языка должен происходить в самую первую очередь, даже ДО импорта
    # BusinessObjectFactory

    # Импорт Container происходит только при запуске модуля как основного (__main__), а не при его импорте в других
    # модулях (например, в Container.py). Это предотвращает циклический импорт на этапе загрузки модуля.
    # Локальный импорт для предотвращения циклического импорта между данным модулем и Container.
    a010_NewLemmasFinder = BusinessObjectFactory.create_a010_NewLemmasFinder()
    res = a010_NewLemmasFinder.find_new_lemmas(input_str,
                                               morph_dict_policy_read_from_last_file=False,
                                               morph_dict_policy_generate_on_the_fly=True,
                                               line_by_line_mode=True,
                                               include_sentences_with_new_lemmas_in_the_output=True,
                                               include_even_sentences_without_new_lemmas_in_the_output=False,
                                               whole_text_mode=False)
    print(res)
