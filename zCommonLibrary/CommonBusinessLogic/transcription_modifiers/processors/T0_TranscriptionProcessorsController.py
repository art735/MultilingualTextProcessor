# -*- coding: utf-8 -*-
import re

from GermanTranscriptionGlottalStopAppender import GermanTranscriptionGlottalStopAppender
from TranscriptionAlveolarMarker import TranscriptionAlveolarMarker
from TranscriptionAspirationService import TranscriptionAspirationService
from TranscriptionAssimilationService import TranscriptionAssimilationService
from TranscriptionFinal_ɪ_with_i_SoundReplacer import TranscriptionFinal_ɪ_with_i_SoundReplacer


class T0_TranscriptionProcessorsController:
    def __init__(self):
        pass

    # Метод-обёртка, принимающий за один раз всю информацию из OpenOffice-макроса. Важно сработать именно "за один раз",
    # т. к. передача данных осуществляется через http-сервер из-за невозможности вызвать напрямую Python3-бизнес-логику
    # из Python2-макроса.
    def process_transcriptions(self, data, lang):
        processed_data = []
        for par_text, par_text_portions in data:
            par_text_processed = self.find_in_text_bracketed_transcriptions_and_process_them(par_text, lang)
            par_text_portions_processed = []
            for par_text_portion in par_text_portions:
                par_text_portion_processed = self.find_in_text_bracketed_transcriptions_and_process_them(par_text_portion, lang)
                par_text_portions_processed.append(par_text_portion_processed)

            processed_data.append((par_text_processed, par_text_portions_processed))

        return processed_data

    # Данный метод вызывается как минимум в 2-х местах:
    # 1) в A2_AnkiTranscriptionsUpdater.py
    # 2) в Python-макросе для LibreOffice.
    # В первом случае метод принимает на вход html-разметку поля Transcription, а во втором - текст элементов
    # "com.sun.star.text.TextPortion" и "com.sun.star.text.Paragraph".
    # Данный метод является умной обёрткой над process_single_transcription(...).
    def find_in_text_bracketed_transcriptions_and_process_them(self, original_transcription_containing_text, lang):
        modified_transcription_containing_text = original_transcription_containing_text
        transcriptions = re.findall(r'\[.*?\]', original_transcription_containing_text)
        for transcription in transcriptions:
            processed_transcription = self.process_single_transcription(transcription, lang)
            if processed_transcription != transcription:
                modified_transcription_containing_text = modified_transcription_containing_text.replace(
                    transcription, processed_transcription)

        return modified_transcription_containing_text

    def process_single_transcription(self, bracketed_transcription, lang):

        # Общая для английского/немецкого языка логика обработки транскрипции
        common_en_de_actions = [
            # Важно, чтобы аспирация была первой в этом списке, т. к. в противном случае (например, после подчёркивания
            # альвеоляров) аспирация может не всегда корректно срабатывать.
            TranscriptionAspirationService().aspirate,
            TranscriptionAlveolarMarker().mark_alveolars
        ]

        language_specific_actions = {
            "eng": [
                *common_en_de_actions,
                TranscriptionAssimilationService().assimilate,
                TranscriptionFinal_ɪ_with_i_SoundReplacer().replace_final_ɪ_with_i
                # EngTranscriptionBlueHtmlFormatter сюда НЕ добавляем, т. к. он вызывается в отдельной логике
            ],
            "deu": [
                *common_en_de_actions,
                GermanTranscriptionGlottalStopAppender().add_glottal_stops
                # DeuTranscriptionYellowHtmlHighlighter сюда НЕ добавляем, т. к. он вызывается в отдельной логике
            ],
            # В итальянском языке [ptk] НЕ придыхаются, но зато [tdszln] являются альвеолярными!
            "ita": [
                TranscriptionAlveolarMarker().mark_alveolars
            ],
        }

        processed_transcription = bracketed_transcription
        for method in language_specific_actions.get(lang, []):
            processed_transcription = method(processed_transcription)

        return processed_transcription


########################################################

transcription = '[wɪð ˈtaɪtl]'
# transcription = '[ˈtaːk]'
# transcription = '[ˈzɔnə]'
# transcription = '[ɡriːn ˈtʌm]'


if __name__ == '__main__':
    t0_TranscriptionProcessorsController = T0_TranscriptionProcessorsController()
    res = t0_TranscriptionProcessorsController.process_single_transcription(transcription, 'eng')
    print(res)

    input1 = [
        '[wɪð ˈtaɪtl]',
        "[ˈtaːk]", "[ˈzɔnə]", "[ˈlaːgə]", "[ˈʃtʊndə]",
        "[ɡriːn ˈtʌm]"
    ]

    er1 = [
        # ChatGPT-4o и другие AI-чаты подтверждают, что аспирация и ассимиляция звука [t] никак не влияют друг на друга
        # и не отменяют друг друга: здесь звук [t] одновременно и аспирируется, и ассимилируется!
        "[wɪd̪ ˈt̪ʰaɪt̲l̲]",
        "[ˈt̲ʰaːk]", "[ˈz̲ɔn̲ə]", "[ˈl̲aːgə]", "[ˈʃt̲ʊn̲d̲ə]",
        "[ɡriːn̲ ˈt̲ʰʌm]"
    ]

    if all(t0_TranscriptionProcessorsController.process_single_transcription(input_val, 'eng') == er for input_val, er in
           zip(input1, er1)):
        print('test1 ok')
    else:
        print('test1 failed')
