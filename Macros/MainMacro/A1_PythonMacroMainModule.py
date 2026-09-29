# -*- coding: utf-8 -*-
import inspect
import os
import sys

# Universal Network Objects (UNO) is the component model used in the OpenOffice.org and LibreOffice.
# It is interface-based and designed to offer interoperability between different programming languages, object models
# and machine architectures, on a single machine, within a LAN or over the Internet.
import uno

# 1.1 Получаем путь к папке, в которой находится данный макрос
script_path = inspect.getfile(inspect.currentframe())
script_dir = os.path.dirname(os.path.abspath(script_path))

# 1.2 Добавляем текущую папку скрипта в classpath, чтобы из этой папки (или относительно этой папки) потом можно было бы
# подтянуть и другие модули.
if script_dir not in sys.path:
    sys.path.append(script_dir)

# Сам факт импорта данного модуля достаточен для добавления в classpath всех папок проекта MultilingualTextProcessor,
# т. к. модуль уже содержит вызов соответствующего метода (см. код модуля)

# ИМПОРТ ВСЕХ ПУТЕЙ, ГДЕ МОГУТ РАСПОЛАГАТЬСЯ МОДУЛИ ДАННОГО МАКРОСА ИЛИ МОДУЛИ БИЗНЕС-ЛОГИКИ
import MultilingualTextProcessorPathsImporter
MultilingualTextProcessorPathsImporter.import_paths()

######################################################

# USER IMPORTS
# Теперь можно импортировать другие модули макроса, используя привычный синтаксис
import S1_SelectedTextToTableConverter
# import S2_StarBasicMacroInvoker
# import S3_TextReplacer
import PyVerUtils
import UnoUtils


def run(doc):
    # Объект doc должен создаваться каждый раз при вызове метода-обработчика для каждого открытого документа.
    # Если макрос запускается через встроенный механизм UNO (например, привязан к кнопке, меню и т. п.), то лучшим
    # решением для получения текущего документа будет следующее:
    # doc = XSCRIPTCONTEXT.getDocument()

    # 1. Конвертируем выделенный текст в таблицу
    S1_SelectedTextToTableConverter.convert_text_to_table(doc)

    # 2. Вызвать StarBasic-макрос, который содержит много полезных правил форматирования и замены текста.
    # Перед вызовом StarBasic-макроса, закомментировать в нём вызов данного Python-макроса, чтобы не было
    # бесконечного цикла и краша системы.
    # S2_StarBasicMacroInvoker.invoke()

    # 3. Произвести дополнительное (или дублирующее) форматирование текста средствами Python
    # S3_TextReplacer.run(doc)

    # 4. Обработать транскрипции из среднего столбца 3-х или 5-ти столбцовой таблицы
    if PyVerUtils.is_python3() or PyVerUtils.is_python2():
        import S4_TranscriptionProcessor
        S4_TranscriptionProcessor.process_transcription(doc)

    # 5. Подчеркнуть правила греческого произношения
    # if PyVerUtils.is_python3():
    #     import S5_GreekPronunciationProcessor
    #     S5_GreekPronunciationProcessor.process(doc)

    # res = http_client.send_http_post()

    UnoUtils.show_messagebox('Info', 'Python macro has worked!')
    # UnoUtils.show_messagebox('Info', res)

    # msgbox("Python macro has worked!")
