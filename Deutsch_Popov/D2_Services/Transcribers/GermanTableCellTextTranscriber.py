import re
from itertools import zip_longest

import SentenceUtils
import Utils
from AnkiCardEntity import SINGLE_NEWLINE_SUBSTITUTE
from GermanSentenceTranscriber import GermanSentenceTranscriber
from DeuTextPreprocessor import DeuTextPreprocessor

SPACE = ' '
SLASH = '/'
SPACE_SLASH_SPACE = f'{SPACE}{SLASH}{SPACE}'


# Класс транскрибирует текст из ячейки таблицы (например, материалов Goethe-Institut) и в целом является обёрткой над
# логикой транскрибирования предложений GermanSentenceTranscriber.
# Текст в ячейке таблицы может представлять собой:
# 1) самое обычное предложение;
# 2) несколько предложений, следующих друг за другом через пробел;
# 3) несколько реплик диалога, объединённых символом новой строки;
# 4) несколько (обычно два) предложения, объединённых через '\nVS.\n'.
class GermanTableCellTextTranscriber:
    def __init__(self):
        self.deuTextPreprocessor = DeuTextPreprocessor()
        self.germanSentenceTranscriber = GermanSentenceTranscriber()

        # Глобальный список, который должен инициализироваться заново при каждом вызове главного метода для очистки
        # результатов предыдущего вызова.
        self.text_unknown_words = None

    def transcribe(self, cell_text, should_lookup_unknown_word_transcription_in_wiktionary=False):
        self.text_unknown_words = []  # поле класса
        text_transcriptions = []  # локальная переменная

        # В самую первую очередь разбиваем текстовое содержимое ячейки таблицы по строке '\nVS.\n'.
        # Если текст ячейки не содержит '\nVS.\n', в результате split-операции будет создан список с одним элементом,
        # в котором будет всё содержимое ячейки. Т. е. данная операция ничего не ломает и ни к чему не обязывает.
        vs_blocks = Utils.split_by(cell_text, '\nVS.\n')
        for vs_block in vs_blocks:
            vs_block_transcriptions = []
            # Разбиваем блок на отдельные строки. Каждая такая строка представляет собой, как правило,
            # одно предложение, но может содержать и несколько предложений, идущих друг за другом через пробел.
            lines = Utils.split_by(vs_block, '\n')
            for line in lines:
                line_transcription = self._process_line(line, should_lookup_unknown_word_transcription_in_wiktionary)
                vs_block_transcriptions.append(line_transcription)
            # end of inner loop
            vs_block_transcription = SINGLE_NEWLINE_SUBSTITUTE.join(vs_block_transcriptions)
            text_transcriptions.append(vs_block_transcription)
        # end of outer loop

        text_unknown_words_set = dict.fromkeys(self.text_unknown_words).keys()
        text_transcription = '^^^VS.^^^'.join(text_transcriptions)

        return text_unknown_words_set, text_transcription

    # 'line' - это строка, которая представляет собой, как правило, одно предложение, но может содержать
    # и несколько предложений, идущих друг за другом через пробел.
    def _process_line(self, line, should_lookup_unknown_word_transcription_in_wiktionary):
        line_transcriptions = []

        # Разбиваем line на отдельные предложения.
        # В бизнес-процессе обработки Гёте-методичек под 'line' будем понимать весь текст, идущий до символа
        # новой строки, т. е. вся строка текста целиком (ячейка таблицы может содержать несколько таких строк).
        # В большинстве случаев строка содержимого ячейки таблицы действительно содержит только ОДНО предложение,
        # но в редких случаях бывает и два предложения подряд (через пробел).
        # Когда два предложения следуют подряд одно за другим через пробел, возникает проблема поиска транскрипции
        # для 1-го слова 2-го предложения, например: 'Ich bin kulturell interessiert. Ich gehe oft ins Museum.'
        # Т. к. "Ich" 2-го предложения написано с большой буквы, его транскрипция не может быть найдена в Excel-файле,
        # т. к. для него НЕ срабатывает доп. логика преобразования 1-го слова предложения к нижнему
        # регистру (если его транскрипция не была найдена с первой попытки).
        # Разбивка такой цепочки предложений на отдельные предложения решает эту проблему, т. к. теперь
        # "Ich" 2-го предложения имеет индекс 0 в рамках своего собственного предложения, и со 2-й попытки (после
        # приведения к нижнему регистру) его транскрипция будет найдена в Excel-файле.
        line = self._preprocess_before_splitting_line_into_sentences(line)
        sentences = SentenceUtils.split_into_sentences(line)

        for sentence in sentences:
            sentence_unknown_words_set, sentence_transcription = self.germanSentenceTranscriber.transcribe_sentence(
                sentence, should_lookup_unknown_word_transcription_in_wiktionary)
            # Собирать unknown_words для каждой отдельной line не имеет бизнес-смысла, поэтому сразу складываем
            # их в коллекцию неизвестных слов всего текста.
            self.text_unknown_words.extend(sentence_unknown_words_set)
            line_transcriptions.append(sentence_transcription[1:-1])

        line_transcription = f'[{SPACE_SLASH_SPACE.join(line_transcriptions)}]'
        return line_transcription

    def _preprocess_before_splitting_line_into_sentences(self, line):
        # Вызваем замену 'z. B.' на 'zum Beispiel', чтобы точки после сокращений не воспринимались как точки в конце
        # предложений.
        line = self.deuTextPreprocessor.preprocess_zum_beispiel(line)

        if line == 'Im Zug fahre ich immer 2. Klasse.':
            line = line.replace('2. Klasse', 'zweite Klasse')

        return line


