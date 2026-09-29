from CharConstants import PIPE, COMBINING_LOW_LINE
from TextColorizer import TextColorizer

# Выделять в транскрипциях синим цветом следующие последовательности символов:

# Захватывает 4 возможных варианта: 'dr', 'd̲r', 'tr', 't̲r'. Т. е. неважно произошло уже подчёркивание альвеолярных
# d/t или нет, синим цветом данные буквы в сочетании с 'r' всё равно будут выделены.
dr_tr_regex = fr'[dt]{COMBINING_LOW_LINE}?r'
nk = r'ŋk'
search_regex = PIPE.join([dr_tr_regex, nk])


class EngTranscriptionHtmlFormatter:
    def __init__(self):
        self.textColorizer = TextColorizer()

    def format_blue(self, bracketed_transcription):
        result = self.textColorizer.colorize_blue(bracketed_transcription, search_regex)
        return result


###############################################

html_str = '[ˈdɛŋkn̩]'
html_str = '[t̲rʌŋk]'
html_str = '[triː]<br><br>[bæ<span style="color: rgb(0, 0, 255);">ŋk</span>]<br><br>[ˈtriːbæ<span style="color: rgb(0, 0, 255);">ŋk</span>]'
html_str = """
"['<span style="color: rgb(0, 0, 255);">t̲r</span>æn̲z̲iən̲t̲]"
"""

if __name__ == '__main__':
    engTranscriptionHtmlFormatter = EngTranscriptionHtmlFormatter()
    res = engTranscriptionHtmlFormatter.format_blue(html_str)
    print(res)

    input1 = [
        # Тестируем 'tr'
        '[t̲riː]',
        '[<span style="color: rgb(0, 0, 255);">t̲r</span>iː]',

        # Тестируем 'ŋk'
        '[ˈdɛŋkn̩]',
        '[ˈdɛ<span style="color: rgb(0, 0, 255);">ŋk</span>n̩]',

        # Тестируем одновременно 'tr' и 'ŋk'
        '[t̲rʌŋk]',
        '[<span style="color: rgb(0, 0, 255);">t̲r</span>ʌ<span style="color: rgb(0, 0, 255);">ŋk</span>]',
    ]

    er1 = [
        '[<span style="color: rgb(0, 0, 255);">t̲r</span>iː]',
        '[<span style="color: rgb(0, 0, 255);">t̲r</span>iː]',

        '[ˈdɛ<span style="color: rgb(0, 0, 255);">ŋk</span>n̩]',
        '[ˈdɛ<span style="color: rgb(0, 0, 255);">ŋk</span>n̩]',

        '[<span style="color: rgb(0, 0, 255);">t̲r</span>ʌ<span style="color: rgb(0, 0, 255);">ŋk</span>]',
        '[<span style="color: rgb(0, 0, 255);">t̲r</span>ʌ<span style="color: rgb(0, 0, 255);">ŋk</span>]',
    ]

    if all(engTranscriptionHtmlFormatter.format_blue(input_val) == er for input_val, er in zip(input1, er1)):
        print("test - ok")
    else:
        print("test - failed")
