import os
import sys

# Данный скрипт добавляет в classpath пути к бизнес-сервисам, у которых веб-сервер вызывает методы.
# Скрипт вызывается из задачи 'Office macro http server' программы Task Scheduler следующей командой:
# python "E:\Languages\[Git repo] MultilingualTextProcessor\Macros\MainMacro\http_client_server\http_server\start_server.py"
# Задача 'Office macro http server', в свою очередь, запускается при старте системы (подробности настройки смотреть
# в документе текущей папки).

# Позволяет подняться на 'levels_up' уровней вверх относительно 'start_path'
def get_ancestor_dir(start_path, levels_up):
    path = start_path
    for _ in range(levels_up):
        # os.path.dirname(path) возвращает путь к директории, в которой находится файл или папка, указанная в path:
        # - если path – это путь к файлу, dirname возвращает путь к папке, где этот файл лежит.
        # - если path – это путь к папке, dirname возвращает путь к РОДИТЕЛЬСКОЙ папке этой папки.
        path = os.path.dirname(path)
    # os.path.abspath(path) преобразует любой путь — относительный или уже абсолютный — в абсолютный путь.
    # Это удобно, чтобы быть уверенным, что в итоге у тебя всегда полный путь, без двусмысленностей.
    return os.path.abspath(path)


#########################################################

# 1. Получаем путь к папке, в которой лежит MultilingualTextProcessorPathsImporter, чтобы можно было его заимпортировать
# и вызвать логику его работы (заключающуюся в импорте всех путей из MultilingualTextProcessor).
# __file__ — путь к текущему скрипту
import_path = get_ancestor_dir(__file__, 3)  # три уровня вверх
if import_path not in sys.path:
    # sys.path.insert(0, import_path)
    sys.path.append(import_path)

# 2. Импортируем и вызываем модуль, который, в свою очередь, заимпортирует все пути из MultilingualTextProcessor
import MultilingualTextProcessorPathsImporter
MultilingualTextProcessorPathsImporter.import_paths()

# 3. Импортируем и запускаем http-server
from office_macro_http_server import OfficeMacroHTTPServer
server = OfficeMacroHTTPServer()
server.run()
