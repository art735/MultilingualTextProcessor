# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import uno
# Используем константу для принудительной вставки разрыва абзаца (Pilcrow)
from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK


def merge_table_columns_in_the_selected_range(doc):
    table, selected_range_str = _get_selected_table_and_range(doc)
    if table and selected_range_str and ':' in selected_range_str:
        _merge_columns_in_range(doc, table, selected_range_str)

# Возвращает объект таблицы и строковое представление выбранного диапазона, например "B2:D4"
def _get_selected_table_and_range(doc):
    range_name = ''
    table = None

    try:
        # Проверка, что это текстовый документ
        if not doc.supportsService("com.sun.star.text.TextDocument"):
            _show_message_box("Error", "This macro only works in Writer (.odt) documents.")
            return None, None

        # Получение текущего выделения
        selection = doc.getCurrentController().getSelection()

        # Проверка, что выделение — это курсор таблицы
        if selection and selection.supportsService("com.sun.star.text.TextTableCursor"):
            # .RangeName возвращает диапазон в формате "A1:B3"
            range_name = selection.getRangeName()

            # Получаем таблицу, внутри которой находится курсор
            view_cursor = doc.getCurrentController().getViewCursor()
            text_table = view_cursor.TextTable
            if text_table:
                table = text_table

    except Exception as e:
        # Обработка ошибок
        _show_message_box("Ошибка определения таблицы", str(e))
        return None, None

    return table, range_name


def _merge_columns_in_range(doc, table, cell_range):
    """
    Объединяет ячейки в каждом столбце, используя диспетчер.
    """

    # --- Получаем необходимые объекты для работы диспетчера ---
    controller = doc.getCurrentController()
    frame = controller.getFrame()
    dispatcher = uno.getComponentContext().getServiceManager().createInstanceWithContext(
        "com.sun.star.frame.DispatchHelper", uno.getComponentContext())

    # --- 1. Разбор диапазона ---
    try:
        # Парсим диапазон, например "B2:D4"
        start_cell_str, end_cell_str = cell_range.split(':')

        # Парсим начальную ячейку диапазона, например "B2"
        start_col_char = ''.join(filter(lambda c: c.isalpha(), start_cell_str))
        start_row_str = ''.join(filter(lambda c: c.isdigit(), start_cell_str))

        # Парсим конечную ячейку диапазона, например "D4"
        end_col_char = ''.join(filter(lambda c: c.isalpha(), end_cell_str))
        end_row_str = ''.join(filter(lambda c: c.isdigit(), end_cell_str))

        # Вычисляем порядковые номера столбцов и строк для того, чтобы их можно было перебрать в цикле
        # функция ord(...) возвращает целочисленное значение (Unicode-код) переданного символа
        start_col = ord(start_col_char.upper()) - ord('A')
        end_col = ord(end_col_char.upper()) - ord('A')
        start_row = int(start_row_str) - 1
        end_row = int(end_row_str) - 1
    except Exception as e:
        _show_message_box("Ошибка парсинга диапазона",
                          "Неверный формат диапазона. Ожидается формат типа 'B2:D4'.\n\n" + str(e))
        return

    # --- 2. Нормализация кол-ва newlines в ячейках каждой строки ---
    for row_index in range(start_row, end_row):  # end_row не включаем в цикл, в последней строке не нужно выравнивать newlines
        max_newlines = 0
        cells_in_row = []
        for col_index in range(start_col, end_col + 1):
            try:
                cell = table.getCellByPosition(col_index, row_index)
                cells_in_row.append(cell)

                text = cell.getString()
                newline_count = text.count('\n')
                if newline_count > max_newlines:
                    max_newlines = newline_count
            except Exception:
                continue

        # --- БЛОК ДЛЯ ГАРАНТИРОВАННОЙ ВСТАВКИ PILCROW (¶) ---
        for cell in cells_in_row:
            try:
                text = cell
                current_text = text.getString()
                current_newlines = current_text.count('\n')
                newlines_to_add = (max_newlines - current_newlines) + 1

                # _show_message_box("info", "{0}: {1} newlines".format(current_text, current_newlines))

                # Нужен именно такой вариант дальнейшего кода для корректного добавления newline-символа в виде pilcrow.
                # Более простой код cell.setString(current_text + '\n' * newlines_to_add) добавляет в качестве
                # newline-символов символы LINE_BREAK, что является неудовлетворительным.
                if newlines_to_add > 0:
                    cursor = text.createTextCursor()
                    cursor.gotoEnd(False)

                    for _ in range(newlines_to_add):
                        # Принудительно вставляем управляющий символ РАЗРЫВА АБЗАЦА
                        text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)
            except Exception as e:
                continue

    # --- 3. Объединение ячеек через диспетчер и ".uno:MergeCells" ---
    # Поочерёдно проходим по столбцам выделенного диапазона и объединяем ячейки в каждом столбце
    for col_index in range(start_col, end_col + 1):
        num_rows_to_merge = end_row - start_row + 1

        if num_rows_to_merge > 1:
            try:
                # 1. Получаем диапазон ячеек для выделения
                range_to_select = table.getCellRangeByPosition(col_index, start_row, col_index, end_row)

                # 2. Программно выделяем этот диапазон в документе
                controller.select(range_to_select)

                # 3. Вызываем команду объединения через диспетчер
                # Это эквивалентно нажатию кнопки "Объединить ячейки" на панели инструментов
                dispatcher.executeDispatch(frame, ".uno:MergeCells", "", 0, ())

            except Exception as e:
                # Даже диспетчер может выдать ошибку в редких случаях (например, защищенная таблица)
                # Просто пропускаем этот столбец.
                _show_message_box("Ошибка объединения", str(e))  # Можно раскомментировать для отладки
                continue


def _show_message_box(title, message):
    """Helper function to display a message box."""
    ctx = uno.getComponentContext()
    smgr = ctx.getServiceManager()

    # Get access to the current document's "window" to bind the MessageBox
    desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    doc = desktop.getCurrentComponent()

    if doc:
        parent_window = doc.getCurrentController().getFrame().getContainerWindow()
    else:
        # If no document is found, there's nothing to bind to
        parent_window = None

    # Create the dialog window service
    toolkit = smgr.createInstanceWithContext("com.sun.star.awt.Toolkit", ctx)

    # Create the MessageBox
    # Arguments: parent window, box type ('infobox', 'warningbox', 'errorbox'),
    # buttons (1=OK), title, message
    msgbox = toolkit.createMessageBox(parent_window, "infobox", 1, title, message)

    # Display the box
    msgbox.execute()


