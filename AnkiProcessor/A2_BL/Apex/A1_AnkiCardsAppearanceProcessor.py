from ParContentsUnitalicizer import ParContentsUnitalicizer
from TranscriptionCommentsGreenAndItalicFormatter import TranscriptionCommentsGreenAndItalicFormatter
from ColorTagProcessor import ColorTagProcessor
import CommonTextIssuesRemover
from DivStripper import DivStripper
import NbspProcessor
import beautiful_soup_helper
from A12_ItalicOnlyFormatter import A12_ItalicOnlyFormatter
from AnkiConnectService import AnkiConnectService

from B1_LastStripeInBoldFormatter import B1_LastStripeInBoldFormatter
from GreenAndItalicAggregator import GreenAndItalicAggregator
from VerbConjugationFormatter import VerbConjugationFormatter
from user_enums import Mode

ankiConnectService = AnkiConnectService()

all_possible_fields = ['Front', 'Front_comment', 'Taggy', 'SSML', 'Audio1', 'Audio2', 'Image', 'Transcription',
                       'Grammar', 'Back', 'Back_comment']

# Добавил в ignored_fields и поле Image, потому что название картинки содержит точку и расширение (.img, .png) и
# иногда текстовый поиск-замена нарушали целостность имени файла картинки (например, точка с расширением отделялись
# пробелом от остальной части имени файла), и она переставала быть доступной.
ignored_fields = ['SSML', 'Audio1', 'Audio2', 'Image']

globally_allowed_fields = [item for item in all_possible_fields if item not in ignored_fields]

# Именно объект класса, а не сам класс, нужен для работы с callback-ом
divStripper = DivStripper()
colorTagProcessor = ColorTagProcessor()
verbConjugationFormatter = VerbConjugationFormatter()
greenAndItalicAggregator = GreenAndItalicAggregator()
transcriptionCommentsGreenAndItalicFormatter = TranscriptionCommentsGreenAndItalicFormatter()
a12_ItalicOnlyFormatter = A12_ItalicOnlyFormatter()
parContentsUnitalicizer = ParContentsUnitalicizer()
b1_LastStripeInBoldFormatter = B1_LastStripeInBoldFormatter()


# TODO Сделать профили-наборы callback-ов на разные случаи жизни:
# - разово очистить содержимое всех полей карточки (кроме поля SSML, там могут быть специальные теги:
# не во внутренней структуре поля, а в самом его текстовом видимом содержимом, их нельзя стрипать,
# иначе эта информация будет утеряна)
# - разово сделать содержимое любых круглых скобок italic

callbacks_dict = {
    CommonTextIssuesRemover.fix_problems: globally_allowed_fields,
    divStripper.strip_div_tags: [*globally_allowed_fields, 'Image'],
    colorTagProcessor.treat_colors: globally_allowed_fields,
    greenAndItalicAggregator.execute_all_the_methods: ['Front', 'Front_comment', 'Back', 'Back_comment'],
    NbspProcessor.insert_nbsp_before_opening_parenthesis: ['Front', 'Front_comment', 'Grammar', 'Back', 'Back_comment'],
    NbspProcessor.replace_nbsp_with_regular_space: ['Transcription'],
    transcriptionCommentsGreenAndItalicFormatter.format_comment: ['Transcription'],
    verbConjugationFormatter.format_verb: ['Front', 'Front_comment', 'Transcription', 'Back', 'Back_comment'],
    # Новая логика!
    # TODO отключать, когда НЕ нужно содержимое всех круглых скобок делать курсивом
    a12_ItalicOnlyFormatter.make_italic_all_contents_of_all_balanced_pars: ['Front', 'Back'],
    parContentsUnitalicizer.unitalicize: ['Front', 'Back'],  # убираем курсив вокруг некоторых слов в круглых скобках

    # b1_LastStripeInBoldFormatter.make_last_stripe_bold: ['Front', 'Back'],

    # lambda m: m.replace('hello', ''): ['Front', 'Back']
    # lambda m: m + ' world': ['Front', 'Back']
}

# Набор callback-ов для работы только с полем Transcription. Раскомментировать при необходимости.
# callbacks_dict = {
#     CommonTextIssuesRemover.fix_problems: ['Transcription'],
#     DivStripper.strip_div_tags: ['Transcription'],
#     colorTagProcessor.treat_colors: ['Transcription'],
#     NbspProcessor.replace_nbsp_with_regular_space: ['Transcription'],
#     a25_TranscriptionGreenAndItalicFormatter.format_transcription: ['Transcription'],
#     verbConjugationFormatter.format_verb: ['Transcription'],
# }

