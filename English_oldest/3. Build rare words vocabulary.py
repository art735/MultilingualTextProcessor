# Поскольку список слов для топика часто бывает довольно объёмный,
# хотелось бы из общего списка слов для топика выделить список из нескольких десятков слов,
# которые по частоте употребляемости из статистики Top1000/2000/3000/4000/5000 встречаются РЕЖЕ других.
# Такие более редкие слова можно было бы выписывать в отдельую тетрадку и повторять их периодически.

from importlib.machinery import SourceFileLoader

excelDao = SourceFileLoader('ExcelDao', 'CommonDAO/LocalDAO/ExcelDaoEnglishTopics.py').load_module()
utils = SourceFileLoader('Utils', 'CommonBusinessLogic/Utils.py').load_module()


def getSelectionFromTop5000(TOP_INDEX):
    selectionFrom5000Words = list()
    for i in range(0, TOP_INDEX):
        selectionFrom5000Words.append(top5000Words[i])

    return selectionFrom5000Words


# STEP 1. Get word list of the current topic

[currentWorkbookFilename, currentWorksheetName] = excelDao.getCurrentWorkbookAndWorksheetNames()
currentWorksheet = excelDao.getWorksheetByName(currentWorkbookFilename, currentWorksheetName)

rawTopicWords = excelDao.getSpecificColumnContents(currentWorksheet, 1)
niceTopicWords = utils.processWordsByRemovingExcessiveSymbols(rawTopicWords)

# STEP 2. Get Top5000 words
top5000WorkbookFilename = "../resources/Top5000.xls"
top5000Wks = excelDao.getWorksheetByIndex(top5000WorkbookFilename, 0)
top5000Words = excelDao.getSpecificColumnContents(top5000Wks, 0)

# STEP 3. Processing
# TOP_INDEX = 4750
TOP_INDEX = 5000
selectionFrom5000Words = getSelectionFromTop5000(TOP_INDEX)
rareWords = utils.subtractLists(niceTopicWords, selectionFrom5000Words)

# STEP 4. Print results
print(len(rareWords))
print(rareWords)

# for word in rareWords:
#     print(word)
