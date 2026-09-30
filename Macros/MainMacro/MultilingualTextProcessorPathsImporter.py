# -*- coding: utf-8 -*-
import os
import sys

base_path = r'E:\Languages\[Git repo] MultilingualTextProcessor'


def import_paths():
    subfolders = _get_subfolders(base_path)
    for subfolder in subfolders:
        if all(path_piece not in subfolder for path_piece in [r'\.idea', r'\resources', r'\test']):
            if subfolder not in sys.path:
                sys.path.append(subfolder)
            # print(subfolder)


# Получить список всех подпапок в указанной директории
# Пути к ПАПКАМ, содержащим импортируемые модули, но не fullpath самих модулей!
def _get_subfolders(directory):
    subfolders = []
    for root, dirs, _ in os.walk(directory):
        for dir_name in dirs:
            subfolder_name = os.path.join(root, dir_name)
            if not subfolder_name.endswith("__pycache__"):  # папки __pycache__ игнорируется
                subfolders.append(subfolder_name)
    return subfolders

##############

# import_paths()





# for folder in get_subfolders(fr"{base_path}\zCommonLibrary"):
#     sys.path.append(folder)
#
# # Данный класс не используется здесь, но импортируется в TranscriptionAspirationService, а потому тоже должен быть
# # включён в class_path. Т. е. в class_path включаются как сами сторонние модули, которые здесь используются, так и их
# # зависимости!
# # После внесения изменений в код сторонних модулей, например TranscriptionAspirationService, Open-/LibreOffice документ
# # нужно закрыть и заново открывать, чтобы внесённые изменения стали доступны в макросе! Если же .odt-файл не закрывать,
# # новые изменения доступны не будут, и макрос будет использовать старый закешированный вариант кода сторонних модулей!
# german_transcription_glottal_stop_appender_class_path = fr"{base_path}\Deutsch_Popov\D2_Services\Transcribers"
# sys.path.append(german_transcription_glottal_stop_appender_class_path)