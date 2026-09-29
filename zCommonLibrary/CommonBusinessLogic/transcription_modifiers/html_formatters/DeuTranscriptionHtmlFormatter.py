import re

from AnkiProcessorConstants import GERMAN_o_VOWEL, YELLOW_COLOR_RGB
from CharConstants import PIPE
from TextColorizer import TextColorizer
from TextHighlighter import TextHighlighter

# Захватывать немецкую гласную 'o', стоящую перед закрывающей квадратной скобкой и highlight её жёлтым цветом.
# Это делается для того, чтобы данная 'o' более чётко звучала в конце слова и не редуцировалась на русский манер.
# Например:
# der Euro [ˈɔɪ̯ʁo]
# das Auto [ˈaʊ̯to]
# search_regex = fr'{GERMAN_o_VOWEL}(?=\])'  # 'o' + positive lookahead

# Ищем немецкую гласную 'o' и следующую за ней закрывающую квадратную скобку и распределяем найденную информацию
# на 2 группы: 'o' и закрывающую скобку.
# Нужно обязательно указывать, что за 'o' следует ']', иначе алгоритм будет заменять любую букву на 'o' на указанный
# replacement, что совершенно сломает входную html-строку.
search_regex = fr'({GERMAN_o_VOWEL})(\])'


class DeuTranscriptionHtmlFormatter:
    def __init__(self):
        self.textHighlighter = TextHighlighter()

    def highlight_o_vowel_before_closing_bracket(self, bracketed_transcription):
        # result = self.textHighlighter.highlight_yellow(html_str, search_regex)

        # Очень прямолинейное решение, не подключает умную логику обхода узлов из A0_CoreAnkiFormatter, которую
        # не получилось быстро сюда подключить через класс-обёртку TextHighlighter.
        result = re.sub(
            search_regex,
            lambda m: fr'<span style="background-color: {YELLOW_COLOR_RGB};">{m.group(1)}</span>{m.group(2)}',
            bracketed_transcription
        )

        return result


###############################################

html_str = '[ˈɔɪ̯ʁo]'
html_str = '[ˈɔɪ̯ʁ<span style="background-color: rgb(255, 255, 0);">o</span>]'
html_str = '[ˈklɪ<span style="color: rgb(0, 0, 255);">ŋk</span>o]'
# html_str = '[ˈklɪ<span style="color: rgb(0, 0, 255);">ŋk</span><span style="background-color: rgb(255, 255, 0);">o</span>]'

# html_str = '[ˈaʊ̯to]'
# html_str = '[ˈaʊ̯t<span style="background-color: rgb(255, 255, 0);">o</span>]'

if __name__ == '__main__':
    deuTranscriptionHtmlFormatter = DeuTranscriptionHtmlFormatter()
    res = deuTranscriptionHtmlFormatter.highlight_o_vowel_before_closing_bracket(html_str)
    print(res)

    input1 = [
        '[ˈɔɪ̯ʁo]',
        '[ˈɔɪ̯ʁ<span style="background-color: rgb(255, 255, 0);">o</span>]',

        '[ˈaʊ̯to]',
        '[ˈaʊ̯t<span style="background-color: rgb(255, 255, 0);">o</span>]',

        # Highlighting буквы 'о' в транскрипции, где уже имеется другое style-форматирование.
        '[ˈklɪ<span style="color: rgb(0, 0, 255);">ŋk</span>o]',
        '[ˈklɪ<span style="color: rgb(0, 0, 255);">ŋk</span><span style="background-color: rgb(255, 255, 0);">o</span>]',
    ]

    er1 = [
        '[ˈɔɪ̯ʁ<span style="background-color: rgb(255, 255, 0);">o</span>]',
        '[ˈɔɪ̯ʁ<span style="background-color: rgb(255, 255, 0);">o</span>]',

        '[ˈaʊ̯t<span style="background-color: rgb(255, 255, 0);">o</span>]',
        '[ˈaʊ̯t<span style="background-color: rgb(255, 255, 0);">o</span>]',

        '[ˈklɪ<span style="color: rgb(0, 0, 255);">ŋk</span><span style="background-color: rgb(255, 255, 0);">o</span>]',
        '[ˈklɪ<span style="color: rgb(0, 0, 255);">ŋk</span><span style="background-color: rgb(255, 255, 0);">o</span>]',
    ]

    if all(deuTranscriptionHtmlFormatter.highlight_o_vowel_before_closing_bracket(input_val) == er for input_val, er in zip(input1, er1)):
        print("test - ok")
    else:
        print("test - failed")
