from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer

wordNetLemmatizer = WordNetLemmatizer()


# def lemmatize(word):
#     lemmatizedAsNoun = wordNetLemmatizer.lemmatize(word, wordnet.NOUN)
#     lemmatizedAsAdjective = wordNetLemmatizer.lemmatize(word, wordnet.ADJ)
#     lemmatizedAsVerb = wordNetLemmatizer.lemmatize(word, wordnet.VERB)
#     lemmatizedAsAdverb = wordNetLemmatizer.lemmatize(word, wordnet.ADV)
#
#     return [lemmatizedAsNoun, lemmatizedAsAdjective, lemmatizedAsVerb, lemmatizedAsAdverb]

def lemmatize(word, vocabularyWords):
    args = [wordnet.NOUN, wordnet.ADJ, wordnet.VERB, wordnet.ADV]

    # False - means that lemmatization gave nothing
    result = [False, word]

    for i in range(0, len(args) - 1):
        lemmatizedWord = wordNetLemmatizer.lemmatize(word, args[i])
        if lemmatizedWord in vocabularyWords:
            result = [True, lemmatizedWord]
            break

    return result

# def canWordBeConsideredAsKnownAfterLemmatization(word, vocabularyWords):
#
#     lemmatizedWord = ""
#
#     if (lemmatizedWord := wordNetLemmatizer.lemmatize(word, wordnet.NOUN)) in vocabularyWords:
#         return True
#     elif wordNetLemmatizer.lemmatize(word, wordnet.ADJ) in vocabularyWords:
#         return True
#     elif wordNetLemmatizer.lemmatize(word, wordnet.VERB) in vocabularyWords:
#         return True
#     elif wordNetLemmatizer.lemmatize(word, wordnet.ADV) in vocabularyWords:
#         return True
#     else:
#         return False


####################################
###### OLD CODE ####################
###### TO DELETE OVE TIME ##########

# def lemmatizeAsNouns(wordsFreq_dict):
#     return lemmatizeWords(wordsFreq_dict, wordnet.NOUN)
#
#
# def lemmatizeAsAdjectives(wordsFreq_dict):
#     return lemmatizeWords(wordsFreq_dict, wordnet.ADJ)
#
# def lemmatizeAsVerbs(wordsFreq_dict):
#     return lemmatizeWords(wordsFreq_dict, wordnet.VERB)
#
# def lemmatizeAsAdverbs(wordsFreq_dict):
#     return lemmatizeWords(wordsFreq_dict, wordnet.ADV)
#
# # key - string
# # value - list of [word,freq] pairs
# def lemmatizeWords(wordsFreq_dict, pos_tag):
#     wordNetLemmatizer = WordNetLemmatizer()
#     lemmas_dict = dict()
#     for rawWord, freq in wordsFreq_dict.items():
#         lemWord = wordNetLemmatizer.lemmatize(rawWord, pos_tag)
#         if(lemWord not in lemmas_dict):
#             val = list()
#             val.append([rawWord, freq])
#         else:
#             val = lemmas_dict[lemWord]
#             val.append([rawWord, freq])
#
#         lemmas_dict[lemWord] = val
#
#     return lemmas_dict
#
#
# def processLemmas(lemmas_dict, knownWordsFreq_dict, wordsFromDb_list, wordsFreq_dict):
#     for lemma, valFreqPairs in lemmas_dict.items():
#         if (lemma in wordsFromDb_list):
#             mergeLemmaPairsToKnownWordsFreqDict(lemma, valFreqPairs, knownWordsFreq_dict)
#             deleteLemmaPairsFromWordsFreqDict(valFreqPairs, wordsFreq_dict)
#
#
# def mergeLemmaPairsToKnownWordsFreqDict(lemmaAsDbWord, valFreqPairs, knownWordsFreq_dict):
#     lemmaAsDbWord_freq = 0
#     for [word, freq] in valFreqPairs:
#         lemmaAsDbWord_freq += freq
#
#     if(lemmaAsDbWord in knownWordsFreq_dict):
#         newFreq = knownWordsFreq_dict[lemmaAsDbWord] + lemmaAsDbWord_freq
#         knownWordsFreq_dict[lemmaAsDbWord] = newFreq
#     else:
#         knownWordsFreq_dict[lemmaAsDbWord] = lemmaAsDbWord_freq
#
#
# def deleteLemmaPairsFromWordsFreqDict(valFreqPairs, wordsFreq_dict):
#     for [word, freq] in valFreqPairs:
#         if(word in wordsFreq_dict):
#             del wordsFreq_dict[word]
#
