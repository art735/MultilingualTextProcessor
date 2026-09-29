import itertools
from collections import OrderedDict

import xlrd

import GermanPronounHelper
from GermanExcelWorkbooksDao import GermanExcelWorkbooksDao
from CharConstants import DOUBLE_NEW_LINE, SINGLE_NEW_LINE, SPACE_DASH_SPACE

NEW_LINE_SUBSTITUTOR = '^^^'
STAR_DELIMITER = '*'


class GermanExcelForAnkiDao:
    def __init__(self):
        self.germanExcelWorkbooksDao = GermanExcelWorkbooksDao()

    def make_anki_card(self, single_verb_excel_rows):
        anki_front_infinitive = ''
        anki_front_Präsens_list = []
        anki_front_Präteritum_list = []
        anki_front_Konjunktiv_I_list = []
        anki_front_Konjunktiv_II_list = []

        anki_transcription_infinitive = ''
        anki_transcription_Präsens_list = []
        anki_transcription_Präteritum_list = []
        anki_transcription_Konjunktiv_I_list = []
        anki_transcription_Konjunktiv_II_list = []

        anki_back_infinitive = ''
        anki_back_Präsens_list = []
        anki_back_Präteritum_list = []
        anki_back_Konjunktiv_I_list = []
        anki_back_Konjunktiv_II_list = []

        anki_card = ''

        counter = 0

        for t in single_verb_excel_rows:
            if any(t):  # returns True if any item in an iterable are true, otherwise it returns False
                # пустая строка в Excel используется как разделитель.
                # продолжать цикл только если строка не пустая, т. е. имеем дело со строкой данных, а не строкой-разделителем

                if t[
                    0]:  # если работаем с 1-й строкой каждого глагола (строкой, содержащей инфинитив, транскрипцию и перевод глагола)
                    anki_front_infinitive = t[0]
                    anki_front_Präsens_list.append("Präsens")
                    anki_front_Konjunktiv_I_list.append("Konjunktiv I")
                    anki_front_Partizip_I = "Partizip I" + "\n" + t[11]
                    anki_front_Partizip_II = "Partizip II" + "\n" + t[13]

                    anki_transcription_infinitive = t[1]
                    anki_transcription_Präsens_list.append("[ˈpʁɛːzɛns]")
                    anki_transcription_Konjunktiv_I_list.append("[ˈkɔnjʊŋktiːf aɪ̯ns]")
                    anki_transcription_Partizip_I = "[paʁtiˈt͡siːp aɪ̯ns]" + "\n" + t[12]
                    anki_transcription_Partizip_II = "[paʁtiˈt͡siːp t͡svaɪ̯]" + "\n" + t[14]

                    anki_back_infinitive = t[2]
                    anki_back_Präsens_list.append("спряжение в Präsens")
                    anki_back_Konjunktiv_I_list.append("спряжение в Konjunktiv I")
                    anki_back_Partizip_I = "форма Partizip I"
                    anki_back_Partizip_II = "форма Partizip II"

                if 0 <= counter <= 2:
                    # не относится к ' if t[0] != "": ', выполняется в любом случае
                    anki_front_Präsens_list.append(t[3] + SPACE_DASH_SPACE + t[5])
                    anki_transcription_Präsens_list.append(
                        GermanPronounHelper.add_personal_pronoun_to_transcription(t[3], t[
                            4]) + SPACE_DASH_SPACE + GermanPronounHelper.add_personal_pronoun_to_transcription(t[5],
                                                                                                               t[6]))

                    anki_front_Konjunktiv_I_list.append(t[7] + SPACE_DASH_SPACE + t[9])
                    anki_transcription_Konjunktiv_I_list.append(
                        GermanPronounHelper.add_personal_pronoun_to_transcription(t[7], t[
                            8]) + SPACE_DASH_SPACE + GermanPronounHelper.add_personal_pronoun_to_transcription(t[9],
                                                                                                               t[10]))

                elif 3 <= counter <= 5:
                    if counter == 3:
                        anki_front_Präteritum_list.append("Präteritum")
                        anki_front_Konjunktiv_II_list.append("Konjunktiv II")

                        anki_transcription_Präteritum_list.append("[pʁɛˈteːʁitʊm]")
                        anki_transcription_Konjunktiv_II_list.append("[ˈkɔnjʊŋktiːf t͡svaɪ̯]")

                        anki_back_Präteritum_list.append("спряжение в Präteritum")
                        anki_back_Konjunktiv_II_list.append("спряжение в Konjunktiv II")

                    anki_front_Präteritum_list.append(t[3] + SPACE_DASH_SPACE + t[5])
                    anki_transcription_Präteritum_list.append(
                        GermanPronounHelper.add_personal_pronoun_to_transcription(
                            t[3], t[4]) + SPACE_DASH_SPACE + GermanPronounHelper.add_personal_pronoun_to_transcription(
                            t[5], t[6]))

                    anki_front_Konjunktiv_II_list.append(t[7] + SPACE_DASH_SPACE + t[9])
                    anki_transcription_Konjunktiv_II_list.append(
                        GermanPronounHelper.add_personal_pronoun_to_transcription(
                            t[7], t[8]) + SPACE_DASH_SPACE + GermanPronounHelper.add_personal_pronoun_to_transcription(
                            t[9], t[10]))

                counter += 1

                if counter == 7:  # случай, когда обработали строки Excel, содержащие Präsens и Präteritum и пока больше не нужно спускаться ниже за другими формами

                    # формируем строковое представление карточки для Anki
                    anki_front = anki_front_infinitive
                    anki_front += DOUBLE_NEW_LINE + SINGLE_NEW_LINE.join(anki_front_Präsens_list)
                    anki_front += DOUBLE_NEW_LINE + SINGLE_NEW_LINE.join(anki_front_Präteritum_list)
                    anki_front += DOUBLE_NEW_LINE + anki_front_Partizip_II

                    anki_transcription = anki_transcription_infinitive
                    anki_transcription += DOUBLE_NEW_LINE + SINGLE_NEW_LINE.join(anki_transcription_Präsens_list)
                    anki_transcription += DOUBLE_NEW_LINE + SINGLE_NEW_LINE.join(anki_transcription_Präteritum_list)
                    anki_transcription += DOUBLE_NEW_LINE + anki_transcription_Partizip_II

                    anki_back = anki_back_infinitive
                    anki_back += DOUBLE_NEW_LINE + SINGLE_NEW_LINE.join(anki_back_Präsens_list)
                    anki_back += DOUBLE_NEW_LINE + SINGLE_NEW_LINE.join(anki_back_Präteritum_list)
                    anki_back += DOUBLE_NEW_LINE + anki_back_Partizip_II

                    anki_card = anki_front + DOUBLE_NEW_LINE + anki_transcription + DOUBLE_NEW_LINE + anki_back

        return anki_card

    def get_verb_conjugations_sheet_data(self):
        verbs_worksheet_indices = [0, 1, 2,  # инфинитив, транскрипция, перевод
                                   4, 5, 6, 7,  # Präsens и под ним Präteritum
                                   9, 10, 11, 12,  # Konjunktiv I и под ним Konjunktiv II
                                   14, 15, 16, 17]  # Partizip I и рядом с ним Partizip II

        sheet_data = []
        for excel_filename in GermanExcelWorkbooksDao.all_excel_filenames:
            workbook = xlrd.open_workbook(excel_filename)
            verbs_worksheet = workbook.sheet_by_name('Verbs')

            columns_list = []

            for i in verbs_worksheet_indices:
                columns_list.append(verbs_worksheet.col_values(i))

            # склеиваем список столбцов Excel так, чтобы получился список строк Excel
            sheet_data.extend(list(itertools.zip_longest(*columns_list, fillvalue="")))

        return sheet_data

    def get_verbs_for_anki(self):
        sheet_data_dict = dict()

        verb_conjugations_sheet_data = self.get_verb_conjugations_sheet_data()

        for row in verb_conjugations_sheet_data:
            if row[0]:  # если работаем со строкой Excel, содержащей инфинитив глагола
                verb_infinitive = row[0]
                sheet_data_dict[verb_infinitive] = []
            sheet_data_dict[verb_infinitive].append(row)

        # key - verb in infinitive
        # value - verb data in Anki format
        anki_cards_dict = dict()
        for infinitive, rows in sheet_data_dict.items():
            anki_cards_dict[infinitive] = self.make_anki_card(rows)

        return anki_cards_dict

    ### *** Awesome TTS ***

    def compose_single_card_for_awesome_tts(self, single_verb_excel_rows):
        anki_front_Präsens_list = []
        präsens_singular_verb_forms = []
        präsens_plural_verb_forms = []

        anki_front_Präteritum_list = []
        präteritum_singular_verb_forms = []
        präteritum_plural_verb_forms = []

        anki_front_Partizip_II_list = []

        counter = 0
        for t in single_verb_excel_rows:
            if any(t):  # returns True if any item in an iterable are true, otherwise it returns False
                # пустая строка в Excel используется как разделитель между глаголами.
                # продолжать цикл только если строка не пустая, т. е. имеем дело со строкой данных, а не строкой-разделителем

                if t[
                    0]:  # если работаем с 1-й строкой каждого глагола (строкой, содержащей инфинитив, транскрипцию и перевод глагола)
                    anki_front_infinitive = t[0]
                    anki_front_Präsens_list.append("Präsens")
                    anki_front_Partizip_II_list.append("Partizip II")
                    anki_front_Partizip_II_list.append(t[3])

                # не относится к ' if t[0] != "": ', выполняется в любом случае
                if 0 <= counter <= 2:
                    präsens_singular_verb_forms.append(t[1])
                    präsens_plural_verb_forms.append(t[2])

                elif 3 <= counter <= 5:
                    if counter == 3:
                        anki_front_Präteritum_list.append("Präteritum")
                    präteritum_singular_verb_forms.append(t[1])
                    präteritum_plural_verb_forms.append(t[2])

                counter += 1

                if counter == 7:  # случай, когда достигли в Excel пустой строки-разделителя между глаголами

                    anki_front_Präsens_list.extend(präsens_singular_verb_forms)
                    anki_front_Präsens_list.extend(präsens_plural_verb_forms)
                    anki_front_Präsens_str = ".\n".join(anki_front_Präsens_list)

                    anki_front_Präteritum_list.extend(präteritum_singular_verb_forms)
                    anki_front_Präteritum_list.extend(präteritum_plural_verb_forms)
                    anki_front_Präteritum_str = ".\n".join(anki_front_Präteritum_list)

                    anki_front_Partizip_II_str = ".\n".join(anki_front_Partizip_II_list)

                    # формируем строковое представление карточки для Anki
                    # anki_front = anki_front_infinitive + ".\n\n" + ".\n".join(anki_front_Präsens_list) + "."

                    anki_front = anki_front_infinitive + "."
                    anki_front += "\n\n" + anki_front_Präsens_str + "."
                    anki_front += "\n\n" + anki_front_Präteritum_str + "."
                    anki_front += "\n\n" + anki_front_Partizip_II_str + "."

        return anki_front

    def get_verbs_for_awesome_tts(self):
        verbs_worksheet_indices = [0,  # инфинитив
                                   4, 6,  # столбцы, содержащие формы Präsens и Präteritum
                                   16]  # Partizip II

        sheet_data = []
        columns_list = []

        anki_front_infinitive = ""

        for i in verbs_worksheet_indices:
            for excel_filename in GermanExcelWorkbooksDao.all_excel_filenames:
                workbook = xlrd.open_workbook(excel_filename)
                verbs_worksheet = workbook.sheet_by_name('Verbs')
                columns_list.append(verbs_worksheet.col_values(i))

        # склеиваем список столбцов Excel так, чтобы получился список строк Excel
        sheet_data.extend(list(itertools.zip_longest(*columns_list, fillvalue="")))
        # В результате склейки столбцов получаем следующие индексы данных:
        # 0 - infinitive
        # 1 - sg.: Präsens & Präteritum
        # 2 - pl.: Präsens & Präteritum
        # 3 - Partizip II

        # key - verb in infinitive
        # value - verb data in Anki format
        anki_cards_dict = dict()

        # Новый код!!!!!
        sheet_data_dict = dict()
        for row in sheet_data:
            if row[0]:  # если работаем со строкой Excel, содержащей инфинитив глагола
                verb_infinitive = row[0]
                sheet_data_dict[verb_infinitive] = []
            sheet_data_dict[verb_infinitive].append(row)
        ############

        for infinitive, rows in sheet_data_dict.items():
            anki_cards_dict[infinitive] = self.compose_single_card_for_awesome_tts(rows)

        return anki_cards_dict

    def get_infinitiv_partizip_ii_pairs(self):
        verbs_worksheet_indices = [0, 1, 2,  # инфинитив, транскрипция, перевод
                                   16, 17]  # Partizip II

        sheet_data = []
        columns_list = []

        for i in verbs_worksheet_indices:
            for excel_filename in GermanExcelWorkbooksDao.all_excel_filenames:
                workbook = xlrd.open_workbook(excel_filename)
                verbs_worksheet = workbook.sheet_by_name('Verbs')
                columns_list.append(verbs_worksheet.col_values(i))

        # склеиваем список столбцов Excel так, чтобы получился список строк Excel
        sheet_data.extend(list(itertools.zip_longest(*columns_list, fillvalue="")))

        # 0 - Infinitiv
        # 1 - транскрипция Infinitiv
        # 2 - перевод
        # 3 - Partizip II
        # 4 - транскрипция Partizip II

        records_dict = dict()
        for t in sheet_data:
            if any(t):  # returns True if any item in an iterable are true, otherwise it returns False
                # пустая строка в Excel используется как разделитель.
                # продолжать цикл только если строка не пустая, т. е. имеем дело со строкой данных, а не строкой-разделителем

                record_fields = []
                if t[
                    0] != "":  # если работаем с 1-й строкой каждого глагола (строкой, содержащей инфинитив, транскрипцию и перевод глагола)

                    infinitive = t[0]
                    front = "{0} – {1}".format(infinitive, t[3])
                    transcription = "{0} – {1}".format(t[1], t[4])
                    escaped_translation = str(t[2]).replace('\n', NEW_LINE_SUBSTITUTOR)
                    back = "{0}{1}{2}".format(escaped_translation, NEW_LINE_SUBSTITUTOR, "(Infinitiv – Partizip II)")

                    record_fields.append(front)
                    record_fields.append(transcription)
                    record_fields.append(back)

                    record = STAR_DELIMITER.join(record_fields)
                    records_dict[infinitive] = record

                    record_fields.clear()

        # сортируем словарь глаголов по алфавиту
        records_dict = OrderedDict(sorted(records_dict.items(), key=lambda t: t[0]))

        result = (STAR_DELIMITER + "\n").join(list(records_dict.values()))
        return result

    def get_superlative_transcription(self, superlative_adjective):
        superlative_transcription = ''
        if superlative_adjective:
            # remove surrounding square brackets and surround again with [] together with 'am'
            superlative_transcription = "[am {0}]".format(superlative_adjective[1:-1])

        return superlative_transcription

    def get_adjectives_comparison_degrees(self):
        adjectives_worksheet_indices = [0, 1,  # положительная степень c транскрипцией
                                        2,  # перевод
                                        4, 5,  # сравнительная степень c транскрипцией
                                        6, 7]  # превосходная степень c транскрипцией

        sheet_data = []
        columns_list = []

        for i in adjectives_worksheet_indices:
            for excel_filename in GermanExcelWorkbooksDao.all_excel_filenames:
                workbook = xlrd.open_workbook(excel_filename)
                adjectives_worksheet = workbook.sheet_by_name('Adjectives')
                columns_list.append(adjectives_worksheet.col_values(i))

        # склеиваем список столбцов Excel так, чтобы получился список строк Excel
        sheet_data.extend(list(itertools.zip_longest(*columns_list, fillvalue="")))

        # 0 - положительная степень
        # 1 - транскрипция положительной степени

        # 2 - перевод

        # 3 - сравнительная степень
        # 4 - транскрипция сравнительной степени

        # 5 - превосходная степень
        # 6 - транскрипция превосходной степени

        records_dict = dict()
        for t in sheet_data:
            if any(t):  # returns True if any item in an iterable are true, otherwise it returns False
                # пустая строка в Excel используется как разделитель.
                # продолжать цикл только если строка не пустая, т. е. имеем дело со строкой данных, а не строкой-разделителем

                record_fields = []
                if t[0] != "":  # если работаем с 1-й строкой каждого прилагательного

                    # если сравнит. и превосх. степени у прилагат. отсутствуют, не включаем его в результирующий набор
                    if t[3] == '' and t[5] == '':
                        continue

                    adjective_positive_degree = t[0]
                    front = "{0} – {1} – {2}".format(t[0], t[3], t[5])
                    transcription = "{0} – {1} – {2}".format(t[1], t[4], self.get_superlative_transcription(t[6]))
                    escaped_translation = str(t[2]).replace('\n', NEW_LINE_SUBSTITUTOR)
                    back = "{0}{1}{2}".format(escaped_translation, NEW_LINE_SUBSTITUTOR, "(3 степени сравнения)")

                    record_fields.append(front)
                    record_fields.append(transcription)
                    record_fields.append(back)

                    record = STAR_DELIMITER.join(record_fields)
                    records_dict[adjective_positive_degree] = record

                    record_fields.clear()

        # сортируем словарь прилагательных по алфавиту
        records_dict = OrderedDict(sorted(records_dict.items(), key=lambda t: t[0]))

        result = (STAR_DELIMITER + "\n").join(list(records_dict.values()))
        return result


##################################

if __name__ == '__main__':
    germanExcelForAnkiDao = GermanExcelForAnkiDao()

    # verb_dict = germanExcelForAnkiDao.get_verbs_for_anki()
    # for key, val in verb_dict.items():
    #     print(val)

    # verb_dict = germanExcelForAnkiDao.get_verbs_for_awesome_tts()
    # for key, val in verb_dict.items():
    #     print(val)

    # verbs = germanExcelForAnkiDao.get_infinitiv_partizip_ii_pairs()
    # print(verbs)

    # adjectives = germanExcelForAnkiDao.get_adjectives_comparison_degrees()
    # print(adjectives)
