import re
from pathlib import Path

import AppContext
from FilenameUtils import FilenameUtils
import SentenceUtils
from AnkiConnectService import AnkiConnectService
from AnkiRegularCardsValidator import AnkiRegularCardsValidator
from MultilingualAnkiDao import MultilingualAnkiDao
from GermanOdtPseudoCardsValidator import GermanOdtPseudoCardsValidator
from GermanRealAnkiCardsValidator import GermanRealAnkiCardsValidator
from OdtFileTableDao import OdtFileTableDao, TableRowsToAnkiCardsMode
from View_enums import CurrentLanguageComboBoxEnum


class A040_VocabFilesConsistencyChecker:

    def __init__(self):
        # Можно смело инициализировать в конструкторе, т. к. классы odtFileTableDao и MultilingualAnkiDao не хранят
        # в себе состояния, а значит вычитываемые их методами данные всегда актуальны.
        self.odtFileTableDao = OdtFileTableDao()
        self.multilingualAnkiDao = MultilingualAnkiDao()
        self.ankiConnectService = AnkiConnectService()
        self.filenameUtils = FilenameUtils()

    def check_consistency(self, should_split_by_space_flag=False):
        # Выполнить проверку с точки зрения КОЛИЧЕСТВЕННОГО аспекта
        # output = self.check_quantitative_aspect()
        output = ''  # заглушка, чтобы каждый раз не запускать проверку количественного аспекта

        if not output:
            # Выполнить проверку с точки зрения КАЧЕСТВЕННОГО аспекта
            output = self.check_qualitative_aspect(should_split_by_space_flag)

        return output

    # Проверяет совпадение кол-ва сабдеков в '!Goethe-Institut A1' и кол-ва Vocab-файлов,
    #  а также совпадение кол-ва слов в каждом сабдеке и соответствующем Vocab-файле.
    def check_quantitative_aspect(self):
        a1_subdeck_names = self.ankiConnectService.get_all_subdeck_names('!Deutsch. !Словарь::!Goethe-Institut A1')

        all_vocab_filenames = self.filenameUtils.get_all_vocab_filenames()
        # Берём в дальнейшую работу только те [Vocab]-файлы, в пути которых содержится 'A1'.
        a1_vocab_filenames = [vocab_filename for vocab_filename in all_vocab_filenames if
                              "A1" in Path(vocab_filename).parts]

        if not a1_subdeck_names:
            raise Exception('No A1 subdecks found!')
        if not a1_vocab_filenames:
            raise Exception('No A1 vocab files found!')
        if len(a1_subdeck_names) != len(a1_vocab_filenames):
            raise Exception('Different number of A1 subdecks and A1 Vocab-files!')

        error_messages = []

        for subdeck_name, vocab_filename in zip(a1_subdeck_names, a1_vocab_filenames):
            # print(f'{subdeck_name} -> {vocab_filename}')

            subdeck_card_entities = self.multilingualAnkiDao.get_data(subdeck_name)
            vocab_file_word_entities = self.odtFileTableDao.convert_table_rows_to_anki_cards_of_single_file(
                vocab_filename, read_words=True, read_sentences=False)

            if len(subdeck_card_entities) != len(vocab_file_word_entities):
                # raise Exception(f"Different number of words in subdeck '{subdeck_name}' and '{vocab_filename}'!")
                error_msg = f"Different number of words in subdeck '{subdeck_name}' and '{vocab_filename}'!"
                error_messages.append(error_msg)
            else:
                # Равенство кол-ва элементов в списках ещё не означает, что их содержимое совпадает.
                subdeck_card_entities_fronts = [vocab_file_word_entity.front for vocab_file_word_entity in
                                                vocab_file_word_entities]
                vocab_file_word_entities_fronts = [vocab_file_word_entity.front for vocab_file_word_entity in
                                                   vocab_file_word_entities]

                # Сравнение двух список, если порядок элементов не имеет значения
                # if Counter(subdeck_card_entities_fronts) != Counter(vocab_file_word_entities_fronts):
                if sorted(subdeck_card_entities_fronts) != sorted(vocab_file_word_entities_fronts):
                    error_msg = f"Different words in subdeck '{subdeck_name}' and '{vocab_filename}'!"
                    # raise Exception(msg)
                    error_messages.append(error_msg)

        output = ''
        if error_messages:
            output = '\n'.join(error_messages)
        return output

    def check_qualitative_aspect(self, should_split_by_space_flag):
        # Суммарно вычитываем содержимое всех [Vocab]-файлов, но распределяем их по двум разным коллекциям.
        all_files_but_last_cards = self.odtFileTableDao.convert_table_rows_to_anki_cards(
            vocab_files=TableRowsToAnkiCardsMode.ALL_FILES_BUT_LAST, read_words=True, read_sentences=True)
        last_file_cards = self.odtFileTableDao.convert_table_rows_to_anki_cards(
            vocab_files=TableRowsToAnkiCardsMode.LAST_FILE, read_words=True, read_sentences=True)

        # Step 1. Валидация псевдо-карточек всех [Vocab]-файлов. Настоящие Анки-карточки здесь ещё не участвуют
        # в процессе валидации.
        germanOdtPseudoCardsValidator = GermanOdtPseudoCardsValidator(all_files_but_last_cards, last_file_cards)
        output1_pseudo_cards = germanOdtPseudoCardsValidator.validate(should_split_by_space_flag)

        # Step 2. Валидация реальных Анки-карточек.
        # Валидация согласованности транскрипции и перевода одного и того же слова в полосах разных карточек.
        # Этот шаг помогает на самой ранней стадии предотвратить нарушение консистентности в словах и уже на этапе
        # работы с распечаткой слов (т. е. до импорта в Анки) работать с согласованной версией каждого слова.
        error_msg = "Inconsistent words {0} (in 'Transcription' and 'Back' fields):\n\n{1}"

        anki_regular_cards = self.multilingualAnkiDao.get_regular_cards()
        anki_aggregate_cards = self.multilingualAnkiDao.get_filtered_aggregate_cards_for_consistency_validation()
        germanRealAnkiCardsValidator = GermanRealAnkiCardsValidator(anki_regular_cards, anki_aggregate_cards)
        output2_real_anki_cards = germanRealAnkiCardsValidator.validate(should_split_by_space_flag)

        # Step 3. Валидируем сумму псевдо-карточек и настоящих Анки-карточек
        # Если запуск валидации отдельно внутри псевдо-карточек и отдельно внутри настоящих Анки-карточек проблем не
        # вызвал, запускаем валидацию на их сумме: подмешиваем к псевдо-карточкам настоящие Анки-карточки и проверяем,
        # что транскрипция и перевод одного и того же слова среди всей этой суммы карточек выглядит одинаково!
        # TODO: почему только транскрипция и перевод, а не все 5 полей???
        output3_pseudo_plus_real_cards = ''
        if not output1_pseudo_cards and not output2_real_anki_cards:
            # validator = AnkiRegularCardsValidator(
            #     anki_regular_cards + anki_aggregate_cards + all_files_but_last_cards + last_file_cards)
            # output3_pseudo_plus_real_cards = validator.find_inconsistent_words()
            # if output3_pseudo_plus_real_cards:
            #     output += output2_error_msg.format("between [Vocab]-files and Anki", output3_pseudo_plus_real_cards)

            # TODO: NEW APPROACH - proceed in a per file mode
            # Учитывая, что на предыдущих этапах отдельно в домене псевдокарточек и отдельно в домене реальных
            # Anki-карточек противоречий нет, то посчитал, что не будет ошибкой передавать на кросс-валидацию не все
            # псевдо-карточки сразу, а порциями (ради вывода информации на экран о том, в каком именно Vocab-файле
            # находится проблемная карточка). В предыдущем подходе, с передачей на валидацию всего объёма
            # псевдо-карточек, информация о принадлежности карточки к тому или иному файлу терялась.
            for vocab_filename in self.filenameUtils.get_all_vocab_filenames():
                single_vocab_file_cards = self.odtFileTableDao.convert_table_rows_to_anki_cards_of_single_file(
                    vocab_filename)
                validator = AnkiRegularCardsValidator(
                    anki_regular_cards + anki_aggregate_cards + single_vocab_file_cards)
                per_file_output = validator.find_inconsistent_translations_of_the_same_word()
                if per_file_output:
                    output3_pseudo_plus_real_cards += f'{vocab_filename}\n{per_file_output}\n\n'
            # end of loop
            if output3_pseudo_plus_real_cards:
                output3_pseudo_plus_real_cards = error_msg.format("between Anki and [Vocab]-files",
                                                                  output3_pseudo_plus_real_cards)

        # Step 4. Валидация содержимого поля Front_comment (2-й столбец 5-столбцовой таблицы)
        cards_with_invalid_front_comment = []
        for card in all_files_but_last_cards + last_file_cards:
            # Если комментарий в поле Front_comment присутствует, он должен соответствовать определённому формату:
            # - или быть валидным C-style комментарием, т. е. начинаться с //
            # - или быть валидным C++-style комментарием, т. е. начинаться с /* и заканчиваться */
            if card.front_comment:
                # Парсинг данных в поля сущности работает так, что символы newline делят front_comment на отдельные
                # части, которые являются отдельными элементами списка. Поэтому для гарантированного восстановления
                # целостного комментария нужно склеивать все элементы списка в одну строку.
                front_comment_str = ' '.join(card.front_comment)
                is_valid_c_style_comment = front_comment_str.startswith('// ')
                is_valid_cpp_style_comment = front_comment_str.startswith('/*') and front_comment_str.endswith('*/')
                is_valid_comment = is_valid_c_style_comment or is_valid_cpp_style_comment
                if not is_valid_comment:
                    front_str = '^^^'.join(card.front)
                    cards_with_invalid_front_comment.append(front_str)

        output4_invalid_front_comment = ''
        if cards_with_invalid_front_comment:
            output4_invalid_front_comment += f"Cards with invalid front comment:\n\n" + '\n'.join(
                cards_with_invalid_front_comment)

        # Step 5. Валидировать, что в конце немецкого предложения и его русского перевода стоит один и тот же знак
        # препинания! Здесь бывают ошибки, когда, например, в конце немецкого предложения стоит восклицательный знак,
        # а в конце его русского перевода - точка.
        sentences_with_mismatching_punctuation_marks = []
        for card in all_files_but_last_cards + last_file_cards:
            # Если карточка содержит немецкое предложение, оно будет находиться в card.front[-1].
            # Даже если карточка содержит целый диалог, все его реплики всё равно будут находиться в card.front[-1]
            # в виде единой строки, в которой все реплики объединены с помощью '\n'
            if card.front and SentenceUtils.is_sentence(card.front[-1]):
                card_front = card.front[-1]
                card_back = card.back[-1]
                card_front_punctuation_mark = card_front[-1]
                # В русском переводе предложения нужно сначала убрать все подсказки: они находятся в конце предложения
                # и отделяются от него пробелом / символом новой строки + круглые скобки с их содержимым, например:
                # - Извините! (-ung)
                # На что Вы жалуетесь?\n(досл. «Чего Вам недостаёт (в плане здоровья)?»)
                # \s* — соответствует любому количеству пробелов или переводов строки.
                card_back = re.sub(r'\s*\(.*\)$', '', card_back)
                card_back_punctuation_mark = card_back[-1]
                if card_front_punctuation_mark != card_back_punctuation_mark:
                    # Для удобства вывода результатов на экран, заменяем символы newline на '^^^'
                    front_str = card_front.replace('\n', '^^^')
                    sentences_with_mismatching_punctuation_marks.append(front_str)

        output5_mismatching_punctuation_marks = ''
        if sentences_with_mismatching_punctuation_marks:
            output5_mismatching_punctuation_marks += f"Sentences with mismatching punctuation marks:\n\n" + '\n'.join(
                sentences_with_mismatching_punctuation_marks)

        # Формирование результирующего вывода по всем категориям
        output = '\n\n# # #\n\n'.join([out for out in [output1_pseudo_cards, output2_real_anki_cards,
                                                       output3_pseudo_plus_real_cards, output4_invalid_front_comment,
                                                       output5_mismatching_punctuation_marks] if out])

        if not output:
            output = 'ok'

        return output

    # Чисто консольный и дополнительный метод, ищущий список Vocab-файлов, в которых встречается указанное слово.
    # Данный метод нужен для того, чтобы найти список Vocab-файлов (по слову), которые не прошли валидацию.
    def find_vocab_filenames_containing_word(self, word):
        for vocab_filename in self.filenameUtils.get_all_vocab_filenames():
            anki_cards = self.odtFileTableDao.convert_table_rows_to_anki_cards_of_single_file(vocab_filename)
            for anki_card in anki_cards:
                is_among_front_stripes = any([stripe for stripe in anki_card.front if word in stripe])
                is_among_back_stripes = any([stripe for stripe in anki_card.back if word in stripe])
                if is_among_front_stripes or is_among_back_stripes:
                    print(vocab_filename)


##########################################

if __name__ == '__main__':
    language = CurrentLanguageComboBoxEnum.GERMAN.value
    # language = CurrentLanguageComboBoxEnum.MODERN_GREEK.value
    # language = CurrentLanguageComboBoxEnum.ANCIENT_GREEK.value
    AppContext.switch_language(language)

    a040_VocabFilesConsistencyChecker = A040_VocabFilesConsistencyChecker()

    # Main use case
    res = a040_VocabFilesConsistencyChecker.check_consistency()
    print(res)

    # Additional console use case
    # a040_VocabFilesConsistencyChecker.find_vocab_filenames_containing_word('часто придаёт')

    # a040_VocabFilesConsistencyChecker.check_quantitative_aspect()
