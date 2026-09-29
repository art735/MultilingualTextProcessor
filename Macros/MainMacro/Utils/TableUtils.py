# -*- coding: utf-8 -*-

# Выключить в настройках таблицы галочку "Allow row to break across pages and columns"
def disable_setting_allow_row_to_break_across_pages_and_columns(table):
    for i in range(table.getRows().getCount()):
        row = table.getRows().getByIndex(i)
        row.IsSplitAllowed = False  # запретить разрыв строки

