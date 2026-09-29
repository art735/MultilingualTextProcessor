# -*- coding: utf-8 -*-
# Делает поведение print таким же, как в Python 3 — то есть превращает print из инструкции в функцию.
# TODO: может импортировать так, чтобы и строки были Юникодные???
# from __future__ import print_function

from __future__ import (
    print_function,
    unicode_literals)

# import MultilingualTextProcessorPathsImporter


import sys

import PyVerUtils


def log_debug(text):
    with open(r"f:/temp/oo_debug.txt", "w") as f:
        f.write(text + "\n")

# Пример:
log_debug("Start")
try:
    import P2P3_Adapter
    log_debug("P2P3_Adapter loaded successfully.")
except ImportError as e:
    log_debug("ImportError: " + str(e))
except Exception as e:
    log_debug("General error: " + str(e))


###########################

# Глобальный флаг
DEBUG = False

# Функция-обёртка над методом print, который нормально поддерживается в UNO-среде LibreOffice (Python3) и
# НЕ поддерживается UNO-среде OpenOffice (Python2).
# Флагом DEBUG можно включать/отключать печать сообщений.
# Импорт from __future__ import (print_function, unicode_literals) всё равно НЕ устраняет те проблемы, которые решает
# данный метод.
def debug_print(*args):
    try:
        if PyVerUtils.is_python2():
            line = u" ".join(unicode(arg) for arg in args)
            sys.stdout.write(line.encode('utf-8') + b'\n')
        else:
            print(" ".join(str(arg) for arg in args))
    except Exception:
        pass

########################################


from P2P3_Adapter import P2P3_Adapter

p2p3_Adapter = P2P3_Adapter()



# TODO: в будущем определять язык динамически:
#  с помощью библиотек:
#  - langdetect
#  - langid
#  - textblob (если установлен nltk)
#  или вручную по ключевым словам (например, top10 или top100 из частотных списков)
lang = 'deu'

# Функция-обёртка на случай, если таблиц (или других итерируемых объектов) в документе нет и нужно безопасно
# вести себя в этом случае.
# def safe_element_names(names):
#     if isinstance(names, basestring):
#         return [names] if names.strip() else []
#     return list(names)


def process_transcription(doc):
    if not doc or not doc.supportsService("com.sun.star.text.TextDocument"):
        debug_print("No valid document is open.")
        return

    tables = doc.getTextTables()
    if not tables.hasElements():
        return  # Нет таблиц

    # Сквозной список всех объектов Paragraph из всех транскрипционных ячеек всех таблиц документа
    paragraphs_with_text_portions = get_paragraphs_with_text_portions(tables)

    # Данные для передачи в Python3-бизнес-логику (через http-сервер / subprocess или напрямую).
    data = []

    # 1. Сбор данных для передачи их в Python3-бизнес-логику
    for paragraph, text_portions in paragraphs_with_text_portions:
        par_text = paragraph.String
        par_text_portions = []

        for text_portion in text_portions:
            par_text_portions.append(text_portion.String)

        # paragraph_struct = {
        #     "par_text": par_text,
        #     "par_text_portions": par_text_portions
        # }

        # data.append(paragraph_struct)
        data.append((par_text, par_text_portions))

    # 2. Передача данных в Python3-бизнес-логику
    # TODO:
    processed_data = p2p3_Adapter.process_transcriptions(data, lang)

    # Если данные от сервера не пришли (например, из-за того, что он не запущен), завершаем работу метода
    if not processed_data:
        return

    # 3. Обновление текста в траскрипционных ячейках (в элементах Paragraph и TextPortion)
    for (paragraph, text_portions), (processed_paragraph, processed_text_portions) in zip(paragraphs_with_text_portions, processed_data):
        for text_portion, processed_text_portion in zip(text_portions, processed_text_portions):
            original_text_portion_text = text_portion.String
            modified_text_portion_text = processed_text_portion
            if modified_text_portion_text != original_text_portion_text:
                replace_in_text_portion(text_portion, modified_text_portion_text)

            # Step 2. Берём текст Paragraph целиком и обрабатываем его. При этом теоретически возможна потеря форматирования
            # внутри какого-либо TextPortion, но на практике такая ситуация маловероятна.
            # Если работа с текстом происходит в рамках обычного workflow (т. е. когда программка сгенерировала
            # pipe-separated-данные, которые затем преобразуются в odt-таблицу), то транскрипции обрабатываются как раз
            # на этапе конвертации данных в таблицу, и последующее ручное форматирование транскрипций не будет потеряно,
            # если не менялся сам текст транскрипции и не менялись правила её обработки.
            original_paragraph_text = paragraph.String
            modified_paragraph_text = processed_paragraph
            if modified_paragraph_text != original_paragraph_text:
                paragraph.String = modified_paragraph_text


