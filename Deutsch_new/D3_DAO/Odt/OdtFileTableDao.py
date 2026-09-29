from enum import Enum

from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.text import P

import AppContext
import SentenceUtils
from AnkiCardEntity import AnkiCardEntity
from DeutschNewConstants import OO_WRITER_STRIPES_DELIMITER, OO_WRITER_STRIPE_LINES_DELIMITER
from FilenameUtils import FilenameUtils
from MultilingualAnkiDao import MultilingualAnkiDao
from OdtCopyPasteTableDao import OdtCopyPasteTableDao
from View_enums import CurrentLanguageComboBoxEnum


# Вычитывает содержимое Odt-таблиц из файла
# TODO: идея в том, чтобы в рабочей папке были .odt-файлы, начинающиеся с [Vocab] и хранящие таблицы со словами.
#  Все эти файлы считываются и строки, содержащиеся в их таблицах, конвертируются в Анки-сущности и складываются
#  в общую коллекцию. Эту коллекцию можно и нужно валидировать. Из этой коллекции вычитываются переводы для
#  морф. форм в модуле A50_GermanTextInflectionsMaker.


class TableRowsToAnkiCardsMode(Enum):
    ALL_FILES = 1
    ALL_FILES_BUT_LAST = 2
    LAST_FILE = 3


