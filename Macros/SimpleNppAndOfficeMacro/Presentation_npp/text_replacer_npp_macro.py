# -*- coding: utf-8 -*-

# Определяем путь к папке, в которой лежит данный макрос
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
# print('current_dir = ' + current_dir)

# Считываем путь к папке с бизнес-логикой из конфигурационного файла
import config_reader
path_to_business_logic = config_reader.get_config_path(current_dir)
# print('path_to_business_logic = ' + path_to_business_logic)

# Добавляем путь к папке с бизнес-логикой в список системных путей
import sys
sys.path.append(path_to_business_logic)

# User modules import section
import text_replacer_service

# Получаем весь текст из текущей вкладки
text = editor.getText()

# Производим замены в тексте
text = text_replacer_service.make_replacements(text)

# Устанавливаем обновлённый текст в редактор
editor.setText(text)
