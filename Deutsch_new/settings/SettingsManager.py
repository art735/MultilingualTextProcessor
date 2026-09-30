import os
import re
from pathlib import Path
from pprint import pprint

import yaml

import AppContext
from View_enums import CurrentLanguageComboBoxEnum

# SETTINGS_FILE = r"E:\Languages\[Git repo] MultilingualTextProcessor\Deutsch_new\settings\settings.yaml"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SETTINGS_FILE = PROJECT_ROOT / "settings" / "settings.yaml"

class SettingsManager:
    def __init__(self, settings_file=SETTINGS_FILE):
        self.settings_file = settings_file
        self.all_settings = {}
        self.current_settings = {}
        self.load_config()

    def load_config(self):
        with open(self.settings_file, "r", encoding="utf-8") as f:
            self.all_settings = yaml.safe_load(f)

    def switch_language(self, lookup_key):
        """Применяет настройки по ключу lookup"""
        if lookup_key in self.all_settings:
            self.current_settings = self.all_settings[lookup_key]
        else:
            print(f"⚠ Lookup choice '{lookup_key}' is not found among 'settings.yaml'!")
        return

    # Возвращает название языка по его коду.
    # Например, возвращает 'Ancient Greek' для кода 'grc'
    def get_language_by_lang_code(self, lang_code):
        for language, settings in self.all_settings.items():
            if isinstance(settings, dict) and settings.get('lang_code', '') == lang_code:
                return language

    def get(self, key, default=None):
        """Получает значение настройки"""

        if not self.current_settings:
            raise Exception(f"No langauge is selected or the selected language is not in 'settings.yaml'")

        current_choice = self.current_settings.get(key, default)

        if not current_choice:
            raise Exception(f"Setting '{key}' is not found in 'settings.yaml' for the selected language!")

        # Находит подстроки вида ${имя_переменной}.
        # \w – любой "словесный" символ (буква, цифра или подчёркивание). Эквивалентно [a-zA-Z0-9_].
        pattern = re.compile(r'\$\{(\w+)\}')
        while pattern.search(current_choice):  # пока в строке есть переменные вида ${...}
            # Программная обработка нотации ${...}, которая нативно в YAML не поддерживается.
            if '${resources_dir}' in current_choice:
                resources_dir = self.all_settings.get('resources_dir', default)
                current_choice = current_choice.replace('${resources_dir}', resources_dir)

            # Использовалось в пути к excel_file, потом эту настройку удалил.
            if '${base_dir}' in current_choice:
                base_dir = self.current_settings.get('base_dir', default)
                current_choice = current_choice.replace('${base_dir}', base_dir)

        # Если текущая настройка содержит путь к файлу или папке, то на всякий случай нормализуем его после возможно
        # проведённых замен связанных с ${...} нотацией.
        if self.is_probable_path(current_choice):
            current_choice = os.path.normpath(current_choice)

        return current_choice

    # Программная обработка нотации ${...}, которая нативно в YAML не поддерживается.
    # Метод заменяет, например, ${resources_dir} её фактическим значением
    def _substitute_variables(self, text, default=""):
        # Находит подстроки вида ${имя_переменной}.
        # \w – любой "словесный" символ (буква, цифра или подчёркивание). Эквивалентно [a-zA-Z0-9_].
        pattern = re.compile(r'\$\{(\w+)\}')
        while pattern.search(text):  # пока в строке есть переменные вида ${...}
            # Вычитывает значение заменяемой переменной (match.group(1) — это имя переменной внутри ${}) и заменяет
            # получает значение переменной из self.all_settings (если её нет, подставляется default) и заменяет в строке
            # text найденное вхождение ${имя_переменной} на полученное значение.
            text = re.sub(pattern, lambda match: self.current_settings.get(match.group(1), default), text)
        return text

    # Метод проверяет, является ли строка путём к файлу или папке (в таких путях нужно нормализовывать слеши
    # после замен, связанных с ${...} нотацией).
    # Если есть буква диска или абсолютный путь, то скорее всего это путь:
    def is_probable_path(self, s):
        """Определяет, является ли строка путем к файлу или папке"""
        drive, tail = os.path.splitdrive(s)

        # Условие 1: есть буква диска (например, "C:") или слэши
        has_drive_or_slash = bool(drive) or any(c in s for c in ["/", "\\"])

        # Условие 2: либо есть расширение файла, либо строка заканчивается на /
        is_file_or_dir = "." in os.path.basename(s) or s.endswith(("/", "\\"))

        return has_drive_or_slash and is_file_or_dir

    def print_all_settings(self):
        pprint(self.all_settings)

    def print_current_settings(self):
        for key, value in self.current_settings.items():
            print(f"{key}: {value}")


#############################################################

if __name__ == "__main__":
    # language = CurrentLanguageComboBoxEnum.GERMAN.value
    language = CurrentLanguageComboBoxEnum.MODERN_GREEK.value
    # language = CurrentLanguageComboBoxEnum.ANCIENT_GREEK.value
    AppContext.switch_language(language)

    base_dir = AppContext.get_base_dir()
    print(base_dir)

    current_language = AppContext.get_current_language()
    print(current_language)


