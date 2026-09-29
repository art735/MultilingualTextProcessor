import AppContext
from BaseDefiniteArticleService import BaseDefiniteArticleService
from MultilingualExcelDao import MultilingualExcelDao
from View_enums import CurrentLanguageComboBoxEnum

# Сервис для работы с артиклем древнегреческого языка
class GrcDefiniteArticleService(BaseDefiniteArticleService):
    MASC_SG_NOM_GRC = "ὁ"
    FEM_SG_NOM_GRC = "ἡ"
    NEUT_SG_NOM_GRC = "τὸ"

    MASC_SG_GEN_GRC = "τοῦ"
    FEM_SG_GEN_GRC = "τῆς"
    NEUT_SG_GEN_GRC = "τοῦ"

    MASC_SG_DAT_GRC = "τῷ"
    FEM_SG_DAT_GRC = "τῇ"
    NEUT_SG_DAT_GRC = "τῷ"

    MASC_SG_ACC_GRC = "τόν"
    FEM_SG_ACC_GRC = "τὴν"
    NEUT_SG_ACC_GRC = "τὸ"

    MASC_DUAL_NOM_GRC = "τὼ"
    FEM_DUAL_NOM_GRC = "τὼ"
    NEUT_DUAL_NOM_GRC = "τὼ"

    MASC_DUAL_GEN_GRC = "τοῖν"
    FEM_DUAL_GEN_GRC = "τοῖν"
    NEUT_DUAL_GEN_GRC = "τοῖν"

    MASC_DUAL_DAT_GRC = "τοῖν"
    FEM_DUAL_DAT_GRC = "τοῖν"
    NEUT_DUAL_DAT_GRC = "τοῖν"

    MASC_DUAL_ACC_GRC = "τὼ"
    FEM_DUAL_ACC_GRC = "τὼ"
    NEUT_DUAL_ACC_GRC = "τὼ"

    MASC_PL_NOM_GRC = "οἱ"
    FEM_PL_NOM_GRC = "αἱ"
    NEUT_PL_NOM_GRC = "τά"

    MASC_PL_GEN_GRC = "τῶν"
    FEM_PL_GEN_GRC = "τῶν"
    NEUT_PL_GEN_GRC = "τῶν"

    MASC_PL_DAT_GRC = "τοῖς"
    FEM_PL_DAT_GRC = "ταῖς"
    NEUT_PL_DAT_GRC = "τοῖς"

    MASC_PL_ACC_GRC = "τοὺς"
    FEM_PL_ACC_GRC = "τάς"
    NEUT_PL_ACC_GRC = "τά"

    grc_definite_articles_dict = {
        "Masc": {
            "Sing": {
                "Nom": MASC_SG_NOM_GRC,
                "Gen": MASC_SG_GEN_GRC,
                "Dat": MASC_SG_DAT_GRC,
                "Acc": MASC_SG_ACC_GRC,
            },
            "Dual": {
                "Nom": MASC_DUAL_NOM_GRC,
                "Gen": MASC_DUAL_GEN_GRC,
                "Dat": MASC_DUAL_DAT_GRC,
                "Acc": MASC_DUAL_ACC_GRC,
            },
            "Plur": {
                "Nom": MASC_PL_NOM_GRC,
                "Gen": MASC_PL_GEN_GRC,
                "Dat": MASC_PL_DAT_GRC,
                "Acc": MASC_PL_ACC_GRC,
            },
        },
        "Fem": {
            "Sing": {
                "Nom": FEM_SG_NOM_GRC,
                "Gen": FEM_SG_GEN_GRC,
                "Dat": FEM_SG_DAT_GRC,
                "Acc": FEM_SG_ACC_GRC,
            },
            "Dual": {
                "Nom": FEM_DUAL_NOM_GRC,
                "Gen": FEM_DUAL_GEN_GRC,
                "Dat": FEM_DUAL_DAT_GRC,
                "Acc": FEM_DUAL_ACC_GRC,
            },
            "Plur": {
                "Nom": FEM_PL_NOM_GRC,
                "Gen": FEM_PL_GEN_GRC,
                "Dat": FEM_PL_DAT_GRC,
                "Acc": FEM_PL_ACC_GRC,
            },
        },
        "Neut": {
            "Sing": {
                "Nom": NEUT_SG_NOM_GRC,
                "Gen": NEUT_SG_GEN_GRC,
                "Dat": NEUT_SG_DAT_GRC,
                "Acc": NEUT_SG_ACC_GRC,
            },
            "Dual": {
                "Nom": NEUT_DUAL_NOM_GRC,
                "Gen": NEUT_DUAL_GEN_GRC,
                "Dat": NEUT_DUAL_DAT_GRC,
                "Acc": NEUT_DUAL_ACC_GRC,
            },
            "Plur": {
                "Nom": NEUT_PL_NOM_GRC,
                "Gen": NEUT_PL_GEN_GRC,
                "Dat": NEUT_PL_DAT_GRC,
                "Acc": NEUT_PL_ACC_GRC,
            },
        },
    }

    def __init__(self):
        super().__init__(AppContext.GRC_LANG_CODE, self.grc_definite_articles_dict)


#################################################################

if __name__ == '__main__':
    grcDefiniteArticleService = GrcDefiniteArticleService()

    # token = 'προφήτης'
    # morph = {'Case': ['Nom'], 'Gender': ['Masc'], 'Number': ['Sing']}
    # res = grcDefiniteArticleService.add_definite_article_to_token(token, 'NOUN', morph)
    # print(res)

    token = 'ἡ θύρα'
    res = grcDefiniteArticleService.strip_definite_article(token)
    print(res)

