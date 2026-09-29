# -*- coding: utf-8 -*-

import os

# Из-за того, что в npp и LibreOffice current_dir самого макроса (а значит и лежащего рядом данного файла) определяется
# по-разному, передаём current_dir как параметр функции, а не выводим его здесь самостоятельно.
# LibreOffice использует UNO и это налагает ограничение на использование os.path.dirname(os.path.abspath(__file__))
def get_config_path(macro_script_dir):
    # Формируем полный путь к config.txt
    config_filename = os.path.join(macro_script_dir, 'config.txt')

    path_to_business_logic = ''
    with open(config_filename, 'r') as f:
        for line in f:
            if line.startswith('path_to_business_logic='):
                path_to_business_logic = line.split('=', 1)[1].strip()
                # sys.path.append(path_to_business_logic)
                # print("Путь добавлен в sys.path:", path_to_business_logic)
                # break

    return path_to_business_logic


#############################################

if __name__ == '__main__':
    res = get_config_path()
    print(res)
