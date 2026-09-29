import AppContext
import GermanWiktionaryService
import Utils
from A020_TranscriptionsAndTranslationsLookUpper import A020_TranscriptionsAndTranslationsLookUpper
from DeuLemmaResolver import DeuLemmaResolver
from DeutschNewConstants import OO_WRITER_STRIPES_DELIMITER
from MultilingualAnkiService import MultilingualAnkiService
from DeuDefiniteArticleService import DeuDefiniteArticleService
from OdtFilesService import OdtFilesService
from MorphologyParser import MorphologyParser
from N3_DashedArticledNounsComposer import DashedArticledNounsComposer
from DeuSpaCyOrStanzaWrapper import DeuSpaCyOrStanzaWrapper
from SpaCyPosResolver import SpaCyPosResolver
from View_enums import CurrentLanguageComboBoxEnum

WHITESPACE = ' '
HYPHEN = '-'


class A030_SplitComplexWordsProcessor:
    def __init__(self):
        self.deuSpaCyOrStanzaWrapper = DeuSpaCyOrStanzaWrapper()
        self.deuLemmaResolver = DeuLemmaResolver()
        self.deuDefiniteArticleService = DeuDefiniteArticleService()
        self.morphologyParser = MorphologyParser()
        self.spaCyPosResolver = SpaCyPosResolver()
        self.dashedArticledNounsComposer = DashedArticledNounsComposer(DeuDefiniteArticleService())
        self.multilingualAnkiService = None
        self.odtFilesService = None
        self.a020_TranscriptionsAndTranslationsLookUpper = A020_TranscriptionsAndTranslationsLookUpper()
        self.deuDefiniteArticleService = DeuDefiniteArticleService()

    def process(self, input_lines):
        # TODO Можно добавить флажки на UI для регулировки момента с перевычиткой данных из Anki и
        #  Vocab-файлов (особенно из Anki) при каждом нажатии на кнопку Process. В принципе вычитка из Anki
        #  не занимает какого-то слишком большого времени и можно всё оставить "как есть". Но чего нельзя делать - это
        #  инициализировать данные сервисы в конструкторе: тогда они инициализируются только один раз и любые изменения
        #  в Anki-карточках или Vocab-файлах не будут доступны в текущей сессии без перезапуска программы.
        self.multilingualAnkiService = MultilingualAnkiService()
        self.odtFilesService = OdtFilesService()

        # Список списков
        all_results = []
        # Разбиваем входной текст по разделителю «\n\n»: это разделитель между композитными словами.
        complex_words_entries = Utils.split_by(input_lines, '\n\n')
        for complex_word_entry in complex_words_entries:
            # В рамках одной и той же complex_word_entry получаем список отдельных слов-строк.
            lines = Utils.split_by(complex_word_entry, '\n')
            # На всякий случай убираем определённые артикли в начале строк, если они туда по ошибке попали.
            lines = [self.deuDefiniteArticleService.strip_definite_article(line) for line in lines]

            # Первым делом должен проверяться факт присутствия сложного/составного слова (последняя строка в каждой
            # группе входных слов-строк) среди регулярных Анки-карточек:
            # если ДА и кол-во полос в Анки-карточке совпадает с количеством строк-составных-частей, вызывается
            # бизнес-логика этапа №2;
            # ИНАЧЕ фиксируем, что сложное/составное слово в Анки отсутствует, значит перевод данного слова
            # вычитать неоткуда, а транскрипцию попробуем вычитать из Wiktionary.
            last_entry_line = lines[-1]
            token, lemma, pos, morph, current_word = self._get_token_lemma_pos_morph_current_word_objects(last_entry_line)
            found_regular_card = self.multilingualAnkiService.search_among_main_regular_cards(current_word)

            # Сложное/составное слово в Анки может присутствовать, но не быть расписанным на части (или быть
            # недостаточно расписанным). Например, в Анки просто может быть anfangen без деления на an- + fangen.
            # Поэтому проверяем: если количество полос в найденной Анки-карточке совпадает с количеством
            # строк-составных-частей слова, которые пользователь ввёл на UI, тогда считаем результат готовым,
            # в противном случае обрабатываем строки-составные-части
            # обычным образом.
            if found_regular_card and len(found_regular_card.front) == len(lines):
                lines = self.a020_TranscriptionsAndTranslationsLookUpper.process_lines([current_word])
            else:
                last_stripe_str_param = ''
                if found_regular_card:
                    last_stripe_str_param = found_regular_card.to_str_by_stripe_index_front_transcription_back_with_comments(-1)
                lines = self._process_non_anki_complex_word(lines, last_stripe_str_param)

            all_results.append(lines)
        # end of loop

        all_results_with_unique_sublists = self._filter_sublists_to_make_them_unique(all_results)

        # Элементы в пределах подсписка объединяем с помощью '\n', а получившиеся чанки объединяем с помощью '\n\n'
        all_results_output = '\n\n'.join(['\n'.join(sublist) for sublist in all_results_with_unique_sublists])
        return all_results_output

    def _get_token_lemma_pos_morph_current_word_objects(self, raw_word):
        token, lemma, pos, morph = self.deuSpaCyOrStanzaWrapper.get_doc_object_tuples(raw_word)[0]
        # Если current_word - это существительное, оно будет возвращено с определённым артиклем.
        current_word = self.deuLemmaResolver.get_single_lemma(token, lemma, pos, morph)
        return token, lemma, pos, morph, current_word

    # Просеивает список списков так, чтобы между подсписками не было повторяющихся элементов, т. е. чтобы не было
    # повторяющихся слов-строк в результате расписывания сложных слов на более простые.
    # input:  [[1, 2, 3], [3, 4, 5], [2, 6, 7, 5], [8, 9, 1]]
    # output: [[1, 2, 3], [4, 5], [6, 7], [8, 9]]
    def _filter_sublists_to_make_them_unique(self, list_of_lists):
        seen = set()
        result = []

        for sublist in list_of_lists:
            new_sublist = []
            for item in sublist:
                if item not in seen:
                    seen.add(item)
                    new_sublist.append(item)
            if new_sublist:
                result.append(new_sublist)

        return result

    def _process_non_anki_complex_word(self, lines, last_stripe_str_param):
        separate_lines_results = []
        merged_line_results = []

        for i, line in enumerate(lines):
            # Ветка для случая, когда работаем с не последней полосой сложного/составного слова: такую полосу
            # теоретически ВОЗМОЖНО найти среди регулярных карточек Анки
            if i < len(lines) - 1:
                # Сначала нужно попытаться найти слово "как есть": например, "Einzel-" нельзя сразу передавать spaCy,
                # иначе из него иногда может получаться "einzel-", которое не будет найдено в Anki
                found_regular_card = self.multilingualAnkiService.search_among_main_regular_cards(line)
                if found_regular_card:
                    # Проверяем не будет ли слово (как составная часть сложного/составного слова), которое мы собираемся
                    # поместить в отдельную строку таблицы, дубликатом по отношению к содержимому предыдущих [Vocab]-файлов.
                    # В текущем [Vocab]-файле не проверяем, т. к. нет привязки к местоположению расписываемого слова
                    # в таблице. Если даже возникнет дублирование в рамках текущего [Vocab]-файла, валидация
                    # консистентности (следующий этап) этот момент подкорректирует.
                    if self.odtFilesService.is_word_absent_from_vocabulary_of_all_files_but_last(line):
                        separate_line_result = found_regular_card.to_str("front_transcription_back_with_comments")
                        separate_lines_results.append(separate_line_result)

                    # Неважно является найденная карточка одно- или многополосной, берём в merged-строку только
                    # последнюю полосу
                    merged_line_result = found_regular_card.to_str_by_stripe_index_front_transcription_back_with_comments(-1)
                    merged_line_results.append(merged_line_result)
                # Иначе, если слово в своём "сыром" виде не было сразу найдено в Anki, обрабатываем его с помощью spaCy
                # и повторяем попытку поиска в Anki
                else:
                    token, lemma, pos, morph, current_word = self._get_token_lemma_pos_morph_current_word_objects(line)
                    found_regular_card = self.multilingualAnkiService.search_among_main_regular_cards(current_word)
                    if found_regular_card:
                        if self.odtFilesService.is_word_absent_from_vocabulary_of_all_files_but_last(current_word):
                            separate_line_result = found_regular_card.to_str("front_transcription_back_with_comments")
                            separate_lines_results.append(separate_line_result)

                        # Если найденное в Анки слово является существительным в форме, отличной от начальной
                        # (ед. ч., им. п.), будем для него строить строку вида: der Bund – des Bundes,
                        # т. е. не-начальную форму существительного будем сопровождать начальной формой.
                        if self.spaCyPosResolver.is_noun(pos) and self.spaCyPosResolver.is_noun_in_non_initial_form(morph):
                            # Формируем результат для merged-строки
                            last_stripe_str = found_regular_card.to_str_by_stripe_index_front_transcription_back_with_comments(-1)
                            front_str, front_comment_str, transcription_str, back_str, back_comment_str = last_stripe_str.split('|')

                            # Существительному в косвенном падеже добавляем артикль
                            token_with_article = self.deuDefiniteArticleService.add_definite_article_to_token(token, pos, morph)
                            # Существительному в косвенном падеже находим транскрипцию
                            token_with_article_transcription = GermanWiktionaryService.get_word_transcription(
                                token_with_article, True)
                            # Существительному в косвенном падеже находим грамматическую подсказку
                            dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(current_word.split()[-1], token, pos, morph)

                            front = f'{front_str} – {token_with_article}'
                            front_comment = front_comment_str
                            transcription = f'{transcription_str} – {token_with_article_transcription}'
                            back = f'{back_str}^^^{grammar_hint}'
                            back_comment = back_comment_str

                            merged_line_result = '|'.join([front, front_comment, transcription, back, back_comment])
                            merged_line_results.append(merged_line_result)
                        else:
                            # Неважно является карточка одно- или многополосной, берём в merged-строку только последнюю
                            # полосу
                            merged_line_result = found_regular_card.to_str_by_stripe_index_front_transcription_back_with_comments(-1)
                            merged_line_results.append(merged_line_result)
                    # Если слово в Анки не найдено
                    else:
                        result = self._compose_result_for_non_anki_word(current_word)
                        separate_lines_results.append(result)
                        merged_line_results.append(result)
            # Если работаем с последней полосой сложного/составного слова
            else:
                # Если последняя полоса была в Анки (просто слово было недорасписано), переиспользуем её
                if last_stripe_str_param:
                    merged_line_results.append(last_stripe_str_param)
                # Значит последняя полоса отсутствует в Анки
                else:
                    token, lemma, pos, morph, current_word = self._get_token_lemma_pos_morph_current_word_objects(line)
                    result = self._compose_result_for_non_anki_word(current_word)
                    merged_line_results.append(result)
        # end of loop

        separate_lines_results_output = '\n'.join(separate_lines_results)
        merged_line_results_output = self._format_merged_line_output(merged_line_results)
        # Объединяем только непустые строки
        # entry_output = '\n'.join([line for line in [separate_lines_results_output, merged_line_results_output] if line])
        entry_output = [line for line in [separate_lines_results_output, merged_line_results_output] if line]

        return entry_output

    def _compose_result_for_non_anki_word(self, word):
        front = word
        front_comment = ''
        transcription = GermanWiktionaryService.get_word_transcription(word, True)
        if not transcription:
            transcription = '???'
        back = '???'  # тройной знак вопроса - напоминание об необходимости заполнения перевода слова
        back_comment = ''
        result = '|'.join([front, front_comment, transcription, back, back_comment])
        return result

    def _format_merged_line_output(self, merged_line_results):
        # Делаем merge строк в пределах каждого столбца (в механике OO Writer) и объединяем их с помощью pipe
        # в одну широкую строку
        col1_results = []
        col2_results = []
        col3_results = []
        col4_results = []
        col5_results = []
        for i in range(0, len(merged_line_results)):
            line = merged_line_results[i]
            if '|' in line:
                card_fields = line.split("|")

                front_str = card_fields[0]
                # комментарии к "словам-составным частям" не должны попадать в расписываемое сложное/составное слово
                front_comment_str = ''
                # комментарии к "словам-составным частям" не должны попадать в расписываемое сложное/составное слово,
                # а комментарий к самому сложному/составному слову должен переноситься в итоговую merge-строку
                # if i < len(merged_line_results) - 1:
                #     front_comment_str = ''
                #     back_comment_str = ''
                # else:
                #     front_comment_str = card_fields[1]
                #     back_comment_str = card_fields[4]
                transcription_str = card_fields[2]
                back_str = card_fields[3]
                # комментарии к "словам-составным частям" не должны попадать в расписываемое сложное/составное слово
                back_comment_str = ''

                col1_results.append(front_str)
                col2_results.append(front_comment_str)
                col3_results.append(transcription_str)
                col4_results.append(back_str)
                col5_results.append(back_comment_str)

        col1_results_output = OO_WRITER_STRIPES_DELIMITER.join(col1_results)
        # Пустые строки с комментариями не должны увеличивать количество newline-символов в соответствующей ячейке
        # merged-строки, поэтому делаем .join только реально непустых строк
        col2_results_output = OO_WRITER_STRIPES_DELIMITER.join([item for item in col2_results if item])
        col3_results_output = OO_WRITER_STRIPES_DELIMITER.join(col3_results)
        col4_results_output = OO_WRITER_STRIPES_DELIMITER.join(col4_results)
        col5_results_output = OO_WRITER_STRIPES_DELIMITER.join([item for item in col5_results if item])

        merged_line_output = "|".join(
            [col1_results_output, col2_results_output, col3_results_output, col4_results_output, col5_results_output])

        return merged_line_output