#############################################################################

table_cell_text = 'Wir haben leider keinen Garten.'
table_cell_text = '– Willst du diese Jacke?\n– Nein, ich möchte die andere.'
table_cell_text = 'Das Licht ist an.\nVS.\nDas Licht ist aus.'
table_cell_text = 'Hallo! Wie geht es dir?'

if __name__ == '__main__':
    germanTableCellTextTranscriber = GermanTableCellTextTranscriber()
    # text_unknown_words_set, text_transcription = germanTableCellTextTranscriber.transcribe(
    #     table_cell_text, True)
    # print(text_unknown_words_set)
    # print(text_transcription)

    input1 = [
        # 1. Самые простые предложения (не содержащие '\n' или '\nVS.\n'), чтобы убедиться, что вся эта сложная логика
        # работает и для них.
        'Wir haben leider keinen Garten.',
        'Am Wochenende haben wir mehrere Gäste.',

        # 2. Предложения, содержащие '\n', но не содержащие '\nVS.\n'.
        '– Willst du diese Jacke?\n– Nein, ich möchte die andere.',
        '– Claudia ist 21.\n– Was? Noch so jung?',
        '– Sind Sie verheiratet?\n– Nein. Ledig.',
        # Объединённый вариант
        '– Willst du diese Jacke?\n– Nein, ich möchte die andere.\n– Claudia ist 21.\n– Was? Noch so jung?',

        # 3. Предложения, содержащие '\nVS.\n'.
        'Das Licht ist an.\nVS.\nDas Licht ist aus.',
        'Das Fenster ist auf.\nVS.\nDas Fenster ist zu.',
        # Объединённый вариант
        'Das Licht ist an.\nVS.\nDas Licht ist aus.\nVS.\nDas Fenster ist auf.\nVS.\nDas Fenster ist zu.',
    ]

    er1 = [
        '[viːɐ̯ ˈhaːbn̩ ˈlaɪ̯dɐ ˈkaɪ̯nən ˈɡaʁtn̩]',
        '[ʔam ˈvɔxn̩ˌʔɛndə ˈhaːbn̩ viːɐ̯ ˈmeːʁəʁə ˈɡɛstə]',

        '[vɪlst duː ˈdiːzə ˈjakə]^^^[naɪ̯n ʔɪç ˈmœçtə diː ˈʔandəʁə]',
        '[ˈklaʊ̯di̯a ʔɪst ˌaɪ̯nʊntˈt͡svant͡sɪç]^^^[vas / nɔx zoː jʊŋ]',
        '[zɪnt ziː fɛɐ̯ˈhaɪ̯ʁaːtət]^^^[naɪ̯n / ˈleːdɪç]',
        '[vɪlst duː ˈdiːzə ˈjakə]^^^[naɪ̯n ʔɪç ˈmœçtə diː ˈʔandəʁə]^^^[ˈklaʊ̯di̯a ʔɪst ˌaɪ̯nʊntˈt͡svant͡sɪç]^^^[vas / nɔx zoː jʊŋ]',

        '[das lɪçt ʔɪst ʔan]^^^VS.^^^[das lɪçt ʔɪst ʔaʊ̯s]',
        '[das ˈfɛnstɐ ʔɪst ʔaʊ̯f]^^^VS.^^^[das ˈfɛnstɐ ʔɪst t͡suː]',
        '[das lɪçt ʔɪst ʔan]^^^VS.^^^[das lɪçt ʔɪst ʔaʊ̯s]^^^VS.^^^[das ˈfɛnstɐ ʔɪst ʔaʊ̯f]^^^VS.^^^[das ˈfɛnstɐ ʔɪst t͡suː]',
    ]

    # Функция zip() по умолчанию останавливается, когда заканчивается самый короткий из переданных ей итераторов.
    # Если нужно перебрать обе коллекции до конца, то можно использовать zip_longest из itertools.
    # '[1]' после вызова функции означает, что обращаемся к 1-му (а не 0-му) возвращаемому значению!
    if all(germanTableCellTextTranscriber.transcribe(
            input_val, True)[1] == er for input_val, er in zip_longest(input1, er1)):
        print('test1 ok')
    else:
        print('test1 failed')
