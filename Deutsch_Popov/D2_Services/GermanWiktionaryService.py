import WiktionaryTranscriptionReader
from DeuDefiniteArticleService import DeuDefiniteArticleService

LANG_CODE = 'de'

deuDefiniteArticleService = DeuDefiniteArticleService()


def get_word_transcription(word, ignore_definite_article=True):
    transcription = ''

    if ignore_definite_article:
        # strip definite article before nouns
        word = deuDefiniteArticleService.strip_definite_article(word.strip())
        word = word.strip()

    if word:
        transcription = WiktionaryTranscriptionReader.get_word_transcription(LANG_CODE, word)

    return transcription


################################################################

# words = ['der', 'die', 'das', 'die Katze', 'der Hund ', 'das     Getriebe   ', ' macht', ' (das) Berlin', '(der) Hans ']
# words = ['zuza', '', '???']
# # words = TxtDao.readLinesFromFile(r'e:\Languages\English\SVN repo\Python software\MultilingualTextProcessor\resources\german_words.txt')
# for word in words:
#     transcription = get_word_transcription(word, True)
#     res = f'{word.strip()}|{transcription.strip()}'
#     print(res)

word = 'Information'
word = 'steig'

if __name__ == '__main__':
    transcription = get_word_transcription(word, True)
    print(transcription)