def get_paragraphs_with_text_portions(tables):
    # Если собрать объекты ячеек (TextTableCell) в список (или любую другую коллекцию), то при последующем обходе
    # этого списка и модификации текста в этих ячейках изменения будут применяться прямо в исходной таблице документа.
    # То есть объекты ячеек — это ссылки на реальные ячейки в документе, и изменения, сделанные через эти объекты,
    # сразу отражаются в документе.
    paragraphs_with_text_portions = []
    for table_name in tables.getElementNames():
        table = tables.getByName(table_name)

        for row_idx in range(table.Rows.Count):
            cells = table.getCellRangeByPosition(0, row_idx, table.Columns.Count - 1, row_idx)
            cell_count = table.Columns.Count

            if cell_count == 3:  # если работаем с portrait-файлом
                transcription_cell = cells.getCellByPosition(1, 0)
            elif cell_count == 5:  # если работаем с Vocab-файлом
                transcription_cell = cells.getCellByPosition(2, 0)
            else:
                continue

            # Вычитываем из ячейки все её объекты Paragraph.
            # У объекта Paragraph можно напрямую изменять его содержимое, не обращаясь при этом к ячейке, в которой он
            # находится. Paragraph — это живой UNO-объект, уже "вшитый" в структуру документа. Изменения производятся
            # в месте его размещения, независимо от того, имеется ли информация о том, в какой ячейке он находится.
            # Ты не обязан обращаться к контейнеру, чтобы модифицировать Paragraph, если ты уже его получил.
            # Но если ты не знаешь, откуда Paragraph взялся, и тебе нужна эта информация — тогда нужно явно отслеживать
            # его «родителя» в момент обхода, так как параграф (com.sun.star.text.Paragraph) в OpenOffice /
            # LibreOffice UNO API сам по себе не содержит прямой ссылки на ячейку (com.sun.star.table.Cell),
            # в которой он находится.
            transcription_cell_enum = transcription_cell.Text.createEnumeration()
            while transcription_cell_enum.hasMoreElements():
                element = transcription_cell_enum.nextElement()
                if element.supportsService("com.sun.star.text.Paragraph"):
                    paragraph = element
                    text_portions = get_text_portions_by_paragraph(paragraph)
                    # Добавляем Paragraph и ассоциированные с ним объекты TextPortion в виде кортежа для удобства
                    # итерации по этим парам в будущем. Не используем словарь, т. к. во-первых, в Python2 нужно
                    # использовать OrderedDict для сохранения порядка вставки, а во-вторых, не понятно как быть с хешами
                    # ключей.
                    paragraphs_with_text_portions.append((paragraph, text_portions))

    return paragraphs_with_text_portions

def get_text_portions_by_paragraph(paragraph):
    text_portions = []
    paragraph_enum = paragraph.createEnumeration()
    while paragraph_enum.hasMoreElements():
        text_portion = paragraph_enum.nextElement()
        if text_portion.supportsService("com.sun.star.text.TextPortion"):
            text_portions.append(text_portion)
    return text_portions

