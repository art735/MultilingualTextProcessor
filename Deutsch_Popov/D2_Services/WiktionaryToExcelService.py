import re

from D2_Services import GermanWiktionaryService

# Список регулярок, учитывающих одновременно английское и немецкое написание падежей с большой и маленькой буквы
# '[Nn]ominative?' соответствует 4-м вариантам: ['Nominative', 'nominative', 'Nominativ', 'nominativ']
# каждая регулярка обрамлена символами начала строки (^) и конца строки ($)

ignored_words_regexp_patterns = ['^[Nn]ominative?$', '^[Gg]enitive?$', '^[Dd]ative?$', '^[Aa][ck][ck]usative?$',
                                 'present_participle', 'past_participle', 'zu-infinitive', 'am']

ignored_imperative_pronouns = ['(du)', '(ihr)']


def is_ignored(word):
    result = False
    for pattern in ignored_words_regexp_patterns:
        if re.search(pattern, word):
            result = True
            break

    return result


non_transcribable_words = ['der', 'die', 'das', 'des', 'dem', 'den',
                           '(der)', '(die)', '(das)', '(des)', '(dem)', '(den)',
                           'ich', 'du', 'er', 'wir', 'ihr', 'sie',
                           '—', 'i', 'ii', 'dass']

# отделяемые приставки немецкого языка
separable_prefixes = ['ab', 'an', 'auf', 'aus', 'bei', 'ein', 'her', 'hin', 'los', 'mit', 'nach', 'vor', 'weg', 'zu',
                      'zurück']

# key - non-Excel german word
# value - transcription from wiktionary
dictionary = dict()
PIPE = '|'
SPACE = ' '


def get_bare_transcription(word):
    if word in dictionary:
        transcription = dictionary.get(word)
        # print(f'{word} is read from temp dictionary'.format(word))
    else:
        transcription = GermanWiktionaryService.get_word_transcription(word, True)
        dictionary[word] = transcription
        # print(f'{word} is read from WIKTIONARY'.format(word))

    return transcription


def get_word_transcription(word):
    transcription = get_bare_transcription(word)
    return f'{word}{PIPE}{transcription}'.format(word, PIPE, transcription)


def pre_process_row(row):
    row = row.replace("present participle", "present_participle")
    row = row.replace("past participle", "past_participle")
    return row


# Данный метод обрабатывает атомарную (неделимую) часть ячейки таблицы. Ячейка считается атомарной, если в ней
# нет слеша, в противном случае атомарной считается та часть ячейки, которая получается после разбития её содержимого
# по слешу.
# des Hofs / des Hofes
def process_table_cell_atomic_part(atomic_cell_part):
    # transcription = ""
    processed_words = list()
    transcriptions = list()

    words = atomic_cell_part.split()
    for word in words:
        word = re.sub(r'\d', '', word)  # в wiktionary после слова иногда стоит цифровая сноска, удалить её

        # порядок замены именно такой: сначала заменяем sie, потом er
        processed_word = word
        processed_word = re.sub(r'^sie$', 'sie/Sie', processed_word)
        processed_word = re.sub(r'^er$', 'er/sie/es', processed_word)

        processed_words.append(processed_word)

        skip_word_transcription_condition = is_ignored(word) \
                                            or word in non_transcribable_words \
                                            or word in ignored_imperative_pronouns
        if not skip_word_transcription_condition:
            transcriptions.append(get_bare_transcription(word))

    processed_words_str = SPACE.join(processed_words)
    transcription_str = "[{}]".format(SPACE.join([t[1:-1] for t in transcriptions if t]))

    cell_result = ''
    if len(transcriptions) > 0:
        cell_result = f'{processed_words_str}{PIPE}{transcription_str}'
    return cell_result


# Each table cell is tab separated from one another
def process_single_table_cell(cell):
    if '/' in cell:  # des Hofs / des Hofes
        slash_separated_words = []
        slash_separated_transcriptions = []
        slash_separated_parts = [piece.strip() for piece in cell.split('/')]
        for slash_separated_part in slash_separated_parts:
            word, transcription = process_table_cell_atomic_part(slash_separated_part).split('|')
            slash_separated_words.append(word)
            slash_separated_transcriptions.append(transcription)
        words_str = ' / '.join(slash_separated_words)
        transcriptions_str = ' / '.join(slash_separated_transcriptions)
        result = f'{words_str}{PIPE}{transcriptions_str}'
    else:
        result = process_table_cell_atomic_part(cell)

    return result


def process_single_row(row):
    row = pre_process_row(row)

    # содержимое каждой из ячеек таблиц в wiktionary отделяется друг от друга знаком табуляции
    cells = row.split('\t')

    cell_res_list = list()
    for cell in cells:
        cell_res_list.append(process_single_table_cell(cell))

    row_result = PIPE.join([c for c in cell_res_list if c != ""])
    return row_result


def process_single_chunk(chunk):
    rows = [r for r in chunk.split("\n") if r]

    row_res_list = list()
    for row in rows:
        row_res_list.append(process_single_row(row))

    chunk_result = "\n".join([r for r in row_res_list if r != ""])
    return chunk_result


def run(text):
    chunks = [chunk for chunk in text.split('\n\n') if chunk not in ['\n', ""]]

    res_list = list()
    for chunk in chunks:
        res_list.append(process_single_chunk(chunk))

    result = "\n\n".join(res_list)
    return result


#######################################

# text = "Nominativ	die Frau	die Frauen\n" \
#        "Genitiv	der Frau	der Frauen\n" \
#        "Dativ	der Frau	den Frauen\n" \
#        "Akkusativ	die Frau	die Frauen"

# text = "nominative	einfacher	einfache	einfaches	einfache\n" \
#        "genitive	einfachen	einfacher	einfachen	einfacher\n" \
# "dative	einfachem	einfacher	einfachem	einfachen\n" \
# "accusative	einfachen	einfache	einfaches	einfache"

# text = "ich bin	wir sind\n" \
#        "du bist	ihr seid\n" \
#        "er ist	sie sind"


# text = 'entschuldig (du)	entschuldigt (ihr)'
# text = 'ich biete an	wir bieten an'

# text = 'stell vor (du)	stellt vor (ihr)'

# text = "ich half	wir halfen	ii	ich hülfe1	wir hülfen1\n" \
#        "du halfst	ihr halft	du hülfest1	ihr hülfet1\n" \
#        "er half	sie halfen	er hülfe1	sie hülfen1"

# text = "er bietet1	sie bieten2	er biete3	sie bieten9"
# text = "er isst"

# text = 'stell vor (du)	stellt vor (ihr)\n' \
#     "er xyzqwerty"
# text = "er xyzqwerty"

text = """
Nominativ	der Hof	die Höfe
Genitiv	des Hofs / des Hofes	der Höfe
Dativ	dem Hof / dem Hofe	den Höfen
Akkusativ	den Hof	die Höfe
"""

# text = 'Genitiv	des Hofs / des Hofes'

# result = run(text)
# print(result)
