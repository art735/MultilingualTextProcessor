import os

import AppContext
from View_enums import CurrentLanguageComboBoxEnum


class FilenameUtils:
    def __init__(self, lang_code=None):
        # Либо язык включается с помощью метода switch_language при запуске того или иного сервиса, либо язык
        # передаётся как параметр конструктора и устанавливается с помощью метода switch_language_by_lang_code
        if lang_code:
            AppContext.switch_language_by_lang_code(lang_code)

    # Business method #1
    def get_all_vocab_filenames(self):
        vocab_predicate = lambda filename: filename.startswith('[!Vocab]') and filename.endswith('.odt')
        vocab_filenames = self.get_filenames_recursively(AppContext.get_base_dir(), vocab_predicate)
        return vocab_filenames

    # Business method #2
    def get_all_portrait_filenames(self):
        portrait_predicate = lambda filename: filename.startswith('[Portrait]') and filename.endswith('.odt')
        portrait_filenames = self.get_filenames_recursively(AppContext.get_base_dir(), portrait_predicate)
        return portrait_filenames

    # Business method #3
    def get_all_sentences_and_inflections_filenames(self):
        sentences_and_inflections_predicate = lambda filename: (filename.startswith('[Sentences & Inflections]') and
                                                                filename.endswith('.odt'))
        sentences_and_inflections_filenames = self.get_filenames_recursively(AppContext.get_base_dir(), sentences_and_inflections_predicate)
        return sentences_and_inflections_filenames

    # Business method #4
    def get_all_morph_dict_filenames(self):
        morph_dict_predicate = lambda filename: (filename.startswith('morph_dict') and filename.endswith('.txt'))
        base_dir = AppContext.get_base_dir()
        morph_dict_filenames = self.get_filenames_recursively(base_dir, morph_dict_predicate)
        return morph_dict_filenames

    # Business method #5
    def get_all_excel_filenames(self):
        excel_predicate = lambda filename: (filename.endswith('.xls'))
        excel_filenames = self.get_filenames_recursively(AppContext.get_base_dir(), excel_predicate)
        return excel_filenames

    # Метод рекурсивно ищет во всех подкаталогах папки folder_path все файлы, имя которых удовлетворяет предикату.
    # os.walk(folder_path) возвращает кортеж из root (текущая папка), dirs (список подкаталогов) и files (список файлов)
    # для каждой директории в folder_path.
    # Данный метод используется не только в текущем классе, но и извне! И чтобы его можно было использовать извне
    # без привязки к SettingsManager, он сделан статическим.
    @staticmethod
    def get_filenames_recursively(folder_path, predicate=None):
        # Если predicate не передан при вызове функции, то будет использоваться лямбда-функция по умолчанию
        # "lambda filename: True", которая всегда возвращает True, тем самым включая все файлы в результат.
        if predicate is None:
            predicate = lambda filename: True

        absolute_filenames = []
        for root, dirs, relative_filenames in os.walk(folder_path):
            for relative_filename in relative_filenames:
                if predicate(relative_filename):
                    absolute_filename = os.path.join(root, relative_filename)
                    absolute_filenames.append(absolute_filename)

        # if not absolute_filenames:
        #     raise Exception(f"Files not found in '{folder_path}'")

        return sorted(absolute_filenames)

#########################################################################


if __name__ == '__main__':
    # language = CurrentLanguageComboBoxEnum.GERMAN.value
    language = CurrentLanguageComboBoxEnum.MODERN_GREEK.value
    # language = CurrentLanguageComboBoxEnum.ANCIENT_GREEK.value
    AppContext.switch_language(language)

    filenameUtils = FilenameUtils()
    filenames = filenameUtils.get_all_vocab_filenames()
    filenames = filenameUtils.get_all_portrait_filenames()
    filenames = filenameUtils.get_all_sentences_and_inflections_filenames()
    filenames = filenameUtils.get_all_morph_dict_filenames()

    print(len(filenames))
    [print(fn) for fn in filenames]
