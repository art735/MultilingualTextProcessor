import re
import urllib.request
from importlib.machinery import SourceFileLoader

from bs4 import BeautifulSoup

excelDao = SourceFileLoader('ExcelDao', 'CommonDAO/LocalDAO/ExcelDaoEnglishTopics.py').load_module()


####################################################################
def getRawTranscription(word):
    url = basicCollinsUrl + word
    httpText = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(httpText)

    rawTranscription = ''

    for tag in soup.find_all('span'):
        if tag.has_attr('class') and (tag['class'] == ['pron']):
            if tag.text != rawTranscription:
                rawTranscription += tag.text

    return rawTranscription


def processRawTranscription(rawTranscription):
    if (rawTranscription is ""):
        return "<not found>"
    regex = re.compile('\((.*?)\)', re.DOTALL | re.MULTILINE)
    foundGroup = regex.search(rawTranscription).group(1)

    fineTranscription = ""
    fineTranscription = foundGroup.replace('\n', ' ').replace('\r', '').replace(' ', '')
    fineTranscription = fineTranscription.replace(';', '; ').replace('unstressed', 'unstressed ')
    return "[{}]".format(fineTranscription)


def getTranslation(word):
    url = basicLingvoUrl + word
    httpText = urllib.request.urlopen(url).read()

    soup = BeautifulSoup(httpText)
    translation = ''

    for tag in soup.find_all('div'):
        if tag.has_attr('data-url') and (tag.text.find("LingvoUniversal") != -1):
            translation = retrieveTranslation(tag)
            break

    return translation


def retrieveTranslation(parentTag):
    finalText = ''
    for tag in parentTag.find_all('p'):
        # if there are no nested <img> tags inside the current tag
        if len(tag.find_all('img')) == 0:
            finalText += tag.text + '\n'

    return finalText


#############################################################

basicCollinsUrl = 'http://www.collinsdictionary.com/dictionary/english/'
basicLingvoUrl = 'http://www.lingvo.ua/ru/Translate/en-ru/'

wordsToLookUp = excelDao.getCurrentWorksheet1stColWords()
##wordsToLookUp = txtDao.readWordsFromFile("wordsToLookUp.txt")
##wordsToLookUp = ['cat', 'dog', 'dream (dreamt, dreamt)']

##print(words)

wordsWithTranscriptions = list()
##result = ""
for word in wordsToLookUp:
    rawTanscription = getRawTranscription(word)
    transcription = processRawTranscription(rawTanscription)
    ##    translation = getTranslation(word)
    ##    result = "{0} {1} \n{2}".format(word, transcription, translation)

    s = "{0}\t{1}".format(word, transcription)
    ##    result += s
    print(s)

##    print("***********************************")

##txtDao.writeToFile(filename, result)
