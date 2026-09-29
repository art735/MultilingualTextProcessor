# coding: utf-8
from __future__ import unicode_literals

from apso_utils import console, msgbox
import re

#import uno


class TranscriptionFormatter:
    document = None
    searchDescriptor = None
    replaceDescriptor = None


    def __init__(self, _document, _searchDescriptor, _replaceDescriptor):
        self.document = _document
        self.searchDescriptor = _searchDescriptor
        self.replaceDescriptor = _replaceDescriptor


    def replaceInsideTranscriptions(self, callbackBusinessLogic):
        self.searchDescriptor.SearchString = "\[.*?\]"        
        allTranscriptions = self.document.findAll(self.searchDescriptor)
        
        transcrDict = dict()
        
        replaceableTranscriptions = list()
        replacingTranscriptions = list()
        
        # for в данном случае не умеет итерироваться по контейнеру,
        # поэтому итерируемся по ИНДЕКСАМ элементов в контейнере
        for i in range(0, allTranscriptions.getCount()):
            transcription = allTranscriptions.getByIndex(i)
            if transcription:
                foundTranscr = transcription.getString()
                
                #msgbox(foundTranscr)                
                #print("i = " + str(i))
                #print("foundTranscr BEFORE = " + foundTranscr)
                
                modifiedTranscr = callbackBusinessLogic(foundTranscr)
                
                #print("foundTranscr = " + foundTranscr + "\n" + "modifiedTranscr = " + modifiedTranscr + "\n\n")
                #print("foundTranscr AFTER = " + foundTranscr + "\n")
                
                if foundTranscr != modifiedTranscr:
                    transcrDict[foundTranscr] = modifiedTranscr
                    #replaceableTranscriptions.append(foundTranscr)
                    #replacingTranscriptions.append(modifiedTranscr)
        
        # очень важно отключить здесь трактовку заменяющей транскрипции как регуляки!
        # В заменяющей транскрипции присутствуют квадратные скобки,
        # которые при True интерпретируются как [класс символов], что совершенно неверно в контексте данной задачи!!!
        self.replaceDescriptor.SearchRegularExpression = False
        
        for k, v in transcrDict.items():
            self.replaceDescriptor.SearchString = k
            self.replaceDescriptor.ReplaceString = v
            self.document.replaceAll(self.replaceDescriptor)            
        
        # надо ли снова включать self.replaceDescriptor.SearchRegularExpression = False ????
    
    
    def _replaceWithRegExp(self, bracketedTranscription, searchFor, replaceWith):
        match = re.search('(?<=\[).*?(?=\])', bracketedTranscription)

        # Предотвращение ошибки 'NoneType' object has no attribute 'group'
        # Если регулярка не нашла транскрипцию (т. е. текст, заключённый в квадратные скобки) в переданном в функцию аргументе,
        # вернуть этот аргумент из функции и ничего с ним не делать
        if match is None:
            return bracketedTranscription

        strippedTranscription = match.group(0)

        # если транскрипция содержит пробелы, т. е. перед нами транскрипция целой фразы, разбиваем её на части
        # и работаем с каждой частью в отдельности, а потом в конце склеиваем в одну строку с пробелами
        pieces = strippedTranscription.split()

        resultAsString = ""
        resultAsList = list()

        for pieceOfTranscription in pieces:
            # искать звук ɪ в таком положении, чтобы перед ним был НЕ-гласный (т. е. согласный) звук, и чтобы он
            # находился в конце строки и заменить его на i, т. к. со слов Влада ни одно англ. слово в современном
            # RP и GA не заканчивается на -ɪ : не ['sɪtɪ], а ['sɪti]
            correctedPieceOfTranscription = re.sub(searchFor, replaceWith, pieceOfTranscription)
            resultAsList.append(correctedPieceOfTranscription)
            
        resultAsString = " ".join(resultAsList)
        bracketedOutput = "[{}]".format(resultAsString)
        return bracketedOutput
    
    
    def reformatFinal_i_sound(self, bracketedTranscription):
        return self._replaceWithRegExp(bracketedTranscription, '(?<=[^iuɪʊeoəɛɜʌɔæaɑɒ])ɪ$', 'i')
    
    
    def replaceCurlyAccentWithStraightAccent(self, bracketedTranscription):
        return self._replaceWithRegExp(bracketedTranscription, "’", "'")


    def run(self):
        # сделать замены в транскрипциях перед согласным звуком -ɪ на -i, как это принято в совр. RP и GA
        # ['sɪtɪ 'lɪlɪ] -> ['sɪti 'lɪli]
        self.replaceInsideTranscriptions(self.reformatFinal_i_sound)
        
        self.replaceInsideTranscriptions(self.replaceCurlyAccentWithStraightAccent)
        
        ###############################################
        
        # msgbox("GeneralFormatter has worked!!!")
        

