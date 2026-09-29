import re

import nltk

import ExcelDaoEnglishVocabulary
from Core import TranscriberCoreEngine, RepositorySearcher
from Lemmatizer import wordNetLemmatizer


def dict_to_str(words_dict):
    output = ""
    for word, count in words_dict.items():
        word_str = re.sub(r'\n', '^^^', word) if '\n' in word else word
        output += "{0}: {1}\n".format(word_str, count)
        # print(str(k))
    return output


def _count_frequency(word, words_dict):
    if word in words_dict:
        words_dict[word] += 1
    else:
        words_dict[word] = 1


def count(text):
    known_words_dict = dict()
    unknown_words_dict = dict()

    vocabulary_dict = ExcelDaoEnglishVocabulary.get_EnglishVocabulary_dict()

    tokenized_text = nltk.word_tokenize(text)
    pos_tagged_text = nltk.pos_tag(tokenized_text)
    print(pos_tagged_text)
    print("\n")

    for word_to_search, pos_tag in pos_tagged_text:
        # for i in range(0, len(pos_tagged_text)):
        #     word_to_search, pos_tag = pos_tagged_text[i]
        if any(c.isalpha() for c in pos_tag):
            word_to_search = word_to_search.lower()
            word_lemma = wordNetLemmatizer.lemmatize(word_to_search, TranscriberCoreEngine.get_wordnet_pos(pos_tag))

            # found_result - это структура данных типа RepositoryLookUpResult
            found_result = RepositorySearcher.search(word_to_search, word_lemma, pos_tag, vocabulary_dict)

            if found_result:
                _count_frequency(found_result.record.word, known_words_dict)
            else:
                unknown_word = 'to ' + word_lemma if pos_tag.startswith('VB') else word_lemma
                _count_frequency(unknown_word, unknown_words_dict)
        # end of 'if any(c.isalpha() for c in pos_tag):'
    # end of loop

    output_known_words = "Known words: {}\n".format(len(known_words_dict))
    output_known_words += dict_to_str(known_words_dict)
    # print(output_known_words)

    output_unknown_words = "Unknown words: {}\n".format(len(unknown_words_dict))
    output_unknown_words += dict_to_str(unknown_words_dict)
    # print(output_unknown_words)

    # output_list = [output_known_words, output_unknown_words]
    # output = ''.join(output_list)
    return output_known_words + output_unknown_words


#######################################

# vocabulary_dict = dict()


# text = "I have a cat. I like it very much!"
# text = "A close close is closing to a close."
# text = "A close close is closing to an ending close."
text = "a grey gray cat"

res = count(text)
print(res)

# item = RepositoryItem("grey (BrE)\ngray (AmE)", "", "")
# print(item)
