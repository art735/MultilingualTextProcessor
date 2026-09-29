import re

# Custom user imports
from CharConstants import SPACE_DASH_SPACE, NEWLINE, CURLY_APOSTROPHE, STRAIGHT_APOSTROPHE
import ExcelDaoEnglishDictionary
import ExcelDaoEnglishVocabulary
import UnknownWordsLookUpService
from Core import TranscriberCoreEngine


def preprocessBeforeTranscribing(sentence):
    # для корректного определения wordNetLemmatizer-ом possessive case, заменить кучерявый апостроф на прямой!
    sentence = sentence.replace(CURLY_APOSTROPHE, STRAIGHT_APOSTROPHE)  # replaces all occurrences

    return sentence


def transcribeSingleSentence(sentence):
    sentence = preprocessBeforeTranscribing(sentence)
    vocabulary_dict = ExcelDaoEnglishVocabulary.get_EnglishVocabulary_dict()
    return TranscriberCoreEngine.transcribe(sentence, vocabulary_dict)


def processDashSeparatedLine(sentence):
    dashSeparatedLineUnknownWords = list()
    dashSeparatedLineTranscriptions = list()

    pieces = [p for p in re.split('\s[-–]\s', sentence) if
              len(p)]  # split by either 'space-hyphen-space' or 'space–dash–space'

    for piece in pieces:
        pieceUnknownWords, pieceTranscription = transcribeSingleSentence(piece)

        # Use the syntax list1.extend(list2) to combine list1 and list2
        # Use the syntax list1.append(list2) to add list2 to list1
        dashSeparatedLineUnknownWords.extend(pieceUnknownWords)
        dashSeparatedLineTranscriptions.append(pieceTranscription)

    dashSeparatedLineTranscription = SPACE_DASH_SPACE.join(dashSeparatedLineTranscriptions)
    return dashSeparatedLineUnknownWords, dashSeparatedLineTranscription


# Игнорировать строки, начинающиеся и заканчивающиеся круглыми скобками, и содержащие внутри скобок грам. термины
def shouldLineBeIgnored(sentence):
    grammar_terms_regex_group = r'(sg[.]|pl[.]|nom[.]|gen[.]|dat[.]|acc[.]|voc[.]|masc[.]|fem[.]|neut[.])'
    delimiter_regex = '\s[-–]\s'
    target_regex = r'^\({0}({1}{0})*\)$'.format(grammar_terms_regex_group, delimiter_regex)
    return re.search(target_regex, sentence)


def transcribeChunk(chunk, isDashSeparator):
    chunkUnknownWords = list()
    chunkTranscriptions = list()

    sentences = [s for s in chunk.split("\n") if len(s)]  # взять в дальнейшую работу только непустые строки
    for sentence in sentences:
        if not shouldLineBeIgnored(sentence):  # если предложение это НЕ строка вида (sg. – pl.) и ей подобные
            if isDashSeparator:
                sentenceUnknownWords, sentenceTranscription = processDashSeparatedLine(sentence)
            else:
                sentenceUnknownWords, sentenceTranscription = transcribeSingleSentence(sentence)

            # Use the syntax list1.extend(list2) to combine list1 and list2
            # Use the syntax list1.append(list2) to add list2 to list1
            chunkUnknownWords.extend(sentenceUnknownWords)
            chunkTranscriptions.append(sentenceTranscription)

    chunkTranscription = NEWLINE.join([ct for ct in chunkTranscriptions if len(ct)])

    return chunkUnknownWords, chunkTranscription


def transcribeWholeText(text, isDashSeparator):
    textUnknownWords = list()
    textTranscriptions = list()

    chunks = [chunk for chunk in text.split('\n\n') if chunk not in ['\n', ""]]

    for chunk in chunks:
        chunkUnknownWords, chunkTranscription = transcribeChunk(chunk, isDashSeparator)
        textUnknownWords.extend(chunkUnknownWords)
        textTranscriptions.append(chunkTranscription)

    outputTranscription = "\n\n".join([t for t in textTranscriptions if len(t)])

    # As of Python 3.7, standard dict is guaranteed to preserve order and is more performant than OrderedDict.
    # Here's an example of how to use dict as an ordered set to filter out duplicate items while preserving order,
    # thereby emulating an ordered set.
    # Use the dict class method fromkeys() to create a dict, then simply ask for the keys() back.
    nonDuplicatedAndOrderedTextUnknownWords = list(dict.fromkeys(textUnknownWords))

    if len(nonDuplicatedAndOrderedTextUnknownWords):
        dictionary_dict = ExcelDaoEnglishDictionary.get_EnglishDictionary_dict()
        outputUnknownWords = UnknownWordsLookUpService.lookUp(nonDuplicatedAndOrderedTextUnknownWords, dictionary_dict)
        output = outputUnknownWords + "\n\n* * * * * * *\n\n" + outputTranscription
    else:
        output = outputTranscription

    return output

################################################################################

# text = "Wie heißen Sie?\n\n\n\n\nHeißen Sie Martin?"
# text = "1 Frau"
# text = "- Entschuldigen Sie! Sind Sie Herr Smirnow?"
# text = "Das ist Manfred."
# text = "Mein Name ist Sindermann." + "\n\n" + "Mein Name ist Sindermann."
# text = "– Kommt Herr Böhme aus Großbritannien?" + "\n" + "– Nein, er kommt nicht aus Großbritannien."


# text = "You complete me!"
# text = "These records are recording a record!"

# text = "better"

# text = "he records music"
#
# output = transcribeWholeText(text, True)
# print(output)
