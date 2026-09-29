class InputTextFromGuiPreprocessor:

    def preprocess(self, input_text: str):
        # Удаляем символ, визуально выглядящий как маленький квадратик. При вставке текста/таблицы из OO Writer в окно
        # программы, он автоматически появляется в самом конце текста.
        result = input_text.replace('\x00', '')
        result = result.strip()  # удаляет символы [ \t\n\r\f\v] в начале и конце строки
        return result


####################################

inputTextFromGuiPreprocessor = InputTextFromGuiPreprocessor()

input_text = """

       Ab morgen muss ich arbeiten. 
Ich bin oft im Büro, aber nur für wenige Stunden.                 

\x00

"""
# res = inputTextFromGuiPreprocessor.preprocess(input_text)
# print(res)
