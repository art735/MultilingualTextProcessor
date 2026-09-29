import re
from enum import Enum

from CharConstants import SPACE
from DeuRegExFinder import DeuRegExFinder


class AnkiField(Enum):
    Front = 'Front'
    Front_comment = 'Front_comment'
    Taggy = 'Taggy'
    SSML = 'SSML'
    Audio1 = 'Audio1'
    Audio2 = 'Audio2'
    Image = 'Image'
    Transcription = 'Transcription'
    Grammar = 'Grammar'
    Back = 'Back'
    Back_comment = 'Back_comment'


# Потенциально многострочный текст каждого поля Анки-карточки мы храним в Excel в виде одной строки.
# Позже, при обратной конвертации в OO Writer этой единой строки в оригинальный многострочный вид, данные разделители
# будут заменяться на соответствующее кол-во символов '\n':
# 1) сначала пять крышечек заменяются на '\n\n',
# 2) а затем три крышечки заменяются на '\n'.
# Это должно быть прописано в макросе OO Writer-а и выполняться автоматически.
SINGLE_NEWLINE_SUBSTITUTE = '^^^'
DOUBLE_NEWLINE_SUBSTITUTE = '^^^^^'
# Если в оригинальном тексте карточки встречается пайп (например, часто при указании кол-ва прожитых лет в биографии
# человека), его нужно временно заменить на техническую последовательность символов
PIPE_SUBSTITUTE = 'PIPE_PIPE_PIPE'


