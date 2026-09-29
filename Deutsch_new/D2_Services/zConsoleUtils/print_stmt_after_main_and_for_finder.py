import os

from FilenameUtils import FilenameUtils

# Вывести список файлов, у которых имеется строка, содержащая "print(" и стоящая:
# 1) ниже строки 'if __name__ == '__main__':'
# 2) ниже строки, содержащей подстроку 'for '
# Данный поиск нужен для того, чтобы представить print-код в следующем однострочном виде: [print(i) for i in diff],
# а не в виде обычного многострочного громоздкого цикла.

input_text = """
def get_all_portrait_filenames():
    portrait_predicate = lambda filename: filename.endswith('(portrait).odt')
    portrait_filenames = _get_filenames_by_predicate(folder_path, portrait_predicate)
    return portrait_filenames


###############################

if __name__ == '__main__':
    filenames = get_all_vocab_filenames()
    # filenames = get_all_portrait_filenames()
    for fn in filenames:
        print(fn)
    # [print(fn) for fn in filenames]
"""


def find_matching_files(directory):
    matching_files = []

    absolute_filenames = FilenameUtils.get_filenames_recursively(directory,
                                                                 predicate=lambda filename: filename.endswith('.py'))

    for absolute_filename in absolute_filenames:
        with open(absolute_filename, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if find_target_line(lines):
            matching_files.append(absolute_filename.split("\\")[-1])

    return matching_files


def find_target_line(lines):
    is_found = False
    for i, line in enumerate(lines):
        if "if __name__ == '__main__':" in line:
            for j in range(i + 1, len(lines)):
                if 'for ' in lines[j]:
                    for k in range(j + 1, len(lines)):
                        if 'print(' in lines[k]:
                            line = lines[k].strip()
                            is_line_square_bracketed = line.startswith('[') and line.endswith(']')
                            if not is_line_square_bracketed:
                                is_found = True
                                # добавили +1, потому что в редакторе коде отсчёт строк начинается с 1 (а в списке строк
                                # lines счёт начинается с 0)
                                # print(k + 1)
                                break

    return is_found


#################################################################

# Укажите путь к директории с Python-файлами
directory_path = r"E:\Languages\English\SVN repo\Python software\MultilingualTextProcessor\Deutsch_new"
result = find_matching_files(directory_path)

# Вывод результата
[print(file) for file in result]
