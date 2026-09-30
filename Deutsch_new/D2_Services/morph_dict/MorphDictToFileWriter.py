from datetime import datetime

import AppContext
from MorphDictToStrConverter import MorphDictToStrConverter
from View_enums import CurrentLanguageComboBoxEnum


class MorphDictToFileWriter:
    def __init__(self):
        self.morphDictToStrConverter = MorphDictToStrConverter()

    def write_to_file(self, morph_dict):
        # Преобразовываем morph_dict в строковое представление
        morph_dict_str = self.morphDictToStrConverter.morph_dict_to_str(morph_dict)

        # Создаём строку с текущей датой и временем
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        base_dir = AppContext.get_base_dir()
        filename = f'{base_dir}\morph_dict {timestamp}.txt'

        # Запись текстового представления словаря в файл
        with open(filename, "w", encoding="utf-8") as f:
            f.write(morph_dict_str)

        shorted_filename_for_info_msg = filename.replace(
            'E:\Languages\[Git repo] MultilingualTextProcessor', '')
        output = f'morph_dict is dumped to "{shorted_filename_for_info_msg}"'

        # Проверяем, что файл на диске действительно создался и словарь, записанный в него, равен исходному
        # morph_dict_from_file = self.morphDictFromFileReader.read_from_file(filename)
        # if morph_dict_from_file == morph_dict:
        #     output = f'morph_dict dumped to "{filename}"'
        # else:
        #     output = f'Failed to dump morph_dict to "{filename}"'

        return output


###################################################

test_dict = {
    "1. Sie ist sehr freundlich und hilfsbereit.": [
        ("Sie", "sie", "PRON", "Case=Nom|Gender=Fem|Number=Sing|Person=3|PronType=Prs"),
        ("ist", "sein", "AUX", "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin"),
        ("sehr", "sehr", "ADV", ""),
        ("freundlich", "freundlich", "ADV", "Degree=Pos"),
        ("und", "und", "CCONJ", ""),
        ("hilfsbereit", "hilfsbereit", "ADV", "Degree=Pos")
    ],
    "2. Gestern haben sie einen neuen Hund adoptiert.": [
        ("Gestern", "gestern", "ADV", ""),
        ("haben", "haben", "AUX", "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin"),
        ("sie", "sie", "PRON", "Case=Nom|Number=Plur|Person=3|PronType=Prs"),
        ("einen", "ein", "DET", "Case=Acc|Definite=Ind|Gender=Masc|Number=Sing|PronType=Art"),
        ("neuen", "neu", "ADJ", "Case=Acc|Degree=Pos|Gender=Masc|Number=Sing"),
        ("Hund", "Hund", "NOUN", "Case=Acc|Gender=Masc|Number=Sing"),
        ("adoptiert", "adoptieren", "VERB", "VerbForm=Part")
    ]
}

if __name__ == '__main__':
    language = CurrentLanguageComboBoxEnum.GERMAN.value
    # language = CurrentLanguageComboBoxEnum.MODERN_GREEK.value
    # language = CurrentLanguageComboBoxEnum.ANCIENT_GREEK.value
    AppContext.switch_language(language)

    morphDictToFileWriter = MorphDictToFileWriter()
    # res = morphDictToFileWriter.write_to_file(test_dict)
    # print(res)

    for language in [CurrentLanguageComboBoxEnum.GERMAN.value, CurrentLanguageComboBoxEnum.MODERN_GREEK.value]:
        AppContext.switch_language(language)
        res = morphDictToFileWriter.write_to_file(test_dict)
        print(res)