class AnkiCardEntity:
    def __init__(self, front=[], front_comment=[], taggy=[], ssml=[], transcription=[], grammar=[], back=[],
                 back_comment=[]):
        # Хорошо бы ввести чёткое разделение терминов "полоса" и "строка".
        # Полосы в Анки-карточке отделяются друг от друга последовательностью <br><br>
        # Строки в Анки-карточке отделяются друг от друга одиночным разрывом <br>
        # Однополосная карточка может, тем не менее, состоять из нескольких строк, например:
        # gemein
        # (hint: 1) ни, п; 2) на, б; 3) о)
        # Это всё одна полоса, но две строки; в верхней строке находится немецкое слово, а в нижней - hint к нему
        # Поле self.front (впрочем как и остальные поля) хранит список полос, а не список строк!
        self.front: list = self._init_field(front)
        self.front_comment: list = self._init_field(front_comment)
        self.taggy: list = self._init_field(taggy)
        self.ssml: list = self._init_field(ssml)
        self.transcription: list = self._init_field(transcription)
        self.grammar: list = self._init_field(grammar)
        self.back: list = self._init_field(back)
        self.back_comment: list = self._init_field(back_comment)

        # Эти списки полей нужны для различных версий методов под общим названием toString()
        self.all_fields_list = [self.front, self.front_comment, self.taggy, self.ssml, self.transcription,
                                self.grammar, self.back, self.back_comment]

        self.front_transcription_back_with_comments_fields_list = [self.front, self.front_comment,
                                                                   self.transcription, self.back,
                                                                   self.back_comment]

        self.front_transcription_back_fields_list = [self.front, self.transcription, self.back]
        self.front_back_fields_list = [self.front, self.back]

    def _init_field(self, input_value):
        if isinstance(input_value, list):
            result = input_value
        elif isinstance(input_value, str):
            result = [input_value]
        else:
            raise ValueError(f"All AnkiCardEntity ctor parameters must be lists, but '{input_value}' is neither a list"
                             f" nor a string (which is automatically wrapped into a list).")
        return result

    # Проверяет тот факт, что ключевые поля содержат одинаковое кол-во элементов.
    # Если, например, в поле Front имеется три слова, то и в поле transcription должно быть три транскрипции,
    # и в поле back должно быть три перевода.
    def validate_consistency(self):

        # Для немецкого языка проверяем как положено, т. е. с учётом поля Transcription
        if AppContext.is_language_german():
            is_consistent = len(self.front) == len(self.transcription) == len(self.back)
        # Для остальных языков (кроме немецкого) временно поле Transcription игнорируем, т. к. его не так легко
        # заполнить и сделать консистентным между регулярными и агрегированными карточками. Когда эта работа будет
        # проделана можно будет убрать все эти проверки.
        else:
            if self.transcription:
                is_consistent = len(self.front) == len(self.transcription) == len(self.back)
            else:
                is_consistent = len(self.front) == len(self.back)

        if not is_consistent:
            print(f"Inconsistent card: {self.front}\n")
            # print("############")

    def validate_german_word_can_be_reached_for_lookup(self):
        deuRegExFinder = DeuRegExFinder()
        # Каждое поле карточки - это список находящихся в нём слов
        for front_field_word in self.front:
            if '\n' in front_field_word:
                # print(f'{front_field_word}\n############')
                word_lines = front_field_word.split('\n')

                german_word = word_lines[0]
                # if ' ' in german_word:
                #     german_word_pieces = german_word.split(' ')
                #     for german_word_piece in german_word_pieces:
                #         # артикли перед словом могут быть и в скобках, поэтому проверяем не на равенство, а на вхождение
                #         if ['der', 'die', 'das'] not in german_word_piece:

                # Убираем в слове пробелы, чтобы не заморачиваться с удалением артиклей.
                # В данном случае главное понять если ли в строке посторонние символы (скобки, тире, точки и пр.)
                # TODO переделать здесь как в методе validate_elements_of_aggregate_cards_can_be_found_among_single_striped_cards
                german_word_itself_without_spaces = german_word.replace(' ', '')
                if not deuRegExFinder.is_token_a_canonical_word(german_word_itself_without_spaces):
                    print(f"Validation message: the first line of the multi-line word should contain symbols,"
                          f" that can be qualified as a German word:\n{front_field_word}\n")

    # TODO валидация того, что в поле Front составных слов присутствуют слова, на которые есть отдельные однострочные карточки
    # TODO после этой валидации можно рассчитывать на то, что если поиск нашёл слво и в однострочной, и в многострочной карточке,
    # TODO можно и даже нужно выбирать именно однострочную карточку, как содержащую, вероятно, наиболее полный перевод слова
    # def validate_complex_words_parts_are_existent_as_separate_cards(self):
    #     if len(self.front) > 1:
    #         for front_word in self.front:

    def is_word_found_in_a_single_striped_card(self, word_to_search, should_split_by_space=True):
        result = False
        if self.is_card_single_striped():
            # front_stripe = self.front[0]
            result = self.is_word_found(word_to_search, should_split_by_space)
        return result

    def is_card_single_striped(self):
        return len(self.front) == 1

    def is_word_found_in_the_last_stripe_of_a_regular_multi_striped_card(self, word_to_search,
                                                                         should_split_by_space=True):
        result = False
        if self.is_card_multi_striped():
            result = self.is_word_found(word_to_search, should_split_by_space)
        return result

    # TODO что имеется в виду "слово найдено в мультиполосной карточке"???
    #  Поиск слова должен идти среди всех полос или только в последней полосе?
    #  Для агрегированных карточек возможно нужно среди всех полос искать (если им нужен такой кейс),
    #  а для регулярных - возможно интересен только поиск только в последней полосе?
    # def is_word_found_in_a_multi_striped_card(self, word_to_search, should_split_by_space=True):
    #     result = False
    #     if self.is_card_multi_striped():
    #         result = self.is_word_found(word_to_search, should_split_by_space)
    #     return result

    def is_card_multi_striped(self):
        return len(self.front) > 1

    # This is a core algorithm of searching words in cards
    # word_to_search - слово, которое требуется найти в карточке
    # front_word:
    # - в однополосной карточке - это верхняя (часто единственная) строка со словом (над hint-ами, комментариями
    # и прочей информацией). Однополосная карточка может быть как однострочной, так и многострочной.
    # Главное чтобы в ней не было <br><br>, который логически отделяет одно слово от другого;
    # - в многополосной карточке - это верхняя (часто единственная) строка последней полосы.
    def is_word_found(self, word_to_search, should_split_by_space=True):
        is_word_found = False

        # TODO: раскоментировать в production-е, для целей отладки лучше, чтобы при пустом self.front код падал в строке
        #  "last_stripe = self.front[-1]"
        #  Такой случай маловероятен в настоящей Анки-карточке, но часто встречается в фейковых Анки-сущностях, которые
        #  получены путём конвертации .odt-таблицы для удобства поиска и валидации. Odt-таблица часто содержит
        #  пустые строки и как раз в этом случае len(self.front) == 0
        if len(self.front) == 0:
            return False

        # В качестве полосы для поиска всегда берём последнюю полосу:
        # - для однополосной карточки - это её единственная полоса и здесь без разницы как её называть: "первая" или
        # "последняя"
        # - для многополосной регулярной (а не агрегированной) карточки - это полоса, представляющая реальный
        # интерес для поиска во многих сценариях
        last_stripe = self.front[-1]

        # Не важно является last_stripe одно- или многострочной полосой.
        # Работаем только с первой (самой верхней) строкой полосы, т. к. остальные (нижние) строки - это hint,
        # комментарий и прочее.
        first_line_of_last_stripe = self.parse_front_stripe(last_stripe,
                                                            True)  # пока сделал 2-й параметр True

        # Шаг №1. Если искомое слово полностью совпадает с верхней (часто единственной) строкой полосы, значит слово
        # найдено!
        # TODO Может сделать сравнение регистронезависимым: word_to_search.lower() == first_line_of_last_stripe.lower()
        if word_to_search == first_line_of_last_stripe:
            is_word_found = True

        if not is_word_found and should_split_by_space:
            # Шаг №2. Если на предыдущем шаге ничего не нашли, значит делим строку на части и ищем совпадение
            # среди них:
            # - при поиске слова Alex должна быть найдена, среди прочих, и карточка «(der) Alex»
            # - при поиске глагола bedanken должна быть найдена, среди прочих, и карточка «bedanken (sich) (bei + D)»
            if word_to_search in first_line_of_last_stripe.split():  # разбили по пробелу:
                is_word_found = True

        # Если первая строка последней полосы заканчивается на ')', то высока вероятность того, что в круглых скобках
        # находится аббревиатура этого слова, которая тоже должна принимать участие в поиске карточки по лемме (особенно
        # в UC#2). Поэтому парсим первую строку последней полосы, чтобы сравнить искомую лемму отдельно с полной версией
        # слова и отдельно с аббревиатурой и возможно сказать, что искомая карточка найдена!
        # Примеры таких случаев:
        # die Bundesrepublik Deutschland (BRD)
        # die Untergrundbahn (U-Bahn)
        # die Aktiengesellschaft (AG)
        if not is_word_found and first_line_of_last_stripe.endswith(')'):
            pieces = first_line_of_last_stripe.split()
            first_piece = pieces[0]
            last_piece = pieces[-1][1:-1]  # убираем круглые скобки вокруг последнего слова

            # 1. Формируем первое слово
            first_word = f'{SPACE.join(pieces[:-1])}'
            # 2. Формируем второе слово
            if first_piece in ['der', 'die', 'das']:
                second_word = f'{first_piece} {last_piece}'
            else:
                second_word = f'{last_piece}'

            is_word_found = word_to_search in [first_word, second_word]

        return is_word_found

    @staticmethod
    def parse_front_stripe(front_stripe, split_by_dash=True):
        # Не важно является front_stripe одно- или многострочной полосой.
        # Работаем только с первой (самой верхней) строкой, т. к. остальные (нижние) строки - это hint,
        # комментарий и пр.
        front_stripe_first_line = front_stripe.split('\n')[0]

        if split_by_dash:
            # если front_stripe_first_line имеет вид 'das Land – des Lands', берём в работу только левую часть,
            # стоящую до ' – '
            front_stripe_first_line_token = front_stripe_first_line.split(' – ')[0]
            return front_stripe_first_line_token
        else:
            return front_stripe_first_line

    # Этот метод нужен для вывода полной информации на экран и с практической точки зрения полезен при создании
    # полного текстового дампа карточек из Anki в Excel
    def __str__(self):
        return self._make_str(self.all_fields_list)

    # После того как полный текстовый дамп карточек сформирован (с помощью метода __str__) и записан в Excel,
    # из Excel можно вычитывать этот дамп и выводить его на экран с разной степенью подробности (с разным кол-вом полей)
    def to_str(self, format_type="front_transcription_back"):
        if format_type == "front_transcription_back":
            return self._make_str(self.front_transcription_back_fields_list)
        elif format_type == "front_transcription_back_with_comments":
            return self._make_str(self.front_transcription_back_with_comments_fields_list)
        # универсальный вариант, подойдёт для любой карточки любого note type
        elif format_type == "front_back":
            return self._make_str(self.front_back_fields_list)
        else:
            return self.__str__()

    # Если в агрегированной/сложной/составной карточке нужно вывести на экран информацию из всех полей
    # только по номеру конкретной полосы
    def to_str_by_stripe_index_all_fields(self, stripe_index):
        output = self._to_str_by_stripe_index_internal(stripe_index, self.all_fields_list)
        return output

    def to_str_by_stripe_index_front_transcription_back(self, stripe_index):
        output = self._to_str_by_stripe_index_internal(stripe_index, self.front_transcription_back_fields_list)
        return output

    def to_str_by_stripe_index_front_transcription_back_with_comments(self, stripe_index):
        output = self._to_str_by_stripe_index_internal(stripe_index,
                                                       self.front_transcription_back_with_comments_fields_list)
        return output

    def _to_str_by_stripe_index_internal(self, stripe_index, fields_list):
        # Список списков: внешний список - поля карточки, внутренний список - с единственным элементом,
        # вычитанным из поля карточки по stripe_index
        results = []

        for field in fields_list:
            if field:
                if stripe_index < len(field):
                    res_as_list_of_strings = [field[stripe_index]]
                else:
                    res_as_list_of_strings = field
            else:
                # print(str([])) - пустой список на экран выводится как '[]', а здесь нужно,
                # чтобы пустое поле (это тоже пустой список) было представлено пустой строкой
                res_as_list_of_strings = ['']

            results.append(res_as_list_of_strings)

        output = self._make_str(results)
        return output

    def _make_str(self, fields_list):
        results = []
        for field in fields_list:
            result = self._prepare_field_str_representation(field)
            results.append(result)

        # объединение в столбцы
        output_str = "|".join(results)
        return output_str

    def _prepare_field_str_representation(self, field_data: list):
        # Перед выводом на экран, временно заменяем некоторые символы их субститутами для преобразования сложного
        # многострочного текста в одну строку для удобства работы с ним и, в частности, хранения в Excel

        substituted_field_data = []
        for fd in field_data:
            fd = fd.replace('\n', SINGLE_NEWLINE_SUBSTITUTE)
            # пайп как технический символ будет служить разделителем полей и нельзя допустить ситуацию, чтобы
            # оригинальный пайп в тексте Anki-поля мешал этой временной технической задаче
            fd = fd.replace('|', PIPE_SUBSTITUTE)
            substituted_field_data.append(fd)

        field_str = DOUBLE_NEWLINE_SUBSTITUTE.join(substituted_field_data)
        # field_str = DOUBLE_NEWLINE_SUBSTITUTE.join(sfd for sfd in substituted_field_data if len(sfd))
        return field_str

    def __eq__(self, other):
        if not isinstance(other, AnkiCardEntity):
            return False
        return self.front == other.front and self.front_comment == other.front_comment and \
            self.taggy == other.taggy and self.ssml == other.ssml and \
            self.transcription == other.transcription and self.grammar == other.grammar and \
            self.back == other.back and self.back_comment == other.back_comment

###########################


# deck_name = '!A_Словари::!Words (new)'
# ankiConnectService = AnkiConnectService()
# notes = ankiConnectService.get_notes_by_deck_name(deck_name)
#
# for note in notes:
#     ankiCardEntity = AnkiCardEntity(note)
#     # ankiCardEntity.validate_consistency()
#     # if 'Wittenberg' in ankiCardEntity.front:
#     # print(ankiCardEntity.to_str())
#     print(ankiCardEntity.to_str("front_transcription_back_with_comments"))
