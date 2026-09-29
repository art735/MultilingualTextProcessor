import AppContext
from BaseDefiniteArticleService import BaseDefiniteArticleService
from MultilingualExcelDao import MultilingualExcelDao
from View_enums import CurrentLanguageComboBoxEnum

german_definite_article_transcription_dict = {
    'der': '[deːɐ̯]',
    'die': '[diː]',
    'das': '[das]',
    'des': '[dɛs]',
    'dem': '[deːm]',
    'den': '[deːn]'
}

exceptional_proper_nouns_with_articles = [
    'die Schweiz', 'die Türkei', 'die USA', 'die Niederlande', 'die Slowakei', 'die Ukraine', 'der Iran', 'der Irak',
    'der Sudan', 'der Libanon', 'die EU'
]

# Сервис для работы с артиклем немецкого языка
class DeuDefiniteArticleService(BaseDefiniteArticleService):
    MASC_SG_NOM_DEU = "der"
    FEM_SG_NOM_DEU = "die"
    NEUT_SG_NOM_DEU = "das"
    PLUR_NOM_DEU = "die"

    MASC_SG_GEN_DEU = "des"
    FEM_SG_GEN_DEU = "der"
    NEUT_SG_GEN_DEU = "des"
    PLUR_GEN_DEU = "der"

    MASC_SG_DAT_DEU = "dem"
    FEM_SG_DAT_DEU = "der"
    NEUT_SG_DAT_DEU = "dem"
    PLUR_DAT_DEU = "den"

    MASC_SG_ACC_DEU = "den"
    FEM_SG_ACC_DEU = "die"
    NEUT_SG_ACC_DEU = "das"
    PLUR_ACC_DEU = "die"

    PLUR_DEU = {
        "Nom": PLUR_NOM_DEU,
        "Gen": PLUR_GEN_DEU,
        "Dat": PLUR_DAT_DEU,
        "Acc": PLUR_ACC_DEU,
    }

    deu_definite_articles_dict = {
        "Masc": {
            "Sing": {
                "Nom": MASC_SG_NOM_DEU,
                "Gen": MASC_SG_GEN_DEU,
                "Dat": MASC_SG_DAT_DEU,
                "Acc": MASC_SG_ACC_DEU,
            },
            "Plur": PLUR_DEU,
        },
        "Fem": {
            "Sing": {
                "Nom": FEM_SG_NOM_DEU,
                "Gen": FEM_SG_GEN_DEU,
                "Dat": FEM_SG_DAT_DEU,
                "Acc": FEM_SG_ACC_DEU,
            },
            "Plur": PLUR_DEU,
        },
        "Neut": {
            "Sing": {
                "Nom": NEUT_SG_NOM_DEU,
                "Gen": NEUT_SG_GEN_DEU,
                "Dat": NEUT_SG_DAT_DEU,
                "Acc": NEUT_SG_ACC_DEU,
            },
            "Plur": PLUR_DEU,
        },
    }

    def __init__(self):
        super().__init__(AppContext.DEU_LANG_CODE, self.deu_definite_articles_dict)

    # Вызывается в BaseDefiniteArticleService.add_definite_article_to_lemma
    def _search_among_exceptional_proper_nouns_with_articles(self, token):
        result = ''
        for proper_noun in exceptional_proper_nouns_with_articles:
            # Разбиваем только по первому пробелу (параметр maxsplit=1) на случай, если название имени собственного
            # будет состоять из нескольких частей, разделённых пробелом. Пример привести сложно, но в целом это будет
            # более правильным подходом.
            article, bare_proper_noun = proper_noun.split(' ', 1)
            if bare_proper_noun == token:
                result = proper_noun
                break
        return result

    def get_definite_article_transcription(self, definite_article):
        result = ''
        if definite_article in german_definite_article_transcription_dict:
            result = german_definite_article_transcription_dict[definite_article]
        return result


#################################################################

if __name__ == '__main__':
    deuDefiniteArticleService = DeuDefiniteArticleService()

    morph = {'Case': ['Nom'], 'Gender': ['Masc'], 'Number': ['Sing']}
    morph = {'Case': ['Dat'], 'Gender': ['Masc'], 'Number': ['Sing']}
    morph = {'Case': ['Nom'], 'Number': ['Plur']}

    res = deuDefiniteArticleService.add_definite_article_to_token('Eltern', 'NOUN', morph)
    print(res)

    # starts_with_definite_article(...) test
    input1 = ['die Ukraine', 'Hamburg']
    er1 = [True, False]
    if all(deuDefiniteArticleService.starts_with_definite_article(input_val) == er for input_val, er in
           zip(input1, er1)):
        print("'starts_with_definite_article(...)' test - ok")
    else:
        print("'starts_with_definite_article(...)' test - failed")

    # strip_definite_article(...) test
    input1 = ['der Moment', '  (der)   Alex', 'Berlin']
    er1 = ['Moment', 'Alex', 'Berlin']
    if all(deuDefiniteArticleService.strip_definite_article(input_val) == er for input_val, er in zip(input1, er1)):
        print("'strip_definite_article(...)' test - ok")
    else:
        print("'strip_definite_article(...)' test - failed")