# transcriptionFinal_ɪ_with_i_SoundReplacer = TranscriptionFinal_ɪ_with_i_SoundReplacer()
# callbacks_dict = {
#     transcriptionFinal_ɪ_with_i_SoundReplacer.replace_final_ɪ_with_i: ['Front', 'Back']
# }

class AnkiCardsAppearanceProcessor:
    def __init__(self):
        pass

    def process(self, notes, mode, strip_all_tags_except_br_and_img_tags=False):
        notes_to_update = []
        info_messages = []

        # 1. Перебор всех карточек для формирования результата
        for note in notes:
            note_updated_fields_dict, info_message = self.process_single_note(note, strip_all_tags_except_br_and_img_tags)
            # Если словарь не пустой, т. е. хотя бы одно поле было обновлено
            if note_updated_fields_dict and mode == Mode.FIND_AND_REPLACE:
                note_dao = {'id': note['noteId'], 'fields': note_updated_fields_dict}
                notes_to_update.append(note_dao)
                info_messages.append(info_message)

        # 2. Вывод результата на экран и в Анки (если позволяет флаг)
        if mode == Mode.SEARCH_ONLY:
            [print(msg) for msg in self.messages]
        elif mode == Mode.FIND_AND_REPLACE:
            # Сохраняем в Анки обновлённые поля карточек
            ankiConnectService.update_multiple_notes_in_anki(notes_to_update)
            # Печатаем на экран отчёт об обновлённых полях карточек
            for i, info_message in enumerate(info_messages):
                print(info_message)
                print(f'note {i + 1} updated\n')

    def process_single_note(self, note, strip_all_tags_except_br_and_img_tags):
        # Количество повторов операций поиска и замены всеми callback-ами. Одного раунда часто бывало не достаточно,
        # поэтому желательно делать 2-3 повтора не вручную (как раньше), а с помощью регуляции этой переменной.
        no_of_find_and_replace_cycles = 2
        field_messages = []
        note_updated_fields_dict = {}
        # Цикл по всем полям 'карточки' (более точно - по всем полям note-а)
        for field_name, field_data_dict in note['fields'].items():

            # сбрасываем флаг
            is_field_already_stripped = False

            # сохранение текущего значения поля карточки в отдельную переменную
            old_value = updated_value = field_data_dict['value']
            # old_value = value['value']
            # updated_value = value['value']

            # 2-й цикл: количество раундов поиска-замены (подбирается эмпирически: одного раунда, как показывает
            # практика, – мало; должно быть несколько раундов)
            for j in range(0, no_of_find_and_replace_cycles):
                # print(f'j = {j}')
                # 3-й цикл: по всем callback-ам бизнес-логики форматирования и разрешённым для каждого из них
                # спискам полей
                for callback, cb_allowed_fields in callbacks_dict.items():
                    if field_name in cb_allowed_fields:
                        # Стрипаем содержимое поля (если флаг разрешает) и снова его форматируем callback-ами.

                        # Если флаг разрешает стрипать поле, сначала процессим его общими функциями, отвечающими за
                        # структуру текста поля, т. е. воздействуем на его теги возможно заменяя их другими тегами,
                        # а затем уже стрипаем его от лишних тегов.
                        if strip_all_tags_except_br_and_img_tags and not is_field_already_stripped:
                            updated_value = CommonTextIssuesRemover.fix_problems(updated_value)
                            updated_value = divStripper.strip_div_tags(updated_value)
                            updated_value = beautiful_soup_helper.strip_all_tags_except_br_and_img_tags(updated_value)
                            is_field_already_stripped = True
                        # Обработка поля с помощью callback-а
                        updated_value = callback(updated_value)

            if updated_value != old_value:
                # Сохранение обновленного значения поля в специальный словарь
                note_updated_fields_dict[field_name] = updated_value
                # Формирование сообщения об обновлённом поле для вывода на экран
                msg_part1 = f'{field_name}:\n'
                msg_part2 = f'{old_value}\n-->\n{updated_value}\n'
                msg = msg_part1 + msg_part2
                field_messages.append(msg)

        info_message = '\n'.join(field_messages).strip()  # удаляет символы [ \t\n\r\f\v] в начале и конце строки
        return note_updated_fields_dict, info_message


###################################

test_note = {
    'fields': {
        # 'noteId': {
        #     'value': 1
        # },
        #
        # 'Front': {
        #     'value': 'Что такое Python?'
        # },
        'Back': {
            'value': '[<span style="color: rgb(0, 170, 0);"><i>амер.</i></span>]<br>1) авто джип<br>2) авиа небольшой разведывательный самолёт<br>3) <span style="color: rgb(0, 170, 0);"><i>воен.; жарг.</i></span> новичок, новобранец'
        }
    }
}

test_notes = [test_note]

# process(notes, Mode.FIND_AND_REPLACE)
