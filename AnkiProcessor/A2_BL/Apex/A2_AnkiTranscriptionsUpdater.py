import beautiful_soup_helper

from AnkiConnectService import AnkiConnectService
from A0_TranscriptionHtmlFormattersController import A0_TranscriptionHtmlFormattersController
from T0_TranscriptionProcessorsController import T0_TranscriptionProcessorsController
from user_enums import Mode


# Добавляет задним числом транскрипциям уже находящимся в Анки различные доп. символы: аспирация, ассимиляция,
# маркировка альвеоляров и т. д. А также добавляет транскрипциям html-форматирование (напр., выделение синим dr/tr в
# англ. транскрипциях, выделение маркером конечного [o] в немецких транскрипциях и т. д.)
class AnkiTranscriptionsUpdater:
    def __init__(self):
        self.ankiConnectService = AnkiConnectService()
        self.t0_TranscriptionProcessorsController = T0_TranscriptionProcessorsController()
        self.a0_TranscriptionHtmlFormattersController = A0_TranscriptionHtmlFormattersController()

    # Обёртка над главным бизнес-методом update()
    def update_transcriptions_in_particular_language_decks(self, lang, mode):
        all_deck_names = self.ankiConnectService.get_all_deck_names()
        # all_deck_names = ['English']

        # Для избежания дублирования обработки одних и тех же карточек с позиций деков разного уровня вложенности,
        # обрабатываем только деки самого верхнего уровня: они и так содержат все карточки вложенных деков.
        upper_level_deck_names_set = dict.fromkeys([deck_name.split('::')[0] for deck_name in all_deck_names])
        for deck_name in upper_level_deck_names_set:
            if lang == 'deu' and not deck_name.startswith(('English', 'Italian')) or \
                    lang == 'eng' and deck_name.startswith('English') or \
                    lang == 'ita' and deck_name.startswith('Italian'):

                # Step 1
                self.update_transcriptions_using_html_formatting(deck_name, lang, mode)

                # Step 2
                # 1-й раз всегда запускать с mode=Mode.SEARCH_ONLY, чтобы увидеть форматирование каких транскрипций будет
                # сломано при последующем запуске с флагом mode=Mode.FIND_AND_REPLACE. Фиксировать в Notepad++ список этих
                # транскрипций, чтобы потом вручную восстановить их форматирование.
                self.update_transcriptions_using_aspiration_assimilation_etc(deck_name, lang, mode)

        return

    # HTML-форматирование транскрипциям добавляем обязательно отдельной транзакцией (т. е. вычитали, модифицировали
    # поле Transcription и СРАЗУ записали результаты в Анки не проводя на этом этапе больше никакого форматирования).
    # А следующий этап форматирования транскрипций тоже отработает отдельной транзакцией и тогда будет полная
    # ясность по поводу того, какое HTML-форматирование ломается логикой 2-го этапа.
    def update_transcriptions_using_html_formatting(self, deck_name, lang, mode):
        notes = self.ankiConnectService.get_notes_by_deck_name(deck_name)
        notes_to_update = []
        info_messages = []
        # цикл по всем карточкам
        for note in notes:
            if 'Transcription' not in note['fields']:
                continue

            current_transcription = note['fields']['Transcription']['value']

            updated_transcription = self.a0_TranscriptionHtmlFormattersController.format_transcription(
                current_transcription, lang)

            if current_transcription != updated_transcription:
                # Перезаписываем транскрипцию только если находимся в режиме FIND_AND_REPLACE
                if mode == Mode.FIND_AND_REPLACE:
                    # 2-й параметр - это словарь полей карточки, которые нужно обновить {название поля: новое значение поля}
                    note_dao = {'id': note['noteId'], 'fields': {'Transcription': updated_transcription}}
                    notes_to_update.append(note_dao)
                    info_message = f'{current_transcription}\n-->\n{updated_transcription}'
                    info_messages.append(info_message)

        # Сохраняем в Анки карточки с обновлённым полем Transcription
        self.ankiConnectService.update_multiple_notes_in_anki(notes_to_update)
        # Печатаем на экран отчёт об обновлённых полях карточек
        for i, info_message in enumerate(info_messages):
            print(info_message)
            print(f'note {i + 1} updated\n')

        if info_messages:
            print('\n#######################################')
            print('############ END OF STEP 1 ############')
            print('#######################################\n')

        return

    # Main business method
    def update_transcriptions_using_aspiration_assimilation_etc(self, deck_name, lang, mode):
        notes = self.ankiConnectService.get_notes_by_deck_name(deck_name)
        notes_to_update = []
        info_messages = []
        # цикл по всем карточкам
        for note in notes:
            if 'Transcription' not in note['fields']:
                continue

            current_transcription = note['fields']['Transcription']['value']

            # Формат содержимого поля 'Transcription':
            # - plain text (однополосные карточки, у которых по определению отсутствует даже тег <br>, но также
            # отсутствует и форматирование в поле 'Transcription');
            # - html-код (как минимум все многополосные карточки (из-за тега <br>), а однополосные карточки с
            # форматированием в поле 'Transcription').
            if beautiful_soup_helper.is_html(current_transcription):
                updated_transcription = self._update_in_html(current_transcription, lang, mode)
            else:
                updated_transcription = self.t0_TranscriptionProcessorsController.process_single_transcription(
                    current_transcription, lang)

            if current_transcription != updated_transcription:
                # Перезаписываем транскрипцию только если находимся в режиме FIND_AND_REPLACE
                if mode == Mode.FIND_AND_REPLACE:
                    # 2-й параметр - это словарь полей карточки, которые нужно обновить {название поля: новое значение поля}
                    note_dao = {'id': note['noteId'], 'fields': {'Transcription': updated_transcription}}
                    notes_to_update.append(note_dao)
                    info_message = f'{current_transcription}\n-->\n{updated_transcription}'
                    info_messages.append(info_message)

        # Сохраняем в Анки карточки с обновлённым полем Transcription
        self.ankiConnectService.update_multiple_notes_in_anki(notes_to_update)
        # Печатаем на экран отчёт об обновлённых полях карточек
        for i, info_message in enumerate(info_messages):
            print(info_message)
            print(f'note {i + 1} updated\n')

        return

    # Не расформировывать данный метод, т. к. он нужен, как минимум, для тестирования
    def _update_in_html(self, original_html, lang, mode):
        # Step 1. Пробуем, не нарушая html-разметки, найти и заменить целые транскрипции в текстовых узлах HTML-кода.
        # "Целые" означает, что внутри текста транскрипции, заключённого в квадратные скобки, нет доп. форматирования,
        # например, выделения цветом или маркером отдельных символов.
        # Данный шаг не сработает, если текстовый узел какого-л. тега не содержит транскрипцию в квадратных скобках
        # целиком. Для этого случая нужен следующий шаг.
        # Здесь точно такая же аналогия, как и в макросе между Paragraph и TextPortion: сначала пробуем аккуратно
        # работать внутри TextPortion (или html-тега), не нарушая форматирование, а затем в качестве проверки результата
        # обрабатываем Paragraph целиком и смотрим есть ли разница в полученных результатах.
        soup = beautiful_soup_helper.getBs(original_html)
        self._process_element_recursively(soup, lang)
        result = step1_updated_html = beautiful_soup_helper.soup_to_str(soup)

        # Step 2. Аналог обработки целого Paragraph в макросе.
        # Стрипаем у содержимого поля 'Transcription' все теги (кроме <br>) и обрабатываем получившийся текст,
        # чтобы потом сравнить его со стрипанной версией результата на 1-м шаге:
        # - совпадение результатов будет означать, что результаты работы 1-го шага удовлетворительны;
        # - несовпадение результатов будет означать, что внутри транскрипций имеется доп. форматирование (напр.,
        # выделение цветом или маркером отдельных символов), которое не дало корректно обработать транскрипцию на 1-м
        # шаге. В этом случае транскрипцию придётся перезаписать стрипанной и обработанной версией оригинального
        # html-кода, что к сожалению приведёт к потере форматирования, которое потом нужно будет восстанавливать
        # вручную.
        stripped_original_html = beautiful_soup_helper.strip_all_tags_except_br_tag(original_html)
        modified_stripped_original_html = (self.t0_TranscriptionProcessorsController.
                                           find_in_text_bracketed_transcriptions_and_process_them(
            stripped_original_html, lang))

        stripped_step1_updated_html = beautiful_soup_helper.strip_all_tags_except_br_tag(step1_updated_html)

        if modified_stripped_original_html != stripped_step1_updated_html:
            # Восстанавливаем стандартное html-форматирование в транскрипции, возможно этого будет достаточно
            # (если у транскрипции не было особенного ручного форматирования).
            # auto_restored_modified_stripped_original_html = self.transcriptionAggregatedHtmlFormatter.make_formatting(
            #     modified_stripped_original_html)
            # result = auto_restored_modified_stripped_original_html
            result = modified_stripped_original_html

            # Сначала логика должна запускаться с mode=Mode.SEARCH_ONLY чтобы увидеть форматирование каких транскрипций
            # будет сломано при запуске с флагом mode=Mode.FIND_AND_REPLACE
            if mode == Mode.SEARCH_ONLY:
                # print(f'{original_html}:\n{stripped_step1_updated_html}\n-->\n{auto_restored_modified_stripped_original_html}\n')
                print(f'{original_html}:\n{stripped_step1_updated_html}\n-->\n{modified_stripped_original_html}\n')

        return result

    # Рекурсивный метод наподобие TextReplacerInOdtFile.replace_in_paragraph(...)
    # Рекурсивно обрабатывает весь текст в HTML-элементе, включая вложенные теги.
    def _process_element_recursively(self, element, lang):
        # Обрабатываем смешанный контент (текст и теги)
        for content in element.children:
            if isinstance(content, str):  # Если это текстовый узел
                processed_text = (self.t0_TranscriptionProcessorsController.
                                  find_in_text_bracketed_transcriptions_and_process_them(content, lang))
                content.replace_with(processed_text)
            else:  # Если это тег
                self._process_element_recursively(content, lang)


