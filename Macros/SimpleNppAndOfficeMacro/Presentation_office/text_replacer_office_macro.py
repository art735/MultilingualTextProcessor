# -*- coding: utf-8 -*-
import inspect
import os
import sys

# Universal Network Objects (UNO) is the component model used in the OpenOffice.org and LibreOffice.
# It is interface-based and designed to offer interoperability between different programming languages, object models
# and machine architectures, on a single machine, within a LAN or over the Internet.
import uno
from com.sun.star.style.ParagraphAdjust import LEFT
from com.sun.star.awt.FontWeight import NORMAL

# 1.1 Получаем путь к папке, в которой находится данный макрос
script_path = inspect.getfile(inspect.currentframe())
script_dir = os.path.dirname(os.path.abspath(script_path))

# 1.2 Добавляем текущую папку скрипта в classpath, чтобы из этой папки (или относительно этой папки) потом можно было бы
# подтянуть и другие модули.
if script_dir not in sys.path:
    sys.path.append(script_dir)

# 2.1 Импортируем пользовательский модуль config_reader и с его помощью считываем путь к папке с бизнес-логикой из
# конфигурационного файла.
# import config_reader
# path_to_business_logic = config_reader.get_config_path(script_dir)

# Поднимаемся на уровень выше, чем script_dir и заходим в папку Services
path_to_business_logic = os.path.join(os.path.dirname(script_dir), 'Services')

# 2.2 Добавляем путь к папке с бизнес-логикой в classpath
if path_to_business_logic not in sys.path:
    sys.path.append(path_to_business_logic)

# Business logic modules import section
# 3. Импортируем сервис, содержащий словарь для выполнения поиска и замены в документе. Перебираем по очереди
# все пары ключ-значение словаря и выполняем замены в тексте документа.
import text_replacer_service

def run(doc):
    # Объект doc должен создаваться каждый раз при вызове метода-обработчика для каждого открытого документа.
    # Если макрос запускается через встроенный механизм UNO (например, привязан к кнопке, меню и т. п.), то лучшим
    # решением для получения текущего документа будет следующее:
    # doc = XSCRIPTCONTEXT.getDocument()

    # 1. Преобразовать выделенный текст в таблицу
    convert_text_to_table(doc)

    # 2. Выполнить замены в тексте
    make_replacements(doc)


# Конвертирует выделенный пользователем текст в таблицу. Разделителем между столбцами является символ PIPE «|».
def convert_text_to_table(doc):
    if not hasattr(doc, "Text"):
        return  # Not a Writer document

    text = doc.Text
    controller = doc.getCurrentController()
    sel = controller.getSelection()
    # Если ничего не выделено, выходим из функции
    if not sel or sel.getCount() == 0:
        return

    selected_range = sel.getByIndex(0)
    selected_text = selected_range.getString()

    # ❗ Проверка: если текст не выделен — выход
    # Если не выполнить данную проверку, то Writer будет вставлять пустую таблицу 1х1 в текущее положение курсора
    # даже если ничего в тексте документа не выделено
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

# Выполняет замены в тексте документа
def make_replacements(doc):
    replace_descriptor = doc.createReplaceDescriptor()
    replace_descriptor.SearchRegularExpression = True

    # В логике формирования словаря find_and_replace_dict автоматически делается поправка на случай, если макрос будет
    # запускаться в Python2-среде (OpenOffice Writer, May 2025). Для корректной работы поиска и замены в Python2, все
    # строки словаря должны быть явно представлены как Unicode-строки.
    find_and_replace_dict = text_replacer_service.get_find_and_replace_dict()
    for pattern, replacement in find_and_replace_dict.items():
        replace_descriptor.SearchString = pattern
        replace_descriptor.ReplaceString = replacement
        doc.replaceAll(replace_descriptor)
