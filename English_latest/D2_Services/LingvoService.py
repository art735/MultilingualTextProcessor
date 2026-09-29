import LingvoTranscriptionDao
import LingvoTranslationDao


def get_word_from_Lingvo(word, delay_between_requests):
    transcription = LingvoTranscriptionDao.get_transcription(word, delay_between_requests)
    translation = LingvoTranslationDao.get_translation(word, delay_between_requests)
    result = "{0}*{1}*{2}".format(word, transcription, translation)
    return result

##############################


# words = ['cat', 'dog']
# for word in words:
#     delay_between_requests = 2  # delay between requests (in seconds)
#     output = get_word_from_Lingvo(word, delay_between_requests)
#     print(output)
