import re

import ExcelDaoEnglishDictionary
import ExcelDaoEnglishVocabulary
import LingvoService
from EnglishConstants import NEWLINE, DOUBLE_NEWLINE


def _find_in_repository(word, repository):
    matched_records_dict = dict()

    # Искать записи репозитория, которые частично или полностью содержали бы искомое слово как среди ключей, так и среди значений
    # "частично" в данном случае означает, что искомое слово находится в репозитории как отдельное слово (\b...\b)
    # Например, при искомом слове 'close' должны быть найдены следующие записи репозитория:
    # close	[kləuz]	конец
    # close (adj.)	[kləus]	закрытый
    # close (adv.)	[kləus]	близко, около; рядом
    # to close	[kləuz]	закрывать(ся)
    # Но НЕ должна быть найдена запись:
    # closeable ['kləʊzəbəl] закрываемый
    # т. к. 'close' не является отделённой флагами (\b...\b) частью 'closeable'

    # При искомом слове is, должна быть найдена словарная статья глагола to be

    # if '.' in word:
    #     word = word.replace('.', '[.]')
    # if '(' in word:
    #     word = word.replace(r'\(', '')
    # if ')' in word:
    #     word = word.replace(r'\)', '')

    for k, v in repository.items():
        if re.search(r'\b{}\b'.format(word), k):  # ищем вхождение среди КЛЮЧЕЙ репозитория
            if k not in matched_records_dict:
                matched_records_dict[k] = repository[k]
        else:
            for mf in v.morphological_forms:
                mf_word = mf[0]
                if re.search(r'\b{}\b'.format(word), mf_word):  # ищем вхождение среди ЗНАЧЕНИЙ репозитория
                    if k not in matched_records_dict:
                        matched_records_dict[k] = repository[k]

    return matched_records_dict.values()


def look_up(input_text):
    if len(input_text) == 0:
        return ""

    vocabulary_records = ['VOCABULARY:']
    dictionary_records = ['DICTIONARY:']
    lingvo_records = ['LINGVO:']
    delay_between_requests = 1  # delay (in seconds) between requests to Lingvo

    words = [s for s in input_text.split("\n") if len(s)]  # взять в дальнейшую работу только непустые строки

    vocabulary_dict = ExcelDaoEnglishVocabulary.get_EnglishVocabulary_dict()
    dictionary_dict = None

    for word in words:
        # При поиске в репозиториях (vocabulary_dict & dictionary_dict) приводить слово поиска к нижнему регистру - word.lower(),
        # а при поиске в Lingvo - нет (иначе имена собственные не будут правильно искаться)
        matched_vocabulary_records = _find_in_repository(word.lower(), vocabulary_dict)
        if len(matched_vocabulary_records):
            vocabulary_records.extend(matched_vocabulary_records)
        else:
            if dictionary_dict is None:
                dictionary_dict = ExcelDaoEnglishDictionary.get_EnglishDictionary_dict()
            matched_dictionary_records = _find_in_repository(word.lower(), dictionary_dict)
            if len(matched_dictionary_records):
                dictionary_records.extend(matched_dictionary_records)
            else:
                # look up in Lingvo
                # print("stub")
                lingvo_records.append(LingvoService.get_word_from_Lingvo(word, delay_between_requests))

    output_vocabulary = ""
    if len(vocabulary_records) > 1:
        output_vocabulary = NEWLINE.join([str(r) for r in vocabulary_records])

    output_dictionary = ""
    if len(dictionary_records) > 1:
        output_dictionary = NEWLINE.join([str(r) for r in dictionary_records])

    output_lingvo = ""
    if len(lingvo_records) > 1:
        output_lingvo = NEWLINE.join([str(r) for r in lingvo_records])

    outputs = [output_vocabulary, output_dictionary, output_lingvo]
    output = DOUBLE_NEWLINE.join([output for output in outputs if len(output)])
    return output

###############################

# input_text = ""
# input_text = "the"
# input_text = "cat\ndog\nmoon"
# input_text = "the\ncat\ndog\nmoon"
# input_text = "mum"
# input_text = "the\ncat\ndog\nmoon\nmum"

# input_text = "close"
# input_text = "\ncat\ndog\nmoon\nclose\nmum\nzuza"
# input_text = "closer"
# input_text = "been"
# input_text = "Moscow"
# input_text = "USA"
# res = look_up(input_text)
# print(res)
