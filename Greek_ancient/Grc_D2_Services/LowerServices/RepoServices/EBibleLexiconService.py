from EBibleLexiconExcelDao import EBibleLexiconExcelDao


class EBibleLexiconService:
    def __init__(self):
        self.eBibleLexiconExcelDao = EBibleLexiconExcelDao()
        self.eBibleLexicon_dict = self.eBibleLexiconExcelDao.get_all_sheets_data_dict()

    def look_up(self, cltk_token):
        results_set = set()

        for eBibleLexicon_entity in self.eBibleLexicon_dict.values():
            # Ищем одновременно среди лемм и морф. форм. Нас интересуют все записи из eBibleLexicon, в которых
            # неважно в качестве леммы или одной из морф. форм встречается искомое слово
            if eBibleLexicon_entity.lemma == cltk_token or eBibleLexicon_entity.has_entity_given_morph_form(cltk_token):
                if eBibleLexicon_entity not in results_set:
                    results_set.add(eBibleLexicon_entity)

        return results_set


##########################################

eBibleLexiconService = EBibleLexiconService()

# res = eBibleLexiconService.look_up('καθὼς')
# CollectionPrinter.print_collection(res)

# res = eBibleLexiconService.look_up('ἐλέησόν')
# CollectionPrinter.print_collection(res)

# res = eBibleLexiconService.look_up('ἰδοὺ')
# CollectionPrinter.print_collection(res)

# text = 'ἀρχὴ τοῦ εὐαγγελίου ἰησοῦ χριστοῦ υἱοῦ θεοῦ'
# for token in text.split():
#     res = eBibleLexiconService.look_up(token)
#     CollectionPrinter.print_collection(res)
