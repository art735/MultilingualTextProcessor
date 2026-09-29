import re
from typing import NamedTuple

from RepositoryItem import RepositoryItem


# Тип возвращаемого значения
class RepositoryLookUpResult(NamedTuple):
    record: RepositoryItem
    transcription: str
    needs_transcription_further_processing: bool

    def __str__(self):
        return "record: {0}\ntranscription: {1}\nneeds_transcription_further_processing: {2}".format(
            self.record, self.transcription, self.needs_transcription_further_processing)


pos_hint_regex_patterns_dict = {

    # критерий явно заданного прилагательного - ' (adj.)' в конце строки (после слова)
    'ADJ_POS_HINT': r'\s\(adj[.]\)$',

    # критерий явно заданного наречия - ' (adv.)' в конце строки (после слова)
    'ADV_POS_HINT': r'\s\(adv[.]\)$',

    # критерий глагола - 'to ' в начале строки (перед словом)
    'VERB_POS_HINT': r'^to\s',

    # критерий существительного - отсутствие пробела в словарной статье (у остальных явно заданных частей речи пробел имеется!)
    'NOUN_POS_HINT': r'^[^\s]+$',

    # другие части речи: критерий такой же как и у сущ. + отсутствие словоформ у основной словарной статьи.
    # Критерий слишком широкий и откровенно слабый, но ничего другого придумать не удаётся.
    'OTHER_POS_HINT': r'^[^\s]+$'
}


def covert_pos_tag(pos_tag):
    if pos_tag.startswith('JJ'):  # adjective: JJ, JJR, JJS
        return 'ADJ_POS_HINT'
    elif pos_tag.startswith('RB'):  # adverb: RB, RBR, RBS
        return 'ADV_POS_HINT'
    elif pos_tag.startswith('VB'):  # verb: VB, VBD, VBG, VBN, VBP, VBZ
        return 'VERB_POS_HINT'
    elif pos_tag.startswith('NN'):  # noun: NN, NNP, NNPS, NNS
        return 'NOUN_POS_HINT'
    else:
        return 'OTHER_POS_HINT'


def _search_through_morphological_forms(str_to_search, repository_dict, k, v):
    result = None
    for t in v.morphological_forms:
        morph_form = t[0]
        morph_form_transcription = t[1]
        if str_to_search == morph_form:
            result = RepositoryLookUpResult(repository_dict[k], morph_form_transcription, False)
        # elif word_lemma == morph_form: # TODO со временем попробовать закоментировать эту ветку
        #     result = RepositoryLookUpResult(repository_dict[k], morph_form_transcription, True)
    return result


def search(word_to_search, word_lemma, pos_tag, repository_dict):
    pos_hint_pattern = covert_pos_tag(pos_tag)

    # поиск только среди явно pos-обозначенных статей словаря
    if pos_hint_pattern in ['ADJ_POS_HINT', 'ADV_POS_HINT',
                            'VERB_POS_HINT']:  # сюда не попали 'NOUN_POS_HINT' и 'OTHER_POS_HINT'
        for i in range(0, 2):
            search_condition1 = lambda key: re.search(pos_hint_regex_patterns_dict[pos_hint_pattern], key)
            if i == 0:  # 0-я итерация - это проверка на соответствие информации из репозитория искомому слову (а не его лемме!)
                # поиск в словарной статье искомого слова:
                # сначала проверка на соотв-е обстрипанному ключу, и в случае неуспеха:
                # проверка на соотв-е всем словоформам
                for k, v in repository_dict.items():
                    if search_condition1(k):  # если ключ словаря явно pos-помечен
                        stripped_k = re.sub(pos_hint_regex_patterns_dict[pos_hint_pattern], '', k)
                        if word_to_search == stripped_k:
                            return RepositoryLookUpResult(repository_dict[k], repository_dict[k].transcription, False)
                        else:
                            res = _search_through_morphological_forms(word_to_search, repository_dict, k, v)
                            if res is not None:
                                return res
            elif i == 1:  # 1-я итерация - это проверка на соответствие информации из репозитория ЛЕММЕ искомого слова
                # поиск в словарной статье ЛЕММЫ искомого слова:
                # сначала проверка на соотв-е обстрипанному ключу, и в случае неуспеха:
                # проверка на соотв-е всем словоформам
                for k, v in repository_dict.items():
                    if search_condition1(k):  # если ключ словаря явно pos-помечен
                        stripped_k = re.sub(pos_hint_regex_patterns_dict[pos_hint_pattern], '', k)
                        if word_lemma == stripped_k:
                            return RepositoryLookUpResult(repository_dict[k], repository_dict[k].transcription, True)
                        # else: # TODO попробовать со временем закоментировать эту ветку
                        #     res = _search_through_morphological_forms(word_lemma, repository_dict, k, v)
                        #     if res is not None:
                        #         return res

    if pos_hint_pattern in ['ADJ_POS_HINT', 'ADV_POS_HINT', 'NOUN_POS_HINT',
                            'OTHER_POS_HINT']:  # сюда не попал 'VERB_POS_HINT'
        for i in range(0, 2):
            search_condition2 = lambda key: (re.search(pos_hint_regex_patterns_dict['ADJ_POS_HINT'],
                                                       key) is False or  # исключаем из поиска явно pos-меченные adj.
                                             re.search(pos_hint_regex_patterns_dict['ADJ_POS_HINT'],
                                                       key) is False or  # исключаем из поиска явно pos-меченные adv.
                                             re.search(pos_hint_regex_patterns_dict['NOUN_POS_HINT'],
                                                       key) or  # включаем в поиск существительные
                                             re.search(pos_hint_regex_patterns_dict['OTHER_POS_HINT'],
                                                       key))  # включаем в поиск другие части речи

            if i == 0:  # 0-я итерация - это проверка на соответствие информации из репозитория искомому слову (а не его лемме!)
                for k, v in repository_dict.items():
                    if search_condition2(k):
                        if word_to_search == k:
                            return RepositoryLookUpResult(repository_dict[k], repository_dict[k].transcription, False)
                        else:
                            res = _search_through_morphological_forms(word_to_search, repository_dict, k, v)
                            if res is not None:
                                return res

            elif i == 1:  # 1-я итерация - это проверка на соответствие информации из репозитория ЛЕММЕ искомого слова
                for k, v in repository_dict.items():
                    if search_condition2(k):
                        if word_lemma == k:
                            return RepositoryLookUpResult(repository_dict[k], repository_dict[k].transcription, True)
                        # else:  # TODO попробовать со временем закоментировать эту ветку
                        #     res = _search_through_morphological_forms(word_lemma, repository_dict, k, v)
                        #     if res is not None:
                        #         return res

######################################################################################

# word_to_search = 'is'
# word_lemma = 'be'
# pos_tag = 'VBZ'
# to_be_repItem = RepositoryItem("to be", "[biː]", "быть; существовать")
# to_be_repItem.add_morphological_forms([("am", "[æm]"), ("is", "[ɪz]"), ("are", "[ɑː(r)]"), ("was", "[wɔz]"),
#                                        ("were", "[wɜː]"), ("been", "[biːn]")])
# repository_dict = {'to be': to_be_repItem}
#
# res = search(word_to_search, word_lemma, pos_tag, repository_dict)
# print(res)
