import asyncio
import re
import sys
from urllib.error import URLError

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QButtonGroup
from qasync import asyncSlot, QEventLoop

import AppContext
from A000_MorphDictGeneratorAndToFileSaver import A000_MorphDictGeneratorAndToFileSaver
from A020_TranscriptionsAndTranslationsLookUpper import A020_TranscriptionsAndTranslationsLookUpper
from A030_SplitComplexWordsProcessor import A030_SplitComplexWordsProcessor
from A040_VocabFilesConsistencyChecker import A040_VocabFilesConsistencyChecker
from A050_Printable3ColVersionOfLastVocabFileComposer import A050_Printable3ColVersionOfLastVocabFileComposer
from A060_VocabFileAgainstPortraitFileValidator import A060_VocabFileAgainstPortraitFileValidator
from A070_UnsentencedVersionOfLastVocabFileForAnkiMaker import A070_UnsentencedVersionOfLastVocabFileForAnkiMaker
from A080_DuplicatesAfterImportToAnkiRevealer import A080_DuplicatesAfterImportToAnkiRevealer
from A091_GermanInflectionsXlsValidator import A091_GermanInflectionsXlsValidator
from A092_SentenceTranscriptionValidator import A092_SentenceTranscriptionValidator
from A100_GermanTextMorphologicalAnalysisPerformer import A100_GermanTextMorphologicalAnalysisPerformer
from BusinessObjectFactory import BusinessObjectFactory
from Container import CONTAINER
from FilenameUtils import FilenameUtils
from MD1_MorphDictWithoutLemmasMaker import MD1_MorphDictWithoutLemmasMaker
from MD2_LlmLemmasIntoMorphDictIntegrator import MD2_LlmLemmasIntoMorphDictIntegrator
from OdtFilesService import OdtFilesService
from InputTextFromGuiPreprocessor import InputTextFromGuiPreprocessor
from TokenLemmaPosMorphDisplayer import TokenLemmaPosMorphDisplayer
from View_enums import CurrentLanguageComboBoxEnum, MorphDictPolicyComboBoxEnum, VocabFileComboBoxEnum, \
    PortraitFileComboBoxEnum


