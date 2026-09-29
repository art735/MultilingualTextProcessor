# from importlib.machinery import SourceFileLoader
#
# excelDao = SourceFileLoader('ExcelDao', '../CommonDAO/LocalDAO/ExcelDaoEnglishTopics.py').load_module()
# utils = SourceFileLoader('Utils', '../CommonBusinessLogic/Utils.py').load_module()
# tokenizer = SourceFileLoader('Tokenizer', '../CommonBusinessLogic/Tokenizer.py').load_module()
# vocabularyWordsService = SourceFileLoader('VocabularyWordsService',
#                                           '../CommonBusinessLogic/VocabularyWordsService.py').load_module()

import Tokenizer
import VocabularyWordsService
import ExcelDaoEnglishTopics

# def lookUpNewWords(rawWordsToLookUp, wordsToLookUp, tuplesTop5000):
#     results = list()
#     for i in range(0, len(wordsToLookUp)):
#         for row in tuplesTop5000:
#             result = [rawWordsToLookUp[i], None, None]
#             if wordsToLookUp[i] == row[0]:
#                 transcription = row[1]
#                 translation = row[2]
#                 result = [rawWordsToLookUp[i], transcription, translation]
#                 break
#         res = "{0}\t{1}\t{2}".format(result[0], result[1], result[2])
#         results.append(res)
#
#     return results

tokenizer = Tokenizer()


def produceTextTranscription(text, vocabulary):
    result = ""
    words = tokenizer.tokenize(text, True, True)

    for word in words:
        result += lookUpWordTranscription(word, vocabulary)
        result += " "

    result = result.strip()  # trim trailing whitespace
    result = "[{0}]".format(result)  # surround with []
    print(result)


def lookUpWordTranscription(wordToLookup, vocabulary):
    transcription = "#None#"

    immediate_transcription = immediate_transcription_dict.get(wordToLookup)
    if immediate_transcription is not None:
        transcription = immediate_transcription
    else:
        for vocabularyTuple in vocabulary:
            if wordToLookup == vocabularyTuple[0]:
                transcription = vocabularyTuple[1]
                break

    if "[" in transcription:
        transcription = transcription[1:-1]  # trims first and last []

    return transcription


# The get() method returns the value of the item with the specified key. If key not found, returns None


immediate_transcription_dict = dict()
immediate_transcription_dict["am"] = "[æm/əm]"
immediate_transcription_dict["is"] = "[ɪz]"
immediate_transcription_dict["are"] = "[ɑː(r)]"
immediate_transcription_dict["has"] = "[hæz/həz/əz]"

##########################################################################

# Step 1. Вычитать слова с транскрипциями из Excel-файла
# mode = {'CURRENT_ONLY', 'UP_TO_CURRENT_INCLUDING', 'ALL'}
wordsWithTranscriptions = ExcelDaoEnglishTopics.getVocabularyWordsWithTranscriptions('UP_TO_CURRENT_INCLUDING')

# Step 2. "Развернуть" словарь, чтобы, например, формы неправильных глаголов были как отдельные слова со своими транскрипциями
# [('to see (saw; seen)', '[siː] ([sɔː]; [siːn])')] ⇒ [('see', '[siː]'), ('saw', '[sɔː]'), ('seen', '[siːn]')]
unfoldedWordsWithTranscriptions = VocabularyWordsService.unfold(wordsWithTranscriptions)

# Step 3. Разбить текст на предложения и для каждого предложения составить транскрипцию

text_sentences = list()
text_sentences.append("I am Max Kovaliov")
text_sentences.append("I am seventeen years old")
text_sentences.append("I want to tell you a few words about my family")
text_sentences.append("My family is large")
text_sentences.append("I have got a mother, a father, a sister, a brother, and a grandmother")
text_sentences.append("There are six of us in the family")
text_sentences.append("First of all, some words about my parents")
text_sentences.append("My mother is a history teacher")
text_sentences.append("She works in a college")
text_sentences.append("She likes her profession")

# TODO сделать текст и слова lowercase!!!!!!!

res = produceTextTranscription(text_sentences[0], unfoldedWordsWithTranscriptions)
print(res)
