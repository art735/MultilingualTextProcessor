# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

# Меняет регистр выделенного текста. Внутри одной ячейки таблицы тоже работает, но при выделении нескольких ячеек уже
# не работает. При необходимости менять регистр слов внутри выделенных ячеек таблицы можно с помощью стандартных команд
# контекстного меню.
def rotate_case(XSCRIPTCONTEXT):
    ctx = XSCRIPTCONTEXT.getComponentContext()
    smgr = ctx.getServiceManager()
    doc = XSCRIPTCONTEXT.getDocument()
    frame = doc.getCurrentController().getFrame()
    controller = doc.getCurrentController()
    selection = controller.getSelection()

    # Внутри таблицы макрос работать не умеет и чтобы при выделении таблицы не генерировался exception, проверяем, что
    # selection имеет атрибут getCount, и только потом вызываем этот метод.
    # Менять регистр слов внутри таблицы можно с помощью стандартных команд контекстного меню.
    if not selection or not hasattr(selection, 'getCount') or selection.getCount() != 1:
        return

    text_range = selection.getByIndex(0)
    text = text_range.getString()
    if not text.strip():
        return

    # Определение текущего регистра
    text_stripped = text.strip()

    if text_stripped.isupper():
        next_command = ".uno:ChangeCaseToLower"
    elif text_stripped.islower():
        next_command = ".uno:ChangeCaseToTitleCase"
    else:
        next_command = ".uno:ChangeCaseToUpper"

    dispatcher = smgr.createInstanceWithContext("com.sun.star.frame.DispatchHelper", ctx)
    dispatcher.executeDispatch(frame, next_command, "", 0, ())

    # Восстановление выделения (иначе Writer его теряет)
    view_cursor = controller.getViewCursor()
    view_cursor.gotoRange(text_range.getStart(), False)
    view_cursor.gotoRange(text_range.getEnd(), True)

