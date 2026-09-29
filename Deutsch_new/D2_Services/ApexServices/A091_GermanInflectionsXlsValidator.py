import itertools

import AppContext
from GermanExcelWorkbooksDao import GermanExcelWorkbooksDao
from DeuLemmaResolver import DeuLemmaResolver
from DeuDefiniteArticleService import DeuDefiniteArticleService
from OdtFileTableDao import OdtFileTableDao
from DeuSpaCyOrStanzaWrapper import DeuSpaCyOrStanzaWrapper
from View_enums import CurrentLanguageComboBoxEnum

# Данный класс валидирует, что все слова из последнего [Vocab]-файла присутствуют в файле "Deutsch Lexikon (other).xls",
# а значит поиск морф. форм на следующем этапе (падежные формы существительных, спряжения глаголов и т. д.) не вызовет
# трудностей.

# считывает vocab-файл, отбрысывет те слова (они все в словарной форме), которые уже есть в файле Попова,
# а для тех слов, кот. там нет (новые слова) строит словарь:
# ключ - pos-тег
# значение - само слово
# У Попова нужно вычитать только 1-й столбец по всем листам (такой код уже есть в методе валидации уникальности 1-го столбца)
# Затем этот словарь выводится на экран и по словам из одного и того же pos-тега начинается работа по добавлению их в Excel-файл

ignored_words = [
    'sie', 'Sie', 'all',
    'Ur-\n/* в словаре с большой буквы! Не путать с такой же приставкой с маленькой буквы! */',
    'hamma\n(древнегерм.)',
    'der Starnberger See',
    'ein-\n(глагольная приставка)',
]

FIVE_NEWLINES = '\n\n\n\n\n'


