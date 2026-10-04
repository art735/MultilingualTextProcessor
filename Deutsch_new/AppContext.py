from Container import CONTAINER
from View_enums import CurrentLanguageComboBoxEnum

# Данная обёртка создана для того, чтобы избежать циклического импорта, связанного с импортом Container, в других
# модулях.

# Константы для кодов языков.
# Используются, например, при создании производных сервисов от базовых сервисов при передаче кода языка как параметра
# конструктора.
DEU_LANG_CODE = 'deu'
ELL_LANG_CODE = 'ell'
GRC_LANG_CODE = 'grc'


# def print_all_settings():
#     CONTAINER.settingsManager().print_all_settings()
#
# def print_current_settings():
#     CONTAINER.settingsManager().print_current_settings()

def get_resources_dir():
    resources_dir = CONTAINER.settingsManager().get("resources_dir")
    return resources_dir


# Данный метод вызывается из обработчика событий переключения языка на UI
def switch_language(language):
    CONTAINER.settingsManager().switch_language(language)

# Обёртка вокруг метода switch_language, переключает язык в некоторых сервисах, куда передаётся поле lang_code
def switch_language_by_lang_code(lang_code):
    if is_language_german(lang_code):
        language = CurrentLanguageComboBoxEnum.GERMAN.value
    elif is_language_modern_greek(lang_code):
        language = CurrentLanguageComboBoxEnum.MODERN_GREEK.value
    elif is_language_ancient_greek(lang_code):
        language = CurrentLanguageComboBoxEnum.ANCIENT_GREEK.value
    elif is_language_english(lang_code):
        language = CurrentLanguageComboBoxEnum.ENGLISH.value
    else:
        raise Exception(f"Language with code '{lang_code}' is not supported.")
    CONTAINER.settingsManager().switch_language(language)


def get_current_language():
    lang_code = CONTAINER.settingsManager().get("lang_code")
    language = CONTAINER.settingsManager().get_language_by_lang_code(lang_code)
    return language

# В Python нет классической перегрузки методов, но использование здесь параметра по умолчанию lang_code=None
# позволяет сделать метод как бы перегруженным, чтобы можно было использовать его как с параметром, так и без.
# Вызываем метод с параметром из тех сервисов, которые хранят lang_code как состояние. Состояние они хранят затем,
# чтобы они не были жёстко привязаны к SettingsManager-контексту и их было бы легче тестировать (как в блоке
# if __name__ == '__main__':, так и с помощью классических юнит-тестов).
# В тех сервисах, которые не имеют поля lang_code (или ему подобных из SettingsManager-контекста), данные методы
# вызываются без параметра, что заставляет их обращаться к текущему контексту SettingsManager-а.
def is_language_german(lang_code=None):
    if lang_code:
        is_german = lang_code == 'deu'
    else:
        is_german = get_lang_code() == 'deu'
    return is_german


def is_language_modern_greek(lang_code=None):
    if lang_code:
        is_modern_greek = lang_code == 'ell'
    else:
        is_modern_greek = get_lang_code() == 'ell'
    return is_modern_greek


def is_language_ancient_greek(lang_code=None):
    if lang_code:
        is_ancient_greek = lang_code == 'grc'
    else:
        is_ancient_greek = get_lang_code() == 'grc'
    return is_ancient_greek

def is_language_english(lang_code=None):
    if lang_code:
        is_english = lang_code == 'eng'
    else:
        is_english = get_lang_code() == 'eng'
    return is_english

def is_language_church_slavonic(lang_code=None):
    if lang_code:
        is_church_slavonic = lang_code == 'chu'
    else:
        is_church_slavonic = get_lang_code() == 'chu'
    return is_church_slavonic


def get_lang_code():
    lang_code = CONTAINER.settingsManager().get("lang_code")
    return lang_code


def get_base_dir():
    base_dir = CONTAINER.settingsManager().get("base_dir")
    return base_dir


def get_excel_filename():
    excel_filename = CONTAINER.settingsManager().get("excel_filename")
    return excel_filename


def get_regular_cards_deck():
    regular_cards_deck = CONTAINER.settingsManager().get("regular_cards_deck")
    return regular_cards_deck


def get_aggregate_cards_deck():
    aggregate_cards_deck = CONTAINER.settingsManager().get("aggregate_cards_deck")
    return aggregate_cards_deck
