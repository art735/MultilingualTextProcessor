import re
import time

import requests
from bs4 import BeautifulSoup

import beautiful_soup_helper

# важно позаботиться о 'правильной' (с точки зрения Oxford-сервера) информации в заголовках запроса, особенно о 'User-Agent'
# в противном случае будет отказ со стороны сервера обработать запрос
headers = requests.utils.default_headers()

headers.update(
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    }
)

common_url = "https://www.oxfordlearnersdictionaries.com/definition/english/{0}?q={1}"

# Данный URL нужен для тех глаголов, которые "по модулю" совпадают с соотв. существительными, но читаются иначе:
# record - to record; advocate - to advocate и т.д. Таких глаголов намного меньше, чем "обычных" глаголов.
# Поэтому пока реализацией данной логики не усложняю общий алгоритм.
# verb_url = "https://www.oxfordlearnersdictionaries.com/definition/english/{0}_2"

verb_url = common_url  # пока для глаголов используем тот же URL, что и для всех остальных слов


def _select_first_word(word_article):
    # ищет первое слово в словарной статье (первое слово не обязательно отделяется от последующих слов символом ПРОБЕЛА)
    # например, в словарной статье to see(saw; seen) нам нужно только 'see', но за ним не идёт пробел, а скобка!
    # Поэтому вариант регулярки в виде \S+ здесь не всегда подходит.
    result = word_article
    m = re.match(r'\w+', word_article)
    if m:
        result = m.group(0)
    return result


def make_sure_single_worded(word):
    result = word
    if ' ' in word:
        result = _select_first_word(word)
    return result


def _strip_word_and_make_url(word):
    url = ''

    # если слово начинается с to, значит это глагол, и для получения его транскрипции нужен запрос на другой url
    if word.startswith('to '):
        bare_verb = re.sub(r'^to\s', '', word)  # убрали частицу to перед глаголом
        bare_verb = make_sure_single_worded(bare_verb)
        url = verb_url.format(bare_verb, bare_verb)
    elif word.startswith('the '):
        bare_noun = re.sub(r'^the\s', '', word)  # убрали артикль the перед существительным
        bare_noun = make_sure_single_worded(bare_noun)
        url = common_url.format(bare_noun.lower(), bare_noun)
    else:
        # https://www.oxfordlearnersdictionaries.com/definition/english/usa?q=USA
        # https://www.oxfordlearnersdictionaries.com/definition/english/abc_1?q=ABC
        word = make_sure_single_worded(word)
        # 1-й параметр обязательно должен быть буквами в нижнем регистире; а 2-й - как есть
        # если 1-й параметр содержит апотроф, он должен быть заменён на дефис: таков формат URL в Oxford Dictionary
        # https://www.oxfordlearnersdictionaries.com/definition/english/aren-t?q=aren’t
        url = common_url.format(word.lower().replace('’', '-'), word)

    return url


def _process_transcription_css_selector_results(results):
    transcription = ''

    if len(results) > 0:  # если у слова имеется транскрипция (или несколько)
        # вытягиваем текст из beautifulsoup-ских объектов и удаляем пробелы внутри каждой отдельно взятой транскрипции
        text_results = [res.text.replace(' ', '') for res in results]
        transcription = ', '.join(text_results)

    while '/' in transcription:
        # text.replace (old, new[, count]) -> string
        transcription = transcription.replace("/", "[", 1)  # only one occurrence is replaced here
        transcription = transcription.replace("/", "]", 1)  # only one occurrence is replaced here

    return transcription


# MAIN BUSINESS METHOD
def get_word_british_and_american_transcriptions(word, delay_between_requests):
    url = _strip_word_and_make_url(word)

    response = requests.get(url, headers=headers)
    html_str = response.text
    soup = beautiful_soup_helper.getBs(html_str)

    # '>' - immediate children of a specified element. Если этого не сделать, то будут вычитываться и транскрипции
    # всех словоформ данного слова (особенно глагола), что является ненужным и лишним в данной задаче
    british_transcription_css_selector = 'div.webtop > span.phonetics div.phons_br span.phon'
    american_transcription_css_selector = 'div.webtop > span.phonetics div.phons_n_am span.phon'

    all_british_results = soup.select(british_transcription_css_selector)
    british_transcription = _process_transcription_css_selector_results(all_british_results)

    all_american_results = soup.select(american_transcription_css_selector)
    american_transcription = _process_transcription_css_selector_results(all_american_results)

    time.sleep(delay_between_requests)  # delay between requests (in seconds)
    return british_transcription, american_transcription


########################################


word = 'cat'
word = 'direct'
word = 'car'
word = 'record'
word = 'to record'
word = 'advocate'
word = 'to advocate'
word = 'to abduct'
word = 'to abide by (abode, abided; abode, abided)'
word = 'to see(saw; seen)'
word = 'simultaneous'
word = 'ABC'
word = 'aged 1.'
# british_transcription, american_transcription = get_word_british_and_american_transcriptions(word, 1)
# print(british_transcription + '\t|\t' + american_transcription)
