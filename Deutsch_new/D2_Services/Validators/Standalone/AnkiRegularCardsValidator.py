import re
from collections import defaultdict
from typing import Dict, List

import AppContext
from AnkiCardEntity import AnkiCardEntity
from BaseValidator import BaseValidator
from CharConstants import SPACE
from MultilingualAnkiDao import MultilingualAnkiDao
from View_enums import CurrentLanguageComboBoxEnum


class AnkiRegularCardsValidator(BaseValidator):

    # Передаём коллекцию регулярных карточек через конструктор.
    # Данный подход позволит гибче использовать текущий класс, формируя коллекцию регулярных карточек "на лету".
    # Это особенно нужно при валидации таблицы со словами из OO Writer, где коллекция регулярных карточек формируется
    # "на лету".
    def __init__(self, regular_cards):
        super().__init__()
        self.regular_cards = regular_cards

        self.multilingualAnkiDao = MultilingualAnkiDao()

        # self.deuRegExFinder = DeuRegExFinder()

        # self.aggregate_cards_deck_name = '!Deutsch. Агрегаты'
        # self.aggregate_cards = self.germanWordsFromAnkiDao.get_data(self.aggregate_cards_deck_name)
        # self.aggregate_cards = self.multilingualAnkiDao.get_all_aggregate_cards()

    # Validation UC#1. Самый первый шаг в валидациях - это запустить AnkiRunner для замены в карточках всех неправильных
    # последовательностей символов на правильные
    def validate_uc1_anki_runner(self):
        super().validate_uc1_anki_runner_base(self.regular_cards_deck_name)

    # Validation UC#2. Валидировать, что каждая карточка содержит одинаковое количество полос в ключевых полях
    def validate_uc2_main_card_fields_pieces_consistency(self):
        super().validate_uc2_main_card_fields_pieces_consistency_base(self.regular_cards)

    # Вывести на экран регулярные карточки, состоящие из 2-х полос.
    # Дело в том, что для регулярной карточки иметь именно две полосы - это довольно нетипичная ситуация:
    # обычно регулярная карточка состоит или из одной полосы (для простых слов) или из трёх и более полос (для
    # сложных/составных слов). Если регулярная карточка имеет две полосы - это признак того, что её нужно перемещать
    # в агрегированные карточки, а на её месте создавать две отдельных карточки с каждым словом отдельно.
    def validate_uc3_regular_card_should_not_be_two_striped(self):
        two_striped_cards = []
        for regular_card in self.regular_cards:
            if len(regular_card.front) == 2:
                two_striped_cards.append(regular_card)

        if len(two_striped_cards) > 0:
            print(f'\nRegular cards with two stripes:')
            for card in two_striped_cards:
                print(f'{str(card)}')

    # Вычитать все регулярные (однополосные и многополосные) карточки и из содержимого их Front-полей сделать общий
    # список слов. Затем итерироваться по этому списку и искать каждое слово всех карточек. Слово, которое не будет
    # найдено ни там, ни там принадлежит неправильно сделанной карточке.
    # 1) это или многополосная карточка, одно из слов которой не встречается среди однополосных карточек;
    # 2) это или многополосная карточка смешанного типа: и содержащая сложное/составное слово, и агрегирующая слова,
    # принадлежащие одному и тому же семантическому полю.
    def validate_uc4_regular_cards_lack_and_excess_consistency(self, should_split_by_space=True):
        lack_results_set, excess_results_set, printable_output = self.find_regular_cards_lack_and_excess_sets(
            should_split_by_space)
        # printable_output = self.find_regular_cards_lack_and_excess_sets(should_split_by_space)
        # self.print_lack_and_excess_consistency_validation_results(lack_results_set, excess_results_set)
        print(printable_output)

    def find_regular_cards_lack_and_excess_sets(self, should_split_by_space=True):
        # lack and excess - недостаток и избыток
        lack_results_set = set()
        excess_results_set = set()

        # Словарь вида "слово -> список карточек, в которых оно встречается"
        # defaultdict полезен тем, что если ключа в словаре нет, он будет автоматически создан с пустым списком,
        # что экономит усилия на кодировании соответствующей логики вручную!
        possible_duplicates_dict: Dict[str, List[AnkiCardEntity]] = defaultdict(list)

        # Формируем сквозной список всех полос из Front-полей всех регулярных карточек
        all_cards_front_field_stripes = []
        for regular_card in self.regular_cards:
            all_cards_front_field_stripes.extend(regular_card.front)

        for front_stripe in all_cards_front_field_stripes:
            if front_stripe not in self.ignored_lines:
                front_stripe_ready_token = AnkiCardEntity.parse_front_stripe(front_stripe)

                # сбрасываем флаг поиска
                is_found = False

                # внутренний цикл по всем регулярным карточкам
                for regular_card in self.regular_cards:
                    if regular_card.is_word_found(front_stripe_ready_token, should_split_by_space):
                        # Флаг отвечающий за поиск НЕДОСТАТКА (LACK) среди карточек. Если получилось выставить в True,
                        # значит НЕДОСТАТКА (LACK) нет
                        is_found = True
                        # не делаем здесь break, чтобы далее накопить информацию о возможном ИЗБЫТКЕ (EXCESS)
                        # среди карточек

                        # Словарь отвечающий за поиск возможного ИЗБЫТКА (EXCESS) среди карточек.
                        # Избыток будет иметь место, когда по одному и тому же ключу будет храниться более одной
                        # сущности в списке.
                        if regular_card not in possible_duplicates_dict[front_stripe_ready_token]:
                            possible_duplicates_dict[front_stripe_ready_token].append(regular_card)

                # Формирование результатов со стороны НЕДОСТАТКА (LACK) слов в деке
                if not is_found:
                    result = f"'{front_stripe_ready_token}' of '{front_stripe}'"
                    lack_results_set.add(result)

                # Формирование результатов со стороны ИЗБЫТКА (EXCESS) слов в деке
                for k, vals in possible_duplicates_dict.items():
                    if len(vals) > 1:
                        result = f'{k}:\n\t' + '\n\t'.join([str(v) for v in vals])
                        excess_results_set.add(result)

        output = ''

        if len(lack_results_set) > 0:
            output += '\nLACK of consistency:\n'
            for result in lack_results_set:
                output += f'\t{result}\n'

        if len(excess_results_set) > 0:
            output += '\nEXCESS of consistency:\n'
            for result in excess_results_set:
                output += f'{result}\n'

        return lack_results_set, excess_results_set, output

    # Валидируем все полосы многополосных карточек.
    # 1. Не последняя полоса многополосных карточек должна встречаться:
    # 1) или среди однополосных карточек
    # 2) или среди последних полос других многополосных карточек

    # TODO Последняя полоса многополосных карточек не должна встречаться:
    #  1) среди однополосных карточек
    #  2) среди последних полос других многополосных карточек!
    #  Проверка этого условия помогла бы обнаружить некоторые из тех карточек, которые я вывел с помощью функции
    #  show_two_striped_regular_cards
    #  Данный метод дополняет 'lack & excess' валидацию, но не в коем случае не дублирует её и не является лишним.
    #  !!! МНЕ КАЖЕТСЯ, ЧТО ДАННЫЙ МЕТОД ВСЁ ЖЕ ДУБЛИРУЕТ ЛОГИКУ 'lack & excess'
    # def validate_last_stripe_of_regular_multi_striped_card_is_not_found_in_single_striped_card(self):
    #     results_dict: Dict[str, List[AnkiCardEntity]] = defaultdict(list)
    #
    #     for regular_card in self.regular_cards:
    #         if regular_card.is_card_multi_striped():
    #             last_stripe = regular_card.front[-1]
    #             last_stripe_ready_token = AnkiCardEntity.parse_front_stripe(last_stripe)
    #
    #             # внутренний цикл с поиском по однополосным карточкам
    #             # TODO доделать проверку среди последних полос других многополосных карточек
    #             for other_regular_card in self.regular_cards:
    #                 if other_regular_card.is_word_found_in_a_single_striped_card(last_stripe_ready_token):
    #                     if other_regular_card not in results_dict[last_stripe_ready_token]:
    #                         results_dict[last_stripe_ready_token].append(other_regular_card)
    #
    #     for k, vals in results_dict.items():
    #         result = f'{k}:\n\t' + '\n\t'.join([str(v) for v in vals])
    #         print(result)

    # Среди регулярных карточек найти все однополосные, у которых более 1 строки в поле Front.
    # Убедиться, что в поле Front этих карточек нет двух и более слов-синонимов, как было раньше (например,
    # die Apfelsine\ndie Orange)
    def show_one_striped_regular_cards_with_more_than_one_line(self):
        for regular_card in self.regular_cards:
            if regular_card.is_card_single_striped() and regular_card.front[0].count('\n') >= 1:
                # Игнорируем карточки, у которых второй строкой идёт hint к слову
                is_second_line_not_hint = not regular_card.front[0].split('\n')[1].startswith('(hint:')
                if is_second_line_not_hint:
                    print(f'{regular_card.front}')

    # Показать карточки, у которых 4 и более полос для того, чтобы визуально убедиться, что среди них нет агрегатов.
    # Наиболее типичные регулярные карточки - это одно- и трёхполосные карточки.
    def show_four_plus_striped_regular_cards(self):
        for regular_card in self.regular_cards:
            if len(regular_card.front) >= 4:
                print(f'{regular_card.front}')

    # Следит за тем, чтобы одни и те же слова (полосы) в разных карточках имели одинаковые транскрипцию и перевод.
    # Запускать данный метод сначала только для регулярных карточек, а затем в дек регулярных карточек в качестве
    # сабдека временно перетаскивать дек с агрегатами и опять запускать этот метод. Таким образом будет достигнуто
    # единообразие в транскрипциях и переводах среди регулярных и агрегированных карточек.
    # Данный метод ещё вызывается в A40_OdtTableConsistencyChecker.check_consistency(...)
    def find_inconsistent_translations_of_the_same_word(self, including_aggregates=False):
        stripes_dict = {}
        inconsistent_words = []

        if including_aggregates:
            cards_to_check = self.regular_cards + self.multilingualAnkiDao.get_all_aggregate_cards()
        else:
            cards_to_check = self.regular_cards

        for card in cards_to_check:
            for i in range(0, len(card.front)):
                front_stripe = card.front[i]
                stripe_str = card.to_str_by_stripe_index_front_transcription_back(i)
                if front_stripe not in stripes_dict:
                    stripes_dict[front_stripe] = stripe_str
                else:
                    unequal_fields = []
                    other_stripe_str = stripes_dict[front_stripe]
                    if stripe_str != other_stripe_str:
                        front, transcription, back = stripe_str.split('|')
                        other_front, other_transcription, other_back = other_stripe_str.split('|')
                        # Нет смысла сравнивать поля Front, в данной точке программе и так понятно, что они не равны
                        # if front != other_front:
                        #     unequal_fields.append('Front')
                        if transcription != other_transcription:
                            unequal_fields.append('Transcription')
                        if back != other_back:
                            unequal_fields.append('Back')

                        # print(card.front)

                        result = f'{stripe_str} != {other_stripe_str} --> ({", ".join(unequal_fields)})'
                        if result not in inconsistent_words:
                            inconsistent_words.append(result)

        output = '\n\n'.join(inconsistent_words)
        return output

    # Метод отображает карточки, в которых 1-я строка последней полосы заканчивается на закрывающую круглую скобку,
    # что может слегка затруднять или нарушать поиск таких карточек, особенно в UC#2.
    # Распечатанный список слов нуждается в визуальном осмотре и нужно убедиться в том, что все закрывающие круглые
    # скобки стоят в конце аббревиатур слов, а не например грамматических подсказок: (sg.), (pl.), (англ.), (лат.), etc.
    # Логика учёта такого случая при поиске карточки находится в AnkiCardEntity.is_word_found(...)
    # TODO: теперь в проверке на excess нужно учитывать, что аббревиатура слова может встречаться как виде отдельной
    #  карточки, так и в скобках после полной версии слова.
    def show_last_stripes_ending_with_closing_parenthesis(self):
        for card in self.regular_cards:
            last_stripe = card.front[-1]
            last_stripe_ready_token = AnkiCardEntity.parse_front_stripe(last_stripe)
            if last_stripe_ready_token.endswith(')'):
                # 1. Печатаем карточку
                print(f'{card.front}')

                # 2. Печатаем транскрипцию последней полосы, если она не соответствует формату (аббревиатура должна быть
                # заключена в отдельные круглые скобки, а внутри них - в отдельные квадратные скобки)
                last_stripe_transcription = card.transcription[-1]
                # В результирующем списке найденных совпадений возьмём последний элемент и уберём у него по краям
                # круглые скобки.
                pars_contents = re.findall(r'\(.*?\)', last_stripe_transcription)[-1][1:-1]
                is_pars_contents_square_bracketed = pars_contents.startswith('[') and pars_contents.endswith(']')
                if not is_pars_contents_square_bracketed:
                    print(
                        f"Last stripe transcription par contents should be square bracketed: {last_stripe_transcription}\n")

    # Двух пробелов, кроме редчайших случаев в роде 'der Mount Everest', в последней полосе быть не должно и если
    # такие полосы есть, может им место среди ВЫРАЖЕНИЙ, а не среди регулярных карточек???
    def show_last_stripes_with_two_or_more_spaces(self):
        for card in self.regular_cards:
            last_stripe = card.front[-1]
            last_stripe_ready_token = AnkiCardEntity.parse_front_stripe(last_stripe)

            exclusions = ['Frankfurt am Main', 'zu Mittag essen', 'zu Abend essen',
                          'das Partizip II', 'das Partizip I', 'die Pommes frites', 'der Mount Everest',
                          'der Starnberger See']

            is_not_in_exclusions = last_stripe_ready_token not in exclusions
            not_ends_with_closing_par = not last_stripe_ready_token.endswith(')')

            # Последняя полоса может заканчиваться аббревиатурой слова (технически - закрывающей круглой скобкой) и
            # скорей всего такая полоса будет иметь 2 и более пробела. Данный случай уже разбирался выше, поэтому эти
            # кейсы мы здесь игнорируем и ищем полосы с 2+ пробелами, НЕ заканчивающимися на ')'.
            if is_not_in_exclusions and not_ends_with_closing_par and last_stripe_ready_token.count(SPACE) >= 2:
                print(f'{card.front}')


    # Найти в полях Front и Back последние строки полос, начинающихся с двойного слеша для того, чтобы вынести эти
    # полосы-комментарии в специально предназначенные для этого поля Front_comment и Back_comment.
    def show_last_line_starting_with_double_slash(self):
        cards_to_check = self.regular_cards + self.multilingualAnkiDao.get_all_aggregate_cards()
        for card in cards_to_check:
            for i in range(0, len(card.back)):
                front_stripe = card.front[i]
                front_lines = front_stripe.split('\n')
                first_line = front_lines[0]
                last_line = front_lines[-1]
                if last_line.startswith('//') and first_line not in ['εφ-', 'προσ-', 'εμ-', 'ξε-', 'δισ-', 'οὐ', 'εξ-', 'εγ-', 'ελ-']:
                    print(f'{front_stripe}\n')

                back_stripe = card.back[i]
                last_line = back_stripe.split('\n')[-1]
                if last_line.startswith('//'):
                    print(f'{back_stripe}\n')


