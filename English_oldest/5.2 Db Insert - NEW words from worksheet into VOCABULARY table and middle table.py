from importlib.machinery import SourceFileLoader

import Constants

dbDao = SourceFileLoader('DbDao', './DAO/DbDao.py').load_module()
excelDao = SourceFileLoader('ExcelDao', './DAO/ExcelDaoEnglishTopics.py').load_module()
txtDao = SourceFileLoader('TxtDao', './DAO/TxtDao.py').load_module()


def prepareWordsForDbEngine(newWordsLines):
    newWordsLinesEscaped = list()
    for [word, freq, transcription] in newWordsLines:
        word = word.lower()
        if ("'" in word):
            word = word.replace("'", "\'")
        newWordsLinesEscaped.append([word, freq, transcription])

    return newWordsLinesEscaped


def prepareWordTranscriptionList(newWordsLines):
    wordTranscription_list = list()

    for [word, freq, transcription] in newWordsLines:
        wordTranscription_list.append([word, transcription])

    return wordTranscription_list


def createWordFreqList(newWordsLines):
    wordFreq_list = list()
    for [word, freq, transcription] in newWordsLines:
        wordFreq_list.append([word, freq])
    return wordFreq_list


########################################################################################

newWordsLines = excelDao.getCurrentWorksheet3ColContents()
newWordsLines = prepareWordsForDbEngine(newWordsLines)

##newWordsFilename = txtDao.composeNewWordsFilename()
##newWordsLines = txtDao.readLinesFromFile(newWordsFilename)

# STEP 1. INSERT newWords tuples [newWord, transcription] INTO VOCABULARY table
wordTranscription_list = prepareWordTranscriptionList(newWordsLines)
dbDao.insertWordTranscriptionListIntoVocabularyTable(wordTranscription_list)

# STEP 2. Get id-s of just inserted newWords
newWords_list = [word for [word, transcription] in wordTranscription_list]
wordId_dict = dbDao.getDbWordIdDictForNewWords(newWords_list)

# STEP 3. INSERT newWords related info into middle table
wordFreq_list = createWordFreqList(newWordsLines)

###
linesToBeInsertedIntoDb = dbDao.createMiddleTableInsertList(wordFreq_list, wordId_dict, Constants.NEW_STATUS)
dbDao.insertWordsInfoListIntoMiddleTable(linesToBeInsertedIntoDb)
