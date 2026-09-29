from unittest import TestCase

import WiktionaryToExcelService


class TestWiktionaryToExcelService(TestCase):

    def test_noun(self):
        text = "Nominativ	die Frau	die Frauen\n" \
               "Genitiv	der Frau	der Frauen\n" \
               "Dativ	der Frau	den Frauen\n" \
               "Akkusativ	die Frau	die Frauen"

        expected_result = "die Frau|[fʁaʊ̯]|die Frauen|[ˈfʁaʊ̯ən]\n" \
                          "der Frau|[fʁaʊ̯]|der Frauen|[ˈfʁaʊ̯ən]\n" \
                          "der Frau|[fʁaʊ̯]|den Frauen|[ˈfʁaʊ̯ən]\n" \
                          "die Frau|[fʁaʊ̯]|die Frauen|[ˈfʁaʊ̯ən]"

        actual_result = WiktionaryToExcelService.run(text)
        self.assertEqual(expected_result, actual_result)

    def test_adjective(self):
        text = "nominative	einfacher	einfache	einfaches	einfache\n" \
               "genitive	einfachen	einfacher	einfachen	einfacher\n" \
               "dative	einfachem	einfacher	einfachem	einfachen\n" \
               "accusative	einfachen	einfache	einfaches	einfache"

        expected_result = "einfacher|[ˈaɪ̯nfaxɐ]|einfache|[ˈaɪ̯nfaxə]|einfaches|[ˈaɪ̯nfaxəs]|einfache|[ˈaɪ̯nfaxə]\n" \
                          "einfachen|[ˈaɪ̯nfaxn̩]|einfacher|[ˈaɪ̯nfaxɐ]|einfachen|[ˈaɪ̯nfaxn̩]|einfacher|[ˈaɪ̯nfaxɐ]\n" \
                          "einfachem|[ˈaɪ̯nfaxm̩]|einfacher|[ˈaɪ̯nfaxɐ]|einfachem|[ˈaɪ̯nfaxm̩]|einfachen|[ˈaɪ̯nfaxn̩]\n" \
                          "einfachen|[ˈaɪ̯nfaxn̩]|einfache|[ˈaɪ̯nfaxə]|einfaches|[ˈaɪ̯nfaxəs]|einfache|[ˈaɪ̯nfaxə]"

        actual_result = WiktionaryToExcelService.run(text)
        self.assertEqual(expected_result, actual_result)

    # обычный глагол (без отделямой приставки)
    def test_verb1(self):
        text = '''present participle	seiend
past participle	gewesen

ich bin	wir sind	i	ich sei	wir seien
du bist	ihr seid	du seist	ihr seiet
er ist	sie sind	er sei	sie seien

ich war	wir waren	ii	ich wäre	wir wären
du warst	ihr wart	du wärst	ihr wärt
er war	sie waren	er wäre	sie wären

sei (du)	seid (ihr)'''

        expected_result = '''seiend|[ˈzaɪ̯ənt]
gewesen|[ɡəˈveːzn̩]

ich bin|[bɪn]|wir sind|[zɪnt]|ich sei|[zaɪ̯]|wir seien|[ˈzaɪ̯ən]
du bist|[bɪst]|ihr seid|[zaɪ̯t]|du seist|[zaɪ̯st]|ihr seiet|[ˈzaɪ̯ət]
er/sie/es ist|[ɪst]|sie/Sie sind|[zɪnt]|er/sie/es sei|[zaɪ̯]|sie/Sie seien|[ˈzaɪ̯ən]

ich war|[vaːɐ̯]|wir waren|[ˈvaːʁən]|ich wäre|[ˈvɛːʁə]|wir wären|[ˈvɛːʁən]
du warst|[vaːɐ̯st]|ihr wart|[vaːɐ̯t]|du wärst|[vɛːɐ̯st]|ihr wärt|[vɛːɐ̯t]
er/sie/es war|[vaːɐ̯]|sie/Sie waren|[ˈvaːʁən]|er/sie/es wäre|[ˈvɛːʁə]|sie/Sie wären|[ˈvɛːʁən]

sei (du)|[zaɪ̯]|seid (ihr)|[zaɪ̯t]'''

        actual_result = WiktionaryToExcelService.run(text)
        self.assertEqual(expected_result, actual_result)

    # глагол с отделяемой приставкой
    def test_verb2(self):
        text = '''present participle	ablegend
past participle	abgelegt

ich lege ab	wir legen ab	i	ich lege ab	wir legen ab
du legst ab	ihr legt ab	du legest ab	ihr leget ab
er legt ab	sie legen ab	er lege ab	sie legen ab

ich legte ab	wir legten ab	ii	ich legte ab1	wir legten ab1
du legtest ab	ihr legtet ab	du legtest ab1	ihr legtet ab1
er legte ab	sie legten ab	er legte ab1	sie legten ab1

leg ab (du)	legt ab (ihr)'''

        expected_result = '''ablegend|[ˈapˌleːɡn̩t]
abgelegt|[ˈapɡəˌleːkt]

ich lege ab|[ˈleːɡə ap]|wir legen ab|[ˈleːɡn̩ ap]|ich lege ab|[ˈleːɡə ap]|wir legen ab|[ˈleːɡn̩ ap]
du legst ab|[leːkst ap]|ihr legt ab|[leːkt ap]|du legest ab|[ˈleːɡəst ap]|ihr leget ab|[ˈleːɡət ap]
er/sie/es legt ab|[leːkt ap]|sie/Sie legen ab|[ˈleːɡn̩ ap]|er/sie/es lege ab|[ˈleːɡə ap]|sie/Sie legen ab|[ˈleːɡn̩ ap]

ich legte ab|[ˈleːktə ap]|wir legten ab|[ˈleːktn̩ ap]|ich legte ab|[ˈleːktə ap]|wir legten ab|[ˈleːktn̩ ap]
du legtest ab|[ˈleːktəst ap]|ihr legtet ab|[ˈleːktət ap]|du legtest ab|[ˈleːktəst ap]|ihr legtet ab|[ˈleːktət ap]
er/sie/es legte ab|[ˈleːktə ap]|sie/Sie legten ab|[ˈleːktn̩ ap]|er/sie/es legte ab|[ˈleːktə ap]|sie/Sie legten ab|[ˈleːktn̩ ap]

leg ab (du)|[leːk ap]|legt ab (ihr)|[leːkt ap]'''

        actual_result = WiktionaryToExcelService.run(text)
        self.assertEqual(expected_result, actual_result)

    def test_verb3(self):
        text = '''present participle	gratulierend
past participle	gratuliert

ich gratuliere	wir gratulieren	i	ich gratuliere	wir gratulieren
du gratulierst	ihr gratuliert	du gratulierest	ihr gratulieret
er gratuliert	sie gratulieren	er gratuliere	sie gratulieren

ich gratulierte	wir gratulierten	ii	ich gratulierte1	wir gratulierten1
du gratuliertest	ihr gratuliertet	du gratuliertest1	ihr gratuliertet1
er gratulierte	sie gratulierten	er gratulierte1	sie gratulierten1

gratulier (du)	gratuliert (ihr)'''

        expected_result = '''gratulierend|[ɡʁatuˈliːʁənt]
gratuliert|[ɡʁatuˈliːɐ̯t]

ich gratuliere|[ɡʁatuˈliːʁə]|wir gratulieren|[ɡʁatuˈliːʁən]|ich gratuliere|[ɡʁatuˈliːʁə]|wir gratulieren|[ɡʁatuˈliːʁən]
du gratulierst|[ɡʁatuˈliːɐ̯st]|ihr gratuliert|[ɡʁatuˈliːɐ̯t]|du gratulierest|[ɡʁatuˈliːʁəst]|ihr gratulieret|[ɡʁatuˈliːʁət]
er/sie/es gratuliert|[ɡʁatuˈliːɐ̯t]|sie/Sie gratulieren|[ɡʁatuˈliːʁən]|er/sie/es gratuliere|[ɡʁatuˈliːʁə]|sie/Sie gratulieren|[ɡʁatuˈliːʁən]

ich gratulierte|[ɡʁatuˈliːɐ̯tə]|wir gratulierten|[ɡʁatuˈliːɐ̯tn̩]|ich gratulierte|[ɡʁatuˈliːɐ̯tə]|wir gratulierten|[ɡʁatuˈliːɐ̯tn̩]
du gratuliertest|[ɡʁatuˈliːɐ̯təst]|ihr gratuliertet|[ɡʁatuˈliːɐ̯tət]|du gratuliertest|[ɡʁatuˈliːɐ̯təst]|ihr gratuliertet|[ɡʁatuˈliːɐ̯tət]
er/sie/es gratulierte|[ɡʁatuˈliːɐ̯tə]|sie/Sie gratulierten|[ɡʁatuˈliːɐ̯tn̩]|er/sie/es gratulierte|[ɡʁatuˈliːɐ̯tə]|sie/Sie gratulierten|[ɡʁatuˈliːɐ̯tn̩]

gratulier (du)|[ɡʁatuˈliːɐ̯]|gratuliert (ihr)|[ɡʁatuˈliːɐ̯t]'''

        actual_result = WiktionaryToExcelService.run(text)
        self.assertEqual(expected_result, actual_result)

    def test_misc(self):
        # misc1
        text = "er xyzqwerty"
        expected_result = "er/sie/es xyzqwerty|[]"

        actual_result = WiktionaryToExcelService.run(text)
        self.assertEqual(expected_result, actual_result)

        # misc2
        text = "rewwww qwerty"
        expected_result = "rewwww qwerty|[]"

        actual_result = WiktionaryToExcelService.run(text)
        self.assertEqual(expected_result, actual_result)
