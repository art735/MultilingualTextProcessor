import AppContext
from FilenameUtils import FilenameUtils
from AnkiCardEntity import SINGLE_NEWLINE_SUBSTITUTE
from GermanTableCellTextTranscriber import GermanTableCellTextTranscriber
from OdtFileTableDao import OdtFileTableDao
from View_enums import CurrentLanguageComboBoxEnum


# Данный класс является по сути юнит-тестом метода GermanSentenceTranscriber.transcribe_sentence(...).
# Он понадобился потому, что метод GermanSentenceTranscriber.transcribe_sentence(...) несколько раз
# модифицировался и его работа должна быть сверена с уже существующими в [Vocab]-файлах транскрипциями предложений.
class A092_SentenceTranscriptionValidator:

    def __init__(self):
        self.odtFileTableDao = OdtFileTableDao()
        self.germanTableCellTextTranscriber = GermanTableCellTextTranscriber()
        self.filenameUtils = FilenameUtils()

    def validate(self):

        # Case #1.
        vocab_filenames = self.filenameUtils.get_all_vocab_filenames()


        # Case #2. Manual list of Vocab-files
        # base_dir = AppContext.get_base_dir()
        # vocab_filenames = [
        # fr'{base_dir}\A1\Aa\[!Vocab] Aa.odt',
        # fr'{base_dir}\A1\Bb\[!Vocab] Bb.odt',
        # fr'{base_dir}\A1\Cc-Dd\[!Vocab] Cc-Dd.odt',
        # fr'{base_dir}\A1\Ee\[!Vocab] Ee.odt',
        # fr'{base_dir}\A1\Ff\[!Vocab] Ff.odt',
        # fr'{base_dir}\A1\Gg\[!Vocab] Gg.odt',
        # fr'{base_dir}\A1\Hh-Jj\[!Vocab] Hh-Jj.odt',
        # fr'{base_dir}\A1\Kk\[!Vocab] Kk.odt',
        # fr'{base_dir}\A1\Ll-Mm\[!Vocab] Ll-Mm.odt',
        # fr'{base_dir}\A1\Nn-Rr\[!Vocab] Nn-Rr.odt',
        # fr'{base_dir}\A1\Ss\[!Vocab] Ss.odt',
        # fr'{base_dir}\A1\Tt-Vv\[!Vocab] Tt-Vv.odt',
        # fr'{base_dir}\A1\Ww-Zz\[!Vocab] Ww-Zz.odt'
        # ]

        results_dict = {}
        for vocab_filename in vocab_filenames:
            table_rows_as_anki_card_entities = self.odtFileTableDao.convert_table_rows_to_anki_cards_of_single_file(
                vocab_filename, read_words=False, read_sentences=True)

            # print(vocab_filename)
            validation_results = self._validate_for_entities(table_rows_as_anki_card_entities)
            results_dict[vocab_filename] = validation_results

        output = ''
        # Если для всех Vocab-файлов результат равен 'ok', то выводим один общий 'ok'.
        if all(val == 'ok' for val in results_dict.values()):
            output = 'ok'
        # Иначе печатаем результаты для каждого проблемного Vocab-файла
        else:
            for vocab_filename, validation_results in results_dict.items():
                if validation_results != 'ok':
                    output += f'{vocab_filename}\n{validation_results}\n\n'

        return output

    def _validate_for_entities(self, table_rows_as_anki_card_entities):
        failed_vocab_transcriptions = []
        failed_excel_or_wiktionary_sentence_transcriptions = []
        failed_sentences = []

        for table_row_as_anki_card_entity in table_rows_as_anki_card_entities:
            sentence = table_row_as_anki_card_entity.front[-1]

            # Со временем, когда все слова будут добавлены в Excel, можно будет убрать эту заглушку
            if sentence in [
                # [Vocab] Hh-Jj
                # 'Hier ist 06131–553221, Pamela Linke.',
                # # 'Der Mount Everest ist 8,848 Meter hoch.',
                # 'Unser Deutschkurs ist international: Silvana kommt aus Italien, Conchi aus Spanien, Yin aus China...',
                # '– Sind Sie Herr Watanabe?\n– Ja.',
                # 'Jenny hat einen neuen Job bei der Post.'
            ]:
                continue

            # 1. Строим заново транскрипцию предложения
            sentence_unknown_words, excel_or_wiktionary_sentence_transcription = (
                self.germanTableCellTextTranscriber.transcribe(sentence, True))

            # 2. Получаем транскрипцию предложения из сущности.
            # У предложений в Vocab-файлах не бывает нескольких полос, эти сущности всегда single-striped, пусть иногда
            # и multiple-lined, но всё равно single-striped. Поэтому обращаемся к полю transcription[0] и получаем всю
            # транскрипцию предложения.
            vocab_transcription = table_row_as_anki_card_entity.transcription[0]
            if '\n' in vocab_transcription:
                vocab_transcription = vocab_transcription.replace('\n', SINGLE_NEWLINE_SUBSTITUTE)

            # 3. Сравниваем новопостроенную транскрипцию с существующей
            if vocab_transcription != excel_or_wiktionary_sentence_transcription:
                failed_vocab_transcriptions.append(vocab_transcription)
                failed_excel_or_wiktionary_sentence_transcriptions.append(excel_or_wiktionary_sentence_transcription)
                failed_sentences.append(sentence)
        # end of loop

        # Main output logic
        output = self._prepare_printable_results_primary_format(failed_vocab_transcriptions,
                                                                failed_excel_or_wiktionary_sentence_transcriptions,
                                                                failed_sentences)

        # Secondary output logic: for letters from Aa to Gg of A1 to add them glottal stops.
        # Output data is then manually inserted into diffchecker.com and compared
        # output = self._prepare_printable_results_secondary_format(failed_vocab_transcriptions,
        #                                                        failed_excel_or_wiktionary_sentence_transcriptions,
        #                                                        failed_sentences)

        if not output:
            output = 'ok'

        return output

    def _prepare_printable_results_primary_format(self, failed_vocab_transcriptions,
                                                  failed_excel_or_wiktionary_sentence_transcriptions, failed_sentences):
        vocab_file_label = '[Vocab]-file:'
        excel_wikt_label = 'Excel / Wiktionary:'
        printable_results = []
        for vocab_transcription, excel_or_wiktionary_sentence_transcription, sentence in zip(
                failed_vocab_transcriptions, failed_excel_or_wiktionary_sentence_transcriptions, failed_sentences):
            t1 = f'{vocab_file_label:19} {vocab_transcription}'
            t2 = f'{excel_wikt_label} {excel_or_wiktionary_sentence_transcription}'

            result = f'{sentence}\n{t1} !=\n{t2}'
            printable_results.append(result)

        output = '\n\n'.join(printable_results)
        return output

    def _prepare_printable_results_secondary_format(self, failed_vocab_transcriptions,
                                                    failed_excel_or_wiktionary_sentence_transcriptions,
                                                    failed_sentences):
        output = ''

        # если все три списка не являются пустыми
        if failed_vocab_transcriptions and failed_excel_or_wiktionary_sentence_transcriptions and failed_sentences:
            vocab_output = '### VOCAB-FILES\n'
            vocab_output += '\n'.join(failed_vocab_transcriptions)

            excel_or_wiktionary_output = '### EXCEL or WIKTIONARY\n'
            excel_or_wiktionary_output += '\n'.join(failed_excel_or_wiktionary_sentence_transcriptions)

            sentences_output = '### SENTENCES\n'
            sentences_output += '\n'.join(failed_sentences)

            output = '\n\n'.join([vocab_output, excel_or_wiktionary_output, sentences_output])
        return output


####################################

if __name__ == '__main__':
    language = CurrentLanguageComboBoxEnum.GERMAN.value
    # language = CurrentLanguageComboBoxEnum.MODERN_GREEK.value
    # language = CurrentLanguageComboBoxEnum.ANCIENT_GREEK.value
    AppContext.switch_language(language)

    a092_SentenceTranscriptionValidator = A092_SentenceTranscriptionValidator()
    output = a092_SentenceTranscriptionValidator.validate()
    print(output)
