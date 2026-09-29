import AppContext
from MorphDictToFileWriter import MorphDictToFileWriter
from View_enums import CurrentLanguageComboBoxEnum


class A000_MorphDictGeneratorAndToFileSaver:
    def __init__(self):
        from BusinessObjectFactory import BusinessObjectFactory
        # self.morphDictService = MorphDictService()
        self.morphDictService = BusinessObjectFactory.get_MorphDictService()
        self.morphDictToFileWriter = MorphDictToFileWriter()

    def perform(self, input_text):
        morph_dict = self.morphDictService.generate_morph_dict_on_the_fly(input_text)
        info_msg = self.morphDictToFileWriter.write_to_file(morph_dict)
        return info_msg


###################################################

input_str = """
1. Sie ist sehr freundlich und hilfsbereit.
2. Gestern haben sie einen neuen Hund adoptiert.
"""

input_str = """
Που δεν είναι ώρα να θυμηθώ τώρα.
"""

if __name__ == '__main__':
    # language = CurrentLanguageComboBoxEnum.GERMAN.value
    language = CurrentLanguageComboBoxEnum.MODERN_GREEK.value
    # language = CurrentLanguageComboBoxEnum.ANCIENT_GREEK.value
    AppContext.switch_language(language)

    a000_MorphDictGeneratorAndToFileSaver = A000_MorphDictGeneratorAndToFileSaver()

    res = a000_MorphDictGeneratorAndToFileSaver.perform(input_str)
    print(res)
