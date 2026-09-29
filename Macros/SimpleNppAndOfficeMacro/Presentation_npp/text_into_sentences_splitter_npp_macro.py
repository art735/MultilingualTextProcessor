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
import text_into_sentences_splitter_service

# Получить выделенный текст
selected_text = editor.getSelText()

if selected_text:
    sentences_str = text_into_sentences_splitter_service.split_into_sentences(selected_text)

    # Заменяем выделенный текст на новый
    editor.replaceSel(sentences_str)
