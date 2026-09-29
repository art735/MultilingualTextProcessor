import Utils
from GermanExcelWorkbooksDao import GermanExcelWorkbooksDao


# Формирует window title для GUI
class MainGuiWindowTitleService:
    def __init__(self):
        self.germanExcelWorkbooksDao = GermanExcelWorkbooksDao()

    def get_window_title(self):
        no_of_words_per_excel_book = []

        # key: excel_filename
        # value: list of 1st column words
        # Хоть метод и возвращает список слов для валидации, в данном случае к валидации данная логика отношения
        # не имеет. Здесь это просто информация о количестве слов в Excel-файлах в статистических целях.
        words_per_excel_book_dict = self.germanExcelWorkbooksDao.get_excel_words_for_validation()

        for excel_book_words in words_per_excel_book_dict.values():
            excel_book_words_size = len(
                Utils.subtract_lists(excel_book_words, GermanExcelWorkbooksDao.validation_ignore_words))
            no_of_words_per_excel_book.append(excel_book_words_size)

        # f'{value:,}' (print value using commas as thousand separators)
        output = ' + '.join([f'{s:,}'.format(s) for s in no_of_words_per_excel_book])
        output += ' = '
        total_words = sum(no_of_words_per_excel_book)
        output += f'{total_words:,}'.format(total_words)

        # main_window_title = 'Deutsch Processor (vocabulary contains {} words)'.format(output)
        main_window_title = 'Deutsch Processor ({} words)'.format(output)
        # print(main_window_title)

        return main_window_title


#############################################################

if __name__ == '__main__':
    mainGuiWindowTitleService = MainGuiWindowTitleService()
    window_title = mainGuiWindowTitleService.get_window_title()
    print(window_title)
