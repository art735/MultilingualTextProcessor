# -*- coding: utf-8 -*-
import uno
from com.sun.star.style.ParagraphAdjust import LEFT
from com.sun.star.awt.FontWeight import NORMAL

import TableUtils


# Конвертирует выделенный пользователем текст в таблицу. Разделителем между столбцами является символ PIPE «|».
def convert_text_to_table(doc):
    if not hasattr(doc, "Text"):
        return  # Not a Writer document

    text = doc.Text
    controller = doc.getCurrentController()
    selection = controller.getSelection()
    # Если ничего не выделено, выходим из функции
    if not selection or selection.getCount() == 0:
        return

    selected_range = selection.getByIndex(0)
    selected_text = selected_range.getString()

    # ❗ Проверка: если текст не выделен — выход
    # Если не выполнить данную проверку, то Writer будет вставлять пустую таблицу 1х1 в текущее положение курсора
    # даже если ничего в тексте документа не выделено.
    if not selected_text.strip():
        return

    table_separator = "|"  # разделитель
    rows = selected_text.strip().split('\n')
    num_rows = len(rows)
    num_cols = len(rows[0].split(table_separator))

    # Создаём таблицу и вставляем её
    text_table = doc.createInstance("com.sun.star.text.TextTable")
    text_table.initialize(num_rows, num_cols)

    # Отключаем поведение заголовков
    text_table.RepeatHeadline = False
    text_table.HeaderRowCount = 0

    # ❗ Вставка таблицы до удаления текста — это важно!
    # Writer иначе применяет стиль к первой строке (жирный+центр)
    text.insertTextContent(selected_range.getStart(), text_table, False)

    # Удалим текст
    selected_range.setString("")

    # Заполняем таблицу
    for i, row in enumerate(rows):
        cells = row.split(table_separator)
        for j, cell in enumerate(cells):
            table_cell = text_table.getCellByPosition(j, i)
            table_cell.setString(cell.strip())

    border_line = uno.createUnoStruct("com.sun.star.table.BorderLine")
    # По умолчанию все границы таблицы в LibreOffice Writer (и в старом OpenOffice) имеют толщину 0,5 pt,
    # что соответствует ≈ 18 в единицах UNO (1 pt = 35).
    border_line.OuterLineWidth = 18

    # Получаем текущие границы таблицы
    table_border = text_table.TableBorder

    # Устанавливаем внешние и внутренние границы
    table_border.TopLine = border_line
    table_border.BottomLine = border_line
    table_border.LeftLine = border_line
    table_border.RightLine = border_line
    table_border.HorizontalLine = border_line
    table_border.VerticalLine = border_line

    # Флаги валидности всех сторон
    table_border.IsTopLineValid = True
    table_border.IsBottomLineValid = True
    table_border.IsLeftLineValid = True
    table_border.IsRightLineValid = True
    table_border.IsHorizontalLineValid = True
    table_border.IsVerticalLineValid = True

    # Применяем
    text_table.TableBorder = table_border

    # Отменяем жирный шрифт и центрирование в первой строке
    for col in range(num_cols):
        cell = text_table.getCellByPosition(col, 0)
        cell_text = cell.getText()
        cursor = cell_text.createTextCursor()

        # Удаляем стиль "заголовка таблицы", сбрасываем в обычный
        cursor.ParaStyleName = "Table Contents"  # или "Standard", если нужно

        # Снимаем жирный шрифт и выравнивание по левому краю
        cursor.CharWeight = NORMAL
        cursor.ParaAdjust = LEFT

    # Выключить в настройках таблицы галочку "Allow row to break across pages and columns"
    TableUtils.disable_setting_allow_row_to_break_across_pages_and_columns(text_table)

