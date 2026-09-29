import json
import os
import re
import sqlite3
import zipfile
from pathlib import Path

import beautiful_soup_helper
from AnkiConnectService import AnkiConnectService
from user_enums import Mode

# Задача данного модуля взять за основу мои немецкие карточки и сравнить их с карточками Наташи, выполняя при
# необходимости замены в Наташиных карточках так, чтобы они соответствовали моим карточкам.

# Мои карточки экспортируются в .apkg-файл и вычитываются из него.
# Наташины карточки вычитываются непосредственно из Анки (из аккаунта Наташи).

# 1. Выполнить экспорт колоды из Анки (File -> Export) со следующими настройками:
# Export format: Anki Deck Package (.apkg)
# обязательно включить галочку "Support older Anki versions (slower/larger files)".

# 2.1 Поменять расширение .apkg -> .zip и распаковать архив вручную.
# .apkg - это, по сути, обычный .zip-архив, который содержит 2 варианта SQLite-базы данных (collection.anki2 и
# collection.anki21) + медиафайлы.
# -или-
# 2.2 Выполнить распаковку .apkg-файла автоматически (без ручной замены расширения на .zip)

# Задаём имя колоды, с которой работаем и имя файла, в который она была импортирована
# natali_deck_name = '!Deutsch. !Словарь::!Goethe-Institut A1'
# apkg_file = r'C:\Users\user\Desktop\apkg\german.apkg'
# ---
natali_deck_name = 'temp'
apkg_file = r'C:\Users\user\Desktop\apkg\temp.apkg'

# Извлекаем путь к папке с .apkg-файлом
apkg_file_dir = str(Path(apkg_file).parent)
# Извлекаем имя .apkg-файла (без расширения)
apkg_filename_without_ext = Path(apkg_file).stem

# Задаём путь к временной папке для извлечения содержимого .apkg-файла:
# 1) расположим эту папку на одном иерархическом уровне с .apkg-файлом;
# 2) дадим этой папке такое же имя, как и у .apkg-файла.
extract_dir = fr'{apkg_file_dir}\{apkg_filename_without_ext}'

