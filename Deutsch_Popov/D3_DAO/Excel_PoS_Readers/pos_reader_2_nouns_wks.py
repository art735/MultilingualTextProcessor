from DeuDefiniteArticleService import DeuDefiniteArticleService
import ExcelDaoUtils
from SlashContainingCellSplitter import SlashContainingCellSplitter

deuDefiniteArticleService = DeuDefiniteArticleService()
slashContainingCellSplitter = SlashContainingCellSplitter()


def _stripDefiniteArticles(tuples):
    result = list()

    # Если кортеж (слово, транскрипция) содержит слеши, например, ("die Worte / die Wörter", "[ˈvɔʁtə] / [ˈvœʁtɐ]"),
    # то такой кортеж должен быть разбит по слешам на отдельные кортежи:
    # ("die Worte", "[ˈvɔʁtə]"), ("die Wörter", "[ˈvœʁtɐ]")
    tuples = slashContainingCellSplitter.split_by_slash(tuples)

    for articled_noun, transcription in tuples:
        bare_noun = deuDefiniteArticleService.strip_definite_article(articled_noun)
        result.append(tuple([bare_noun, transcription]))
    return result


def get_tuples(nouns_worksheet):
    nouns_worksheet_indices = [[0, 1], [4, 5], [6, 7]]
    articled_nouns_worksheet_tuples = ExcelDaoUtils.getWorksheetData(nouns_worksheet, nouns_worksheet_indices)
    bare_nouns_worksheet_tuples = _stripDefiniteArticles(articled_nouns_worksheet_tuples)
    return bare_nouns_worksheet_tuples
