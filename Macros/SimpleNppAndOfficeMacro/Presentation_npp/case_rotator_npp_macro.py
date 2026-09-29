# -*- coding: utf-8 -*-

# Определяем путь к папке, в которой лежит данный макрос
import os
current_dir = os.path.dirname(os.path.abspath(__file__))

# Считываем путь к папке с бизнес-логикой из конфигурационного файла
import config_reader
path_to_business_logic = config_reader.get_config_path(current_dir)

# Добавляем путь к папке с бизнес-логикой в список системных путей
import sys
sys.path.append(path_to_business_logic)

# User modules import section
import case_rotator_service

# Получить начальную и конечную позиции выделения
start_pos = editor.getSelectionStart()
end_pos = editor.getSelectionEnd()

# Получить выделенный текст
selected_text = editor.getSelText()

if selected_text:
    # Получаем преобразованный текст
    sentences_str = case_rotator_service.rotate_case(selected_text)

    # Заменяем выделенный текст
    editor.replaceSel(sentences_str)

    # Вычисляем новую конечную позицию (если текст изменился по длине)
    # new_end_pos = start_pos + len(sentences_str)

    # Восстанавливаем выделение
    editor.setSelectionStart(start_pos)
    editor.setSelectionEnd(end_pos)

