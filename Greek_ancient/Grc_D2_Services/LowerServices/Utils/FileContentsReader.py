base_dir = r'/resources/Greek\\'


def get_file_text(full_path_filename):
    # здесь лучше использовать именно None, а не пустую строку, т. к. пустую строку лучше интерпретировать как то,
    # что файл есть и он успешно был найден и открыт, но его содержимое - пустое.
    text = None
    file = _try_to_open_file_and_get_file_object(full_path_filename)
    if file:
        try:
            text = file.read()
        finally:
            file.close()
    return text

    # text = ''
    # # file_path = base_dir + filename
    # try:
    #     with open(full_path_filename, 'r', encoding='utf-8') as file:
    #         text = file.read()
    #     # print("Содержимое файла:")
    #     # print(text)
    # except FileNotFoundError:
    #     print(f"Файл {full_path_filename} не найден.")
    # except Exception as e:
    #     print(f"Произошла ошибка: {e}")
    # return text


def get_file_text_as_lines(full_path_filename):
    lines = []

    file = _try_to_open_file_and_get_file_object(full_path_filename)
    if file:
        try:
            lines = [line.strip() for line in file.readlines()]
        finally:
            file.close()
    return lines

    # lines = []
    # # file_path = base_dir + filename
    # try:
    #     with open(full_path_filename, 'r', encoding='utf-8') as file:
    #         lines = [line.strip() for line in file.readlines()]
    # except FileNotFoundError:
    #     print(f"Файл {full_path_filename} не найден.")
    # except Exception as e:
    #     print(f"Произошла ошибка: {e}")
    # return lines


def read_dict_from_file(full_path_filename):
    my_dict = {}

    file = _try_to_open_file_and_get_file_object(full_path_filename)
    if file:
        try:
            for line in file:
                key, value = line.strip().split(':', 1)

                key = key.strip()
                value = value.strip()

                if value.isdigit():
                    my_dict[key] = int(value)
                else:
                    my_dict[key] = value
        finally:
            file.close()
    return my_dict


def _try_to_open_file_and_get_file_object(full_path_filename):
    try:
        file = open(full_path_filename, 'r', encoding='utf-8')
        return file
    except FileNotFoundError:
        print(f"Файл {full_path_filename} не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    return None

###########################

# filename_5all_gospels = '5all_four_Gospels_freq_dict.txt'
# freq_dict = read_freq_dict_from_file(filename_5all_gospels)
# print(freq_dict)
# print(len(freq_dict))
