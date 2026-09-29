import sys

import mysql.connector

from LocalDAO import ConfigDao


# from importlib.machinery import SourceFileLoader
# configDao = SourceFileLoader('ConfigDao', '../CommonDAO/LocalDAO/ConfigDao.py').load_module()

############# DATABASE DAO #############

def selectOneRowHelperMethod(selectQuery):
    connection = connectToDb()
    cursor = connection.cursor()

    cursor.execute(selectQuery)
    row = cursor.fetchone()

    connection.close()
    return row


def selectManyRowsHelperMethod(selectQuery):
    connection = connectToDb()
    cursor = connection.cursor()

    cursor.execute(selectQuery)
    rows = cursor.fetchall()

    connection.close()
    return rows


def connectToDb():
    try:
        dbConfig = ConfigDao.getDbConfig()
        connection = mysql.connector.connect(**dbConfig)
    except Exception as e:
        sys.exit('Cannot connect to a database')
    return connection


### TOPIC-TABLE-START ###

def getTopic(theme, number):
    select_part = "SELECT title, text FROM topic "
    where_part = "WHERE theme = '{0}' AND number = {1}".format(theme, number)
    query = select_part + where_part

    row = selectOneRowHelperMethod(query)

    text = processTopicRow(row)
    return text


def getAllTopicsByTheme(theme):
    where_part = "WHERE theme = '{0}'".format(theme)
    text = __getManyTopics(where_part)
    return text


def getTopicsRange(theme, startTopicIndex, endTopicIndex):
    where_part = "WHERE theme = '{0}' AND number BETWEEN {1} AND {2}".format(theme, startTopicIndex, endTopicIndex)
    text = __getManyTopics(where_part)
    return text


def __getManyTopics(where_part):
    select_part = "SELECT title, text FROM topic "
    query = select_part + where_part
    rows = selectManyRowsHelperMethod(query)

    text = ""
    for row in rows:
        text += processTopicRow(row)

    return text


def processTopicRow(row):
    title = row[0]
    text = row[1]
    ##    data = "{0} {1} ".format(title, text)
    ##    return data
    return "{0} {1} ".format(title, text)

    ### TOPIC-TABLE-END ###


def getNewIdWordListFromVocabularyTable(newWords_list):
    tupleOfParameters = (newWords_list,)

    select_part = "SELECT vocabulary_id, word FROM VOCABULARY "
    where_part = "WHERE word = %s".format(tupleOfParameters)
    # where_part = "WHERE IN(%s)".format((newWords_list,))
    query = select_part + where_part

    rows = selectManyRowsHelperMethod(query)

    newIdWord_list = list()
    for row in rows:
        vocabulary_id = row[0]
        word = row[1]
        newIdWord_list.append([vocabulary_id, word])

    return newIdWord_list


### INSERT METHODS ###

def insertWordTranscriptionListIntoVocabularyTable(wordTranscription_list):
    insert_part = "INSERT INTO vocabulary (word, transcription) "
    values_part = "VALUES (%s, %s)"
    query = insert_part + values_part

    insertListOfTuplesHelperMethod(query, wordTranscription_list)


def insertWordsInfoListIntoMiddleTable(wordsInfoList):
    insert_part = "INSERT INTO topic_to_vocabulary (top_to_voc_topic_id, top_to_voc_vocabulary_id, top_to_voc_frequency, top_to_voc_status) "
    values_part = "VALUES (%s, %s, %s, %s)"
    query = insert_part + values_part

    insertListOfTuplesHelperMethod(query, wordsInfoList)


def insertListOfTuplesHelperMethod(insertQuery, listOfTuples):
    connection = connectToDb()
    cursor = connection.cursor()

    try:
        # insert list of tuples at a time
        cursor.executemany(insertQuery, listOfTuples)
        connection.commit()
    except:
        print("Exceptions have happened during insert operation.")
        connection.rollback()

    connection.close()


### VOCABULARY-TABLE-BEGIN ###

def getDbWordIdDictForAllWords():
    vocabularyTuples = getDbVocabularyTuples()

    wordId_dict = dict()
    for [vocabulary_id, word, *other] in vocabularyTuples:
        wordId_dict[word] = vocabulary_id

    return wordId_dict


def getDbWordIdDictForNewWords(newWords_list):
    vocabularyTuples = getDbVocabularyTuples()

    wordId_dict = dict()
    for [vocabulary_id, word, *other] in vocabularyTuples:
        if (word in newWords_list):
            wordId_dict[word] = vocabulary_id

    return wordId_dict


def getDbVocabularyWords():
    vocabularyTuples = getDbVocabularyTuples()
    ##    words = list()
    ##    for [vocabulary_id, word, *other] in wordsWithTranscriptions:
    ##        words.append(word)
    words = [word for [vocabulary_id, word, *other] in vocabularyTuples]
    return words


def getDbVocabularyTuples():
    query = "SELECT * FROM vocabulary"
    rows = selectManyRowsHelperMethod(query)

    vocabularyTuples = list()
    for row in rows:
        vocabulary_id = row[0]
        word = row[1].replace('\ufeff', '').lower()
        transcription = row[2]
        translation = row[3]
        vocabularyTuples.append([vocabulary_id, word, transcription, translation])

    return vocabularyTuples

    ### VOCABULARY-TABLE-END ###


########### BUSINESS LOGIC #################

def createMiddleTableInsertList(wordFreq_list, wordId_dict, status):
    [themeNumber, themeName, topicNumber] = getTopicEnvironmentFromConfig()

    tuplesToBeInsertedIntoDb = list()

    for [word, freq] in wordFreq_list:
        word_id = wordId_dict[word]

        # важно, чтобы каждую вставляемую в базу строчку представлял именно tuple
        insert_tuple = [topicNumber, word_id, freq, status]
        tuplesToBeInsertedIntoDb.append(insert_tuple)

    return tuplesToBeInsertedIntoDb
