## ДАННЫЙ СКРИПТ НИГДЕ НИЧЕГО НЕ ЗАПИСЫВАЕТ И НЕ МЕНЯЕТ,
## ОН ПРОСТО ВЫВОДИТ НА КОНСОЛЬ РЕКОМЕНДАЦИИ

## Скрипт просматривает каждое слово из МОДИФИЦИРОВАННОГО ВРУЧНУЮ в Excel списка newWords и формулирует следующие заключения:
##   1) слово действительно является "новым" и ничего предпринимать не нужно
##   2) слово уже имеется в базе, значит оно не "новое", следовательно его надо удалить из списка "новых" слов в Excel и
##      интегрировать одним из двух способов в список knownWords:
##	    2.1) если список knownWords уже содержит такое слово, его частота должна быть увеличина на 1
##	    2.2) если список knownWords НЕ содержит такого слова, оно должно быть добавлено новой строкой с частотой 1

from importlib.machinery import SourceFileLoader

dbDao = SourceFileLoader('DbDao', './DAO/DbDao.py').load_module()
excelDao = SourceFileLoader('ExcelDao', './DAO/ExcelDaoEnglishTopics.py').load_module()
txtDao = SourceFileLoader('TxtDao', './DAO/TxtDao.py').load_module()

from sys import exit

dbVocabulary_words = dbDao.getDbVocabularyWords()
##dbVocabulary_words = ['a', 'airplane', 'method', 'cat', 'plum']

wordsToValidate = excelDao.getCurrentWorksheet1stColWords()
##wordsToValidate = txtDao.readWordsFromFile("wordsToValidate.txt")
##wordsToValidate = ['dog', 'the', 'a', 'plum']

knownWordsFilename = txtDao.composeKnownWordsFilename()
knownWords = txtDao.readWordsFromFile(knownWordsFilename)
##knownWords = ['a', 'airplane', 'method', 'cat']

# validate to prevent duplicates
wordsToValidate_set = set(wordsToValidate)

if (len(wordsToValidate) != len(wordsToValidate_set)):
    print("!!! EXCEL WORKSHEET CONTAINS DUPLICATES !!!")
    exit()

words_toBeMergedTo_knownWords = list()
words_toBeAddedTo_knownWords = list()

nonNewWords = [item for item in wordsToValidate if item in dbVocabulary_words]

for nonNewWord in nonNewWords:
    if (nonNewWord in knownWords):
        words_toBeMergedTo_knownWords.append(nonNewWord)
    else:
        words_toBeAddedTo_knownWords.append(nonNewWord)

if (len(words_toBeMergedTo_knownWords) == 0 and len(words_toBeAddedTo_knownWords) == 0):
    print("Validation is successful! All the words are really NEW!")
else:
    if (len(words_toBeMergedTo_knownWords) > 0):
        print(
            "These words are already both in DB and in knownWords list, so DELETE them from Excel worksheet and MERGE to knownWords list incrementing their frequency:")
        print(words_toBeMergedTo_knownWords)

    if (len(words_toBeAddedTo_knownWords) > 0):
        print(
            "These words are already in DB, but not in knownWords list, so DELETE from Excel worksheet and ADD to knownWords list with freq = 1")
        print(words_toBeAddedTo_knownWords)
