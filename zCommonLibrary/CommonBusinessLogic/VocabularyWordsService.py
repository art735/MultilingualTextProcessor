import re

import Tokenizer


# dbDao = SourceFileLoader('DbDao',           '../CommonDAO/LocalDAO/DbDao.py').load_module()

# configDao = SourceFileLoader('ConfigDao', '../CommonDAO/LocalDAO/ConfigDao.py').load_module()
# excelDao = SourceFileLoader('ExcelDao', '../CommonDAO/LocalDAO/ExcelDaoEnglishTopics.py').load_module()
# txtDao = SourceFileLoader('TxtDao',         '../CommonDAO/LocalDAO/TxtDao.py').load_module()
#
# wordMorphologyAndFrequencyProcessor = SourceFileLoader('CoreEngine', '../CommonBusinessLogic/WordMorphologyAndFrequencyProcessor.py').load_module()
# printResultsService = SourceFileLoader('PrintResultsService', 'PrintResultsService.py').load_module()
# validationService = SourceFileLoader('ValidationService', '../CommonBusinessLogic/ValidationUtils.py').load_module()
# utils = SourceFileLoader('Utils', '../CommonBusinessLogic/Utils.py').load_module()
# tokenizer = SourceFileLoader('Tokenizer', '../CommonBusinessLogic/Tokenizer.py').load_module()

########################

# Примеры СУЩЕСТВИТЕЛЬНЫХ:
# man (pl. men)
# craftsman (pl. craftsmen)
# crisis (pl. crises)

# Примеры ПРИЛАГАТЕЛЬНЫХ:
# good (better, best)
# nice (nicer, nicest)

# Примеры глаголов:
# любой обычный глагол с частицей to: to love, to risk
# любой неправильный глагол: to be (was, were; been), to see (saw; seen)

# Данный метод используется на самом 1-м этапе работы с тектом, когда строятся списки newWords & knownWords
# Метод "пропускает" в работу только начальную форму слова (лемму) и отсекает всё лишнее
# Данный метод НЕ используется для построения транскрипций!
def preprocessCompoundVocabularyWords(vocabularyWords):
    # key - compound word "as it is" in vocabulary in Excel cell
    # value - initial word form
    compoundWords_dict = dict()

    for word in vocabularyWords:
        # если в "слове" есть пробел, его уже можно считать "сложным" ("compound") и требующим доп. обработки
        match = re.search(r"\s", word)

        if match:
            # если в начале слова находится частица to с пробелом - отбросить её
            processed_word = re.sub(r"^to\s", "", word)

            # \S matches any character which is NOT a whitespace character. This is the opposite of \s
            # ^([\S]+) matches word before first whitespace
            match = re.search(r"^([\S]+)", processed_word)
            lemma = match.group(0)

            compoundWords_dict[word] = lemma

    return compoundWords_dict


# обрезать (trim) всё лишнее вокруг основной формы слова:
# - частицу "to" во всех глаголах
# - круглые скобки с их содержимым в сущ., прил. и непр. глаголах
def trim(vocabularyWords):
    # key - compound word "as it is" in vocabulary in Excel cell
    # value - initial word form
    compoundWords_dict = preprocessCompoundVocabularyWords(vocabularyWords)

    for k, v in compoundWords_dict.items():
        # найти индекс элемента, подлежащего замене
        i = vocabularyWords.index(k)
        # произвести замену сложного вида слова на простой
        vocabularyWords[i] = v

    return vocabularyWords


def getVocabularyWordsFromSpreadsheets(mode):
    # mode = {'CURRENT_ONLY', 'UP_TO_CURRENT_INCLUDING', 'ALL'}
    vocabularyWords = ExcelDao.getVocabularyWords(mode)

    # TODO ???
    # niceWords = processWords(rawWords)

    # VALIDATION
    ValidationService.validate_vocabulary_uniqueness(vocabularyWords)

    # COUNTING
    print("vocabularyWords contains {0} words".format(len(vocabularyWords)))

    return vocabularyWords


# to unfold ['ʌn'fəuld] развёртывать; раскрывать
def unfold(wordTuples):
    result = list()
    for wordTuple in wordTuples:

        word = wordTuple[0]
        transcription = wordTuple[1]

        # for verbs remove 'to + whitespace' only at the beginning of the string
        word = re.sub("^to\s", "", word)

        # если англ. слово содержит пробел (напр. "to go (went; gone); "grey (BrE) \n gray (AmE)"
        # 1) у неправильных глаголов каждую форму рассматривать как отдельное слово
        # 2) у слов с брит. и амер. вариантами данные формы считать как два отдельных слова

        # если в "слове" есть пробел, его уже можно считать "сложным" ("compound") и требующим доп. обработки
        match = re.search(r"\s", word)
        if match:
            res = processWordsCellContainingWhitespace(word, transcription)
            result.extend(res)
        else:
            result.append(wordTuple)

    # TODO добавить валидацию на уникальность всех кортежей в получившемся развёрнутом списке
    # unique_words = set(result)

    return result


tokenizer = Tokenizer()


def processWordsCellContainingWhitespace(word, transcription):
    # разбить на токены (как и текст! по тем же правилам!), чтобы легче было избавиться от ненужных компонент
    word_tokens = tokenizer.tokenize(word, True, True)

    bare_transcription_tokens = tokenizer.tokenize(transcription, True, True)
    transcription_tokens = map(wrapInBrackets_func, bare_transcription_tokens)

    result = list(zip(word_tokens, transcription_tokens))
    return result


def wrapInBrackets_func(transription):
    return "[{0}]".format(transription)