###################################################################

if __name__ == '__main__':
    # language = CurrentLanguageComboBoxEnum.GERMAN.value
    language = CurrentLanguageComboBoxEnum.MODERN_GREEK.value
    # language = CurrentLanguageComboBoxEnum.ANCIENT_GREEK.value
    AppContext.switch_language(language)  # выбор языка должен происходить в самую первую очередь, даже ДО импорта

    multilingualAnkiDao = MultilingualAnkiDao()
    regular_cards = multilingualAnkiDao.get_regular_cards()
    ankiRegularCardsValidator = AnkiRegularCardsValidator(regular_cards)

    ankiRegularCardsValidator.validate_uc2_main_card_fields_pieces_consistency()
    ankiRegularCardsValidator.validate_uc3_regular_card_should_not_be_two_striped()

    # UC #4
    # Запускать поочерёдно с двумя значениями флага: True и False
    # - более придирчивый поиск (с разбиением слова по пробелам: (der) Alex vs. Alex) (часто не нужен) - значение флага True
    # - сравнение слов "как есть" (без разбиения на пробелы) - значение флага False
    ankiRegularCardsValidator.validate_uc4_regular_cards_lack_and_excess_consistency(should_split_by_space=False)

    ankiRegularCardsValidator.show_one_striped_regular_cards_with_more_than_one_line()
    print()
    ankiRegularCardsValidator.show_four_plus_striped_regular_cards()
    print()
    res = ankiRegularCardsValidator.find_inconsistent_translations_of_the_same_word(including_aggregates=True)
    print(res)

    ankiRegularCardsValidator.show_last_stripes_ending_with_closing_parenthesis()

    ankiRegularCardsValidator.show_last_stripes_with_two_or_more_spaces()

    ankiRegularCardsValidator.show_last_line_starting_with_double_slash()
