from DeuDefiniteArticleService import DeuDefiniteArticleService
from NounInflectionTableSearcher import NounInflectionTableSearcher


class NounInflectionService:
    def __init__(self):
        self.deuDefiniteArticleService = DeuDefiniteArticleService()
        self.nounInflectionTableSearcher = NounInflectionTableSearcher()

    def get_noun_inflections(self, input_text):
        results = list()
        for token in input_text.split('\n'):
            noun = token.strip()
            if noun:
                pure_noun = self.deuDefiniteArticleService.strip_definite_article(noun)
                inflections = self.nounInflectionTableSearcher.get_noun_inflection_tables(pure_noun)
                results.append(inflections)

        output = '\n\n'.join(results)
        return output


#########################################

input_text = "    das Grundrecht\n      der Mensch  \nder Politikunterricht         \n\n\ndie Regierung         "
input_text = "der Hof"

if __name__ == '__main__':
    nounInflectionService = NounInflectionService()
    result = nounInflectionService.get_noun_inflections(input_text)
    print(result)
