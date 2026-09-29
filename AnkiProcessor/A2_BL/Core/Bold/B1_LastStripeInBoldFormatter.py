import beautiful_soup_helper
from A0_CoreAnkiFormatter import A0_CoreAnkiFormatter


# Класс форматирует жирным РЕГУЛЯРНЫЕ МНОГОПОЛОСНЫЕ карточки словаря, делая определённые строки их последней полосы
# жирными (для полей Front и Back)
class B1_LastStripeInBoldFormatter:
    def __init__(self):
        self.a0_CoreAnkiFormatter = A0_CoreAnkiFormatter()

    def make_last_stripe_bold(self, html_str: str):
        result = html_str

        all_stripes = html_str.split('<br><br>')

        is_field_multi_striped = len(all_stripes) > 1
        if is_field_multi_striped:
            # Берём последнюю полосу.
            last_stripe = all_stripes[-1]

            # Разбираем последнюю полосу на отдельные строки.
            last_stripe_lines = last_stripe.split('<br>')

            # Делим строки последней полосы на 2 категории:
            # 1) верхние строки, которые нужно отформатировать жирным
            # 2) нижние строки, которые не нуждаются в жирном форматировании.
            # Не форматируем жирным те строки последней полосы, которые:
            # 2.1) содержат hint в скобках: (abc...)
            # 2.2) начинаются с С-style комментария: // высок. = высокий стиль (редкий случай, обычно эта информация
            # выносится в поле Back_comment)

            last_stripe_upper_lines = []
            last_stripe_lower_lines = []
            for i in range(0, len(last_stripe_lines)):
                line = last_stripe_lines[i]
                if self._should_line_be_bold(line):
                    if not self._is_bold(line):
                        # Нужно обрамлять в теги <b></b> каждую строку в отдельности, а не все строки вместе!
                        # Это очень важно, иначе html-разметка будет ломаться другими модулями форматирования (в частности,
                        # логикой итализации содержимого скобок).
                        bold_line = self._make_bold(line)
                        last_stripe_upper_lines.append(bold_line)
                    else:
                        # если сторока уже отформатирована жирным, просто доавляем её в результирующий список
                        last_stripe_upper_lines.append(line)
                else:
                    # Зашли в эту ветку, потому что встретили строку, которую не нужно форматировать жирным.
                    # А раз не нужно форматировать эту строку, значит не нужно форматировать и все лежащие ниже её
                    # строки! Поэтому данную строку и все оставшиеся строки складываем в отдельный список и выходим
                    # из цикла.
                    last_stripe_lower_lines = last_stripe_lines[i:]
                    break

            # Восстанавливаем текст последней полосы
            restored_last_stripe = '<br>'.join(last_stripe_upper_lines + last_stripe_lower_lines)

            # Восстанавливаем список всех полос Anki-поля, заменив последнюю из них обработанным вариантом
            # all_stripes[:-1] - берёт все элементы списка, кроме последнего
            restored_all_stripes = [*all_stripes[:-1], restored_last_stripe]
            # Восстанавливаем текст Anki-поля.
            restored_field = '<br><br>'.join(restored_all_stripes)
            result = restored_field

        return result

    def _should_line_be_bold(self, line):
        if self._is_line_hint(line) or self._is_line_comment(line) or self._is_line_not_to_be_formatted_bold(line):
            return False
        else:
            return True

    def _is_line_hint(self, line):
        line_plain_text = beautiful_soup_helper.getBs(line).get_text()
        # hint, характерный для поля Front
        is_hint_1 = line_plain_text.startswith('(hint: ') and line_plain_text.endswith(')')
        # hint, характерный для поля Back
        is_hint_2 = line_plain_text.startswith('(') and line_plain_text.endswith('...)')
        is_hint_3 = line_plain_text.startswith('(...') and line_plain_text.endswith(')')
        # TODO Может просто заменить в будущем все эти проверки одной единственной: если строка начинается со скобки,
        #  то игнорируем её для жирного форматирования, т. е. возвращаем False здесь???
        if is_hint_1 or is_hint_2 or is_hint_3:
            return True
        else:
            return False

    def _is_line_comment(self, line):
        line_plain_text = beautiful_soup_helper.getBs(line).get_text()
        if line_plain_text.startswith('// ') or line_plain_text.startswith('/* '):
            return True
        else:
            return False

    def _is_line_not_to_be_formatted_bold(self, line):
        line_plain_text = beautiful_soup_helper.getBs(line).get_text()
        if line_plain_text.startswith('(досл. '):
            return True
        else:
            return False

    def _is_bold(self, html_str):
        is_tag_bold = False
        soup = beautiful_soup_helper.getBs(html_str)
        first_tag = soup.find()  # находит первый тег в документе
        if first_tag:
            is_tag_bold = first_tag.name == 'b'
        return is_tag_bold

    def _make_bold(self, html_str):
        text_in_bold = f'<b>{html_str}</b>'
        return text_in_bold


###########################################

# Примеры строк
html_strings = [
    "s1<br><br>s2<br><br><b>Текст строки</b>",
    "s1<br><br>s2<br><br><p><i><b>Текст строки</b></i></p>",
    "s1<br><br>s2<br><br><p><b><i>Текст строки</i></b></p>",

    "s1<br><br>s2<br><br>нежирный текст",
    "s1<br><br>s2<br><br><p><i>нежирный текст</i></p>",
    "s1<br><br>s2<br><br><p>нежирный текст</p>",
]

if __name__ == '__main__':
    b1_LastStripeInBoldFormatter = B1_LastStripeInBoldFormatter()

    # for s in html_strings:
    #     res = b1_LastStripeInBoldFormatter.make_last_stripe_bold(s)
    #     print(res)

    s = 's1<br><br>s2<br><br>нежирный текст'
    s = 'modernist<br><br>theology<br><br>modernist theology<br>(<i>hint: м т</i>)'
    s = 'на-<br><br>щёлкать<br><br><span style="color: rgb(0, 170, 0);"><i>информ.</i></span> кликнуть мышью<br>(<i>an...</i>)'
    s = 'приставка<br><br>закрывать<br>(<i>sch...</i>)<br><br>1) запирать замком<br>2) присоединять, подключать'

    s = 'приставка, которая указывает на:<br>1) начало действия<br>2) приближение, прикосновение, прикрепление<br>3) увеличение объёма<br><br>закрывать<br>(<i>sch...</i>)<br><br>1) запирать замком&nbsp;(<i>напр. велосипед</i>)<br>2) присоединять, подключать'
    # s = 's1<br><br>s2<br><br>нежирный текст'
    # s = 'an-<br><br>schließen<br><br>anschließen'
    s = 'приставка, которая указывает на:<br>1) начало действия<br>2) приближение, прикосновение, прикрепление<br>3) увеличение объёма<br><br>закрывать<br>(<i>sch...</i>)<br><br><b>1) запирать замком&nbsp;(<i>напр. велосипед</i>)</b><br>2) присоединять, подключать'

    res = b1_LastStripeInBoldFormatter.make_last_stripe_bold(s)
    # print(res.split('<br><br>')[-1])
    # print(res)

    # b1_LastStripeInBoldFormatter.test()
