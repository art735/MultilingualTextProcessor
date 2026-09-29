import sys

from PyQt6 import QtWidgets
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication

import EnglishTextTranscriber
import EnglishValidator
import ExcelDaoEnglishDictionary
import ExcelDaoEnglishVocabulary
# Для того, чтобы сделать радио-переключатели 'по ширине' - выделить самый левый radio-переключатель
# и в Object Inspector в разделе Size Policy экспериментировать с вариантами опции 'Horizontal Policy' (она по умолчанию fixed)
import OxfordTranscriptionService
import StatisticsCounter
import WordLookupService


class View(QtWidgets.QMainWindow):
    def __init__(self):
        super(QtWidgets.QMainWindow, self).__init__()
        ### User code ###
        uic.loadUi("D1_ViewController/View.ui", self)

        # временно сместил дифолтный фокус на другую радио-кнопку
        # self.textTranscriberModeRadioButton.setChecked(True)
        self.oxfordTranscriptionLookup.setChecked(True)

        # при щелчке на радио-кнопку ставить фокус в поле ввода
        self.textTranscriberModeRadioButton.clicked.connect(self.radioButton_Clicked)
        self.wordLookupModeRadioButton.clicked.connect(self.radioButton_Clicked)
        self.textStatisticsModeRadioButton.clicked.connect(self.radioButton_Clicked)
        self.oxfordTranscriptionLookup.clicked.connect(self.radioButton_Clicked)

        self.processButton.clicked.connect(self.processButton_Clicked)
        self.reloadDataFromExcelButton.clicked.connect(self.reloadDataFromExcelButton_Clicked)

        # Validation
        EnglishValidator.validate_englishDictionary_uniqueness()
        EnglishValidator.validate_englishVocabulary_uniqueness(
            'EnglishVocabulary.xls')  # TODO подставлять имя в зависимости от выбранного в лукапе профиля

    def radioButton_Clicked(self):
        self.inputTextEdit.setFocus()  # place cursor into this field upon app startup

    def clearOutputPane(self):
        # self.outputTextEdit.setText("")
        self.outputTextEdit.clear()

    def processButton_Clicked(self):
        self.clearOutputPane()  # очистка output-поля на GUI от результатов предыдущей работы
        QApplication.processEvents()  # без данной строчки output-поля не срабатывает!

        input_text = self.inputTextEdit.toPlainText()

        output_text = ''
        if self.textTranscriberModeRadioButton.isChecked():
            output_text = EnglishTextTranscriber.transcribeWholeText(input_text, False)
        elif self.wordLookupModeRadioButton.isChecked():
            output_text = WordLookupService.look_up(input_text)
        elif self.textStatisticsModeRadioButton.isChecked():
            output_text = StatisticsCounter.count(input_text)
        elif self.oxfordTranscriptionLookup.isChecked():
            output_text = OxfordTranscriptionService.look_up(input_text)

        self.outputTextEdit.setText(output_text)

    def reloadDataFromExcelButton_Clicked(self):
        ExcelDaoEnglishDictionary.reloadDataFromExcel()
        ExcelDaoEnglishVocabulary.reloadDataFromExcel()
        self.processButton_Clicked()


#####################################################################################

def run():
    # if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    # создание экземпляра пользовательского класса и вызов его метода
    view = View()
    view.show()
    view.inputTextEdit.setFocus()  # place cursor into this field upon app startup

    sys.exit(app.exec())
