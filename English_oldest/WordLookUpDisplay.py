from importlib.machinery import SourceFileLoader

# excelDao = SourceFileLoader('ExcelDao', './DAO/ExcelDaoEnglishTopics.py').load_module()
txtDao = SourceFileLoader('TxtDao', 'CommonDAO/LocalDAO/TxtDao.py').load_module()

lingvoTranscriptionDao = SourceFileLoader('LingvoTranscriptionDao',
                                          'CommonDAO/NetworkDAO/LingvoTranscriptionDao.py').load_module()
lingvoTranslationDao = SourceFileLoader('LingvoTranslationDao',
                                        'CommonDAO/NetworkDAO/LingvoTranslationDao.py').load_module()


def getTranscription(word):
    transcription = lingvoTranscriptionDao.getTranscription(word)
    return transcription


def getTranslation(word):
    # time.sleep(1)
    translation = lingvoTranslationDao.getTranslation(word)

    attempts = 0
    while translation == "":
        translation = lingvoTranslationDao.getTranslation(word)
        attempts = attempts + 1
        if attempts == 5:
            exit(1)

    return translation


########################################

# wordsToLookUp = excelDao.getCurrentWorksheet1stColWords()
# wordsToLookUp = txtDao.readLinesFromFile("../resources/wordsToLookUp.txt")
wordsToLookUp = ['cat', 'dog']

##print(words)

import re

WHITESPACE_CHARACTER = " "
NON_BREAKING_SPACE_CHARACTER = '\xc2\xa0'

current_word_pointer = 1

for wordToLookUp in wordsToLookUp:
    if current_word_pointer == 1:
        pattern = "[{0}]".format(NON_BREAKING_SPACE_CHARACTER)
        wordToLookUp = re.sub(pattern, WHITESPACE_CHARACTER, wordToLookUp)

    transcription = getTranscription(wordToLookUp)
    translation = getTranslation(wordToLookUp)

    result = "{0}\t{1}\t{2}\t{3}".format(current_word_pointer, wordToLookUp, transcription, translation)
    # result = "{0}\t{1}\t{2}".format(wordToLookUp, transcription, translation)
    # result = "{0}\t{1}".format(wordToLookUp, transcription)
    print(result)

    current_word_pointer = current_word_pointer + 1
