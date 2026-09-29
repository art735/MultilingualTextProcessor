from GermanNounDeclensionDao import GermanNounDeclensionDao


class GermanNounDeclensionService:

    def __init__(self):
        # self.germanNounDeclensionDao = GermanNounDeclensionDao()
        # self.noun_transcription_dict = self._get_noun_transcription_dict()

        self.noun_entities = GermanNounDeclensionDao().convert_excel_rows_to_entities()

    # def _get_noun_transcription_dict(self):
    #     results_dict = {}
    #     nouns_worksheet_tuples = self.germanNounDeclensionDao.get_tuples()
    #     for noun_tup in nouns_worksheet_tuples:
    #         # print(noun_tup)
    #         noun = noun_tup[0]
    #         transcription = noun_tup[1]
    #         processed_transcription = self._add_definite_article_to_transcription(noun, transcription)
    #         results_dict[noun] = processed_transcription
    #
    #     return results_dict

    # Для существительного die Frau с транскрипцией [fʁaʊ̯] сделать транскрипцию [diː fʁaʊ̯]
    # def _add_definite_article_to_transcription(self, noun, transcription):
    #     result = transcription
    #     # Метод startswith() принимает кортеж значений и возвращает True, если строка начинается с одного из элементов
    #     # этого кортежа.
    #     if noun.startswith(('der', 'die', 'das', 'des', 'dem', 'den')):
    #         article = noun.split(SPACE)[0]
    #         article_transcription = german_definite_article_transcription_dict[article]
    #         new_transcription = f'[{article_transcription[1:-1]} {transcription[1:-1]}]'
    #         result = new_transcription
    #
    #     return result

    def get_noun_declension_entity(self, articled_lemma):
        result = None
        for noun_entity in self.noun_entities:
            if articled_lemma == noun_entity.word:
                result = noun_entity
                break
        return result

    # def get_noun_transcription(self, articled_noun):
    #     result = ''
    #     for noun_entity in self.noun_entities:
    #         if articled_noun == noun_entity.word:
    #             result = noun_entity.transcription
    #             break
    #     return result


#########################################

noun = 'die Frau'
noun = 'Hamburg'

if __name__ == '__main__':
    germanNounDeclensionService = GermanNounDeclensionService()
    noun_declension_entity = germanNounDeclensionService.get_noun_declension_entity(noun)
    print(noun_declension_entity)
