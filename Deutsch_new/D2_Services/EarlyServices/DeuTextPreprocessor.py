import re

from CharConstants import STRAIGHT_APOSTROPHE, CURLY_APOSTROPHE, DOUBLE_SPACE, SPACE
from DeuRegExFinder import DeuRegExFinder


class DeuTextPreprocessor:

    def __init__(self):
        self.deuRegExFinder = DeuRegExFinder()

    def preprocess(self, input_text):
        # Добавленный позже кусок логики, который частично препроцессит входной текст. В дальнейшем подумать как с ним
        # быть: оставить "как есть" или расформировать
        input_text = self._early_preprocess_input_text(input_text)

        # Отклеиваем от немецких слов возможно прилипшие к ним цифры/числа (напр., номера стихов Библии), апострофы
        # и прочее. В результате получаем текст, в котором немецкие элементы чётко отделены пробелами от не-немецких.
        # Теперь такой текст легко токенизировать и лемматизировать.
        preprocessed_text = self.deuRegExFinder.surround_with_spaces_non_german_inclusions(input_text)

        # После отклеивания всего ненемецкого от канонических немецких слов возникает ситуация, когда  «’s» (обычно
        # обозначающий сокращение слов es или das) оказывается разделённым пробелом: «’» + пробел + «s», а значит
        # апостроф и буква s становятся разными токенами, что приводит к ошибке обработки буквы s как якобы немецкого
        # слова. Нужно убрать пробел между апострофом и отдельно стоящей маленькой буквой s, чтобы они считались одним
        # токеном и в spaCy версии 3.7.5 такой токен будет автоматически проигнорирован при создании doc-объета.
        # 'Wo geht ’ s hier bitte zur Autobahn?' -> 'Wo geht ’s hier bitte zur Autobahn?'
        preprocessed_text = self._preprocess_apostrophe_plus_s(preprocessed_text)

        # Немецкие существительные нельзя принудительно преобразовывать к нижнему регистру, иначе лемматизация
        # начинает работать хуже и не всегда даёт правильные леммы, оставляя словоформу "как есть" и
        # выдавая её за лемму.
        # preprocessed_text = preprocessed_text.lower()

        return preprocessed_text
        # return input_text

    def _early_preprocess_input_text(self, input_text):
        result = input_text

        # Сокращение z.B. с возможным пробелом между буквами заменить полным текстом.
        # Здесь символ "точка" экранируется слешом, чтобы она воспринималась именно как текстовая точка, а не как
        # метасимвол регулярных выражений.
        # Пришлось поставить по краям символы \s (а не \b, как хотел изначально), т. к. \b обозначает границу слова,
        # а символ пробела не учитывается как граница слова (со слов ChatGPT), которая существует только между:
        # - буквой и не-буквой;
        # - цифрой и не-цифрой.
        # result = re.sub(r'\sz\.\s?B\.\s', ' zum Beispiel ', result)
        result = self.preprocess_zum_beispiel(result)

        # «So, das war’s / wär’s!» - заменить в подобного рода фразах «’s» на слово es.
        result = re.sub(r'\bwär’s\b', 'wäre es', result)
        result = result.replace("’s", " es").replace(DOUBLE_SPACE, SPACE)

        return result

    # Логика специально вынесена в отдельный метод, чтобы её можно было вызывать из других модулей, в частности
    # из модуля GermanSentenceTranscriber.py
    def preprocess_zum_beispiel(self, input_text):
        result = re.sub(r'\sz\.\s?B\.\s', ' zum Beispiel ', input_text)
        return result

    def _preprocess_apostrophe_plus_s(self, preprocessed_text):
        apostrophe_regex_group = f'[{STRAIGHT_APOSTROPHE}{CURLY_APOSTROPHE}]'

        # positive lookbehind апострофа
        positive_lookbehind = f'(?<={apostrophe_regex_group})'

        # positive lookahead буквы s, за которой:
        # - не следует немецкое слово (по смыслу) / немецкая буква (по буквальной записи регулярного выражения)
        # - или -
        # - следует символ конца строки
        # positive_lookahead = '(?=s([^a-zA-ZäöüÄÖÜß]|$))'
        positive_lookahead = fr'(?=s([^{DeuRegExFinder.german_letters}]|$))'
        # positive_lookahead = '(?=s )'

        # Ищем такой «пробел + s», перед которым стоит апостроф, а после что угодно, но только не следующее
        # немецкое слово (т. е. пробел, знак пунктуации, конец строки и т. д.)
        pattern = f"{positive_lookbehind} {positive_lookahead}"

        # Замена найденного паттерна на строку без пробела (т. е. удаление пробела между апострофом и буквой s, чтобы
        # они стали единым токеном)
        preprocessed_text = re.sub(pattern, '', preprocessed_text)
        return preprocessed_text


#############################

# input_str = "1Das ist ein Test-Text mit deutschen Wörtern wie Fußgängerübergang und E-Mail2."

# input_str = "Wo geht ’ s hier bitte zur Autobahn?"
# input_str = "Wo geht ’ s?"
# input_str = "Wo geht ’ s"

# input_str = "Wo geht ' s hier bitte zur Autobahn?"
# input_str = "Wo geht ' s?"
# input_str = "Wo geht ' s"

# input_str = "Ich (will)"
# input_str = "Ich ((will))"
# input_str = "Ich (will-(das))"
# input_str = "Ich (((will-(((das))))))"
# input_str = "Ich kaufe (Auto)mobile"
# input_str = "Ich kaufe ((Auto)mobile)"
#
# input_str = "Ich kaufe Auto(mobile)"
# input_str = "Ich kaufe (Auto(mobile))"
input_str = "Viele meiner Verwandten, z.B. (zum Beispiel) meine beiden Brüder, arbeiten auch hier."

if __name__ == '__main__':
    deuTextPreprocessor = DeuTextPreprocessor()
    res = deuTextPreprocessor.preprocess(input_str)
    print(res)
