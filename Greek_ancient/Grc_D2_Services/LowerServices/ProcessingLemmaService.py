import GrcRegExFinder
import S1_TextLemmasFinder
from GrcConstants import NEWLINE, PIPE
from GrcRegExFinder import GrcRegExFinder
from ProcessingLemmaEntity import ProcessingLemmaEntity

NUMBER_OF_PIPED_ELEMENTS_IN_A_LINE = 4


class ProcessingLemmaService:

    def __init__(self):
        self.entities: list[ProcessingLemmaEntity] = list()

        error_msg = f'\n- - -\nНеправильный формат следующих строк.' \
                    f' Каждая строка должна содержать ровно {NUMBER_OF_PIPED_ELEMENTS_IN_A_LINE}' \
                    f' правильно отформатированных элемента, разделённых знаком "|":'
        self.incorrectly_formatted_lines = [error_msg]
        self.grcRegExFinder = GrcRegExFinder()

    def parse_input_lines(self, input_lines):
        # взять в дальнейшую работу только непустые строки, содержащие PIPE (pipe является разделителем в строках
        # с леммами, а те строки, в которых его нет, - декоративные строки для удобства чтения
        lines = [line for line in input_lines.split(NEWLINE) if len(line) and PIPE in line]
        for line in lines:
            # лемма - это предпоследний элемент из строки вида: 1|ἰησοῦ|ἰησοῦς|100%
            if self._is_line_format_correct(line):
                line_pieces = [lp.strip() for lp in line.split(PIPE)]

                counter = line_pieces[0]
                token = line_pieces[1]
                lemma = line_pieces[2]
                verdict = line_pieces[3]

                # counter по бизнес-процессу является первым параметром, но технически из-за механизма перегрузки
                # конструктора его пришлось сделать последним (необязательным) параметром и по-другому никак
                entity = ProcessingLemmaEntity(token, lemma, verdict, counter)
                self.entities.append(entity)
            else:
                self.incorrectly_formatted_lines.append(line)

        # Удаляем заголовок таблицы, кот. был сгенерирован на 1-м этапе.
        # По форме он, конечно, является "некорректно отформатированной строкой",
        # но по смыслу он не имеет к этой категории никакого отношения.
        table_heading_1st_line = S1_TextLemmasFinder.table_heading.split('\n')[0]
        if table_heading_1st_line in self.incorrectly_formatted_lines:
            self.incorrectly_formatted_lines.remove(table_heading_1st_line)

        # Входные строки могут приходить в неотсортированном виде. Парсим их и располагаем в отсортированном виде
        # с т. з. поля counter.
        # Сортируем сущности по полю counter, чтобы слова в vocabulary размещались в том порядке,
        # в котором они были естественным образом встречены в тексте
        self.entities.sort(key=lambda x: x.counter)

        return self.entities, self.incorrectly_formatted_lines

    def _is_line_format_correct(self, line):
        is_format_ok = False
        # пример правильного форматирования строки: 3|εὐαγγελίου|εὐαγγέλιον|100%
        # 1) '3' - порядковый номер строки
        # 2) 'εὐαγγελίου' - словоформа (токен) в том виде, в котором она встретилась в тексте
        # 3) 'εὐαγγέλιον' - лемма
        # 4) '100%' - комментарий (их разновидностей существует штук 5)
        line_pieces = [lp.strip() for lp in line.split(PIPE)]
        if len(line_pieces) == NUMBER_OF_PIPED_ELEMENTS_IN_A_LINE:  # если строка имеет правильный и ожидаемый формат
            counter = line_pieces[0]
            token = line_pieces[1]
            lemma = line_pieces[2]
            # если counter действительно является цифрой/числом
            if counter.isdigit():
                # если token действительно является греческим словом
                if self.grcRegExFinder.is_greek_word(token):
                    # если lemma действительно является греческим словом
                    if self.grcRegExFinder.is_greek_word(lemma):
                        is_format_ok = True

        return is_format_ok
