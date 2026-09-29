import re

from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.text import P
from pathlib import Path

from T0_TranscriptionProcessorsController import T0_TranscriptionProcessorsController
from TranscriptionAspirationService import TranscriptionAspirationService

# input_filename = r"/test.odt"
# output_filename = r"/test1.odt"

current_dir = Path(__file__).parent.resolve()  # папка, в которой находится данный скрипт


# Класс для модификации столбца с транскрипциями в ODT-файле.
# Запускает логику добавления аспирации для всего содержимого столбца транскрипций.
# Данный класс понадобился в конце курса А1, когда было принято решение добавить задним числом аспирацию всем словам и
# предложениям курса, т. е. единоразово сделать то, что должно было быть неотъемлемой частью процесса с самого начала.
# Поэтому данный класс является одноразовой утилитой, а не неотъемлемой частью бизнес-процесса.
class TextReplacerInOdtFile:
    def __init__(self):
        # self.transcriptionAspirationService = TranscriptionAspirationService()
        self.t0_TranscriptionProcessorsController = T0_TranscriptionProcessorsController()
        self.lang = 'deu'  # 'eng', 'ita'

    def replace_in_odt_files(self):

        input_filenames = [fr"{current_dir}\test.odt"]

        # Case #1.
        # input_filenames = FilenameUtils.get_all_vocab_filenames()
        # input_filenames = FilenameUtils.get_all_portrait_filenames()

        # Case #2. Manual list of Vocab-files
        # input_filenames = [
        #     fr'{goethe_institut_dir}\A1\Aa\[Vocab] Aa.odt',
        #     fr'{goethe_institut_dir}\A1\Bb\[Vocab] Bb.odt',
        #     fr'{goethe_institut_dir}\A1\Cc-Dd\[Vocab] Cc-Dd.odt',
        #     fr'{goethe_institut_dir}\A1\Ee\[Vocab] Ee.odt',
        #     fr'{goethe_institut_dir}\A1\Ff\[Vocab] Ff.odt',
        #     fr'{goethe_institut_dir}\A1\Gg\[Vocab] Gg.odt',
        #     fr'{goethe_institut_dir}\A1\Hh-Jj\[Vocab] Hh-Jj.odt',
        #     fr'{goethe_institut_dir}\A1\Kk\[Vocab] Kk.odt',
        #     fr'{goethe_institut_dir}\A1\Ll-Mm\[Vocab] Ll-Mm.odt',
        #     fr'{goethe_institut_dir}\A1\Nn-Rr\[Vocab] Nn-Rr.odt',
        #     fr'{goethe_institut_dir}\A1\Ss\[Vocab] Ss.odt',
        #     fr'{goethe_institut_dir}\A1\[Vocab] Tt-Vv.odt',
        #     fr'{goethe_institut_dir}\A1\[Vocab] Ww-Zz.odt'
        # ]

        # Case #3
        # input_filenames = [
        #     fr'{goethe_institut_dir}\A1\[Vocab] Ww-Zz.odt',
        #     fr'{goethe_institut_dir}\A1\Ww-Zz (portrait).odt',
        # ]

        for input_filename in input_filenames:
            # Добавляем цифру 1 к имени выходного файла, чтобы отличать его от исходного файла.
            # Замена производится гарантированно с конца строки и 1 раз.
            output_filename = re.sub(r'\.odt$', r'_new.odt', input_filename, count=1)
            # output_filename = input_filename
            # print(output_filename)
            self._replace_in_single_file(input_filename, output_filename)

        return

    def _replace_in_single_file(self, input_filename, output_filename):
        # Загрузка ODT-файла
        doc = load(input_filename)

        tables = doc.getElementsByType(Table)
        for table in tables:
            rows = table.getElementsByType(TableRow)
            for row in rows:
                cells = row.getElementsByType(TableCell)

                # Берём в работу только ячейку с транскрипцией
                if len(cells) == 3:  # если имеем дело с 3-столбцовым portrait-файлом
                    transcription_cell = cells[1]
                elif len(cells) == 5:  # если имеем дело с 5-столбцовым Vocab-файлом
                    transcription_cell = cells[2]

                # Получаем все абзацы ячейки с транскрипцией
                paragraphs = transcription_cell.getElementsByType(P)
                # Для каждого абзаца вызываем функцию, которая производит замену в тексте этого абзаца, работая с
                # рекурсивно вложенными в него элементами (кот. появляются в рез-те форматирования текста жирным,
                # курсивом, выделения текста цветом или маркером и т. д.)
                for paragraph in paragraphs:
                    # передаём на обработку сам абзац и callback его обработки
                    # self.replace_in_paragraph_recursively(paragraph, self.transcriptionAspirationService.aspirate)
                    self.replace_in_paragraph_recursively(paragraph)

        # Сохранение нового ODT-файла.
        # Из получившегося .odt-файла (например, Vocab-файла) можно целиком копировать столбец с аспирированными
        # транскрипциями и вставлять в другой файл (например, portrait-файл).
        doc.save(output_filename)

    def replace_in_paragraph_recursively(self, paragraph):
        for node in paragraph.childNodes:
            # Если узел является текстовым, производим замены в тексте этого узла
            if node.nodeType == node.TEXT_NODE:
                # node.data = processing_cb(node.data)
                node.data = self.t0_TranscriptionProcessorsController.find_in_text_bracketed_transcriptions_and_process_them(node.data, self.lang)
            # иначе если узел содержит другие узлы, обрабатываем их рекурсивно
            elif node.nodeType == node.ELEMENT_NODE:
                self.replace_in_paragraph_recursively(node)
        return


##################################################

if __name__ == '__main__':
    textReplacerInOdtFile = TextReplacerInOdtFile()
    textReplacerInOdtFile.replace_in_odt_files()
