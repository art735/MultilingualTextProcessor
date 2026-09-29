import os

import FileContentsReader

# Данный утилитный системный скрипт выводит список .py-файлов, в которых ещё нет следующей строки:
# if __name__ == '__main__':
# Эту строку часто называют "защита от выполнения при импорте" (guarding against execution on import) в Python.
# Она используется, чтобы определить, выполняется ли скрипт напрямую, как основная программа, или импортируется в
# другой модуль.
# Идея состоит в том, чтобы такая строка была в каждом файле и данный скрипт помогает найти файлы, в которых
# эта строка по ошибке отсутствует.

folder_path = r'E:\Languages\English\SVN repo\Python software\MultilingualTextProcessor\Deutsch_new'


def get_file_paths():
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        if 'test' not in root and 'Entities' not in root:  # папка c юнит-тестами в поиске не участвует
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    file_paths.append(file_path)
    return file_paths


for file_path in get_file_paths():
    file_content = FileContentsReader.get_file_text(file_path)
    if "if __name__ == '__main__':" not in file_content:
        print(file_path.split('\\')[-1])
