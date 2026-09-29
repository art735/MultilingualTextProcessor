# import Constants
# import time

import WiktionaryTranscriptionReader

# constants = SourceFileLoader('Constants', '../English_oldest/Constants.py').load_module()

# txtDao = SourceFileLoader('TxtDao', '../LocalDAO/TxtDao.py').load_module()
# wiktionaryTranscriptionReader = SourceFileLoader('WiktionaryTranscriptionReader',
#                                                  '../../CommonBusinessLogic/WiktionaryTranscriptionReader.py').load_module()

################
LANG_CODE = 'en'
################

### Cлова для поиска лежат в массиве ###
# words = ['schedule', 'box']
# words = ['twenty']
words = ['one']
# words = TxtDao.readLinesFromFile(r'e:\Languages\English\SVN repo\Python software\MultilingualTextProcessor\resources\numerals.txt')

for word in words:
    transcription = WiktionaryTranscriptionReader.get_word_transcription(LANG_CODE, word)
    output = "{word}\t{transcription}".format(word=word, transcription=transcription)
    print(output)
