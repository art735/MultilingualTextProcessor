import re

import OxfordDictionaryDao


def _preprocess_input(input_text):
    result = input_text
    # заменить символ переноса строки, стоящий перед открывающей круглой скобкой + pl на пробел
    # эта замена нужна для того, чтобы форма мн. ч., отформатированная для красоты с новой строки, не воспринималась как новое и другое слово
    # символ \n окружён \s* потому что в GUI компонент ввода работает так, что добавляет лишние пробелы в начале и конце каждой строки
    # так что нужно захватывать и эти лишние авто-добавляемые пробелы, которых нет в оригинальном тексте в .odt-файле со словами
    result = re.sub(r'\s*\n\s*(?=\(pl)', r' ', result)
    return result


def look_up(input_text):
    results = []
    preprocessed_input_text = _preprocess_input(input_text)
    words = [s.strip() for s in preprocessed_input_text.split("\n") if
             len(s)]  # взять в дальнейшую работу только непустые строки
    for word in words:
        british_transcr, american_transcr = OxfordDictionaryDao.get_word_british_and_american_transcriptions(word, 1)

        if british_transcr == american_transcr:
            transcription = british_transcr
        else:
            transcription = british_transcr + ' (BrE)^^^' + american_transcr + ' (AmE)'

        result = "{0}|{1}".format(word, transcription)
        results.append(result)

    output = '\n'.join(results)
    return output


###########################################


input = """a
to abandon
abbreviation
ABC
ABC-book
to abduct
"""

input = 'ABC'

input = """Englishman 
(pl Englishmen)"""

# out = look_up(input)
# print(out)

# input = """Englishman
# (pl Englishmen)"""
# output = preprocess_input(input)
# print(output)