# def update_paragraph(paragraph, processed_paragraph_struct):
#     processed_par_text = processed_paragraph_struct["par_text"]
#     processed_par_text_portions = processed_paragraph_struct["par_text_portions"]
#
#     k = 0
#     paragraph_enum = paragraph.createEnumeration()
#     while paragraph_enum.hasMoreElements():
#         element = paragraph_enum.nextElement()
#         if element.supportsService("com.sun.star.text.TextPortion"):
#             text_portion = element
#             original_text_portion_text = text_portion.String
#             modified_text_portion_text = processed_par_text_portions[k]
#             k += 1
#             if modified_text_portion_text != original_text_portion_text:
#                 replace_in_text_portion(text_portion, modified_text_portion_text)
#
#     # Step 2. Берём текст Paragraph целиком и обрабатываем его. При этом теоретически возможна потеря форматирования
#     # внутри какого-либо TextPortion, но на практике такая ситуация маловероятна.
#     # Если работа с текстом происходит в рамках обычного workflow (т. е. когда программка сгенерировала
#     # pipe-separated-данные, которые затем преобразуются в odt-таблицу), то транскрипции обрабатываются как раз
#     # на этапе конвертации данных в таблицу, и последующее ручное форматирование транскрипций не будет потеряно,
#     # если не менялся сам текст транскрипции и не менялись правила её обработки.
#     original_paragraph_text = paragraph.String
#     modified_paragraph_text = processed_par_text
#     if modified_paragraph_text != original_paragraph_text:
#         paragraph.String = modified_paragraph_text

##################################################################################
##################################################################################
##################################################################################


def process_transcription_cell(transcription_cell):
    transcription_cell_enum = transcription_cell.Text.createEnumeration()
    while transcription_cell_enum.hasMoreElements():
        element = transcription_cell_enum.nextElement()
        # Типичная ситуация в ячейке transcription: содержимое ячейки состоит из paragraphs в обычном смысле этого
        # термина (фрагменты текста отделённые друг от друга переносом строки), а каждый paragraph содержит
        # один или несколько блоков данных типа TextPortion:
        # - если абзац имеет форматирование, блоков TextPortion будет столько, сколько различных форматирований
        # применено к разным участкам текста абзаца (выделение текста цветом, курсивом и т. п.);
        # - если абзац не имеет форматирования, то один блок TextPortion всё равно будет, и он будет содержать
        # весь текст абзаца целиком.
        if element.supportsService("com.sun.star.text.Paragraph"):
            process_paragraph(element)
        # else:
        #     # На практике не встречал, чтобы в ячейке лежал текст "напрямую", т. е. не обёрнутый в TextPortion,
        #     # который, в свою очередь, был бы обёрнут в Paragraph.
        #     original_element_text = element.String
        #     modified_element_text = (t0_TranscriptionAggregatedProcessor.
        #                              find_in_text_bracketed_transcriptions_and_process_them(original_element_text,
        #                                                                                     lang))
        #     if modified_element_text != original_element_text:
        #         element.String = modified_element_text
        #         # element.setString(process_text(element.getString()))

def process_paragraph(paragraph):
    # Step 1. Рассматриваем текст элемента Paragraph как набор входящих в его состав текстов элементов TextPortion.
    # При этом с точки зрения обработки транскрипции здесь возможны два случая:
    # 1) если транскрипция целиком находится в TextPortion (т. е. транскрипция целиком выделена маркером, например),
    # то мы её обрабатываем и при этом не теряем форматирование данного TextPortion;
    # 2) если TextPortion целиком транскрипции не содержит, данный этап ничего не даст и обработка транскрипции
    # будет осуществляться на 2-м шаге.
    paragraph_enum = paragraph.createEnumeration()
    # has_text_portions = False
    while paragraph_enum.hasMoreElements():
        element = paragraph_enum.nextElement()
        if element.supportsService("com.sun.star.text.TextPortion"):
            # has_text_portions = True
            process_text_portion(element)

    # Step 2. Берём текст Paragraph целиком и обрабатываем его. При этом теоретически возможна потеря форматирования
    # внутри какого-либо TextPortion, но на практике такая ситуация маловероятна.
    # Если работа с текстом происходит в рамках обычного workflow (т. е. когда программка сгенерировала
    # pipe-separated-данные, которые затем преобразуются в odt-таблицу), то транскрипции обрабатываются как раз
    # на этапе конвертации данных в таблицу, и последующее ручное форматирование транскрипций не будет потеряно,
    # если не менялся сам текст транскрипции и не менялись правила её обработки.
    original_paragraph_text = paragraph.String
    modified_paragraph_text = p2p3_Adapter.find_in_text_bracketed_transcriptions_and_process_them(original_paragraph_text, lang)
    if modified_paragraph_text != original_paragraph_text:
        paragraph.String = modified_paragraph_text

    # Не встречал такой ситуации, но AI считает, что она возможна
    # if paragraph.String.strip() and not has_text_portions:
    #     paragraph.String = process_text(paragraph.String)

