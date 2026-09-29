from DictionaryExcelDao import DictionaryExcelDao


class DictionaryService:
    def __init__(self):
        self.dictionaryExcelDao = DictionaryExcelDao()
        self.excel_dictionary_dict = self.dictionaryExcelDao.get_all_sheets_data_dict()

    def look_up_by_lemma(self, lemma):
        # result = None
        # if lemma in self.dictionary_dict:
        #     result = self.dictionary_dict[lemma]
        # return result
        result = ''
        results = []
        found_lemma = ''
        for dictionary_entity in self.excel_dictionary_dict.values():
            if lemma in dictionary_entity.lemmas:
                found_lemma = lemma
                results.append(dictionary_entity)

        if len(results):
            if len(results) > 1:
                raise Exception(f"Lemma '{found_lemma}' is duplicated in dictionary!")
            else:
                result = results[0]

        return result

    def look_up(self, word):
        results_set = set()

        for dictionary_entity in self.excel_dictionary_dict.values():
            # Ищем одновременно среди лемм и морф. форм. Нас интересуют все записи из Greek Dictionary, в которых
            # неважно в качестве леммы или одной из морф. форм встречается искомое слово
            if word in dictionary_entity.lemmas or word in dictionary_entity.morphological_forms:
                if dictionary_entity not in results_set:
                    results_set.add(dictionary_entity)

        return results_set


##########################################

dictionaryService = DictionaryService()

# res = dictionaryService.look_up_by_lemma("ἀρχή")
# CollectionPrinter.print_collection(res)

# res = dictionaryService.look_up("ἀρχή")
# CollectionPrinter.print_collection(res)
