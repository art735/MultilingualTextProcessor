import re

import NbspProcessor
from CharConstants import COMBINING_LOW_LINE, BRIDGE_BELOW

# альвеолярные согласные
alveolar_consonant = fr'[tdszln]'




class TranscriptionAlveolarMarker:
    """
    A service for marking alveolar consonants in English/German phonetic transcription
    by adding combining low line (U+0332) to specified characters.
    """

    def __init__(self):
        pass

    def mark_alveolars(self, bracketed_transcription):
        # Неразрывные пробелы (&nbsp;) в поле Transcription и так удаляются при запуске AnkiCardsAppearanceProcessor,
        # который обычно запускается вручную после каждого импорта карточек из .csv-файла.
        # Но нередко карточка добавляется вручную и в этом случае '&nbsp;' иногда просачиваются в поле Transcription.
        # Следующая строка гарантирует, что неразрывные пробелы будут заменяться на обычные пробелы, иначе логика
        # подчёркивания альвеолярных согласных сделает из правильного '&nbsp;' битый '&n̲bs̲p;'.
        bracketed_transcription = NbspProcessor.replace_nbsp_with_regular_space(bracketed_transcription)

        # Не добавляем соединительную нижнюю линию в двух случаях:
        # 1) если она уже ранее была добавлена (т. е. технически если она следует за альвеолярным согласным);
        # 2) если альвеолярный согласный стал зубным (для него сработали ранее правила ассимиляции).
        # В остальных случаях добавляем соединительную нижнюю линию.
        pattern = fr"{alveolar_consonant}(?![{COMBINING_LOW_LINE}{BRIDGE_BELOW}])"  # negative lookahead
        replacement = fr"\g<0>{COMBINING_LOW_LINE}"
        result = re.sub(pattern, replacement, bracketed_transcription)
        return result


#################################################################

test_str = '[triː]<br><br>[bæ<span style="color: rgb(0, 0, 255);">ŋk</span>]<br><br>[ˈtriːbæ<span style="color: rgb(0, 0, 255);">ŋk</span>]'
test_str = '[ˈtriːbæ'

# Usage example
if __name__ == '__main__':
    transcriptionAlveolarMarker = TranscriptionAlveolarMarker()
    res = transcriptionAlveolarMarker.mark_alveolars(test_str)
    print(res)

    input1 = [
        # Проверяем, что маркер добавляется
        "[ˈtaːk]", "[ˈzɔnə]", "[ˈlaːgə]", "[ˈʃtʊndə]",
        # Проверяем, что маркер НЕ добавляется повторно
        "[ˈt̲aːk]", "[ˈz̲ɔn̲ə]", "[ˈl̲aːgə]", "[ˈʃt̲ʊn̲d̲ə]",
        # Проверяем, что маркер НЕ добавляется к тем альвеолярам, которые стали зубными (напр., в рез-те ассимиляции)
        "[feɪt̪ d̪eɪ]",
    ]

    er1 = [
        "[ˈt̲aːk]", "[ˈz̲ɔn̲ə]", "[ˈl̲aːgə]", "[ˈʃt̲ʊn̲d̲ə]",
        "[ˈt̲aːk]", "[ˈz̲ɔn̲ə]", "[ˈl̲aːgə]", "[ˈʃt̲ʊn̲d̲ə]",
        "[feɪt̪ d̪eɪ]",
    ]

    if all(transcriptionAlveolarMarker.mark_alveolars(input_val) == er for input_val, er in zip(input1, er1)):
        print('test1 ok')
    else:
        print('test1 failed')
