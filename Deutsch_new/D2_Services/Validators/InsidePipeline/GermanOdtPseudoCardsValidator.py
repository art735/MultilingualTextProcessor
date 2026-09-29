from AnkiRegularCardsValidator import AnkiRegularCardsValidator
from OdtFileTableDao import TableRowsToAnkiCardsMode, OdtFileTableDao


class GermanOdtPseudoCardsValidator:
    error_msg = "Inconsistent words {0} (in 'Transcription' and 'Back' fields):\n\n{1}"

    def __init__(self, all_files_but_last_cards, last_file_cards):
        self.all_files_but_last_cards = all_files_but_last_cards
        self.last_file_cards = last_file_cards

    def validate(self, should_split_by_space_flag):
        output_lack_and_excess = self.validate_lack_and_excess(should_split_by_space_flag)

        output_consistency = self.validate_consistency()
        if output_consistency:
            output_consistency = self.error_msg.format("among [Vocab]-files' pseudo cards", output_consistency)

        # Формирование результирующего вывода по всем категориям
        pseudo_cards_output = '\n\n* * *\n\n'.join([out for out in [output_lack_and_excess, output_consistency] if out])
        return pseudo_cards_output

    # Сначала валидируем всю получившуюся коллекцию псевдо-Анки-карточек ЦЕЛИКОМ (без учёта последовательности строк
    # в таблице .odt-файла). Данный подход хорош тем, что выведет сразу все ошибки как со стороны lack,
    # так и со стороны excess, и исправление этих ошибок решит многие проблемы валидации.
    # Но в то же время успешное прохождение "валидации целиком" не означает полное отсутствие ошибок: количественно
    # строки могут соответствовать критериям консистентности, но качественно идти не в том порядке, в котором это было
    # бы естественно и логично. Поэтому второй пункт валидации на этом шаге заключается в том, чтобы взять
    # все строки из предыдущих файлов и поочерёдно добавлять к ним всё возрастающие срезы строк последнего файла и
    # следить за тем, чтобы валидация на каждом таком шажке была успешной!
    # На втором шаге невозможно нарушение валидации с excess-стороны, т. к. первый шаг полностью закрывает эту проблему.
    # На втором шаге возможно только нарушение валидации с lack-стороны, т. к. отдельные слова мультиполосных карточек
    # могут по ошибке следовать ПОСЛЕ мультиполосных карточек, использующих эти слова.
    # Q: Надо ли прибавлять слайсы к карточкам ВСЕХ ПРЕДЫДУЩИХ VOCAB-ФАЙЛОВ, или достаточно только к карточкам
    # последнего VOCAB-ФАЙЛА?
    # A: Да, к сожалению, нужно добавлять слайсы ко всем предыдущим карточкам!, но делать это нужно только для
    #  составных (мульти-полосных слов), т. к. прогонка однополосных слов в таком режиме ничего нового не даёт, а только
    #  занимает существенные ресурсы и время!
    def validate_lack_and_excess(self, should_split_by_space_flag):

        output1_interlinear_consistency = ''  # interlinear_consistency - "межстрочная согласованность"

        # Step 1.1 Валидируем целиком
        ankiRegularCardsValidator = AnkiRegularCardsValidator(self.all_files_but_last_cards + self.last_file_cards)
        # TODO: может сделать флажок как checkBox на UI ???
        lack_results_set, excess_results_set, printable_output = \
            ankiRegularCardsValidator.find_regular_cards_lack_and_excess_sets(should_split_by_space_flag)
        # Если обнаружены ошибки, возвращаем текстовый отчёт по ним и завершаем работу метода
        if lack_results_set or excess_results_set:
            return printable_output.strip()  # удаляет символы [ \t\n\r\f\v] в начале и конце строки

        # Step 1.2 Валидируем строку за строкой
        for i in range(0, len(self.last_file_cards)):
            # Поскольку Vocab-файлы создаются пользователем не сразу, а постепенно в процессе работы над словами и
            # предложениями, то предполагается, что для всех [Vocab]-файлов, кроме последнего, такая валидация уже
            # запускалась. Поэтому делаем поочерёдные слайсы строк только для последнего [Vocab]-файла.
            # При чём делаем слайс только если карточка многополосная, потому что именно составные части-полосы
            # многополосной карточки нуждаются в валидации, а однополосные карточки на lack/excess уже и так проверены
            # на шаге 1.1.
            if self.last_file_cards[i].is_card_multi_striped():
                last_file_rows_slice = self.last_file_cards[:i + 1]
                ankiRegularCardsValidator = AnkiRegularCardsValidator(
                    self.all_files_but_last_cards + last_file_rows_slice)
                lack_results_set, excess_results_set, printable_output = \
                    ankiRegularCardsValidator.find_regular_cards_lack_and_excess_sets(should_split_by_space_flag)
                if lack_results_set or excess_results_set:
                    # При обнаружении первой же проблемы завершаем цикл, т. к. дальше проверять смысла нет, пока
                    # эта проблема неконсистентности не будет исправлена.
                    return printable_output.strip()  # удаляет символы [ \t\n\r\f\v] в начале и конце строки

        return output1_interlinear_consistency

    def validate_consistency(self):
        ankiRegularCardsValidator = AnkiRegularCardsValidator(self.all_files_but_last_cards + self.last_file_cards)
        result = ankiRegularCardsValidator.find_inconsistent_translations_of_the_same_word()
        return result


##############################################################

if __name__ == '__main__':
    # Вычитываем псевдо-карточки
    odtFileTableDao = OdtFileTableDao()
    all_files_but_last_cards = odtFileTableDao.convert_table_rows_to_anki_cards(
        vocab_files=TableRowsToAnkiCardsMode.ALL_FILES_BUT_LAST, read_words=True, read_sentences=True)
    last_file_cards = odtFileTableDao.convert_table_rows_to_anki_cards(
        vocab_files=TableRowsToAnkiCardsMode.LAST_FILE, read_words=True, read_sentences=True)

    germanOdtPseudoCardsValidator = GermanOdtPseudoCardsValidator(all_files_but_last_cards, last_file_cards)

    res = germanOdtPseudoCardsValidator.validate(should_split_by_space_flag=False)
    if not res:
        res = 'ok'
    print(res)
