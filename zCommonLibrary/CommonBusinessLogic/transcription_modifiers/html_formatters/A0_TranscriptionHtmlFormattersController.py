from DeuTranscriptionHtmlFormatter import DeuTranscriptionHtmlFormatter
from EngTranscriptionHtmlFormatter import EngTranscriptionHtmlFormatter
from TranscriptionCommentsGreenAndItalicFormatter import TranscriptionCommentsGreenAndItalicFormatter


class A0_TranscriptionHtmlFormattersController:
    def __init__(self):
        self.transcriptionCommentsGreenAndItalicFormatter = TranscriptionCommentsGreenAndItalicFormatter()
        self.deuTranscriptionHtmlFormatter = DeuTranscriptionHtmlFormatter()
        self.engTranscriptionHtmlFormatter = EngTranscriptionHtmlFormatter()

    def format_transcription(self, transcription, lang):
        # common logic for all languages
        transcription = self.transcriptionCommentsGreenAndItalicFormatter.format_comment(transcription)

        # language-specific logic
        if lang == 'eng':
            updated_transcription = self.engTranscriptionHtmlFormatter.format_blue(transcription)
        elif lang == 'deu':
            updated_transcription = self.deuTranscriptionHtmlFormatter.highlight_o_vowel_before_closing_bracket(
                transcription)
        else:
            raise Exception(f"Language '{lang}' is not supported for transcription html formatting!")

        return updated_transcription


################################################

if __name__ == "__main__":
    a0_TranscriptionHtmlFormattersController = A0_TranscriptionHtmlFormattersController()

    input_eng = [
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
    er_eng = [
        '[<span style="color: rgb(0, 0, 255);">t̲r</span>iː]',
        '[<span style="color: rgb(0, 0, 255);">t̲r</span>iː]',

        '[ˈdɛ<span style="color: rgb(0, 0, 255);">ŋk</span>n̩]',
        '[ˈdɛ<span style="color: rgb(0, 0, 255);">ŋk</span>n̩]',

        '[<span style="color: rgb(0, 0, 255);">t̲r</span>ʌ<span style="color: rgb(0, 0, 255);">ŋk</span>]',
        '[<span style="color: rgb(0, 0, 255);">t̲r</span>ʌ<span style="color: rgb(0, 0, 255);">ŋk</span>]',
    ]
    if all(a0_TranscriptionHtmlFormattersController.format_transcription(input_val, 'eng') == er for input_val, er in zip(input_eng, er_eng)):
        print("test_eng - ok")
    else:
        print("test_eng - failed")

    input_deu = [
        '[ˈɔɪ̯ʁo]',
        '[ˈɔɪ̯ʁ<span style="background-color: rgb(255, 255, 0);">o</span>]',

        '[ˈaʊ̯to]',
        '[ˈaʊ̯t<span style="background-color: rgb(255, 255, 0);">o</span>]',

        # Highlighting буквы 'о' в транскрипции, где уже имеется другое style-форматирование.
        '[ˈklɪ<span style="color: rgb(0, 0, 255);">ŋk</span>o]',
        '[ˈklɪ<span style="color: rgb(0, 0, 255);">ŋk</span><span style="background-color: rgb(255, 255, 0);">o</span>]',
    ]
    er_deu = [
        '[ˈɔɪ̯ʁ<span style="background-color: rgb(255, 255, 0);">o</span>]',
        '[ˈɔɪ̯ʁ<span style="background-color: rgb(255, 255, 0);">o</span>]',

        '[ˈaʊ̯t<span style="background-color: rgb(255, 255, 0);">o</span>]',
        '[ˈaʊ̯t<span style="background-color: rgb(255, 255, 0);">o</span>]',

        '[ˈklɪ<span style="color: rgb(0, 0, 255);">ŋk</span><span style="background-color: rgb(255, 255, 0);">o</span>]',
        '[ˈklɪ<span style="color: rgb(0, 0, 255);">ŋk</span><span style="background-color: rgb(255, 255, 0);">o</span>]',
    ]
    if all(a0_TranscriptionHtmlFormattersController.format_transcription(input_val, 'deu') == er for input_val, er in zip(input_deu, er_deu)):
        print("test_deu - ok")
    else:
        print("test_deu - failed")