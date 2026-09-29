import RegExConstants
from A20_GreenAndItalicFormatter import A20_GreenAndItalicFormatter

# Форматировщик зелёным и курсивом содержимого круглых скобок в Anki-поле Transcription
class TranscriptionCommentsGreenAndItalicFormatter:
    # Регулярное выражение для захвата следующих последовательностей символов, заключённых в круглые скобки:
    # ['eɪərɪs̲t̲], ['ɛərɪs̲t̲] (BrE)
    # ['eɪərɪs̲t̲], ['ɛərɪs̲t̲] (BrE, CollinsDictionary) /* после BrE ещё может идти произвольный текст */
    # ['kʰæt̲əɡɔːri] (AmE)
    # ['kʰæt̲əɡɔːri] (AmE, Lingvo) /* после AmE ещё может идти произвольный текст */
    # [mə'riːə] (BrE, AmE)
    # [prɪ's̲ɪʒ(ə)n̲] (BrE, AmE; Oxford) /* после BrE & AmE ещё может идти произвольный текст */
    terms = r'(?:BrE|AmE).*'
    search_regex_bre_ame = RegExConstants.parentheses_lookarounds.format(terms)

    START_OF_SINGLE_LINE_COMMENT = r'//'
    search_regex_single_line_comment = fr'{START_OF_SINGLE_LINE_COMMENT}.*'

    # Здесь под многострочным комментарием имеется в виду его декоративный вид (начало на '/*' и конец на '*/'), но
    # не то, что он буквально может занимать несколько строк, разделённых символами <br>. Нет! Так его форматирование
    # зелёным цветом и курсивом работать не будет! Такой комментарий должен занимать одну строку и символы <br>
    # не должны входить в него.
    START_OF_MULTILINE_COMMENT = r'/\*'
    END_OF_MULTILINE_COMMENT = r'\*/'
    search_regex_multi_line_comment = fr'{START_OF_MULTILINE_COMMENT}.*{END_OF_MULTILINE_COMMENT}'

    def __init__(self):
        self.a20_GreenAndItalicFormatter = A20_GreenAndItalicFormatter()

    def format_comment(self, html_str):

        html_stripes = html_str.split("<br><br>")
        processed_html_stripes = []
        for html_stripe in html_stripes:
            html_lines = html_stripe.split("<br>")
            processed_stripe_lines = []
            for html_line in html_lines:
                processed_html_line = self.process_single_html_line(html_line)
                processed_stripe_lines.append(processed_html_line)
            processed_stripe = "<br>".join(processed_stripe_lines)
            processed_html_stripes.append(processed_stripe)
        processed_html_str = "<br><br>".join(processed_html_stripes)
        return processed_html_str

    def process_single_html_line(self, html_line):
        result = html_line
        for regex in [self.search_regex_bre_ame, self.search_regex_single_line_comment,
                      self.search_regex_multi_line_comment]:
            result = self.a20_GreenAndItalicFormatter.make_green_and_italic(result, regex)
        return result


##############################################################

test_html_str = "[prɪ's̲ɪʒ(ə)n̲] (BrE, AmE; Oxford)"
# test_html_str = "['kʰæt̲əɡəri] (BrE)<br>['kʰæt̲əɡɔːri] (AmE)"
# test_html_str = "['eɪərɪs̲t̲], ['ɛərɪs̲t̲] (BrE, CollinsDictionary)"

test_html_str = """
[транскрипция1]<br><br>[транскрипция2]<br>// это однострочный комментарий<br><br>[транскрипция3]<br>/* это многострочный комментарий */<br><br>[транскрипция4]
"""

if __name__ == '__main__':
    transcriptionCommentsGreenAndItalicFormatter = TranscriptionCommentsGreenAndItalicFormatter()
    res = transcriptionCommentsGreenAndItalicFormatter.format_comment(test_html_str)
    print(res)

    input1 = [
        # BrE
        "['eɪərɪs̲t̲], ['ɛərɪs̲t̲] (BrE)",
        "['eɪərɪs̲t̲], ['ɛərɪs̲t̲] (BrE, CollinsDictionary)",
        # AmE
        "['kʰæt̲əɡɔːri] (AmE)",
        "['kʰæt̲əɡɔːri] (AmE, Lingvo)",
        # BrE, AmE
        "[mə'riːə] (BrE, AmE)",
        "[prɪ's̲ɪʒ(ə)n̲] (BrE, AmE; Oxford)",
        # обработка одно- и многострочных комментариев
        "[транскрипция1]<br><br>[транскрипция2]<br>// это однострочный комментарий<br><br>[транскрипция3]<br>/* это многострочный комментарий */<br><br>[транскрипция4]"
    ]

    er1 = [
        # BrE
        """['eɪərɪs̲t̲], ['ɛərɪs̲t̲] (<span style="color: rgb(0, 170, 0);"><i>BrE</i></span>)""",
        """['eɪərɪs̲t̲], ['ɛərɪs̲t̲] (<span style="color: rgb(0, 170, 0);"><i>BrE, CollinsDictionary</i></span>)""",
        # AmE
        """['kʰæt̲əɡɔːri] (<span style="color: rgb(0, 170, 0);"><i>AmE</i></span>)""",
        """['kʰæt̲əɡɔːri] (<span style="color: rgb(0, 170, 0);"><i>AmE, Lingvo</i></span>)""",
        # BrE, AmE
        """[mə'riːə] (<span style="color: rgb(0, 170, 0);"><i>BrE, AmE</i></span>)""",
        """[prɪ's̲ɪʒ(ə)n̲] (<span style="color: rgb(0, 170, 0);"><i>BrE, AmE; Oxford</i></span>)""",
        # обработка одно- и многострочных комментариев
        """[транскрипция1]<br><br>[транскрипция2]<br><span style="color: rgb(0, 170, 0);"><i>// это однострочный комментарий</i></span><br><br>[транскрипция3]<br><span style="color: rgb(0, 170, 0);"><i>/* это многострочный комментарий */</i></span><br><br>[транскрипция4]"""
    ]

    if all(transcriptionCommentsGreenAndItalicFormatter.format_comment(input_val) == er for input_val, er in zip(input1, er1)):
        print('test1 ok')
    else:
        print('test1 failed')
