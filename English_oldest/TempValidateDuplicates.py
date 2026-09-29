from importlib.machinery import SourceFileLoader

excelDao = SourceFileLoader('ExcelDao', 'CommonDAO/LocalDAO/ExcelDaoEnglishTopics.py').load_module()
txtDao = SourceFileLoader('TxtDao', 'CommonDAO/LocalDAO/TxtDao.py').load_module()
utils = SourceFileLoader('Utils', 'CommonBusinessLogic/Utils.py').load_module()

top5000WorkbookFilename = "../resources/Top5000.xls"
# worksheetName = "Sheet1"


# STEP 2
tuplesTop5000Wks = excelDao.getWorksheetByIndex(top5000WorkbookFilename, 0)
tuplesTop5000 = excelDao.getSpecificColumnContents(tuplesTop5000Wks, 0)

# Step 2. Get words from .txt-file, which are words from .odt topic vocabulary
wordsToLookUp = txtDao.readLinesFromFile('../resources/wordsToLookUp.txt')

res = utils.subtractLists(wordsToLookUp, tuplesTop5000)

print(len(res))

for word in res:
    print(word)