class A091_GermanInflectionsXlsValidator:
    def __init__(self):
        # self.odtFilesService = OdtFilesService()
        self.odtFileTableDao = OdtFileTableDao()
        self.deuSpaCyOrStanzaWrapper = DeuSpaCyOrStanzaWrapper()
        self.deuLemmaResolver = DeuLemmaResolver()
        self.deuDefiniteArticleService = DeuDefiniteArticleService()
        self.germanExcelWorkbooksDao = GermanExcelWorkbooksDao()

    def validate_oo_writer_words_are_present_in_excel(self):

        words_per_excel_book_dict = self.germanExcelWorkbooksDao.get_excel_words_for_validation()
        excel_1st_col_words = list(itertools.chain.from_iterable(words_per_excel_book_dict.values()))

        results_dict = {}

        # Старый рабочий вариант, когда планировалось, что скрипт нужно запускать сразу после выучивания одного
        # нового Vocab-файла
        # table_rows_as_anki_card_entities = self.odtFileTableDao.convert_table_rows_to_anki_cards(
        #     vocab_files=TableRowsToAnkiCardsMode.LAST_FILE)

        # Текущий рабочий вариант, когда запуск скрипта планируется не для каждого отдельного только что выученного
        # Vocab-файла, а сразу для нескольких Vocab-файлов. Такой подход сэкономит время и силы на форматирование
        # особенно спряжений глаголов.
        # Не должен смущать тот факт, что вычитываются данные вообще всех Vocab-файлов. Это хоть и немного избыточно,
        # но не влияет на конечный результат. Вместо того чтобы каждый раз указывать диапазон новых Vocab-файлов,
        # проще вычитать их все, всё равно старые данные не забирают много времени на обработку, spaCy для них
        # не запускается, проверяется только вхождение слов в список уже изученных слов.

        table_rows_as_anki_card_entities = self.odtFileTableDao.convert_table_rows_to_anki_cards()

        # table_rows_as_anki_card_entities = self.odtFileTableDao.convert_table_rows_to_anki_cards_of_single_file(
        #     r'E:\Languages\Deutsch\Goethe-Institut\A1\Hh-Jj\[Vocab] Hh-Jj.odt')

        for table_row_as_anki_card_entity in table_rows_as_anki_card_entities:
            if table_row_as_anki_card_entity.front:
                # На данном этапе слова в [Vocab]-файле отвалидированы: аномалии в виде недостатка или излишка слов
                # точно не наблюдаются, поэтому достаточно всегда брать последнюю полосу карточки (будь она одно-
                # или многополосной) чтобы перебрать все новые слова
                oo_writer_word = table_row_as_anki_card_entity.front[-1]

                is_not_in_excel = oo_writer_word not in excel_1st_col_words
                is_not_in_ignored = oo_writer_word not in ignored_words
                is_not_started_or_ended_with_hyphen = not (
                            oo_writer_word.startswith('-') or oo_writer_word.endswith('-'))
                if is_not_in_excel and is_not_in_ignored and is_not_started_or_ended_with_hyphen:
                    if oo_writer_word.startswith(('der ', 'die ', 'das ')):
                        oo_writer_word = self.deuDefiniteArticleService.strip_definite_article(oo_writer_word)

                    spacy_tuples = self.deuSpaCyOrStanzaWrapper.get_doc_object_tuples(oo_writer_word)
                    if spacy_tuples:
                        token, lemma, pos, morph = spacy_tuples[0]
                        if pos not in results_dict:
                            results_dict[pos] = []

                        # Ветка для большинства случаев, в которых в слове (после стрипания артикля у существительных)
                        # пробела нет.
                        if ' ' not in oo_writer_word:
                            processed_lemma = self.deuLemmaResolver.get_single_lemma(token, lemma, pos, morph)
                        # Иначе оставляем слово "как есть": это слова с неотъемлемым пробелом типа "Pommes frites",
                        # "Mount Everest", etc.
                        else:
                            processed_lemma = oo_writer_word

                        if processed_lemma not in excel_1st_col_words and processed_lemma not in results_dict[pos]:
                            if table_row_as_anki_card_entity.transcription:  # если список не пустой
                                # У списка транскрипций в последнем элементе оставляем только самую верхнюю строчку
                                # (сама транскрипция), а возможный комментарий к транскрипции игнорируем:
                                # он не должен попасть в Excel.
                                table_row_as_anki_card_entity.transcription[-1] = \
                                table_row_as_anki_card_entity.transcription[-1].split('\n')[0]
                            result = table_row_as_anki_card_entity.to_str_by_stripe_index_front_transcription_back(-1)
                            results_dict[pos].append(result)

        output = ''

        # 1. Имя существительное
        common_nouns_str = ''
        proper_nouns_str = ''
        # Существительные объединяем через 5 newlines (т. е. через 4 пустые строки) для вставки их сразу всех в
        # Excel-файл. Далее в Excel-файле им нужно будет добавить склонение по падежам.
        if 'NOUN' in results_dict:
            common_nouns_str = FIVE_NEWLINES.join(results_dict['NOUN'])
        if 'PROPN' in results_dict:
            proper_nouns_str = FIVE_NEWLINES.join(results_dict['PROPN'])
        nouns_str = self._join_ignoring_empty_strings(common_nouns_str, proper_nouns_str, FIVE_NEWLINES)
        if nouns_str:
            output += f'NOUNS:\n{nouns_str}\n\n'

        # 2. Имя прилагательное
        if 'ADJ' in results_dict:
            adjectives_str = FIVE_NEWLINES.join(results_dict['ADJ'])
            if adjectives_str:
                output += f'ADJECTIVES:\n{adjectives_str}\n\n'

        # 3. Имя числительное
        if 'NUM' in results_dict:
            numerals_str = '\n'.join(results_dict['NUM'])
            if numerals_str:
                output += f'NUMERALS:\n{numerals_str}\n\n'

        # 4. Местоимение
        if 'PRON' in results_dict:
            pronouns_str = '\n'.join(results_dict['PRON'])
            if pronouns_str:
                output += f'PRONOUNS:\n{pronouns_str}\n\n'

        # 5. Глагол
        common_verbs_str = ''
        aux_verbs_str = ''
        if 'VERB' in results_dict:
            common_verbs_str = '\n'.join(results_dict['VERB'])
        if 'AUX' in results_dict:
            aux_verbs_str = '\n'.join(results_dict['AUX'])
        verbs_str = self._join_ignoring_empty_strings(common_verbs_str, aux_verbs_str)
        if verbs_str:
            output += f'VERBS:\n{verbs_str}\n\n'

        # 6. Наречие
        if 'ADV' in results_dict:
            adverbs_str = '\n'.join(results_dict['ADV'])
            if adverbs_str:
                output += f'ADVERBS:\n{adverbs_str}\n\n'

        # 7. Предлог
        # Adposition (предлог или послелог)
        if 'ADP' in results_dict:
            adpositions_str = '\n'.join(results_dict['ADP'])
            if adpositions_str:
                output += f'ADPOSITIONS:\n{adpositions_str}\n\n'

        # 8. Союз
        coordinating_conjunctions_str = ''
        subordinating_conjunctions_str = ''
        if 'CCONJ' in results_dict:
            coordinating_conjunctions_str = '\n'.join(results_dict['CCONJ'])
        if 'SCONJ' in results_dict:
            subordinating_conjunctions_str = '\n'.join(results_dict['SCONJ'])
        conjunctions_str = self._join_ignoring_empty_strings(coordinating_conjunctions_str,
                                                             subordinating_conjunctions_str)
        if conjunctions_str:
            output += f'CONJUNCTIONS:\n{conjunctions_str}\n\n'

        # 9. Частица
        if 'PART' in results_dict:
            particles_str = '\n'.join(results_dict['PART'])
            if particles_str:
                output += f'PARTICLES:\n{particles_str}\n\n'

        # 10. Междометие
        if 'INTJ' in results_dict:
            interjections_str = '\n'.join(results_dict['INTJ'])
            if interjections_str:
                output += f'INTERJECTIONS:\n{interjections_str}\n\n'

        # Печатаем информацию по оставшимся pos-тегам
        for pos, new_words in results_dict.items():
            if pos not in ['NOUN', 'PROPN', 'ADJ', 'NUM', 'PRON', 'VERB', 'AUX', 'ADV',
                           'ADP', 'CCONJ', 'SCONJ', 'PART', 'INTJ']:
                if new_words:
                    output += f'{pos}:\n'
                    new_words_str = '\n'.join(new_words)
                    output += f'{new_words_str}\n\n'

        output = output.strip()  # удаляет символы [ \t\n\r\f\v] в начале и конце строки
        if not output:
            output = 'ok'

        return output

    def _join_ignoring_empty_strings(self, str1, str2, delimiter='\n'):
        str1 = str1.strip()
        str2 = str2.strip()
        # Используется filter(None, [str1, str2]), чтобы исключить пустые строки из списка перед объединением.
        # Использование None в функции filter позволяет отфильтровывать все "ложные" значения в iterable
        # (в данном случае — в списке строк). Это включает в себя:
        # - пустые строки ''
        # - значение None
        # - числа, равные нулю 0
        # - логическое значение False.
        # Метод join объединяет оставшиеся строки с помощью '\n'.
        # Таким образом, если одна или обе строки пустые, лишний '\n' не будет добавлен.
        result = delimiter.join(filter(None, [str1, str2]))
        return result


######################################################

if __name__ == '__main__':
    language = CurrentLanguageComboBoxEnum.GERMAN.value
    # language = CurrentLanguageComboBoxEnum.MODERN_GREEK.value
    # language = CurrentLanguageComboBoxEnum.ANCIENT_GREEK.value
    AppContext.switch_language(language)

    a091_GermanInflectionsXlsValidator = A091_GermanInflectionsXlsValidator()
    res = a091_GermanInflectionsXlsValidator.validate_oo_writer_words_are_present_in_excel()
    print(res)
