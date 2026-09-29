import re

from CharConstants import HYPHEN, DASH, NEWLINE, SPACE_DASH_SPACE
from GermanSentenceTranscriber import GermanSentenceTranscriber


class GermanPopovTextTranscriber:
    def __init__(self):
        self.germanSentenceTranscriber = GermanSentenceTranscriber()

    def transcribe_whole_text(self, text, is_dash_separator):
        text_unknown_words = []
        text_transcriptions = []

        chunks = [chunk for chunk in text.split('\n\n') if chunk not in ['\n', '']]

        for chunk in chunks:
            chunk_unknown_words, chunk_transcription = self.transcribe_chunk(chunk, is_dash_separator)
            text_unknown_words.extend(chunk_unknown_words)
            text_transcriptions.append(chunk_transcription)

        # As of Python 3.7, standard dict is guaranteed to preserve order and is more performant than OrderedDict.
        # Here's an example of how to use dict as an ordered set to filter out duplicate items while preserving order,
        # thereby emulating an ordered set.
        # Use the dict class method fromkeys() to create a dict, then simply ask for the keys() back.
        non_duplicated_and_ordered_text_unknown_words = list(dict.fromkeys(text_unknown_words))
        output_unknown_words = NEWLINE.join(non_duplicated_and_ordered_text_unknown_words)

        output_transcription = "\n\n".join([t for t in text_transcriptions if len(t)])

        if len(output_unknown_words):
            output = output_unknown_words + "\n\n* * * * * * *\n\n" + output_transcription
        else:
            output = output_transcription

        return output

    def transcribe_chunk(self, chunk, is_dash_separator):
        chunk_unknown_words = list()
        chunk_transcriptions = list()

        sentences = [s for s in chunk.split('\n') if len(s)]  # взять в дальнейшую работу только непустые строки
        for sentence in sentences:
            if not self._should_line_be_ignored(
                    sentence):  # если предложение это НЕ строка вида (sg. – pl.) и ей подобные
                if is_dash_separator:
                    sentence_unknown_words, sentence_transcription = self.process_dash_separated_line(sentence)
                else:
                    sentence_unknown_words, sentence_transcription = self.germanSentenceTranscriber.transcribe_sentence(
                        sentence)

                # Use the syntax list1.extend(list2) to combine list1 and list2
                # Use the syntax list1.append(list2) to add list2 to list1
                chunk_unknown_words.extend(sentence_unknown_words)
                chunk_transcriptions.append(sentence_transcription)

        chunk_transcription = NEWLINE.join([ct for ct in chunk_transcriptions if len(ct)])
        return chunk_unknown_words, chunk_transcription

    # Игнорировать строки, начинающиеся и заканчивающиеся круглыми скобками, и содержащие внутри скобок грам. термины
    def _should_line_be_ignored(self, sentence):
        grammar_terms_regex_group = r'(sg[.]|pl[.]|nom[.]|gen[.]|dat[.]|acc[.]|voc[.]|masc[.]|fem[.]|neut[.])'
        delimiter_regex = '\s[-–]\s'
        target_regex = r'^\({0}({1}{0})*\)$'.format(grammar_terms_regex_group, delimiter_regex)
        return re.search(target_regex, sentence)

    def process_dash_separated_line(self, sentence, should_lookup_unknown_word_transcription_in_wiktionary=False):
        dash_separated_line_unknown_words = []
        dash_separated_line_transcriptions = []

        # split by either 'space-hyphen-space' or 'space–dash–space'
        pieces = [p for p in re.split(fr'\s[{HYPHEN}{DASH}]\s', sentence) if p]

        for piece in pieces:
            piece_unknown_words, piece_transcription = self.germanSentenceTranscriber.transcribe_sentence(
                piece, should_lookup_unknown_word_transcription_in_wiktionary)

            # Use the syntax list1.extend(list2) to combine list1 and list2
            # Use the syntax list1.append(list2) to add list2 to list1
            dash_separated_line_unknown_words.extend(piece_unknown_words)
            dash_separated_line_transcriptions.append(piece_transcription)

        dash_separated_line_transcription = SPACE_DASH_SPACE.join(dash_separated_line_transcriptions)
        return dash_separated_line_unknown_words, dash_separated_line_transcription


################################################################################

# text = "Wie heißen Sie?\n\n\n\n\nHeißen Sie Martin?"
# text = "1 Frau"
# text = "- Entschuldigen Sie! Sind Sie Herr Smirnow?"
# text = "Das ist Manfred."
# text = "Mein Name ist Sindermann." + "\n\n" + "Mein Name ist Sindermann."
# text = "– Kommt Herr Böhme aus Großbritannien?" + "\n" + "– Nein, er kommt nicht aus Großbritannien."

# text = '''in
#
# das Zimmer – dem Zimmer – das Zimmer
#
# in Ihr Zimmer
#
# in meinem Zimmer'''

# text = '''a
#
# das Zimmer – dem b – das Zimmer
#
# in Ihr Zimmer
#
# in meinem Zimmer'''
#
# # text = 'das Zimmer – dem Zimmer – das Zimmer'
#
# output = transcribeWholeText(text, True)
# print(output)

# text = '''das Formular – das Formular
# (nom. – acc.)
#
# das Formular ausfüllen
#
# – Haben Sie das Formular ausgefüllt?
# – Ja, das Formular ist schon ausgefüllt.'''
#
# text = "Gibt ihr der Ober auf DM 17,- heraus?"
# output = transcribeWholeText(text, True)
# print(output)

# text = "DM 10,50"
# output = preprocessBeforeTranscribing(text)
# print(output)

# line = 'das Büro – dem Büro'
# line = 'das Büro'
# dash_separated_line_unknown_words, dash_separated_line_transcription = process_dash_separated_line(line, True)
#
# print(dash_separated_line_unknown_words)
# print(dash_separated_line_transcription)

text = 'sein'

if __name__ == '__main__':
    germanPopovTextTranscriber = GermanPopovTextTranscriber()
    result = germanPopovTextTranscriber.transcribe_whole_text(text, True)
    print(result)