class View(QMainWindow):
    def __init__(self):
        super().__init__()
        # uic.loadUi("D1_ViewController/View.ui", self)
        uic.loadUi("D1_ViewController/View_new.ui", self)
        # uic.loadUi("View.ui", self)

        self.makeMorphDictRadioButton.setChecked(True)
        self.findNewLemmasRadioButton.setChecked(True)
        self.lineByLineModeRadioButton.setChecked(True)
        self.includeSentencesWithNewLemmasInTheOutputCheckBox.setChecked(True)
        self.includeEvenSentencesWithoutNewLemmasInTheOutputCheckBox.setChecked(True)
        # self.outputFormatAsFrequencyDictionaryCheckBox.setChecked(False)

        # Создаём объект типа QButtonGroup и добавляем в него те радиокнопки, которые должны включаться и отключаться
        # только в пределах этой группы и не должны влиять и мешать включению/отключению основного набора радиокнопок.
        # Компонент QButtonGroup не имеет графического представления и его нельзя найти в Qt Designer и перетащить
        # мышкой на форму. Это логический компонент, который можно использовать только через код.
        self.buttonGroup = QButtonGroup(self)  # Создаем группу
        self.buttonGroup.addButton(self.lineByLineModeRadioButton)  # Добавляем кнопки в группу
        self.buttonGroup.addButton(self.wholeTextModeRadioButton)

        # Current language lookup
        for option in CurrentLanguageComboBoxEnum:
            # combo_box.addItem("Отображаемое значение 1", реальное_значение)
            # addItem(text, userData) добавляет в lookup текст опции и связанный с ней пользовательский объект
            self.currentLanguageComboBox.addItem(option.value, option)  # передаём сам enum в userData
        self.currentLanguageComboBox.currentIndexChanged.connect(self.currentLanguageComboBox_selection_changed)
        self.switch_language()

        # UC #00 (optional)
        # self.generateMorphDictAndSaveItToFileRadioButton.clicked.connect(self.generateMorphDictAndSaveItToFileRadioButton_Clicked)

        # UC #01
        for option in MorphDictPolicyComboBoxEnum:
            # combo_box.addItem("Отображаемое значение 1", реальное_значение)
            # addItem(text, userData) добавляет в lookup текст опции и связанный с ней пользовательский объект
            self.morphDictPolicyComboBox.addItem(option.value, option)  # передаём сам enum в userData
        self.morphDictPolicyComboBox.currentIndexChanged.connect(self.morphDictPolicyComboBox_selection_changed)

        # Используем дифолтное значение morphDictPolicyComboBox для активации/деактивации других контроллов при старте
        # приложения
        self.update_wholeTextModeRadioButton_state()

        self.findNewLemmasRadioButton.clicked.connect(self.findNewLemmasRadioButton_Clicked)
        self.lineByLineModeRadioButton.clicked.connect(self.lineByLineModeRadioButton_Clicked)
        self.includeSentencesWithNewLemmasInTheOutputCheckBox.clicked.connect(
            self.includeSentencesWithNewLemmasInTheOutputCheckBox_Clicked)
        self.includeEvenSentencesWithoutNewLemmasInTheOutputCheckBox.clicked.connect(
            self.includeEvenSentencesWithoutNewLemmasInTheOutputCheckBox_Clicked)
        self.wholeTextModeRadioButton.clicked.connect(self.wholeTextModeRadioButton_Clicked)

        # UC #02
        self.lookUpTranscriptionsAndTranslationsRadioButton.clicked.connect(
            self.lookUpTranscriptionsAndTranslationsRadioButton_Clicked)

        # UC #03
        self.processManuallySplitComplexWordsRadioButton.clicked.connect(
            self.processManuallySplitComplexWordsRadioButton_Clicked)

        # UC #04
        self.checkConsistencyOfAllVocabFilesRadioButton.clicked.connect(
            self.checkConsistencyOfAllVocabFilesRadioButton_Clicked)

        # UC #05
        self.printable3ColVersionOfLastVocabFileComposerRadioButton.clicked.connect(
            self.printable3ColVersionOfLastVocabFileComposerRadioButton_Clicked)

        # UC #06
        self.vocabFileAgainstPortraitFileValidatorRadioButton.clicked.connect(
            self.vocabFileAgainstPortraitFileValidatorRadioButton_Clicked)

        for option in VocabFileComboBoxEnum:
            # combo_box.addItem("Отображаемое значение 1", реальное_значение)
            # addItem(text, userData) добавляет в lookup текст опции и связанный с ней пользовательский объект
            self.vocabFileComboBox.addItem(option.value, option)  # передаём сам enum в userData
        self.vocabFileComboBox.currentIndexChanged.connect(self.vocabFileComboBox_selection_changed)

        self.portraitFileComboBox.currentIndexChanged.connect(self.portraitFileComboBox_selection_changed)

        # UC #07
        self.unsentencedVersionOfLastVocabFileForAnkiMakerRadioButton.clicked.connect(
            self.unsentencedVersionOfLastVocabFileForAnkiMakerRadioButton_Clicked)

        # UC #08
        self.duplicatesAfterImportToAnkiRevealerRadioButton.clicked.connect(
            self.duplicatesAfterImportToAnkiRevealerRadioButton_Clicked)

        # UC #09.1
        self.validateGermanInflectionsXlsRadioButton.clicked.connect(
            self.validateGermanInflectionsXlsRadioButton_Clicked)

        # UC #09.2
        self.validateAllVocabFilesSentencesHaveCorrectTranscriptionsRadioButton.clicked.connect(
            self.validateAllVocabFilesSentencesHaveCorrectTranscriptionsRadioButton_Clicked)

        # UC #10
        self.performMorphologicalAnalysisRadioButton.clicked.connect(
            self.performMorphologicalAnalysisRadioButton_Clicked)

        self.displayTokenLemmaPosMorphRadioButton.clicked.connect(self.displayTokenLemmaPosMorphRadioButton_Clicked)

        # Настройка кнопок
        self.processButton.clicked.connect(self.processButton_Clicked)
        self.forceReReadExternalSourcesButton.clicked.connect(self.forceReReadExternalSourcesButton_Clicked)

        # Инициализация Apex-сервисов
        # вкладка "morph_dict"
        self.md1_MorphDictWithoutLemmasMaker = None
        self.md2_LlmLemmasIntoMorphDictIntegrator = None
        # вкладка "Main"
        self.a000_MorphDictGeneratorAndToFileSaver = None
        self.a010_NewLemmasFinder = None
        self.a020_TranscriptionsAndTranslationsLookUpper = None
        self.a030_SplitComplexWordsProcessor = None
        self.a040_VocabFilesConsistencyChecker = None
        self.a050_Printable3ColVersionOfLastVocabFileComposer = None
        self.a060_VocabFileAgainstPortraitFileValidator = None
        self.a070_UnsentencedVersionOfLastVocabFileForAnkiMaker = None
        self.a080_DuplicatesAfterImportToAnkiRevealer = None
        self.a091_GermanInflectionsXlsValidator = None
        self.a092_SentenceTranscriptionValidator = None
        self.a100_GermanTextMorphologicalAnalysisPerformer = None

        # Инициализация бизнес-сервисов
        self.tokenLemmaPosMorphDisplayer = None
        self.inputTextFromGuiPreprocessor = InputTextFromGuiPreprocessor()

        # Window title
        # main_window_title = Validator.validate_excel1st_col_words_uniqueness()
        self.set_word_count_in_main_window_title()

    # Переопределяем данный метод, чтобы форма открывалась ровно по центру окна (как по вертикали, так и по горизонтали)
    def showEvent(self, event):
        super().showEvent(event)
        self.centerWindow()

    def centerWindow(self):
        frameGm = self.frameGeometry()
        screen = self.screen().availableGeometry().center()
        frameGm.moveCenter(screen)
        self.move(frameGm.topLeft())

    def switch_language(self):
        # .currentText() — используется когда нужен именно текст, отображаемый на UI.
        # .currentData() — используется когда нужен внутренний объект, связанный с отображаемым текстом (например,
        # enum, идентификатор, код).
        current_language = self.currentLanguageComboBox.currentText()
        AppContext.switch_language(current_language)
        # base_dir = AppContext.get_base_dir()
        # print(base_dir)
        self.set_word_count_in_main_window_title()

        self.fill_portraitFileComboBox()

        # Сбрасываем все Apex-сервисы, чтобы они переинициализировались, когда к ним будет происходить обращение
        # вкладка "morph_dict"
        self.md1_MorphDictWithoutLemmasMaker = None
        self.md2_LlmLemmasIntoMorphDictIntegrator = None
        # вкладка "Main"
        self.a000_MorphDictGeneratorAndToFileSaver = None
        self.a010_NewLemmasFinder = None
        self.a020_TranscriptionsAndTranslationsLookUpper = None
        self.a030_SplitComplexWordsProcessor = None
        self.a040_VocabFilesConsistencyChecker = None
        self.a050_Printable3ColVersionOfLastVocabFileComposer = None
        self.a060_VocabFileAgainstPortraitFileValidator = None
        self.a070_UnsentencedVersionOfLastVocabFileForAnkiMaker = None
        self.a080_DuplicatesAfterImportToAnkiRevealer = None
        self.a091_GermanInflectionsXlsValidator = None
        self.a092_SentenceTranscriptionValidator = None
        self.a100_GermanTextMorphologicalAnalysisPerformer = None

    # Активируем/деактивируем wholeTextModeRadioButton в зависимости от стартового значения в morphDictPolicyComboBox
    def update_wholeTextModeRadioButton_state(self):
        # .currentText() — используется когда нужен именно текст, отображаемый на UI.
        # .currentData() — используется когда нужен внутренний объект, связанный с отображаемым текстом (например,
        # enum, идентификатор, код).
        current_morph_dict_policy = self.morphDictPolicyComboBox.currentData()
        if current_morph_dict_policy == MorphDictPolicyComboBoxEnum.READ_MORPH_DICT_FROM_LAST_FILE:
            self.wholeTextModeRadioButton.setEnabled(False)
        elif current_morph_dict_policy == MorphDictPolicyComboBoxEnum.GENERATE_MORPH_DICT_ON_THE_FLY:
            self.wholeTextModeRadioButton.setEnabled(True)
        else:
            raise Exception(f'Unknown morphDictPolicyComboBox value: {current_morph_dict_policy}')

    def fill_portraitFileComboBox(self):
        # Очищаем лукап от предыдущих значений (это важно при переключении с одного иностранного языка на другой)
        self.portraitFileComboBox.clear()

        # Добавляем в лукап фиксированные значения из enum
        for option in PortraitFileComboBoxEnum:
            # combo_box.addItem("Отображаемое значение 1", реальное_значение)
            # addItem(text, userData) добавляет в lookup текст опции и связанный с ней пользовательский объект
            self.portraitFileComboBox.addItem(option.value, option)  # передаём сам enum в userData

        # В данном лукапе вводим разграничение на "display_value" и "real_value".
        # Пути к файлам слишком длинные, поэтому отображаем только их бизнес-значащую часть, а настоящие значения
        # путей храним в "real_value".
        # filenameUtils должен быть инициализирован только после выбора языка, т. е. ниже по коду, чем currentLanguageComboBox
        filenameUtils = FilenameUtils()
        portrait_filenames = filenameUtils.get_all_portrait_filenames()
        for portrait_filename in portrait_filenames:
            # self.combo_box.addItem("Отображаемое значение 1", реальное_значение)
            display_value = self._get_display_value_of_filename(portrait_filename)
            real_value = portrait_filename
            self.portraitFileComboBox.addItem(display_value, real_value)

    def _get_display_value_of_filename(self, full_path_str):
        pattern = r'\\(?:A1|A2|B1)\\'  # захватывает папки '\A1\', '\A2\' или '\B1\'
        match = re.search(pattern, full_path_str)  # ищет первое вхождение
        if match:
            display_value = full_path_str[match.start():]
        else:
            display_value = full_path_str

        return display_value

    def set_word_count_in_main_window_title(self):
        # ссылку на сервис каждый раз записываем в локальную переменную, но не в поле класса
        odtFilesService = OdtFilesService()
        main_window_title = odtFilesService.get_word_count_for_gui_title()
        self.setWindowTitle(main_window_title)

    async def clear_output_text_edit(self):
        self.outputTextEdit.clear()
        await asyncio.sleep(0)  # Не блокируем основной поток

    @asyncSlot()  # для работы данной аннотации необходимо установить библиотеку qasync
    async def processButton_Clicked(self):

        # При каждом нажатии на кнопку "Process" обновляем счётчики Vocab-файлов и слов в заголовке окна, чтобы
        # информация, отображаемая там, была максимально актуальной!
        self.set_word_count_in_main_window_title()

        # асинхронно очищаем поле вывода от результатов предыдущей работы
        await self.clear_output_text_edit()

        input_text_as_plain_text = self.inputTextFromGuiPreprocessor.preprocess(self.inputTextEdit.toPlainText())
        # input_text_as_html = self.inputTextEdit.toHtml()
        output_text = ''
        current_tab = self.tabWidget.tabText(self.tabWidget.currentIndex())

        try:
            if current_tab == "morph_dict":
                if self.makeMorphDictRadioButton.isChecked():
                    if self.md1_MorphDictWithoutLemmasMaker is None:
                        self.md1_MorphDictWithoutLemmasMaker = BusinessObjectFactory.create_md1_MorphDictWithoutLemmasMaker()
                    output_text = self.md1_MorphDictWithoutLemmasMaker.process(input_text_as_plain_text)
                elif self.integrateLlmLemmasIntoMorphDictRadioButton.isChecked():
                    if self.md2_LlmLemmasIntoMorphDictIntegrator is None:
                        self.md2_LlmLemmasIntoMorphDictIntegrator = MD2_LlmLemmasIntoMorphDictIntegrator()
                    output_text = self.md2_LlmLemmasIntoMorphDictIntegrator.integrate_llm_lemmas_into_orig_dict(input_text_as_plain_text)

            elif current_tab == "Main":
                # UC #00
                # if self.generateMorphDictAndSaveItToFileRadioButton.isChecked():
                #     if self.a000_MorphDictGeneratorAndToFileSaver is None:
                #         self.a000_MorphDictGeneratorAndToFileSaver = A000_MorphDictGeneratorAndToFileSaver()
                #     output_text = self.a000_MorphDictGeneratorAndToFileSaver.perform(input_text_as_plain_text)

                # UC #01
                if self.findNewLemmasRadioButton.isChecked():
                    if self.a010_NewLemmasFinder is None:
                        self.a010_NewLemmasFinder = BusinessObjectFactory.create_a010_NewLemmasFinder()

                    morph_dict_policy = self.morphDictPolicyComboBox.currentData()
                    morph_dict_policy_read_from_last_file_flag = morph_dict_policy == MorphDictPolicyComboBoxEnum.READ_MORPH_DICT_FROM_LAST_FILE
                    morph_dict_policy_generate_on_the_fly_flag = morph_dict_policy == MorphDictPolicyComboBoxEnum.GENERATE_MORPH_DICT_ON_THE_FLY

                    line_by_line_mode_radio_state = self.lineByLineModeRadioButton.isChecked()
                    include_sentences_with_new_lemmas_in_the_output_flag = self.includeSentencesWithNewLemmasInTheOutputCheckBox.isChecked()
                    include_even_sentences_without_new_lemmas_in_the_output_flag = self.includeEvenSentencesWithoutNewLemmasInTheOutputCheckBox.isChecked()
                    whole_text_mode_radio_state = self.wholeTextModeRadioButton.isChecked()

                    output_text = self.a010_NewLemmasFinder.find_new_lemmas(
                        input_text_as_plain_text,
                        morph_dict_policy_read_from_last_file=morph_dict_policy_read_from_last_file_flag,
                        morph_dict_policy_generate_on_the_fly=morph_dict_policy_generate_on_the_fly_flag,
                        line_by_line_mode=line_by_line_mode_radio_state,
                        include_sentences_with_new_lemmas_in_the_output=include_sentences_with_new_lemmas_in_the_output_flag,
                        include_even_sentences_without_new_lemmas_in_the_output=include_even_sentences_without_new_lemmas_in_the_output_flag,
                        whole_text_mode=whole_text_mode_radio_state)

                # UC #02
                elif self.lookUpTranscriptionsAndTranslationsRadioButton.isChecked():
                    if self.a020_TranscriptionsAndTranslationsLookUpper is None:
                        self.a020_TranscriptionsAndTranslationsLookUpper = A020_TranscriptionsAndTranslationsLookUpper()

                    # Если значения и их порядок фиксированы и не будут изменяться, использование индекса может быть проще
                    # и более надёжным: index = self.comboBox.currentIndex()
                    # Если значения могут изменяться, лучше ориентироваться на текст, чтобы избежать привязки к жёстким
                    # индексам: text = self.comboBox.currentText()
                    # combo_box_item_index = self.transcriptionsAndTranslationsComboBox.currentIndex()
                    # .currentText() — используется когда нужен именно текст, отображаемый на UI.
                    # .currentData() — используется когда нужен внутренний объект, связанный с отображаемым текстом (например,
                    # enum, идентификатор, код).
                    output_text = self.a020_TranscriptionsAndTranslationsLookUpper.look_up(input_text_as_plain_text)

                # UC #03
                elif self.processManuallySplitComplexWordsRadioButton.isChecked():
                    if self.a030_SplitComplexWordsProcessor is None:
                        self.a030_SplitComplexWordsProcessor = A030_SplitComplexWordsProcessor()

                    output_text = self.a030_SplitComplexWordsProcessor.process(input_text_as_plain_text)

                # UC #04
                elif self.checkConsistencyOfAllVocabFilesRadioButton.isChecked():
                    if self.a040_VocabFilesConsistencyChecker is None:
                        self.a040_VocabFilesConsistencyChecker = A040_VocabFilesConsistencyChecker()

                    output_text = self.a040_VocabFilesConsistencyChecker.check_consistency()

                # UC #05
                elif self.printable3ColVersionOfLastVocabFileComposerRadioButton.isChecked():
                    if self.a050_Printable3ColVersionOfLastVocabFileComposer is None:
                        self.a050_Printable3ColVersionOfLastVocabFileComposer = A050_Printable3ColVersionOfLastVocabFileComposer()

                    output_text = self.a050_Printable3ColVersionOfLastVocabFileComposer.compose_3col_version()

                # UC #06
                elif self.vocabFileAgainstPortraitFileValidatorRadioButton.isChecked():
                    if self.a060_VocabFileAgainstPortraitFileValidator is None:
                        self.a060_VocabFileAgainstPortraitFileValidator = A060_VocabFileAgainstPortraitFileValidator()

                    # .currentText() — используется когда нужен именно текст, отображаемый на UI.
                    # .currentData() — используется когда нужен внутренний объект, связанный с отображаемым текстом (например,
                    # enum, идентификатор, код).
                    vocab_option = self.vocabFileComboBox.currentText()
                    # portrait_option = self.portraitFileComboBox.currentText()
                    # Вызывать метод self.portraitFileComboBox.currentText() уже нельзя, т. к. лукап теперь хранит пары
                    # значений "displayValue - realValue" и для получения именно realValue нужно вызывать
                    # метод .currentData()
                    portrait_option = self.portraitFileComboBox.currentData()
                    output_text = self.a060_VocabFileAgainstPortraitFileValidator.validate(vocab_option, portrait_option)

                # UC #07
                elif self.unsentencedVersionOfLastVocabFileForAnkiMakerRadioButton.isChecked():
                    if self.a070_UnsentencedVersionOfLastVocabFileForAnkiMaker is None:
                        self.a070_UnsentencedVersionOfLastVocabFileForAnkiMaker = A070_UnsentencedVersionOfLastVocabFileForAnkiMaker()

                    output_text = self.a070_UnsentencedVersionOfLastVocabFileForAnkiMaker.print_vocabulary()

                # UC #08
                elif self.duplicatesAfterImportToAnkiRevealerRadioButton.isChecked():
                    if self.a080_DuplicatesAfterImportToAnkiRevealer is None:
                        self.a080_DuplicatesAfterImportToAnkiRevealer = A080_DuplicatesAfterImportToAnkiRevealer()

                    output_text = self.a080_DuplicatesAfterImportToAnkiRevealer.reveal_duplicates()

                # UC #09.1
                elif self.validateGermanInflectionsXlsRadioButton.isChecked():
                    if self.a091_GermanInflectionsXlsValidator is None:
                        self.a091_GermanInflectionsXlsValidator = A091_GermanInflectionsXlsValidator()

                    output_text = self.a091_GermanInflectionsXlsValidator.validate_oo_writer_words_are_present_in_excel()

                # UC #09.2
                elif self.validateAllVocabFilesSentencesHaveCorrectTranscriptionsRadioButton.isChecked():
                    if self.a092_SentenceTranscriptionValidator is None:
                        self.a092_SentenceTranscriptionValidator = A092_SentenceTranscriptionValidator()

                    output_text = self.a092_SentenceTranscriptionValidator.validate()

                # UC #10
                elif self.performMorphologicalAnalysisRadioButton.isChecked():
                    if self.a100_GermanTextMorphologicalAnalysisPerformer is None:
                        self.a100_GermanTextMorphologicalAnalysisPerformer = A100_GermanTextMorphologicalAnalysisPerformer()

                    output_text = self.a100_GermanTextMorphologicalAnalysisPerformer.process_german_text(
                        input_text_as_plain_text)

                elif self.displayTokenLemmaPosMorphRadioButton.isChecked():
                    if self.tokenLemmaPosMorphDisplayer is None:
                        self.tokenLemmaPosMorphDisplayer = TokenLemmaPosMorphDisplayer()

                    output_text = self.tokenLemmaPosMorphDisplayer.display(input_text_as_plain_text)

        # В первую очередь перехватываем более специфичный exception
        except URLError as e:
            # Проверка на WinError 10061: эта ошибка связана с попыткой вычитать данные из Anki, когда она не запущена.
            if '[WinError 10061]' in str(e):
                self.show_error_message("Please, start Anki!")
            else:
                self.show_error_message(str(e))
        except Exception as e:
            self.show_error_message(str(e))

        self.outputTextEdit.setText(output_text)

    def show_error_message(self, error_message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Error")
        # msg_box.setText(f"Exception:\n{error_message}")
        msg_box.setText(f"{error_message}")
        # msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def forceReReadExternalSourcesButton_Clicked(self):
        # UC #01
        if self.findNewLemmasRadioButton.isChecked():
            self.a010_NewLemmasFinder = None
        # UC #02
        elif self.lookUpTranscriptionsAndTranslationsRadioButton.isChecked():
            self.a020_TranscriptionsAndTranslationsLookUpper = None
        # UC #03
        elif self.processManuallySplitComplexWordsRadioButton.isChecked():
            self.a030_SplitComplexWordsProcessor = None
        # UC #04
        elif self.checkConsistencyOfAllVocabFilesRadioButton.isChecked():
            self.a040_VocabFilesConsistencyChecker = None
        # UC #05
        elif self.printable3ColVersionOfLastVocabFileComposerRadioButton.isChecked():
            self.a050_Printable3ColVersionOfLastVocabFileComposer = None
        # UC #06
        elif self.vocabFileAgainstPortraitFileValidatorRadioButton.isChecked():
            self.a060_VocabFileAgainstPortraitFileValidator = None
        # UC #07
        elif self.unsentencedVersionOfLastVocabFileForAnkiMakerRadioButton.isChecked():
            self.a070_UnsentencedVersionOfLastVocabFileForAnkiMaker = None
        # UC #08
        elif self.duplicatesAfterImportToAnkiRevealerRadioButton.isChecked():
            self.a080_DuplicatesAfterImportToAnkiRevealer = None
        # UC #09.1
        elif self.validateGermanInflectionsXlsRadioButton.isChecked():
            self.a091_GermanInflectionsXlsValidator = None
        # UC #09.2
        elif self.validateAllVocabFilesSentencesHaveCorrectTranscriptionsRadioButton.isChecked():
            self.a092_SentenceTranscriptionValidator = None
        # UC #10
        elif self.performMorphologicalAnalysisRadioButton.isChecked():
            self.a100_GermanTextMorphologicalAnalysisPerformer = None

    # **********************

    # UC #00
    # def generateMorphDictAndSaveItToFileRadioButton_Clicked(self):
    #     # self.dashSeparatorCheckBox.setEnabled(True)
    #     self.inputTextEdit.setPlaceholderText('')
    #     self.forceReReadExternalSourcesButton.setEnabled(True)

    # UC #01
    def morphDictPolicyComboBox_selection_changed(self, index):
        self.update_wholeTextModeRadioButton_state()

    def findNewLemmasRadioButton_Clicked(self):
        # self.dashSeparatorCheckBox.setEnabled(True)
        self.inputTextEdit.clear()
        self.inputTextEdit.setPlaceholderText('')
        self.forceReReadExternalSourcesButton.setEnabled(True)

    def lineByLineModeRadioButton_Clicked(self):
        self.includeSentencesWithNewLemmasInTheOutputCheckBox.setEnabled(True)
        self.includeEvenSentencesWithoutNewLemmasInTheOutputCheckBox.setEnabled(True)

    def includeSentencesWithNewLemmasInTheOutputCheckBox_Clicked(self):
        # self.dashSeparatorCheckBox.setEnabled(True)
        self.forceReReadExternalSourcesButton.setEnabled(True)

        # Если 1-я галка включена, то и 2-я галка активна (не обязательно включена, но доступна для работы!)
        if self.includeSentencesWithNewLemmasInTheOutputCheckBox.isChecked():
            self.includeEvenSentencesWithoutNewLemmasInTheOutputCheckBox.setEnabled(True)
        # в противном случае со снятием 1-й галки должна отключаться и деактивироваться и 2-я галка, иначе создаётся
        # абсурдная ситуация, когда предложения, даже потенциально имеющие новые леммы, мы не включаем в результирующий
        # набор, тогда как опция для предложений таковых лемм точно не имеющих продолжает работать...
        else:
            self.includeEvenSentencesWithoutNewLemmasInTheOutputCheckBox.setEnabled(False)
            self.includeEvenSentencesWithoutNewLemmasInTheOutputCheckBox.setChecked(False)

    def includeEvenSentencesWithoutNewLemmasInTheOutputCheckBox_Clicked(self):
        # self.dashSeparatorCheckBox.setEnabled(True)
        self.forceReReadExternalSourcesButton.setEnabled(True)

    def wholeTextModeRadioButton_Clicked(self):
        self.includeSentencesWithNewLemmasInTheOutputCheckBox.setEnabled(False)
        self.includeEvenSentencesWithoutNewLemmasInTheOutputCheckBox.setEnabled(False)

    # Именно здесь происходит глобальное переключение контекста между разными языками (пути к папкам,
    # названия Анки-деков и т. д.)
    def currentLanguageComboBox_selection_changed(self, index):
        self.switch_language()

    # UC #02
    def lookUpTranscriptionsAndTranslationsRadioButton_Clicked(self):
        # self.dashSeparatorCheckBox.setEnabled(True)
        # self.forceReReadExternalSourcesButton.setEnabled(True)
        self.inputTextEdit.setPlaceholderText('')

    # def transcriptionsAndTranslationsComboBox_selection_changed(self, index):
    #     # selected_option = self.comboBox.itemText(index)
    #     # print(f"Selected option: {selected_option}")
    #     self.forceReReadExternalSourcesButton.setEnabled(True)

    # UC #03
    def processManuallySplitComplexWordsRadioButton_Clicked(self):
        # self.dashSeparatorCheckBox.setEnabled(True)
        placeholder_text = """Пример входного текста:

Wort
gruppen
liste
Wortgruppenliste

ab-
geben
abgeben"""
        self.inputTextEdit.setPlaceholderText(placeholder_text)
        # self.forceReReadExternalSourcesButton.setEnabled(True)

    # UC #04
    def checkConsistencyOfAllVocabFilesRadioButton_Clicked(self):
        # self.dashSeparatorCheckBox.setEnabled(False)
        # self.forceReReadExternalSourcesButton.setEnabled(False)
        self.inputTextEdit.setPlaceholderText('')

    # UC #05
    def printable3ColVersionOfLastVocabFileComposerRadioButton_Clicked(self):
        self.inputTextEdit.setPlaceholderText('')

    # UC #06
    def vocabFileAgainstPortraitFileValidatorRadioButton_Clicked(self):
        self.inputTextEdit.setPlaceholderText('')

    def vocabFileComboBox_selection_changed(self, index):
        # selected_option = self.comboBox.itemText(index)
        # print(f"Selected option: {selected_option}")
        self.forceReReadExternalSourcesButton.setEnabled(True)

    def portraitFileComboBox_selection_changed(self, index):
        # selected_option = self.comboBox.itemText(index)
        # print(f"Selected option: {selected_option}")
        self.forceReReadExternalSourcesButton.setEnabled(True)

        # Получение реального значения при изменении выбора
        # real_value = self.portraitFileComboBox.currentData()
        # print(f"Выбрано: {real_value}")

    # UC #07
    def unsentencedVersionOfLastVocabFileForAnkiMakerRadioButton_Clicked(self):
        self.inputTextEdit.setPlaceholderText('')

    # UC #08
    def duplicatesAfterImportToAnkiRevealerRadioButton_Clicked(self):
        self.inputTextEdit.setPlaceholderText('')

    # UC #09.1
    def validateGermanInflectionsXlsRadioButton_Clicked(self):
        # self.dashSeparatorCheckBox.setEnabled(True)
        # self.forceReReadExternalSourcesButton.setEnabled(True)
        self.inputTextEdit.setPlaceholderText('')

    # UC #09.2
    def validateAllVocabFilesSentencesHaveCorrectTranscriptionsRadioButton_Clicked(self):
        # self.dashSeparatorCheckBox.setEnabled(True)
        # self.forceReReadExternalSourcesButton.setEnabled(True)
        self.inputTextEdit.setPlaceholderText('')

    # UC #10
    def performMorphologicalAnalysisRadioButton_Clicked(self):
        # self.dashSeparatorCheckBox.setEnabled(True)
        # self.forceReReadExternalSourcesButton.setEnabled(True)
        self.inputTextEdit.setPlaceholderText('')

    def displayTokenLemmaPosMorphRadioButton_Clicked(self):
        # self.dashSeparatorCheckBox.setEnabled(True)
        # self.forceReReadExternalSourcesButton.setEnabled(True)
        self.inputTextEdit.setPlaceholderText('')


def run():
    app = QApplication(sys.argv)
    loop = QEventLoop(app)  # это класс именно сторонней библиотеки qasync, а не PyQt6
    asyncio.set_event_loop(loop)

    view = View()
    view.show()
    view.inputTextEdit.setFocus()  # place cursor into this field upon app startup

    with loop:
        loop.run_forever()

    # sys.exit(app.exec())

# if __name__ == '__main__':
#     run()
