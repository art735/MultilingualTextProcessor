import collections

import Lemmatizer
import Tokenizer
import Utils
import VocabularyWordsService


# from importlib.machinery import SourceFileLoader
# utils = SourceFileLoader('Utils', '../CommonBusinessLogic/Utils.py').load_module()
# tokenizer = SourceFileLoader('Tokenizer', '../CommonBusinessLogic/Tokenizer.py').load_module()
# vocabularyWordsService = SourceFileLoader('VocabularyWordsService', '../CommonBusinessLogic/VocabularyWordsService.py').load_module()
# lemmatizer = SourceFileLoader('Lemmatizer', '../CommonBusinessLogic/Lemmatizer.py').load_module()


def countWordFrequencies(words):
    # Тип данных именно collections.OrderedDict(), чтобы порядок слов в таком словаре следовал естественному порядку
    # появления слов в тексте
    freq_dict = collections.OrderedDict()
    for word in words:
        smartAddWordToDict(word, freq_dict, 1)
        # if word not in freq_dict:
        #     freq_dict[word] = 1
        # else:
        #      freq_dict[word] = freq_dict[word] + 1

    # freq_dict = dict(sorted(freq_dict.items(), key = lambda t:t[1], reverse = True))
    return freq_dict


def smartAddWordToDict(word, dict, frequency):
    if word not in dict:
        dict[word] = frequency
    else:
        # плюсуем к ранее существовшей в словаре частоте значение аргумента frequency
        dict[word] += frequency


def chooseKnownWords(wordsFreq_dict, vocabularyWords):
    knownWordsFreq_dict = collections.OrderedDict()

    wordsToDeleteFrom_wordsFreq_dict = list()

    for word, freq in wordsFreq_dict.items():
        # 1) Если слово из текста находится в вокабуляре - оно, конечно же, known!
        # or
        # 2) Если слово "как есть" из текста не совпадает ни с одним из слов вокабуляра напрямую,
        # но совпадает после лемматизации, оно тоже known!

        # Python evaluates boolean conditions lazily: the expression x OR y first evaluates x;
        # if x is true, its value is returned; otherwise, y is evaluated and the resulting value is returned.
        if (word in vocabularyWords):
            # добавить слово в словарь knownWords
            smartAddWordToDict(word, knownWordsFreq_dict, freq)
            wordsToDeleteFrom_wordsFreq_dict.append(word)
        else:
            [isLemmatizationSuccessful, lemmatizedWord] = Lemmatizer.lemmatize(word, vocabularyWords)
            if isLemmatizationSuccessful:
                smartAddWordToDict(lemmatizedWord, knownWordsFreq_dict, freq)
                wordsToDeleteFrom_wordsFreq_dict.append(word)

    # удалить из wordsFreq_dict те слова, которые признаны в качестве knownWords
    # таким образом в wordsFreq_dict останутся действительно новые слова
    for wordToDelete in wordsToDeleteFrom_wordsFreq_dict:
        del wordsFreq_dict[wordToDelete]

    return knownWordsFreq_dict


# minuend ['mɪnjuːend] мат. уменьшаемое
# subtrahend ['sʌbtrəhend] мат. вычитаемое
# difference ['dɪf(ə)r(ə)ns] мат. разность
# minuend_dict minus subtrahend_dict
def subtractDictionaries(minuend_dict, subtrahend_dict):
    for k in subtrahend_dict.keys():
        if k in minuend_dict:
            del minuend_dict[k]


# Если в "главном" OrderedDict словаре присутствует значение, являющееся одним из ключей замещающего словаря, тогда:
# key главного словаря подменяется на value замещающего словаря
# value главного словаря заменяется на key замещающего словаря
# Данный метод участвует в обработке "составных" слов, таких как непр. глаголы и др.
def revertTemporaryReplacementsInDictionaries(main_dict, replacing_dict):
    for k, v in replacing_dict.items():
        if v in main_dict:
            change_key(main_dict, v, k)


# Подменить ключ в существующем OrderedDict без нарушения порядка следования ключей
# Удалить старое значение и добавить новое - проще, но нарушится порядок следования ключей в OrderedDict
# поэтому работаем сложнее, но элегантнее
# This works by iterating over the whole OrderedDict (using its length),
# and pop'ing its first item (by passing False to .popitem(): the default of this method is to pop the last item) into k and v (respectively standing for key and value);
# and then inserting this key/value pair, or the new key with its original value, at the end of the OrderedDict.
# By repeating this logic for the entire size of the dict, it effectively rotates the dict completely, thus recreating the original order.
def change_key(dict, old_key, new_key):
    for _ in range(len(dict)):
        k, v = dict.popitem(False)
        dict[new_key if old_key == k else k] = v


###################################################
################### MAIN METHOD ###################
###################################################

# 1st argument: 'text' - any English text to find new_key words in
# 2nd argument: 'vocabularyTuplesOfKnownWords' - list of tuples; each tuple is a data structure containing:
#       - English word itself
#       - transcription(s) (RP, GA)
#       - maybe another info (tuple structure may be changing over time)

tokenizer = Tokenizer()


def process(text, vocabularyWords, ignoredWords):
    rawWords = tokenizer.tokenize(text, False, True)

    # BEGIN Выделить из общего поступившего списка словарных слов - СЛОЖНЫЕ слова и сделать их временную замену
    # key (of compoundWords_dict) - compound word "as it is" in vocabulary in Excel cell
    # value (of compoundWords_dict) - initial word form
    compoundWords_dict = VocabularyWordsService.preprocessCompoundVocabularyWords(vocabularyWords)

    # 1) заменить (replace) "сложные" слова в vocabularyWords на их начальные формы, хранящиеся в value словаря compoundWords_dict
    # 2) провести весь процессинг
    # 3) в самом конце процессинга сделать обратную замену: начальные формы сложных слов заменить их первоначальным видом

    # 1) заменить (replace) "сложные" слова в vocabularyWords на их начальные формы, хранящиеся в value словаря compoundWords_dict
    for k, v in compoundWords_dict.items():
        if k in vocabularyWords:
            # Узнать индекс элемента в списке vocabularyWords, подлежащего временной замене
            index = vocabularyWords.index(k)
            # Произвести временную замену
            vocabularyWords[index] = v
    # END

    # Convert all input data to lowercase
    rawWordsLowercase = [rword.lower() for rword in rawWords]
    vocabularyWords = [lword.lower() for lword in vocabularyWords]
    ignoredWords = [iword.lower() for iword in ignoredWords]

    pureWords = Utils.subtract_lists(rawWordsLowercase, ignoredWords)

    wordsFreq_dict = countWordFrequencies(pureWords)

    # Выписать knownWords в отдельный словарь:
    # слово из текста считается known, если оно совпадает с одним из слов вокабуляра напрямую, либо после лемматизации
    knownWordsFreq_dict = chooseKnownWords(wordsFreq_dict, vocabularyWords)
    ##printDict(knownWordsFreq_dict)

    # Delete from "wordsFreq_dict" words that are in "knownWordsFreq_dict"
    # subtractDictionaries(wordsFreq_dict, knownWordsFreq_dict)

    # replaceKeyValuePairsInDictionaries(main_dict, replacing_dict)
    revertTemporaryReplacementsInDictionaries(knownWordsFreq_dict, compoundWords_dict)

    return [knownWordsFreq_dict, wordsFreq_dict]