class OdtFileTableDao:
    def __init__(self):
        self.filenameUtils = FilenameUtils()
        self.odtCopyPasteTableDao = OdtCopyPasteTableDao()
        self.multilingualAnkiDao = MultilingualAnkiDao()

    def convert_table_rows_to_anki_cards(self, vocab_files=TableRowsToAnkiCardsMode.ALL_FILES,
                                         read_words=True, read_sentences=False, ignore_empty_rows=True):

        vocab_filenames = []
        all_vocab_filenames = self.filenameUtils.get_all_vocab_filenames()
        if all_vocab_filenames:  # если есть хотя бы один [Vocab]-файл
            if vocab_files == TableRowsToAnkiCardsMode.ALL_FILES:
                vocab_filenames = all_vocab_filenames
            elif vocab_files == TableRowsToAnkiCardsMode.ALL_FILES_BUT_LAST:
                vocab_filenames = all_vocab_filenames[:-1]
            elif vocab_files == TableRowsToAnkiCardsMode.LAST_FILE:
                # Поскольку имя одного файла - это строка, её нужно обернуть в список для соответствия контракту дальнейшего
                # алгоритма
                vocab_filenames = [all_vocab_filenames[-1]]

        table_rows_as_anki_card_entities = []
        for vocab_filename in vocab_filenames:
            single_file_entities = self.convert_table_rows_to_anki_cards_of_single_file(vocab_filename, read_words,
                                                                                        read_sentences,
                                                                                        ignore_empty_rows)
            table_rows_as_anki_card_entities.extend(single_file_entities)

        return table_rows_as_anki_card_entities

    def convert_table_rows_to_anki_cards_of_single_file(self, filename, read_words=True, read_sentences=False,
                                                        ignore_empty_rows=True):
        table_rows_as_anki_card_entities = []

        all_rows_of_all_tables_of_single_file = self.read_single_file_all_tables_data(filename, ignore_empty_rows)
        for table_row in all_rows_of_all_tables_of_single_file:
            if table_row.count('|') == 4:  # работаем с [Vocab]-файлом: у 5-столбцового файла 4 пайп-разделителя
                front_tr, front_comment_tr, transcription_tr, back_tr, back_comment_tr = table_row.split('|')

                if SentenceUtils.is_sentence(front_tr):
                    # if read_sentences:
                    front_tr = front_tr.replace(OO_WRITER_STRIPES_DELIMITER, OO_WRITER_STRIPE_LINES_DELIMITER)
                    transcription_tr = transcription_tr.replace(OO_WRITER_STRIPES_DELIMITER,
                                                                OO_WRITER_STRIPE_LINES_DELIMITER)
                    back_tr = back_tr.replace(OO_WRITER_STRIPES_DELIMITER, OO_WRITER_STRIPE_LINES_DELIMITER)
                # else:
                #     continue

                # Сформировали поле Front, чтобы выяснить имеет ли смысл тратить время и силы на парсинг остальных полей
                front = self.parse(front_tr)
                should_proceed = self._should_proceed_with_other_fields(front, read_words, read_sentences)
                if not should_proceed:
                    continue
                front_comment = self.parse(front_comment_tr)
                transcription = self.parse(transcription_tr)
                back = self.parse(back_tr)
                back_comment = self.parse(back_comment_tr)

            elif table_row.count('|') == 2:  # работаем с portrait-файлом: у 3-столбцового файла 2 пайп-разделителя
                front_tr, transcription_tr, back_tr = table_row.split('|')

                front_tr_parsed = self.parse(front_tr)
                transcription_tr_parsed = self.parse(transcription_tr)
                back_tr_parsed = self.parse(back_tr)

                front, front_comment = self._split_into_front_and_front_comment(front_tr_parsed)

                # Сформировали поле Front, чтобы выяснить имеет ли смысл тратить время и силы на парсинг остальных полей
                should_proceed = self._should_proceed_with_other_fields(front, read_words, read_sentences)
                if not should_proceed:
                    continue

                transcription = transcription_tr_parsed  # каждое поле Anki-карточки - это список строк

                if '* * *' in back_tr_parsed:
                    delimiter_index = back_tr_parsed.index('* * *')
                    back = back_tr_parsed[:delimiter_index]
                    # +1 потому что разделитель не включается в список поля Back_comment
                    back_comment = back_tr_parsed[delimiter_index + 1:]
                else:
                    back = back_tr_parsed
                    back_comment = []

                # Если хотя бы первая полоса front-поля является предложением, значит и другие полосы (если они есть)
                # тоже являются предложениями. Значит в такого рода табличной строке не может быть полос: предложение
                # или диалог по определению однополосны. Такими их и делаем склеивая мнимые полосы полей front,
                # transcription, back в одну полосу и делая получившуюся строку списком, т. к. каждое поле
                # Anki-карточки - это список строк, даже если она всего одна.
                # Данная логика нужна для того, чтобы сгладить возможно разное количество переносов строки в одном и
                # том же предложении в Vocab- и portrait-файле. В portrait-файле иногда удобно добавить лишние переносы
                # строки для того, чтобы каждая немецкая реплика, её транскрипция и русский перевод стояли чётко
                # напротив друг друга. А при валидации (сравнении соотв. строк таблицы в Vocab- и portrait-файлах) эти
                # переносы должны игнорироваться, т. к. носят чисто декоративный характер.
                if SentenceUtils.is_sentence(front[-1]):
                    # if read_sentences:
                    front = ['\n'.join(front)]
                    transcription = ['\n'.join(transcription)]
                    back = ['\n'.join(back)]
                # else:
                #     continue

            else:
                error_msg = (f"Файл '{filename}' содержит некорректное количество пайп-разделителей в строке:"
                             f" '{table_row}'. Пайп-разделителей должно быть 4 в 5-столбцовом (Vocab-) файле или"
                             f" 2 в 3-столбцовом (portrait-) файле")
                raise ValueError(error_msg)

            anki_card_entity = AnkiCardEntity(front, front_comment, [], [], transcription, [], back, back_comment)
            table_rows_as_anki_card_entities.append(anki_card_entity)
        # end of loop

        return table_rows_as_anki_card_entities

    def _should_proceed_with_other_fields(self, front, read_words, read_sentences):
        should_proceed = False

        is_sentence = SentenceUtils.is_sentence(front[-1])
        is_word = not is_sentence

        if read_words and is_word or read_sentences and is_sentence:
            should_proceed = True

        return should_proceed

    # Разбить список на два подсписка, начиная с элемента, начинающегося с '//' или '/*'
    def _split_into_front_and_front_comment(self, first_col_vals_list):

        front = first_col_vals_list
        front_comment = []

        for i, line in enumerate(first_col_vals_list):
            if line.startswith('//') or line.startswith('/*'):
                front = first_col_vals_list[:i]
                front_comment = first_col_vals_list[i:]
                return front, front_comment  # каждое поле Anki-карточки - это список строк

        # Если разделителя нет, вернуть список без изменений
        return front, front_comment

    def parse(self, contents):
        return self.multilingualAnkiDao.parse_contents(contents, OO_WRITER_STRIPES_DELIMITER,
                                                 OO_WRITER_STRIPE_LINES_DELIMITER)

    def read_single_file_all_tables_data(self, filename, ignore_empty_rows=True):
        all_tables_rows = []

        # Загружаем документ
        doc = load(filename)

        # Получаем все таблицы в документе
        tables = doc.getElementsByType(Table)

        # Перебираем таблицы и парсим их содержимое
        for table in tables:
            # Проверяем имя таблицы: пропускаем таблицу, если её имя заканчивается на "_ignore".
            # Этот трюк (давать именам таблиц имена, заканчивающиеся на "_ignore") нужен для того, чтобы исключить
            # таблицы, которые, например, добавлены в грамматическую справку в конце portrait-файла.
            # Если эти таблицы не игнорировать, их содержимое будет также восприниматься как немецкие слова или
            # предложения, что приведёт к некорретной работе программы.
            table_name = table.getAttribute('name')
            # Проверяем, заканчивается ли имя таблицы на "_ignore"
            if table_name and table_name.endswith('_ignore'):
                continue  # Пропускаем таблицу

            table_rows = self._parse_single_odt_table(table, ignore_empty_rows)
            all_tables_rows.extend(table_rows)

        return all_tables_rows

    def _parse_single_odt_table(self, table, ignore_empty_rows=True):
        table_rows = []

        # print(f"Table: {table.getAttribute('name')}")

        # Перебираем строки в таблице
        for row in table.getElementsByType(TableRow):
            row_cells = []
            # Перебираем ячейки в строке
            for cell in row.getElementsByType(TableCell):
                cell_paragraphs = []
                # Перебираем все параграфы (P) в ячейке
                for p in cell.getElementsByType(P):
                    paragraph_text = self._extract_text_from_element(p)  # Получаем текст параграфа
                    cell_paragraphs.append(paragraph_text)  # Добавляем параграф в список

                # Соединяем параграфы с переносами строк
                cell_text = '\n'.join(cell_paragraphs)
                processed_cell_text = self.odtCopyPasteTableDao.process_cell(cell_text)
                row_cells.append(processed_cell_text)

            # Проверка, что все элементы списка - пустые строки: ['', '', '', '', '']
            is_row_empty = all(item == '' for item in row_cells)
            if is_row_empty and ignore_empty_rows:
                continue  # пропускаем пустые строки
            else:
                piped_row_cells = '|'.join(row_cells)
                table_rows.append(piped_row_cells)

        # table_rows_str = '\n'.join(table_rows)
        # return table_rows_str

        return table_rows

    # Рекурсивная функция для извлечения текста из элементов, включая форматирование
    def _extract_text_from_element(self, element):
        text = ''
        for node in element.childNodes:
            if node.nodeType == node.TEXT_NODE:
                text += node.data
            elif node.nodeType == node.ELEMENT_NODE:
                text += self._extract_text_from_element(node)  # Рекурсивная обработка вложенных элементов
        return text


