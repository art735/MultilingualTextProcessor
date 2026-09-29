import AppContext
import Utils
from FilenameUtils import FilenameUtils
from MorphDictFromFileReader import MorphDictFromFileReader
from MorphDictToStrConverter import MorphDictToStrConverter
from OdtFilesService import OdtFilesService
from View_enums import CurrentLanguageComboBoxEnum


# Предоставляет вызывающему коду словарь с морфологическим анализом каждого слова строки текста.
# Ключами словаря являются отдельные строки текста (как правило, каждая строка представляет одно предложение).
# Значениями словаря являются списки кортежей (token, lemma, pos, morph) всех слов строки текста, указанной как ключ
# словаря. Морфологические формы могут быть получены двумя способами:
# 1) из анализа текста с помощью spaCy "на лету" (такой способ подходит для тех иностранных языков, у которых для
# spaCy имеются хорошо натренированные модели, как правило, это _trf-модели, т. к. _sm, _md, _lg модели дают слабый
# результат с точки зрения морфологического анализа и нахождения лемм). Такими языками являются, например:
# - немецкий язык (модель 'de_dep_news_trf');
# - древнегреческий язык (модель 'grc_odycy_joint_trf').
# 2) из анализа текста, ранее выполненного с помощью AI и сохранённого в виде Python-словаря в отдельном .txt файле
# для последующей обработки с помощью Python-пайплайна. Данный способ особенно подходит для языков, у которых для spaCy
# нет _trf-моделей (например, новогреческий, март 2025 г.) или вообще нет никаких моделей (напр., церковнославянский).
# AI (особенно ChatGPT-4o, март 2025) неплохо справляется с морфологическим анализом текста и дальше эти результаты
# можно обрабатывать программно.
# Примечание: но даже для тех иностранных языков, для которых имеются _trf-модели, хорошей практикой следует признать
# работу с текстом не "на лету", а тоже с помощью предварительно подготовленного (как с помощью spaCy, так и
# с помощью AI, или комбинацией обоих способов) и сохранённого в txt-файл Python-словаря морфологических форм.
# Такой способ позволит при необходимости вручную исправлять в файле ошибки определения морфологии/лемм тех или иных
# токенов, что повысит точность анализа текста и избавит от необходимости использования различных "заглушек"
# (как программных, так и текстовых в виде различных "списков игнорируемых токенов" или "списков исключений").
class MorphDictService:
    def __init__(self, spaCyEngineWrapper):
        self.spaCyEngineWrapper = spaCyEngineWrapper
        self.odtFilesService = OdtFilesService()
        self.morphDictFromFileReader = MorphDictFromFileReader()
        self.filenameUtils = FilenameUtils()

    # Business method #1. Reads either spaCy-generated or AI-prepared in advance morphological dictionary from a file.
    def read_morph_dict_from_last_file(self):
        # Вычитываем имена всех morph_dict файлов
        all_morph_dict_filenames = self.filenameUtils.get_all_morph_dict_filenames()

        # Берём в работу последний morph_dict файл
        last_morph_dict_filename = all_morph_dict_filenames[-1]

        # Вычитываем из файла строковое представление morph_dict и преобразуем его в Python-объект.
        morph_dict = self.morphDictFromFileReader.read_from_file(last_morph_dict_filename)

        # print(morph_dict)
        return morph_dict

    # Бизнес-метод для новогреческого с новым подходом: формирование первичного morph_dict (только token, pos, morph,
    # т. е. без лемм!) с помощью Stanza, прогон его через LLM для определения лемм и затем уже сборка из всего этого
    # полноценного morph_dict с кортежами вида (token, LEMMA, pos, morph)
    # В работу при этом подходе будут браться только те токены, которых ещё не было в предыдущих morph_dict-словарях.
    def read_and_merge_morph_dicts_from_all_files(self):
        # Вычитываем имена всех morph_dict файлов
        all_morph_dict_filenames = self.filenameUtils.get_all_morph_dict_filenames()

        result = []
        for morph_dict_filename in all_morph_dict_filenames:
            # Вычитываем из файла строковое представление morph_dict и преобразуем его в Python-объект.
            morph_dict = self.morphDictFromFileReader.read_from_file(morph_dict_filename)

            # Перебираем все кортежи в словаре и формируем из них список кортежей вида (token, pos)
            for lst in morph_dict.values():
                for token, lemma, pos, morph in lst:
                    result.append((token, pos))

        return result

    # Business method #2. Generates a morphological dictionary for a given text on the fly.
    def generate_morph_dict_on_the_fly(self, input_text):
        morph_dict = {}
        input_text = input_text.strip()  # Убирает по краям строки пробел и следующие символы [\t\n\r\v\f]

        # Разбиваем текст на список строк
        input_sentences_with_possible_duplicates = Utils.split_by(input_text, '\n')

        # Текст может содержать дублирующиеся строки, что создаст дополнительную вычислительную нагрузку на spaCy.
        # Убираем возможные дубликаты строк, сохраняя порядок их следования.
        input_sentences_unique = list(dict.fromkeys(input_sentences_with_possible_duplicates))

        # Вычитываем уже ранее обработанные предложения из всех предыдущих [Vocab]-файлов, чтобы если одно из таких
        # предложений встретится в новой порции предложений, оно было бы проигнорировано (предложения-дубликаты в
        # Гёте-методичке и других текстах (напр., субтитрах) могут встречаться).
        vocab_files_sentences = self.odtFilesService.get_sentences_from_all_vocab_files()

        # Перебираем предложения в порядке их следования в тексте
        for input_sentence in input_sentences_unique:
            if input_sentence not in vocab_files_sentences:
                tuples = self.spaCyEngineWrapper.get_doc_object_tuples(input_sentence, True)
                morph_dict[input_sentence] = tuples

        return morph_dict


####################################################################

input_str = """
1. Sie ist sehr freundlich und hilfsbereit.
2. Gestern haben sie einen neuen Hund adoptiert.
"""

input_str = """
Που δεν είναι ώρα να θυμηθώ τώρα.
"""

if __name__ == '__main__':
    from BusinessObjectFactory import BusinessObjectFactory

    # language = CurrentLanguageComboBoxEnum.GERMAN.value
    language = CurrentLanguageComboBoxEnum.MODERN_GREEK.value
    # language = CurrentLanguageComboBoxEnum.ANCIENT_GREEK.value
    AppContext.switch_language(language)

    # morphDictService = MorphDictService()
    morphDictService = BusinessObjectFactory.get_MorphDictService()
    morphDictToStrConverter = MorphDictToStrConverter()

    # Case 1
    # res_morph_dict = morphDictService.read_morph_dict_from_last_file()
    # print(morphDictToStrConverter.morph_dict_to_str(res_morph_dict))

    # Case 2
    res_morph_dict = morphDictService.generate_morph_dict_on_the_fly(input_str)
    print(morphDictToStrConverter.morph_dict_to_str(res_morph_dict))




