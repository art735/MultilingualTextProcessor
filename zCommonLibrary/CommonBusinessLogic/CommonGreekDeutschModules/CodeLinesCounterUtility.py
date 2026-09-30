import os

from FilenameUtils import FilenameUtils


# Метод написан Codeium-плагином
def count_code_lines(directory):
    total_lines = 0

    absolute_filenames = FilenameUtils.get_filenames_recursively(directory,
                                                                 predicate=lambda filename: filename.endswith('.py'))

    for absolute_filename in absolute_filenames:
        # print(absolute_filename)
        with open(absolute_filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                # Строка, содержащая комментарий, не обязательно начинается со знака '#', а может начинаться с
                # пробела и табуляции, за которыми уже идёт знак '#'. Поэтому лучше использовать не такой
                # вариант:
                # not line.startswith('#')
                # а следующий вариант:
                # '#' not in line
                if line and '#' not in line:
                    total_lines += 1

    return total_lines


directory = r'E:\Languages\[Git repo] MultilingualTextProcessor\Deutsch_new'
no_of_lines = count_code_lines(directory)
print(no_of_lines)