#######################################################################

test_html = """
<span style="background-color: rgb(255, 255, 0);">[ˌkiloˈmeːtɐ]</span>, [ˈkiːloˌmeːtɐ]<br><span style="color: rgb(0, 170, 0);"><i>/* Более распространённым вариантом в стандартном немецком считается вариант [ˌkiloˈmeːtɐ] (с ударением на втором слоге).<br>Вариант [ˈkiːloˌmeːtɐ] (с ударением на первом слоге) встречается реже и характерен больше для южных диалектов немецкого языка или для влияния других языков, например английского.<br>Официальные словари, такие как Duden, указывают в качестве основного произношение [ˌkiloˈmeːtɐ]. */</i></span>
"""

test_html = """
[ˈd̲ɛ<span style="color: rgb(0, 0, 255);">ŋk</span>n̲̩]
"""

test_html = '[ˈtʁɪ<span style="color: rgb(0, 0, 255);">ŋk</span>n]'

test_html = '[ˈpɜːsiəs ˈtriːbæŋk]'
test_html = '[ˈpɜːsiəs ˈ<span style="color: rgb(0, 0, 255);">tr</span>iːbæŋk]'

if __name__ == '__main__':
    ankiTranscriptionsUpdater = AnkiTranscriptionsUpdater()
    # res = ankiTranscriptionsUpdater._update_in_html(test_html, 'eng', Mode.SEARCH_ONLY)
    # print(res)

    # DEUTSCH
    # Step 1. Запускаем с mode=Mode.SEARCH_ONLY, чтобы увидеть форматирование каких транскрипций будет сломано при
    # последующем запуске с флагом mode=Mode.FIND_AND_REPLACE. Фиксировать в Notepad++ список этих транскрипций,
    # чтобы потом вручную восстановить их форматирование.
    # ankiTranscriptionsUpdater.update_transcriptions_in_particular_language_decks('deu', Mode.SEARCH_ONLY)
    # Step 2. Запускаем с mode=Mode.FIND_AND_REPLACE
    # ankiTranscriptionsUpdater.update_transcriptions_in_particular_language_decks('deu', Mode.FIND_AND_REPLACE)

    # ENGLISH
    # Step 1. Запускаем с mode=Mode.SEARCH_ONLY, чтобы увидеть форматирование каких транскрипций будет сломано при
    # последующем запуске с флагом mode=Mode.FIND_AND_REPLACE. Фиксировать в Notepad++ список этих транскрипций,
    # чтобы потом вручную восстановить их форматирование.
    # ankiTranscriptionsUpdater.update_transcriptions_in_particular_language_decks('eng', Mode.SEARCH_ONLY)
    # Step 2. Запускаем с mode=Mode.FIND_AND_REPLACE
    # ankiTranscriptionsUpdater.update_transcriptions_in_particular_language_decks('eng', Mode.FIND_AND_REPLACE)

    # ITALIAN
    # Step 1. Запускаем с mode=Mode.SEARCH_ONLY, чтобы увидеть форматирование каких транскрипций будет сломано при
    # последующем запуске с флагом mode=Mode.FIND_AND_REPLACE. Фиксировать в Notepad++ список этих транскрипций,
    # чтобы потом вручную восстановить их форматирование.
    # ankiTranscriptionsUpdater.update_transcriptions_in_particular_language_decks('ita', Mode.SEARCH_ONLY)
    # Step 2. Запускаем с mode=Mode.FIND_AND_REPLACE
    # ankiTranscriptionsUpdater.update_transcriptions_in_particular_language_decks('ita', Mode.FIND_AND_REPLACE)

    input1 = [
        '<span style="background-color: rgb(255, 255, 0);">[ˌkiloˈmeːtɐ]</span>, [ˈkiːloˌmeːtɐ]<br><span style="color: rgb(0, 170, 0);"><i>/* Более распространённым вариантом в стандартном немецком считается вариант [ˌkiloˈmeːtɐ] (с ударением на втором слоге).<br>Вариант [ˈkiːloˌmeːtɐ] (с ударением на первом слоге) встречается реже и характерен больше для южных диалектов немецкого языка или для влияния других языков, например английского.<br>Официальные словари, такие как Duden, указывают в качестве основного произношение [ˌkiloˈmeːtɐ]. */</i></span>',
        '[ˈd̲ɛ<span style="color: rgb(0, 0, 255);">ŋk</span>n̲̩]',
        '[ˈʔɪmp<font color="#0000ff">e</font>ʁat̲iːf]',
        '[ˈt̲ʁɪ<span style="color: rgb(0, 0, 255);">ŋk</span>n̲̩]',
    ]

    er1 = [
        '<span style="background-color: rgb(255, 255, 0);">[ˌkʰil̲oˈmeːt̲ɐ]</span>, [ˈkʰiːl̲oˌmeːt̲ɐ]<br><span style="color: rgb(0, 170, 0);"><i>/* Более распространённым вариантом в стандартном немецком считается вариант [ˌkʰil̲oˈmeːt̲ɐ] (с ударением на втором слоге).<br>Вариант [ˈkʰiːl̲oˌmeːt̲ɐ] (с ударением на первом слоге) встречается реже и характерен больше для южных диалектов немецкого языка или для влияния других языков, например английского.<br>Официальные словари, такие как Duden, указывают в качестве основного произношение [ˌkʰil̲oˈmeːt̲ɐ]. */</i></span>',
        '[ˈd̲ɛ<span style="color: rgb(0, 0, 255);">ŋk</span>n̲̩]',
        '[ˈʔɪmp<font color="#0000ff">e</font>ʁat̲iːf]',
        '[ˈt̲ʁɪ<span style="color: rgb(0, 0, 255);">ŋk</span>n̲̩]',
    ]

    if all(ankiTranscriptionsUpdater._update_in_html(
            input_val, 'deu', Mode.FIND_AND_REPLACE) == er for input_val, er in zip(input1, er1)):
        print('test1 ok')
    else:
        print('test1 failed')
