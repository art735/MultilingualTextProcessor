import re

from importlib.machinery import SourceFileLoader

excelDao = SourceFileLoader('ExcelDao', 'CommonDAO/LocalDAO/ExcelDaoEnglishTopics.py').load_module()
txtDao = SourceFileLoader('TxtDao', 'CommonDAO/LocalDAO/TxtDao.py').load_module()

# Step 1. Get words from current spreadsheet
[currentWorkbookFilename, currentWorksheetName] = workbookFilename = excelDao.getCurrentWorkbookAndWorksheetNames()
currentWks = excelDao.getWorksheetByName(currentWorkbookFilename, currentWorksheetName)
wordsFromCurrentSpreadsheet = excelDao.getSpecificColumnContents(currentWks, 1)

# Step 2. Get words from .txt-file, which are words from .odt topic vocabulary
wordsFromOdtToValidateWks = txtDao.readLinesFromFile('../resources/wordsFromOdtToValidateWks.txt')

pureWordsFromOdtToValidateWks = list()
for word in wordsFromOdtToValidateWks:
    pattern = "\s\(BrE\)|\s\(AmE\)"
    pureWord = re.sub(pattern, '', word)
    pureWordsFromOdtToValidateWks.append(pureWord)

### PROCESSING ###

nonFoundWords = list()

for wksWord in wordsFromCurrentSpreadsheet:
    if wksWord not in pureWordsFromOdtToValidateWks:
        nonFoundWords.append(wksWord)

if (len(nonFoundWords) > 0):
    print("Validation FAILED!")
    print("The following spreadsheet word(s) not found in .odt vocabulary:")
    print(nonFoundWords)
else:
    print("Congrats! Validation is successful!")