#####################################

input_str = """
Wort
gruppen
liste
Wortgruppenliste
"""

input_str = """
Wort
gruppen
liste
Wortgruppenliste
# # ####
Bahn
Hof
Bahnhof
"""

# input_str = """
# Wort gruppen
# liste
# Wortgruppenliste
# # # ####
# Bahn
# Hof
# Bahnhof
# """

# input_str = """
# ab-
# geben
# abgeben
# """

# input_str = 'abholen'

# input_str = """
# Bahnhof
# straße
# Bahnhofstraße
# """

input_str = """
Bahnhöfe
Leute
Bahnhöfeleute
"""

# input_str = """
# Bahn
# Hof
# Bahnhof
# """

# input_str = 'Bahnhof'

input_str = """
an-
sagen
ansagen
"""

input_str = """
Auto
Bahn
Autobahn
"""

input_str = """
Wörter
Buch
Wörterbuch
"""

input_str = """
Ehe
Mann
Ehemann

Ehe
Frau
Ehefrau
"""

input_str = """
Einzel-
fahren
Karte
die Einzelfahrkarte
"""

if __name__ == '__main__':
    language = CurrentLanguageComboBoxEnum.GERMAN.value
    # language = CurrentLanguageComboBoxEnum.MODERN_GREEK.value
    # language = CurrentLanguageComboBoxEnum.ANCIENT_GREEK.value
    AppContext.switch_language(language)

    a030_SplitKompositaProcessor = A030_SplitComplexWordsProcessor()
    res = a030_SplitKompositaProcessor.process(input_str)
    print(res)
