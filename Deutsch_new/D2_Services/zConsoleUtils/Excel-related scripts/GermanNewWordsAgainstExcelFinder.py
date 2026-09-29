import itertools

import Utils
from GermanExcelWorkbooksDao import GermanExcelWorkbooksDao

input_str = """
anklicken|[ˈʔanklɪkn̩]|кликать (мышью)  
fehlen|[ˈfeːlən]|отсутствовать  
duschen|[ˈduːʃn̩]|принимать душ  
besichtigen|[bəˈzɪçtɪɡən]|осматривать  
buchstabieren|[ˌbuːxʃtaˈbiːrən]|произносить по буквам  
ehren|[ˈʔeːʁən]|почитать, уважать  
enden|[ˈʔɛndən]|заканчиваться  
gebären|[ɡəˈbɛːʁən]|рожать  
verheiraten|[fɛɐ̯ˈhaɪ̯ʁatən]|жениться, выходить замуж  
kennenlernen|[ˈkɛnənˌlɛʁnən]|знакомиться  
atmen|[ˈʔaːtmən]|дышать  
kreuzen|[ˈkʁɔɪ̯t͡sən]|пересекать  
telefonieren|[teləfoˈniːʁən]|говорить по телефону  
verdienen|[fɛɐ̯ˈdiːnən]|зарабатывать  
vermieten|[fɛɐ̯ˈmiːtən]|сдавать в аренду
senden|[ˈzɛndən]|отправлять, посылать
passen | [ˈpasn̩] | подходить, соответствовать
ruhen | [ˈʁuːən] | отдыхать, покоиться
basteln | [ˈbastl̩n] | мастерить
bedanken | [bəˈdaŋkn̩] | благодарить
beeilen | [bəˈʔaɪ̯lən] | торопиться
beschweren | [bəˈʃveːʁən] | жаловаться
bewerben | [bəˈvɛʁbn̩] | подавать заявление
bewölken | [bəˈvœlkən] | затягивать облаками
umsteigen | [ˈʊmˌʃtaɪ̯ɡn̩] | пересаживаться
erkälten | [ɛʁˈkɛltn̩] | простужаться
räumen | [ˈʁɔɪ̯mən] | убирать, освобождать
rauskommen | [ˈʁaʊ̯sˌkɔmən] | выходить
rausbringen | [ˈʁaʊ̯sˌbʁɪŋən] | выносить
reinkommen | [ˈʁaɪ̯nˌkɔmən] | входить
verletzen | [fɛɐ̯ˈlɛtsn̩] | пораниться, травмироваться
wiegen | [ˈviːɡən] | весить, взвешивать
merken | [ˈmɛʁkn̩] | замечать
wegwerfen | [ˈvɛkˌvɛʁfn̩] | выбрасывать
notieren|[noˈtiːʁən]|записывать, отмечать  
surfen|[ˈzœʁfn̩]|заниматься сёрфингом  
probieren|[pʁoˈbiːʁən]|пробовать, пытаться  
renovieren|[ʁenoˈviːʁən]|ремонтировать  
schimpfen|[ˈʃɪmpfn̩]|ругать, бранить  
schneien|[ˈʃnaɪ̯ən]|идти (о снеге)  
sprechen|[ˈʃpʁɛçn̩]|говорить, разговаривать  
tauschen|[ˈtaʊ̯ʃn̩]|менять, обменивать  
trainieren|[tʁɛˈniːʁən]|тренировать(ся)  
weglaufen|[ˈvɛkˌlaʊ̯fn̩]|убегать  
üben|[ˈyːbn̩]|упражняться, практиковаться  
übersetzen|[ˌyːbɐˈzɛtsn̩]|переводить  
verabreden|[fɛʁˈʔapʁeːdn̩]|договариваться  
verlieben|[fɛʁˈliːbn̩]|влюбляться  
verreisen|[fɛʁˈʁaɪ̯zn̩]|уезжать, отправляться в поездку  
verschieben|[fɛʁˈʃiːbn̩]|передвигать, откладывать  
wegfahren|[ˈvɛkˌfaːʁən]|уезжать  
wegmachen|[ˈvɛkˌmaχn̩]|убирать  
weitermachen|[ˈvaɪ̯tɐˌmaχn̩]|продолжать  
weiterhelfen|[ˈvaɪ̯tɐˌhɛlfn̩]|помогать дальше  
schreien|[ˈʃʁaɪ̯ən]|кричать  
"""


# Данный код проверяет, присутствуют ли слова в Excel файлах "Deutsch Lexikon (!Popov).xls" и "Deutsch Lexikon (other).xls"
class GermanNewWordsAgainstExcelFinder:
    def __init__(self):
        self.germanExcelWorkbooksDao = GermanExcelWorkbooksDao()

    def find_new_words(self):
        words_per_excel_book_dict = self.germanExcelWorkbooksDao.get_excel_words_for_validation()
        all_excel_words = list(itertools.chain.from_iterable(words_per_excel_book_dict.values()))

        already_processed_verbs = set()
        new_verbs = []
        lines = [line for line in Utils.split_by(input_str, '\n') if line]
        for line in lines:
            # Разбиваем строку по двум причинам:
            # 1) чтобы вычитать из неё инфинитив глагола
            # 2) чтобы удалить пробелы вокруг пайпа
            line_pieces = Utils.split_by(line, '|')
            verb = line_pieces[0]
            if verb not in all_excel_words and verb not in already_processed_verbs:
                already_processed_verbs.add(verb)
                restored_line_without_spaces = '|'.join(line_pieces)
                if restored_line_without_spaces not in new_verbs:
                    new_verbs.append(restored_line_without_spaces)

        output = ''
        for i in range(0, len(new_verbs)):
            output += new_verbs[i] + '\n'
            # после каждого 5-го глагола добавляем пустую строку
            if i > 0:
                if i % 5 == 0:
                    output += '\n'
                if i % 100 == 0:
                    output += '********** 100 verbs delimiter **********\n\n'

        # output = '\n\n\n\n\n\n\n\n\n\n'.join(new_verbs)
        # output = '\n'.join(new_verbs)

        return output


########################################

if __name__ == '__main__':
    germanNewWordsAgainstExcelFinder = GermanNewWordsAgainstExcelFinder()
    res = germanNewWordsAgainstExcelFinder.find_new_words()
    print(res)
