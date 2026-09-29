# -*- coding: utf-8 -*-
from aqt import mw
from aqt.utils import showInfo
from aqt.qt import QAction, QKeySequence

# При написании Anki addon, если все модули находятся в одной папке (например, addons21/auto_replace/),
# нужно использовать относительный импорт:
from . import auto_replace_core
from . import auto_reset_outdated_cards

# Храним ссылку на действие, чтобы избежать дублирования
action = None

def get_note_form(count):
    """Returns the correct form of 'note' based on the count."""
    return "note" if count == 1 else "notes"

def auto_replace_dashes_on_load():
    # Получаем коллекцию; mw = main window
    col = mw.col
    if col is None:
        showInfo("Ошибка: коллекция не загружена!")
        return

    # Получаем все ID карточек
    card_ids = col.db.all("SELECT id FROM cards")
    modified_count = 0

    # Метод col.db.all("SELECT id FROM cards") возвращает список кортежей, где каждый кортеж содержит результат одной
    # строки запроса. Поскольку запрос выбирает только одно поле (id), каждый кортеж состоит из одного элемента,
    # например: [(123,), (124,), (125,), ...].
    # Каждый элемент списка — это кортеж с одним значением, и в Python такие кортежи записываются с запятой, чтобы
    # отличать их от простых выражений в скобках (например, (123) интерпретируется как число 123, а (123,) — как кортеж
    # с одним элементом).
    # Цикл for позволяет распаковывать элементы итерируемого объекта. Поскольку card_ids — это список кортежей, где
    # каждый кортеж содержит один элемент (ID карточки), запись for (cid,) in card_ids: распаковывает каждый кортеж,
    # присваивая его единственный элемент переменной cid.
    # Круглые скобки и запятая в (cid,) соответствуют структуре кортежа (123,), возвращаемого запросом.
    # Запятая обязательна, чтобы Python понял, что это кортеж с одним элементом, а не просто выражение в скобках.
    for (cid,) in card_ids:
        card = col.get_card(cid)
        note = card.note()
        modified = False

        # Обходим все поля заметки
        for field_name in note.keys():
            original_value = field_value = note[field_name]

            # Применяем все правила замены
            field_value = auto_replace_core.make_replacements(field_value)

            # Если поле изменилось, обновляем его
            if field_value != original_value:
                note[field_name] = field_value
                modified = True

        # Если были изменения, сохраняем заметку
        if modified:
            note.flush()
            modified_count += 1

    # Сохраняем изменения в коллекции
    col.save()

    # Показываем результат с согласованной формой слова
    note_form = get_note_form(modified_count)
    showInfo(f"Updated: {modified_count} {note_form}")


def run_macro_functions():
    # функция текстовых замен
    auto_replace_dashes_on_load()

    # функция сброса due interval у "старых" карточек
    auto_reset_outdated_cards.reset_cards()


def setup_shortcut():
    # Пункт меню "Tools -> Custom auto replace" представлен в коде объектом action
    global action
    # Проверяем, не добавлено ли действие ранее
    if action is not None:
        print("--- [DEBUG] Действие уже добавлено, пропускаем ---")
        return

    # Создаем QAction для меню Tools
    action = QAction("Custom auto replace", mw)

    # Устанавливаем горячую клавишу
    action.setShortcut(QKeySequence("Ctrl+Alt+M"))

    # Подключаем действие к функции
    action.triggered.connect(run_macro_functions)

    # Добавляем действие в меню Tools
    mw.form.menuTools.addAction(action)
    print("--- [DEBUG] Горячая клавиша Ctrl+Alt+M установлена ---")

# Запускаем настройку после полной загрузки профиля
from aqt.gui_hooks import profile_did_open
profile_did_open.append(setup_shortcut)

print("--- [DEBUG] Аддон AutoReplaceDash успешно загружен ---")