# Извлечение архива.
# По умолчанию метод extractall() будет распаковывать файлы в указанную папку, даже если она уже существует и содержит
# файлы. При этом:
# 1) если в папке уже есть файлы с такими же именами, они будут перезаписаны новыми файлами из архива;
# 2) существующие файлы в папке, имена которых не совпадают с файлами в архиве, останутся нетронутыми.
directory_exists = os.path.exists(extract_dir)  # Папка существует
is_directory_empty = not os.listdir(extract_dir) if directory_exists else True  # Папка пуста, если существует
if not directory_exists or is_directory_empty:
    with zipfile.ZipFile(apkg_file, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    print("The archive has been successfully unpacked.")
else:
    print("The folder already exists and is not empty. Unpacking was not performed.")

# 3. Подключиться с помощью Python-скрипта к базе данных collection.anki21 и вычитать из неё данные.

# Путь к файлу базы данных
anki_db_path = fr'{extract_dir}\collection.anki21'


# 5. Вычитать из Анки карточки Наташи и провести сравнение с моими карточками.


class AnkiLocalApkgWithNataliAccountSynchronizer:

    def __init__(self):
        self.ankiConnectService = AnkiConnectService()

        self.apkg_notes = self._read_notes_from_unzipped_apkg_db()
        self.inverted_media_json = self._load_and_invert_media_json()

        natali_notes = self.ankiConnectService.get_notes_by_deck_name(natali_deck_name)
        # key: Front field; value: note itself
        self.natali_notes_dict = {natali_note['fields']['Front']['value']: natali_note for natali_note in natali_notes}

        self.note_updated_fields_dict = {}
        self.print_log_dict = {}
        self.should_reset_note_cards_to_new = False

    def _load_and_invert_media_json(self):
        """Загружает media.json из .apkg"""
        # E.g.:
        # '976': 'google-196e02eb-f8b5b393-b5ed84e8-a4527351-6d242448-ae88577ae168efb3a60bf52a7f1e248f61b8fa14.mp3'
        # '119': 'google-3d24cbb4-03c63587-390c70a1-80ed0e36-ca78ea65.mp3'
        # '196': 'google-2aec7ba9-943e6ed3-35a29370-f955aa09-8c2b7eba-17c9fa3817a2c9d35f75cbb69365ce3f56553ed5.mp3'
        with open(fr'{extract_dir}\media', 'r', encoding='utf-8') as f:
            original_json = json.load(f)
            # Меняем местами ключи и значения, чтобы по хранимому в поле карточки имени файла (ключ) удобно
            # было находить реальное имя файла (в виде числа без расширения) в распакованной apkg-папке
            inverted_json = {v: k for k, v in original_json.items()}
            return inverted_json

    def _read_notes_from_unzipped_apkg_db(self):
        # Подключение к базе данных
        conn = sqlite3.connect(anki_db_path)
        cursor = conn.cursor()

        # Получение всех КАРТОЧЕК (cards)
        # cursor.execute("SELECT * FROM cards")
        # cards = cursor.fetchall()

        # Получение всех ЗАМЕТОК (notes)
        cursor.execute("SELECT flds FROM notes")
        notes = cursor.fetchall()

        # Закрытие соединения
        conn.close()

        return notes

    #  Убедиться, что все Front-поля локальной (моя) и удалённой (Natali) карточек совпадают. Если есть несовпадающие
    #  Front-поля, эту ситуацию нужно разрешать вручную, пока не наступит ситуация, когда несовпадающих Front-полей
    #  не останется.
    def validate_1_front_fields_coincidence(self):
        is_valid = True
        for apkg_note in self.apkg_notes:
            # apkg_note - это кортеж, который содержит единственный элемент - строку, которая содержит текст полей
            # карточки, разделённых символом \x1f
            apkg_note_fields = apkg_note[0].split('\x1f')
            # Среди примерно десятка полей карточки поле 'Front' идёт самым первым!
            apkg_front = apkg_note_fields[0]
            if apkg_front not in self.natali_notes_dict.keys():
                print(f"Not found in Natali cards: '{apkg_front}'")
                if is_valid:
                    is_valid = False

        return is_valid

    # Проверяет, совпадает ли содержимое текстовых полей локальной (.apkg) и удалённой (Natali) карточек.
    # При несовпадении производится перезапись Natali-карточек содержимым локальных .apkg-карточек.
    def validate_2(self, mode=Mode.SEARCH_ONLY):
        # Если 1-й валидационный метод не отрабатывает положительно, то не продолжаем дальше
        if not self.validate_1_front_fields_coincidence():
            print('validate_1_front_fields_coincidence() failed!')
            return False

        # При совпадении Front-полей сравнивать между собой и остальные поля:
        # - если не совпадают поля комментариев (Front_comment или Back_comment) просто их тихо перезаписывать
        # - если не совпадают поля Transcription - тоже тихо перезаписывать
        # - если не совпадают поля Back - перезаписывать и менять статус карточки на New!!!
        # Обработка данных
        for apkg_note in self.apkg_notes:
            # note - это кортеж, который содержит единственный элемент - строку, которая содержит текст полей карточки,
            # разделённых символом \x1f
            front, front_comment, taggy, image, ssml, audio1, audio2, transcription, grammar, back, back_comment = \
                apkg_note[0].split('\x1f')

            natali_note = self.natali_notes_dict.get(front)

            # Данная обёртка позволяет сократить и упростить запись в бизнес-коде:
            # было: natali_note['fields']['Front_comment']['value']
            # стало: natali_note_wrapper['Front_comment']
            # теперь в коде фигурирует только бизнес-ключ словаря, а "технические" поля словаря инкапсулированы
            natali_note_wrapper = {key: value['value'] for key, value in natali_note['fields'].items()}
            natali_note_id = natali_note['noteId']

            # В каждой итерации цикла сбрасываем состояние следующих переменных
            self.note_updated_fields_dict = {}  # хранит данные для пересылки через AnkiConnect
            self.print_log_dict = {}  # хранит данные для печати на экран
            self.should_reset_note_cards_to_new = False

            if natali_note_id not in []:  # TODO добавлять в список id тех карточек, которые нужно проигнорировать
                self._compare_fields(front_comment, natali_note_wrapper['Front_comment'], 'Front_comment')

            self._compare_fields(taggy, natali_note_wrapper['Taggy'], 'Taggy')
            self._compare_fields(image, natali_note_wrapper['Image'], 'Image')
            self._compare_fields(ssml, natali_note_wrapper['SSML'], 'SSML')
            self._compare_fields(audio1, natali_note_wrapper['Audio1'], 'Audio1')
            self._compare_fields(audio2, natali_note_wrapper['Audio2'], 'Audio2')
            self._compare_fields(transcription, natali_note_wrapper['Transcription'], 'Transcription')
            self._compare_fields(grammar, natali_note_wrapper['Grammar'], 'Grammar')
            self._compare_fields(back, natali_note_wrapper['Back'], 'Back')

            # Два правила обработки 'Back_comment'-поля:
            # 1) если 'Back_comment'-поле Natali-карточки содержит слово "тире" - очищаем его
            if 'тире' in natali_note_wrapper['Back_comment'].lower():
                self.note_updated_fields_dict['Back_comment'] = ''  # очищаем содержимое 'Back_comment'-поля
                self.is_at_least_one_mismatch = True
            # 2) если 'Back_comment'-поле .apkg-карточки не содержит слова "тире", синхронизируем содержимое данного
            # поля в обоих карточках
            if 'тире' not in back_comment:
                self._compare_fields(back_comment, natali_note_wrapper['Back_comment'], 'Back_comment')

            # Вывод информации о несовпадениях
            if self.print_log_dict:
                output = f"note_id = {natali_note_id}; Front = '{front}'\n"
                for field_name, (apkg_note_field, anki_note_field) in self.print_log_dict.items():
                    output += f"\t'{field_name.upper()}':\n\t\tapkg: '{apkg_note_field}' != Anki: '{anki_note_field}'\n"
                print(output)

            # Обновляем карточку в Natali account, если:
            # 1) было замечено несовпадение содержимого хотя бы в одном поле (словарь note_updated_fields_dict не пуст)
            # 2) это действие разрешено параметром mode
            if self.note_updated_fields_dict and mode == Mode.FIND_AND_REPLACE:
                self._update_natali_note(natali_note)

        # end of loop
        return

    def _compare_fields(self, apkg_note_field, anki_note_field, field_name):
        if apkg_note_field != anki_note_field:
            self.note_updated_fields_dict[field_name] = apkg_note_field
            self.print_log_dict[field_name] = (apkg_note_field, anki_note_field)
            # self.is_at_least_one_mismatch = True

        # Если не совпадает содержимое Back-полей, то дополнительно включаем флаг, сигнализирующий о
        # необходимости сбросить карточки текущей note в статус New
        if field_name == 'Back':
            self.should_reset_note_cards_to_new = True

    def _update_natali_note(self, natali_note):
        # 1. Обновляем поля карточки
        self.ankiConnectService.update_single_note_in_anki(natali_note, self.note_updated_fields_dict)

        # 2. Если изменения касались мультимедийных полей (Image, Audio1, Audio2), то в дополнение к обновлению
        # текстового содержимого полей, необходимо подложить в папку %APPDATA%\Anki2\account_name\collection.media
        # и сами мультимедиа-файлы.
        for media_field_name in ['Image', 'Audio1', 'Audio2']:
            filenames = []
            if media_field_name in self.note_updated_fields_dict:
                media_field_text_content = self.note_updated_fields_dict[media_field_name]
                if media_field_name == 'Image':
                    # Текстовое содержимое Image-поля это html-разметка: <img src="Саар.png"><br><img src="cat_new.jpg">
                    soup = beautiful_soup_helper.getBs(media_field_text_content)
                    filenames = [img_tag['src'] for img_tag in soup.find_all('img')]  # ['Саар.png', 'cat_new.jpg']
                elif media_field_name in ['Audio1', 'Audio2']:
                    # Текстовое содержимое аудио-поля может иметь следующий вид и из него нужно достать имена файлов:
                    # GT: [sound:google-95ae4a99-xyz.mp3]
                    # MA: [sound:azure-c59d83ab5-xyz.mp3]
                    # re.findall() по умолчанию возвращает только содержимое групп захвата, если они есть.
                    # В данном случае re.findall() вернёт ['google-95ae4a99-xyz.mp3', 'azure-c59d83ab5-xyz.mp3']
                    filenames = re.findall(r"\[sound:(.*?)\]", media_field_text_content)

                for media_file_in_anki_relative_name in filenames:
                    self._proceed_with_media_file_name(media_file_in_anki_relative_name)

        # 3. Сбрасываем статус карточки в New, если у неё отличается Back-поле
        if self.should_reset_note_cards_to_new:
            self.ankiConnectService.reset_note_cards_to_new(natali_note)

    # Чтобы отправить файл по сети в папку %APPDATA%\Anki2\account_name\collection.media нужно 2 вещи:
    # 1) указать этому файлу имя, под которым он окажется в Анки-папке
    # 2) знать имя этого файла в текущей системе, чтобы обратиться к нему, закодировать и переслать
    def _proceed_with_media_file_name(self, media_file_in_anki_relative_name):
        media_file_in_apkg_extract_dir_relative_name = self.inverted_media_json.get(
            media_file_in_anki_relative_name)  # имя файла это просто число 0, 1, 2, etc.
        if media_file_in_apkg_extract_dir_relative_name:
            media_file_in_apkg_extract_dir_fullpath_name = fr'{extract_dir}\{media_file_in_apkg_extract_dir_relative_name}'
            self.ankiConnectService.upload_media_file_to_anki(media_file_in_anki_relative_name,
                                                              media_file_in_apkg_extract_dir_fullpath_name)


################################################################

if __name__ == '__main__':
    ankiLocalApkgWithNataliAccountSynchronizer = AnkiLocalApkgWithNataliAccountSynchronizer()

    # val_1_res = ankiLocalApkgWithNataliAccountSynchronizer.validate_1_front_fields_coincidence()
    # [print('val1 - ok') if val_1_res else print('val1 - failed')]

    # Перед вызовом метода заскриншотить результат поиска: "Back_comment:re:[Тт]ире". Впрочем, данное слово встречается
    # в 'Back_comment'-поле предложений, а не отдельных слов.
    ankiLocalApkgWithNataliAccountSynchronizer.validate_2()
    # ankiLocalApkgWithNataliAccountSynchronizer.validate_2(mode=Mode.FIND_AND_REPLACE)
