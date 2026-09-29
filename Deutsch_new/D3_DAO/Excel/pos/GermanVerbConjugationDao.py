import FileContentsSplitter
import GermanPronounHelper
from GermanExcelForAnkiDao import GermanExcelForAnkiDao
from GermanVerbConjugationEntity import GermanVerbConjugationEntity


class GermanVerbConjugationDao:
    def __init__(self):
        self.germanExcelForAnkiDao = GermanExcelForAnkiDao()

    def convert_excel_rows_to_entities(self):

        results = []

        # Вычитываем Excel-данные, пользуясь наработками проекта для самоучителя Попова
        sheet_data = self.germanExcelForAnkiDao.get_verb_conjugations_sheet_data()

        # Разбиваем содержимое файла на список списков, где разделителем служит строка, содержащая инфинитив глагола
        delimiter_cb = lambda row: True if row[0] else False
        # Добавляем строку в результаты ВСЕГДА, т. е. без дополнительных условий
        addition_condition_cb = lambda row: True
        grouped_sheet_data = FileContentsSplitter.split_file_contents_by_delimiter(
            sheet_data, delimiter_cb, addition_condition_cb, include_line_with_delimiter_in_results=True)

        # Удаляем кортежи, состоящие полностью из пустых строк
        # any(t) returns True if any item in an iterable are true, otherwise it returns False
        grouped_sheet_data = [[tup for tup in sublist if any(tup)] for sublist in grouped_sheet_data]

        dashed_pattern = '{} – {}'
        for verb_rows in grouped_sheet_data:
            verb_conjugation_entity = GermanVerbConjugationEntity()
            for i in range(0, len(verb_rows)):
                row = verb_rows[i]

                # если работаем с 1-й строкой глагола (строкой, содержащей инфинитив, транскрипцию и перевод глагола)
                # if row[0]:
                if i == 0:
                    verb_conjugation_entity.infinitive = row[0]
                    verb_conjugation_entity.transcription = row[1]
                    verb_conjugation_entity.translation = row[2]

                    verb_conjugation_entity.partizip_I.front.append(row[11])
                    verb_conjugation_entity.partizip_I.transcription.append(row[12])

                    verb_conjugation_entity.infinitiv_partizip_II.front.append(
                        dashed_pattern.format(verb_conjugation_entity.infinitive, row[13]))
                    verb_conjugation_entity.infinitiv_partizip_II.transcription.append(
                        dashed_pattern.format(verb_conjugation_entity.transcription, row[14]))

                # не относится к 'if i == 0', выполняется в любом случае
                if 0 <= i <= 2:
                    # Заполняем спряжение Präsens
                    verb_conjugation_entity.präsens.front.append(dashed_pattern.format(row[3], row[5]))

                    transcr_sg = GermanPronounHelper.add_personal_pronoun_to_transcription(row[3], row[4])
                    transcr_pl = GermanPronounHelper.add_personal_pronoun_to_transcription(row[5], row[6])
                    verb_conjugation_entity.präsens.transcription.append(
                        dashed_pattern.format(transcr_sg, transcr_pl))

                    # Заполняем спряжение Konjunktiv I
                    verb_conjugation_entity.konjunktiv_I.front.append(dashed_pattern.format(row[7], row[9]))

                    transcr_sg = GermanPronounHelper.add_personal_pronoun_to_transcription(row[7], row[8])
                    transcr_pl = GermanPronounHelper.add_personal_pronoun_to_transcription(row[9], row[10])
                    verb_conjugation_entity.konjunktiv_I.transcription.append(
                        dashed_pattern.format(transcr_sg, transcr_pl))

                elif 3 <= i <= 5:
                    # Заполняем спряжение Präteritum
                    verb_conjugation_entity.präteritum.front.append(dashed_pattern.format(row[3], row[5]))

                    transcr_sg = GermanPronounHelper.add_personal_pronoun_to_transcription(row[3], row[4])
                    transcr_pl = GermanPronounHelper.add_personal_pronoun_to_transcription(row[5], row[6])
                    verb_conjugation_entity.präteritum.transcription.append(
                        dashed_pattern.format(transcr_sg, transcr_pl))

                    # Заполняем спряжение Konjunktiv II
                    verb_conjugation_entity.konjunktiv_II.front.append(dashed_pattern.format(row[7], row[9]))

                    transcr_sg = GermanPronounHelper.add_personal_pronoun_to_transcription(row[7], row[8])
                    transcr_pl = GermanPronounHelper.add_personal_pronoun_to_transcription(row[9], row[10])
                    verb_conjugation_entity.konjunktiv_II.transcription.append(
                        dashed_pattern.format(transcr_sg, transcr_pl))

                elif i == 6:
                    # Заполняем спряжение Imperativ
                    imp_sg = row[3].replace(' (du)', '!').capitalize()
                    imp_pl = row[5].replace(' (ihr)', '!').capitalize()
                    verb_conjugation_entity.imperativ.front.append(dashed_pattern.format(imp_sg, imp_pl))
                    verb_conjugation_entity.imperativ.transcription.append(dashed_pattern.format(row[4], row[6]))

            results.append(verb_conjugation_entity)

        return results


#######################################

if __name__ == '__main__':
    germanVerbConjugationService = GermanVerbConjugationDao()

    res = germanVerbConjugationService.convert_excel_rows_to_entities()
    print(res)
