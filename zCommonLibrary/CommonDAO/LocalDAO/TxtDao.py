# from importlib.machinery import SourceFileLoader
# configDao = SourceFileLoader('ConfigDao', '../CommonDAO/LocalDAO/ConfigDao.py').load_module()
# configDao = SourceFileLoader('ConfigDao', '../LocalDAO/ConfigDao.py').load_module()

from LocalDAO import ConfigDao

############# FILE DAO #############

relative_path = 'resources/'


def composeKnownWordsFilename():
    filename = 'knownWords'
    return composeFilename(relative_path + filename)


def composeNewWordsFilename():
    filename = 'newWords'
    return composeFilename(relative_path + filename)


def composeFilename(pieceOfFilename):
    [themeNumber, themeName, topicNumber] = ConfigDao.getTopicEnvironmentFromConfig()
    filename = "{0} {1}.{2}.txt".format(pieceOfFilename, themeNumber, topicNumber)
    return filename


def readWordsFromFile(fullPath):
    word_lines = readLinesFromFile(fullPath)

    words = list()
    for word_line in word_lines:
        [word, *other] = word_line.split('\t')
        words.append(word)

    return words


def readLinesFromFile(fullPath):
    word_lines = open(fullPath, encoding='utf-8').read().splitlines()
    # U+FEFF is the Byte Order Mark character, which should only occur at the start of a document.
    # In documents, it should be treated as a ZERO WIDTH NON-BREAKING SPACE.
    # If this causes issues, you can remove it like any other character:
    word_lines[0] = word_lines[0].replace(u'\ufeff', '')
    return word_lines


def readTextFromFile(fullPath):
    text = open(fullPath, encoding='utf-8').read()
    return text


def writeDictToFile(fullPath, dictToPrint):
    text = ""
    counter = 0
    for word, freq in dictToPrint.items():
        if counter < len(dictToPrint.items()) - 1:
            text += "{0}\t{1}\n".format(word, freq)
            counter = counter + 1
        else:
            text += "{0}\t{1}".format(word, freq)

    writeTextToFile(fullPath, text)


def writeLinesToFile(fullPath, lines):
    text = ""
    for line in lines:
        text += "{0}\n".format(line)

    writeTextToFile(fullPath, text)


def writeTextToFile(fullPath, text):
    file = open(fullPath, 'w', encoding='utf-8')

    # Файл может не создаваться только из-за того, что его заблокировал firewall!!!
    # У меня была такая проблема!!! Полдня пропало из-за этого!!!
    # Пришлось открывать firewall и удалять из него почему-то втихаря заблокированные Python-скрипты!!!
    file.write(text)

    file.close()
