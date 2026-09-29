# coding: utf-8
from __future__ import unicode_literals

from apso_utils import console, msgbox
import re


# Данная функция должна быть в самом верху и нужна для импорта других .py-скриптов
# В Python3 всё намного проще, а для Python2 пришлось сильно заморочиться...
# Возвращает полный путь к файлу, лежащему в одной папке с текущим скриптом
# Моя функция, собранная из разных кусков на форумах
def get_full_path(filename):
    import inspect
    current_file_full_path = inspect.getfile(lambda: None)
    # из полного пути текущего файла нам нужна только текущая директория,
    # к которой мы добавим имя файла, переданное параметром в функцию
    # и таким образом получим полное имя ДРУГОГО скрипта из этой же папки
    # разбиваем полное имя файла на куски и склеиваем их все, кроме последнего

    pieces_of_path = current_file_full_path.split("\\")

    dir_path = ""
    for i in range(0, len(pieces_of_path)-1):
        dir_path += (pieces_of_path[i] + "\\")

    fileFullPath = dir_path + "\\" + filename
    #msgbox(fileFullPath)

    return fileFullPath

#######################

# for Python2
import imp

# данная подгрузка файла обязательно нужна для того, чтобы потом сработал импорт класса, размещённого в этом файле!
generalFormatter = imp.load_source('GeneralFormatter', get_full_path('GeneralFormatter.py'))
transcriptionFormatter = imp.load_source('TranscriptionFormatter', get_full_path('TranscriptionFormatter.py'))
transcriptionAspirationLogic = imp.load_source('TranscriptionAspirationLogic', get_full_path('TranscriptionAspirationLogic.py'))

####################################################################################

# The CreateUnoService() method (in OO Basic) is a shortcut to obtaining the global service manager and then calling createInstance() on the service manager.
import uno
def createUnoService(serviceName):
    serviceManager = uno.getComponentContext().ServiceManager
    return serviceManager.createInstanceWithContext(serviceName, uno.getComponentContext())

def runOpenOfficeBasicMacro():
    sMacroURL = "macro:///standard.GreekModule.Main"
    dispatchHelper = createUnoService("com.sun.star.frame.DispatchHelper")
    dispatchHelper.executeDispatch(desktop, sMacroURL, "", 0, tuple([]))

####################################################################################

desktop = XSCRIPTCONTEXT.getDesktop()
document = XSCRIPTCONTEXT.getDocument()

searchDescriptor = document.createSearchDescriptor()
searchDescriptor.SearchRegularExpression = True

replaceDescriptor = document.createReplaceDescriptor()
replaceDescriptor.SearchRegularExpression = True

# импорт имени своего класса из другого файла
from GeneralFormatter import GeneralFormatter
from TranscriptionFormatter import TranscriptionFormatter
# создание экземпляра своего класса как глобальной переменной
generalFormatter = GeneralFormatter(document, replaceDescriptor)
transcriptionFormatter = TranscriptionFormatter(document, searchDescriptor, replaceDescriptor)

#def test():
#    msgbox(document.Title)


def aspirePtk():
    # в качестве параметра передаём имя callback-функции
    transcriptionFormatter.replaceInsideTranscriptions(transcriptionAspirationLogic.makeAspirationForPtkConsonants)


def makeAspirational_h_Superscript():
    ####### Поднятие придыхательного звука h в superscript ##########

    from com.sun.star.beans import PropertyValue

    # Specify the Short Integer representing the percentage of raising or lowering for superscript/subscript characters
    charEscapement = PropertyValue()
    charEscapement.Name = "CharEscapement"
    charEscapement.Value = 33 # значение 33 является дифолтным в GUI OO Writer-а

    # Specify the additional height used for subscript or superscript characters as an Integer percent
    charEscapementHeight = PropertyValue()
    charEscapementHeight.Name = "CharEscapementHeight"
    charEscapementHeight.Value = 58 # значение 58 является дифолтным в GUI OO Writer-а

    # Specify the scaling for superscript and subscript as a percentage using a Short Integer
    charScaleWidth = PropertyValue()
    charScaleWidth.Name = "CharScaleWidth"
    charScaleWidth.Value = 100 # значение 100 является дифолтным в GUI OO Writer-а

    # если создавать список свойств напрямую, без "туполизации", выдаёт ошибку при присвоении replaceDescriptor.ReplaceAttributes
    replaceProperties = tuple([charEscapement, charEscapementHeight, charScaleWidth])
    replaceDescriptor.ReplaceAttributes = replaceProperties

    # снова включил замену с помощью регулярок, эту возможность отключал выше и теперь надо не забыть включить!
    replaceDescriptor.SearchRegularExpression = True

    # Чтобы поиск осуществлялся только внутри транскрипций и не распространялся за их пределы на слова с ph, th, kh, искать h перед [ptk] следующим образом:
    # 1) или непосредственно перед открывающей квадратной скобкой (например, для [khæt] - кот)
    # 2) или в начале ударного слога со знаками ударения ['ˌˈ]
    # 3) или перед пробелом в транскрипциях целых фраз, а не только отдельных слов
    replaceDescriptor.SearchString = "(?<=[\['ˌˈ\s][ptk])h" # формула данного regex: positive lookbehind + h
    # replaceDescriptor.SearchString = "(?<=\[.*?)[ptk]h" # формула данного regex: positive lookbehind + h

    replaceDescriptor.ReplaceString = "$0" # $0 - это найденный символ h
    document.replaceAll(replaceDescriptor)

    # обнулить "режим superscript-а" и вернуться в обычный регистр
    replaceDescriptor.ReplaceAttributes = tuple()




def main():

    # вызов макроса, написанного на OpenOffice Basic!!!
    # runOpenOfficeBasicMacro()

    # произвести общее форматирование текста: убрать двойные пробелы и т. д.
    generalFormatter.run()

    # произвести форматирование внутри транскрипций
    transcriptionFormatter.run()

    # сделать транскрипции аспирированными
    aspirePtk()
    # отформатировать аспирированный h как superscript
    makeAspirational_h_Superscript()


    msgbox("English macro has worked!")
