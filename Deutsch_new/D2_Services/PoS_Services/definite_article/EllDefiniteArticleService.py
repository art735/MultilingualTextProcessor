import AppContext
from BaseDefiniteArticleService import BaseDefiniteArticleService
from MultilingualExcelDao import MultilingualExcelDao
from View_enums import CurrentLanguageComboBoxEnum

# Сервис для работы с артиклем новогреческого языка
class EllDefiniteArticleService(BaseDefiniteArticleService):
    MASC_SG_NOM_ELL = "ο"
    FEM_SG_NOM_ELL = "η"
    NEUT_SG_NOM_ELL = "το"

    MASC_SG_GEN_ELL = "του"
    FEM_SG_GEN_ELL = "της"
    NEUT_SG_GEN_ELL = "του"

    MASC_SG_ACC_ELL = "τον"
    FEM_SG_ACC_ELL = "την"
    NEUT_SG_ACC_ELL = "το"

    MASC_PL_NOM_ELL = "οι"
    FEM_PL_NOM_ELL = "οι"
    NEUT_PL_NOM_ELL = "τα"

    MASC_PL_GEN_ELL = "των"
    FEM_PL_GEN_ELL = "των"
    NEUT_PL_GEN_ELL = "των"

    MASC_PL_ACC_ELL = "τους"
    FEM_PL_ACC_ELL = "τις"
    NEUT_PL_ACC_ELL = "τα"

    ell_definite_articles_dict = {
        "Masc": {
            "Sing": {
                "Nom": MASC_SG_NOM_ELL,
                "Gen": MASC_SG_GEN_ELL,
                "Acc": MASC_SG_ACC_ELL,
            },
            "Plur": {
                "Nom": MASC_PL_NOM_ELL,
                "Gen": MASC_PL_GEN_ELL,
                "Acc": MASC_PL_ACC_ELL,
            },
        },
        "Fem": {
            "Sing": {
                "Nom": FEM_SG_NOM_ELL,
                "Gen": FEM_SG_GEN_ELL,
                "Acc": FEM_SG_ACC_ELL,
            },
            "Plur": {
                "Nom": FEM_PL_NOM_ELL,
                "Gen": FEM_PL_GEN_ELL,
                "Acc": FEM_PL_ACC_ELL,
            },
        },
        "Neut": {
            "Sing": {
                "Nom": NEUT_SG_NOM_ELL,
                "Gen": NEUT_SG_GEN_ELL,
                "Acc": NEUT_SG_ACC_ELL,
            },
            "Plur": {
                "Nom": NEUT_PL_NOM_ELL,
                "Gen": NEUT_PL_GEN_ELL,
                "Acc": NEUT_PL_ACC_ELL,
            },
        },
    }

    def __init__(self):
        super().__init__(AppContext.ELL_LANG_CODE, self.ell_definite_articles_dict)


#################################################################

if __name__ == '__main__':
    ellDefiniteArticleService = EllDefiniteArticleService()

    morph = {'Case': ['Nom'], 'Gender': ['Masc'], 'Number': ['Sing']}
    morph = {'Case': ['Dat'], 'Gender': ['Masc'], 'Number': ['Sing']}
    morph = {'Case': ['Nom'], 'Number': ['Plur']}

    res = ellDefiniteArticleService.add_definite_article_to_token('γονείς', 'NOUN', morph)
    print(res)

    # starts_with_definite_article(...) test
    input1 = ['η Ελλάδα', 'Αθήνα']
    er1 = [True, False]
    if all(ellDefiniteArticleService.starts_with_definite_article(input_val) == er for input_val, er in
           zip(input1, er1)):
        print("'starts_with_definite_article(...)' test - ok")
    else:
        print("'starts_with_definite_article(...)' test - failed")

    # strip_definite_article(...) test
    input1 = ['ο χρόνος', '  η  Μαρία ', 'η Θεσσαλονίκη']
    er1 = ['χρόνος', 'Μαρία', 'Θεσσαλονίκη']
    if all(ellDefiniteArticleService.strip_definite_article(input_val) == er for input_val, er in zip(input1, er1)):
        print("'strip_definite_article(...)' test - ok")
    else:
        print("'strip_definite_article(...)' test - failed")