def process_text_portion(text_portion):
    if text_portion.TextPortionType not in ["Text", "Sentence"]:
        debug_print("Пропускаем TextPortion с типом " + text_portion.TextPortionType)
        return

    if not hasattr(text_portion, "getStart") or not hasattr(text_portion, "getEnd"):
        debug_print("Ошибка: text_portion " + text_portion.String + " не поддерживает XTextRange!")
        return

    original_text_portion_text = text_portion.String
    modified_text_portion_text = p2p3_Adapter.find_in_text_bracketed_transcriptions_and_process_them(original_text_portion_text, lang)
    if modified_text_portion_text != original_text_portion_text:
        replace_in_text_portion(text_portion, modified_text_portion_text)

    debug_print('old text = ' + original_text_portion_text)
    debug_print('new text = ' + modified_text_portion_text)

def replace_in_text_portion(text_portion, new_text):
    """
    Заменяет текст в TextPortion с сохранением форматирования

    Args:
        text_portion: com.sun.star.text.TextPortion объект
        new_text: str, новый текст для вставки
    """
    try:
        # Сохраняем текущие характеристики форматирования
        char_props = {}

        # Получаем все доступные свойства форматирования
        properties_to_preserve = [
            'CharFontName',
            'CharHeight',
            'CharWeight',
            'CharPosture',
            'CharColor',
            'CharUnderline',
            'CharBackColor',
            'CharKeepTogether',
            'CharScaleWidth'
        ]

        # Безопасное получение свойств
        for prop in properties_to_preserve:
            try:
                if hasattr(text_portion, prop):
                    char_props[prop] = getattr(text_portion, prop)
            except Exception:
                continue

        # Получаем текстовый диапазон
        text_range = text_portion.getText()
        # Создаём курсор в начале TextPortion
        cursor = text_range.createTextCursorByRange(text_portion.getStart())
        # Выделяем весь текст в TextPortion
        portion_length = len(text_portion.getString())
        cursor.goRight(portion_length, True)
        # Заменяем текст
        cursor.setString(new_text)

        # Применяем сохранённое форматирование к новому тексту
        for prop, value in char_props.items():
            try:
                setattr(cursor, prop, value)
            except Exception:
                continue

        return True

    except Exception as e:
        debug_print("Ошибка при замене текста: " + str(e))
        return False

# # Метод принимает на вход текст элементов "com.sun.star.text.Paragraph" или "com.sun.star.text.TextPortion"
# def _process_text(original_transcription_containing_text):
#     modified_transcription_containing_text = original_transcription_containing_text
#     transcriptions = re.findall(r'\[.*?\]', original_transcription_containing_text)
#     for transcription in transcriptions:
#         processed_transcription = t0_TranscriptionAggregatedProcessor.process(transcription, 'de')
#         if processed_transcription != transcription:
#             # modified_transcription_containing_text = modified_transcription_containing_text.replace(
#             #     transcription, processed_transcription.encode('utf-8').decode('utf-8'))
#             modified_transcription_containing_text = modified_transcription_containing_text.replace(
#                 transcription, processed_transcription)
#
#     return modified_transcription_containing_text

# Чисто отладочный метод для печати структуры текста (Paragraph, TextPortion, etc.) в APSO-консоли
def analyze_cell_structure(cell):
    debug_print("\nАнализ структуры ячейки")

    text = cell.Text
    text_enum = text.createEnumeration()

    while text_enum.hasMoreElements():
        element = text_enum.nextElement()
        debug_print("Найден элемент: " + element.getImplementationName())

        if element.supportsService("com.sun.star.text.Paragraph"):
            debug_print("- Это параграф")

            # Проверяем содержимое параграфа
            para_enum = element.createEnumeration()
            has_portions = False

            while para_enum.hasMoreElements():
                portion = para_enum.nextElement()
                has_portions = True
                debug_print("  - Найдена часть: " + portion.getImplementationName())
                if portion.supportsService("com.sun.star.text.TextPortion"):
                    debug_print("    TextPortion: " + portion.String)
                    debug_print("    TextPortionType: " + portion.TextPortionType)

            if not has_portions:
                debug_print("  - Простой текст: " + element.String)
        else:
            debug_print("- Неизвестный элемент: " + element.getImplementationName())
    # end of loop
# end of method
