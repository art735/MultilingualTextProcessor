from pathlib import Path

import AppContext
from FilenameUtils import FilenameUtils
from OdtFileTableDao import OdtFileTableDao
from View_enums import CurrentLanguageComboBoxEnum


class A110_SentencesAndInflectionsFileAgainstVocabFileValidator:
    def __init__(self):
        self.odtFileTableDao = OdtFileTableDao()
        self.filenameUtils = FilenameUtils()

    def validate(self):
        # 1. Валидировать, что кол-во предложений в обоих файлах совпадает, т. е. что при поиске морф. форм хотя бы
        # не потерялись исходные предложения

        vocab_filenames = self.filenameUtils.get_all_vocab_filenames()
        sentences_and_inflections_filenames = self.filenameUtils.get_all_sentences_and_inflections_filenames()
        for vocab_filename, sai_filename in zip(vocab_filenames, sentences_and_inflections_filenames):
            vocab_sentences = self.odtFileTableDao.convert_table_rows_to_anki_cards_of_single_file(
                vocab_filename, read_words=False, read_sentences=True)
            sai_sentences = self.odtFileTableDao.convert_table_rows_to_anki_cards_of_single_file(
                sai_filename, read_words=False, read_sentences=True)

            vocab_filename_printable = Path(*Path(vocab_filename).parts[-3:])
            sai_filename_printable = Path(*Path(sai_filename).parts[-3:])

            # Не получится сравнивать len(vocab_sentences) != len(sai_sentences) потому, что в sai_sentences могут быть
            # повелительные формы глаголов с '!' в конце, что ложно интерпретируется как предложение.
            for vocab_sentence in vocab_sentences:
                if vocab_sentence not in sai_sentences:  # работает на сущностях с переопределённым методом __eq__
                    # if str(vocab_sentence) not in [str(sentence) for sentence in sai_sentences]:
                    print(f"Vocab sentence '{vocab_sentence}' not found in {sai_filename_printable}")


#########################################

if __name__ == '__main__':
    language = CurrentLanguageComboBoxEnum.GERMAN.value
    # language = CurrentLanguageComboBoxEnum.MODERN_GREEK.value
    # language = CurrentLanguageComboBoxEnum.ANCIENT_GREEK.value
    AppContext.switch_language(language)

    a110_SentencesAndInflectionsFileAgainstVocabFileValidator = A110_SentencesAndInflectionsFileAgainstVocabFileValidator()
    a110_SentencesAndInflectionsFileAgainstVocabFileValidator.validate()