#################################

if __name__ == '__main__':
    language = CurrentLanguageComboBoxEnum.GERMAN.value
    # language = CurrentLanguageComboBoxEnum.MODERN_GREEK.value
    # language = CurrentLanguageComboBoxEnum.ANCIENT_GREEK.value
    AppContext.switch_language(language)
    base_dir = AppContext.get_base_dir()

    odtFileTableDao = OdtFileTableDao()

    # all_rows_of_all_tables_of_all_files = odtFileTableDao.read_all_vocab_files_data()
    # output = '\n'.join(all_rows_of_all_tables_of_all_files)
    # print(output)

    # table_rows_as_anki_card_entities = odtFileTableDao.convert_table_rows_to_anki_cards()
    # print(len(table_rows_as_anki_card_entities))

    # filenames = FilenameUtils.get_all_vocab_filenames()
    # print(filenames)

    # portrait_lookup_selection = fr'{goethe_institut_dir}\A1\Gg\Gg (portrait).odt'
    # res = odtFileTableDao.convert_table_rows_to_anki_cards_of_single_file(
    #     filename=portrait_lookup_selection, read_words=False, read_sentences=True)
    # [print(r) for r in res]

    table_rows_as_anki_card_entities = odtFileTableDao.convert_table_rows_to_anki_cards_of_single_file(
        fr'{base_dir}\Cc-Dd\[!Vocab] Cc-Dd.odt', read_words=True, read_sentences=False)
    [print(r) for r in table_rows_as_anki_card_entities]
