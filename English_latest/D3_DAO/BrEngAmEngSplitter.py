import re
from itertools import zip_longest

from RepositoryItem import RepositoryItem


def split(record):
    word_pieces = record.word.split('\n')

    # если ячейка Excel реально не содержит символ '\n' в транскрипции, всё равно будет создан список!,
    # состоящий из одного элемента; а поскольку результат - список!, следовательно по нему можно итерироваться
    transcription_pieces = record.transcription.split('\n')
    translation = record.translation
    morphological_forms = record.morphological_forms

    res_dict = dict()
    for word_piece, transcription_piece in zip_longest(word_pieces, transcription_pieces):
        word_piece = re.sub(r'\s\((BrE|AmE)\)', '', word_piece)
        if transcription_piece is None:  # если слово разбилось на 2 части, а транскрипция всего одна
            # вместо None использовать последний элемент списка кусочков транскрипций
            transcription_piece = transcription_pieces[-1]
        # res = word_piece + " " + transcription_piece
        # res_dict[word_piece.lower()] = RepositoryItem(word_piece, transcription_piece, translation)

        # в RepositoryItem сохраняем первоначальную форму слова (как в ячейке Excel), а ключом к нему словаре будет кусочек (британский или американский)
        repo_item = RepositoryItem(record.word, transcription_piece, translation)
        repo_item.add_morphological_forms(morphological_forms)
        res_dict[word_piece.lower()] = repo_item

    return res_dict  # на вход получили одну запись, а возвращаем словарь с 2-мя записями

########################

# word = "grey (BrE)\ngray (AmE)"
# transcription = "[greɪ]"
# # transcription = "[greɪ_BR]\n[greɪ_AM]"
# translation = "1) серый\n2) седой (о волосах)"
# test_morph_forms = [('k1', 'v1'), ('k2', 'v2')]
#
# test_record = RepositoryItem(word, transcription, translation)
# test_record.add_morphological_forms(test_morph_forms)
#
# result = split(test_record)
# print(result)
