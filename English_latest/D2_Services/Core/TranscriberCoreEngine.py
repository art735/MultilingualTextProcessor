import nltk
from nltk.corpus import wordnet

import ExcelDaoEnglishVocabulary
from CharConstants import STRAIGHT_APOSTROPHE
from Core import RepositorySearcher, TranscriptionComposer
from Lemmatizer import wordNetLemmatizer


# nltk.help.upenn_tagset()

# vocabulary_dict
# dictionary_dict


def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


def transcribe(sentence, vocabulary_dict):
    sentenceTranscriptions = list()
    sentenceUnknownWords = list()

    tokenized_sentence = nltk.word_tokenize(sentence)
    pos_tagged_sentence = nltk.pos_tag(tokenized_sentence)
    print(pos_tagged_sentence)

    # for word_to_search, pos_tag in pos_tagged_sentence:
    for i in range(0, len(pos_tagged_sentence)):
        word_to_search, pos_tag = pos_tagged_sentence[i]
        if any(c.isalpha() for c in pos_tag):
            word_to_search = word_to_search.lower()
            word_lemma = wordNetLemmatizer.lemmatize(word_to_search, get_wordnet_pos(pos_tag))

            # POS - genitive marker (possessive ending)
            if pos_tag == 'POS':
                general_condition = word_to_search == "'s"
                specific_condition = False

                if general_condition is False:
                    previous_word_to_search, previous_pos_tag = pos_tagged_sentence[i - 1]
                    is_previous_word_sg = previous_pos_tag in ['NN', 'NNP']
                    # Существуют некоторые разногласия в использовании окончания -’s после собственных имён и
                    # существительных единственного числа, которые оканчиваются на -s или -ss, а также -z, -x.
                    # Некоторые писатели и составители английских грамматик настаивают на использовании
                    # окончания -’s для всех существительных единственного числа или имён собственных,
                    # независимо от их окончания.
                    # Однако использование -’s или апострофа «’» в таких случаях относится больше
                    # к стилистическим особенностям и приёмам авторов. Поэтому можно встретить разные варианты
                    # использования -’s и апострофа «’».

                    # James -> James’ or James’s (возможны оба варианта)
                    # Smiths’ -> Smiths’ or Smiths’s (возможны оба варианта)
                    specific_condition = (word_to_search == STRAIGHT_APOSTROPHE) and is_previous_word_sg

                if general_condition or specific_condition:
                    previous_word_transcription_old = sentenceTranscriptions[-1]
                    previous_word_transcription_new = TranscriptionComposer.compose_noun_possessive_case_transcription(
                        previous_word_transcription_old, pos_tag)
                    sentenceTranscriptions[-1] = previous_word_transcription_new
            else:
                # found_result - это структура данных типа RepositoryLookUpResult
                found_result = RepositorySearcher.search(word_to_search, word_lemma, pos_tag, vocabulary_dict)

                if found_result:
                    if found_result.needs_transcription_further_processing:
                        if pos_tag.startswith('JJ') or pos_tag.startswith(
                                'RB'):  # adjective: JJ, JJR, JJS; adverb: RB, RBR, RBS
                            word_transcription = TranscriptionComposer.compose_adjective_adverb_transcription(
                                word_to_search, found_result.transcription)
                        elif pos_tag.startswith('VB'):  # verb: VB, VBD, VBG, VBN, VBP, VBZ
                            word_transcription = TranscriptionComposer.compose_verb_transcription(word_to_search,
                                                                                                  word_lemma,
                                                                                                  found_result.transcription)
                        elif pos_tag.startswith('NN'):  # noun: NN, NNP, NNPS, NNS
                            word_transcription = TranscriptionComposer.compose_noun_transcription(word_to_search,
                                                                                                  word_lemma,
                                                                                                  found_result.transcription)
                        # else: # если ни один из тегов не подошёл, считать существительным
                        #     word_transcription = NounProcessor.compose_transcription(word_to_search, word_lemma, found_result.transcription)
                        # чтобы 'апостроф' или 'апостроф s' как маркер possessive case корректно определялся, он должен быть ПРЯМЫМ, но не кучерявым!!!
                    else:
                        word_transcription = found_result.transcription
                else:
                    word_transcription = "???"
                    unknown_word_tuple = (word_to_search, word_lemma, pos_tag)
                    sentenceUnknownWords.append(unknown_word_tuple)

                    ####################################################################

                if word_transcription.startswith('[') and word_transcription.endswith(']'):
                    word_transcription = word_transcription[1:-1]

                sentenceTranscriptions.append(word_transcription)
        # end of 'if any(c.isalpha() for c in pos_tag):'
    # end of loop

    sentenceTranscription = "[{0}]".format(" ".join(sentenceTranscriptions))  # surround with []
    return sentenceUnknownWords, sentenceTranscription


##################################

vocabulary_dict = ExcelDaoEnglishVocabulary.get_EnglishVocabulary_dict()
#
# # sentence = "And now for something completely different"
# sentence = "These records are recording a record!"
# sentence = "Theseses"
# sentence = "to goes"
# sentence = "The closest closer is coming closer." # 'Ближайший закрывальщик подходит ближе'
# sentence = "a smaller house"
# sentence = "records"
# sentence = "he records music"
# sentence = "men"
# sentence = "girl's hair"
# sentence = "girl's"
# sentence = "girls' hair"
# sentence = "Charles's"
# sentence = "actress'"
# sentence = "USA's'"
#
# sentenceUnknownWords, sentenceTranscription = transcribe(sentence, vocabulary_dict)
#
# print("Unknown words: ")
# print(sentenceUnknownWords)

# print("Transcription: ")
# print(sentenceTranscription)
