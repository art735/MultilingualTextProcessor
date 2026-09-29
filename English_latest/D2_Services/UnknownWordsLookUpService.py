from Core import RepositorySearcher
from EnglishConstants import NEWLINE


def lookUp(unknown_words, dictionary_dict):
    # попробовать поискать незнакомые системе слова в "большом" словаре (в EnglishDictionary.xls)

    output_unknown_words = list()
    for (word_to_search, word_lemma, pos_tag) in unknown_words:
        found_result = RepositorySearcher.search(word_to_search, word_lemma, pos_tag, dictionary_dict)
        if found_result:
            printable_result = str(found_result.record)
        else:
            printable_result = word_to_search

        output_unknown_words.append(printable_result)

    return NEWLINE.join(output_unknown_words)

########################################

# unknown_words = [('men', 'NNS'), ('is', 'VBZ')]
# unknown_words = [('is', 'be', 'VBZ')]
# dictionary_dict = ExcelDaoEnglishDictionary.get_EnglishDictionary_dict()
#
# res = lookUp(unknown_words, dictionary_dict)
# print(res)
