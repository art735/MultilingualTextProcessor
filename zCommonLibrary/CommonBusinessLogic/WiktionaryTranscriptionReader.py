import requests
from bs4 import BeautifulSoup

base_url = "https://{lang}.wiktionary.org/wiki/"


# lang_code = {de, en}
def get_word_transcription(lang_code, word):
    url = base_url.format(lang=lang_code) + word

    response = requests.get(url)
    # time.sleep(0.5)  # пауза на 0,5 секунды

    parser = 'html.parser'  # or lxml or html5lib
    encoding = response.encoding if 'charset' in response.headers.get('content-type', '').lower() else None

    beautifulSoup = BeautifulSoup(response.content, parser, from_encoding=encoding)

    allSpans = beautifulSoup.find_all('span')

    transcription = ''
    for span in allSpans:
        if span.has_attr('class') and ((span['class'][0] == "ipa") or (span['class'][0] == "IPA")):
            # Транскрипция "как есть": в английском wiktionary окружена слешами, в немецком - нет
            raw_transcription = span.text
            if raw_transcription.startswith('/') and raw_transcription.endswith('/'):
                unbracketed_transcription = raw_transcription[1:-1]
            else:
                unbracketed_transcription = raw_transcription

            # Если транскрипция слова в Wiktionary - пустая или представляет собой троеточие как единый символ
            # (например, у слова adresse с маленькой буквы), ставим "???" для большей наглядности в OO Writer
            if not unbracketed_transcription or unbracketed_transcription == '…':
                unbracketed_transcription = '???'
            transcription = "[{}]".format(unbracketed_transcription)
            break
    return transcription

############################

# ## Test 1. Get transcription from de.wiktionary.org
# LANG_CODE = 'de'
# word = 'Katze'
# transcription = get_word_transcription(LANG_CODE, word)
# print(word + "\t " + transcription)


# ## Test 2. Get transcription from de.wiktionary.org
# LANG_CODE = 'de'
# word = 'adresse'  # IPA: […]
# transcription = get_word_transcription(LANG_CODE, word)
# print(word + "\t " + transcription)


# ## Test 3. Get transcription from en.wiktionary.org
# LANG_CODE = 'en'
# word = 'dog'
# transcription = get_word_transcription(LANG_CODE, word)
# print(word + "\t " + transcription)
