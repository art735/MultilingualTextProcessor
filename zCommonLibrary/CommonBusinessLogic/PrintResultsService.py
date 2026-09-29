from LocalDAO import TxtDao


# from importlib.machinery import SourceFileLoader
# txtDao = SourceFileLoader('TxtDao', '../CommonDAO/LocalDAO/TxtDao.py').load_module()


# def printDict(dictToPrint):
#     for word, freq in dictToPrint.items():
#         s = "{0}\t{1}".format(word, freq)
#         print(s)
#     print("Total amount of words - {0}".format(len(dictToPrint)))


def __printFinalStatisticsToConsole(knownWordsFreq_dict, wordsFreq_dict):
    print("Known words - {0}".format(len(knownWordsFreq_dict)))
    print("New words - {0}".format(len(wordsFreq_dict)))


def __saveKnownWordsAndNewWordsToFiles(knownWordsFreq_dict, wordsFreq_dict):
    knownWordsFilename = TxtDao.composeKnownWordsFilename()

    # Печатать слова в алфавитном порядке, а не в том порядке, в котором они идут в словаре
    # knownWordsFreq_dict = collections.OrderedDict(
    #     sorted(knownWordsFreq_dict.items(), key=lambda t: t[0], reverse=False))

    TxtDao.writeDictToFile(knownWordsFilename, knownWordsFreq_dict)

    newWordsFilename = TxtDao.composeNewWordsFilename()
    TxtDao.writeDictToFile(newWordsFilename, wordsFreq_dict)


# BUSINESS METHOD
def printResults(knownWordsFreq_dict, wordsFreq_dict):
    __printFinalStatisticsToConsole(knownWordsFreq_dict, wordsFreq_dict)
    __saveKnownWordsAndNewWordsToFiles(knownWordsFreq_dict, wordsFreq_dict)
