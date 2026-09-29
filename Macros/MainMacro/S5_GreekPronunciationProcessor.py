# -*- coding: utf-8 -*-
# import uno
from com.sun.star.awt.FontUnderline import SINGLE, NONE
from com.sun.star.beans import PropertyValue

# from MultilingualTextProcessorPathsImporter import MultilingualTextProcessorPathsImporter
# multilingualTextProcessorPathsImporter = MultilingualTextProcessorPathsImporter()
# multilingualTextProcessorPathsImporter.import_paths()

import GreekPronunciationPatternsComposer
from A1_GreekPronunciationUnderliner import A1_GreekPronunciationUnderliner

def process(doc):
    search_descriptor = doc.createSearchDescriptor()
    search_descriptor.SearchRegularExpression = True

    replace_descriptor = doc.createReplaceDescriptor()
    replace_descriptor.SearchRegularExpression = True

    # 1. Правила палатализации работают только внутри слов, но не на стыках между соседними словами
    consonant_plus_unstressed_i_plus_vowel_patterns = GreekPronunciationPatternsComposer.get_consonant_plus_unstressed_i_plus_vowels()
    for pattern in consonant_plus_unstressed_i_plus_vowel_patterns:
        # search_descriptor = doc.createSearchDescriptor()
        search_descriptor.SearchString = pattern
        find_all_and_underline(search_descriptor, doc)

    # 2. Отменяем некоторые подчёркивания и только после этого выполняем этап №3 - подчёркивание правил чтения
    # на стыках слов
    remove_underlining_from_sequences_inside_exceptional_words(search_descriptor, doc)

    # 3. Самым последним шагом подчёркиваем правила чтения на стыках слов. Это важно делать после этапа 2, который
    # частично отменяет подчёркивания в пределах тех или иных слов-исключений.
    other_patterns = GreekPronunciationPatternsComposer.get_other_patterns()
    for pattern in other_patterns:
        search_descriptor.SearchString = pattern
        find_all_and_underline(search_descriptor, doc)

def find_all_and_underline(search_descriptor, doc):
    found_pieces = doc.findAll(search_descriptor)
    for i in range(found_pieces.getCount()):
        found_text = found_pieces.getByIndex(i)
        # found_text.CharUnderline = com.sun.star.awt.FontUnderline.SINGLE
        found_text.CharUnderline = SINGLE
        # found_text.setPropertyValue("CharUnderline", 1)  # 1 = SINGLE underline

# def remove_underlining(self, search_string):
#     prop = PropertyValue()
#     prop.Name = "CharUnderline"
#     prop.Value = com.sun.star.awt.FontUnderline.NONE
#
#     replace_descriptor.setSearchString(search_string)
#     replace_descriptor.setReplaceString("$0")
#     replace_descriptor.ReplaceAttributes = (prop,)
#
#     doc.replaceAll(replace_descriptor)


def remove_underlining_from_sequences_inside_exceptional_words(search_descriptor, doc):

    # После всех подчёркиваний — применяем исключения
    # Система работает максимально гибко, т. к. поддерживает задание подстрок для удаления подчёркивания внутри
    # слова следующими способами:
    # 1) с помощью букв ('διάλεξη': ['διά'])
    # 2) с помощью диапазона индексов начала и конца подстроки, заданного кортежем ('διάλεξη': [(0, 3)])
    # 3) комбинацией вариантов 1 и 2 ('διαγώνιος': [(0, 3), 'νιο'])
    # Вариант №3 также полезен для случая, когда слово содержит несколько одинаковых подстрок, а удалить
    # подчёркивание нужно только в некоторых из них (трудно придумать пример, но в теории такой вариант нельзя исключать).
    exceptions_dict = A1_GreekPronunciationUnderliner.exceptions_dict

    for exception_word, substrings_to_clear in exceptions_dict.items():
        # Ищем все вхождения слова
        search_descriptor.SearchString = exception_word
        # search_descriptor.SearchCaseSensitive = True
        found_ranges = doc.findAll(search_descriptor)

        for i in range(found_ranges.getCount()):
            found = found_ranges.getByIndex(i)
            word_text = found.getString()
            cursor = doc.Text.createTextCursorByRange(found)

            for substring in substrings_to_clear:
                if isinstance(substring, str):
                    # Снимаем подчёркивание со всех вхождений подстроки
                    start = 0
                    while True:
                        idx = word_text.find(substring, start)
                        if idx == -1:
                            break
                        cursor.gotoRange(found.getStart(), False)
                        cursor.goRight(idx, False)
                        cursor.goRight(len(substring), True)
                        cursor.CharUnderline = NONE
                        start = idx + 1

                elif isinstance(substring, tuple) and len(substring) == 2:
                    start_idx, end_idx = substring
                    if 0 <= start_idx < end_idx <= len(word_text):
                        cursor.gotoRange(found.getStart(), False)
                        cursor.goRight(start_idx, False)
                        cursor.goRight(end_idx - start_idx, True)
                        cursor.CharUnderline = NONE

                # elif isinstance(substring, tuple) and len(substring) == 2:
                #     start_idx, end_idx = substring
                #     if 0 <= start_idx < end_idx <= len(word_text):
                #         # создаём курсор из found, двигаемся внутри него
                #         sub_cursor = doc.Text.createTextCursorByRange(found)
                #         sub_cursor.goRight(start_idx, False)
                #         sub_cursor.goRight(end_idx - start_idx, True)
                #         sub_cursor.CharUnderline = NONE
