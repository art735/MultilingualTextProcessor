from DeuSpaCyOrStanzaWrapper import DeuSpaCyOrStanzaWrapper


class MorphologyParser:

    def parse(self, morph, key):
        entity = ''
        entity_list = morph.get(key)
        if isinstance(entity_list, list) and len(entity_list):
            entity = entity_list[0]
            # entity_str = inbound_entity_list[0]
            # entity = entity_str
            # if my_spaCy_enum:
            #     entity = GrammarEnums.str_to_enum(my_spaCy_enum, entity_str)
        return entity

    # def parse_pronominal_type(self, morph):
    #     inbound_case_list = morph.get("PronType")
    #     result = self._parse_entity(inbound_case_list, GrammarEnums.CaseSpaCy)
    #     return result

    # def parse_case(self, morph):
    #     inbound_case_list = morph.get("Case")
    #     result = self._parse_entity(inbound_case_list, GrammarEnums.CaseSpaCy)
    #     return result

    # def parse_gender(self, morph):
    #     inbound_gender_list = morph.get("Gender")
    #     result = self._parse_entity(inbound_gender_list, GrammarEnums.GenderSpaCy)
    #     return result

    # def parse_number(self, morph):
    #     inbound_number_list = morph.get("Number")
    #     result = self._parse_entity(inbound_number_list, GrammarEnums.NumberSpaCy)
    #     return result

    # def parse_person(self, morph):
    #     inbound_person_list = morph.get("Person")
    #     result = self._parse_entity(inbound_person_list, None)
    #     return result

    # def _parse_entity(self, inbound_entity_list: list, my_spaCy_enum):
    #     entity = ''
    #     if isinstance(inbound_entity_list, list) and len(inbound_entity_list):
    #         entity = inbound_entity_list[0]
    #         # entity_str = inbound_entity_list[0]
    #         # entity = entity_str
    #         # if my_spaCy_enum:
    #         #     entity = GrammarEnums.str_to_enum(my_spaCy_enum, entity_str)
    #     return entity


#############################################################

if __name__ == '__main__':
    deuSpaCyOrStanzaWrapper = DeuSpaCyOrStanzaWrapper()
    morphologyParser = MorphologyParser()

    input_text = "Ab morgen muss ich arbeiten."
    input_text = "Wann kann ich den Schrank bei dir abholen?"
    # input_text = "Ich sehe ihn auf der Straße"

    # doc_tuples = deuSpaCyEngineWrapper.get_doc_object_tuples(input_text)
    # for token, lemma, pos, morph in doc_tuples:
    #     if pos in ['NOUN', 'PRON']:
    #         case = morphologyParser.parse(morph, "Case")
    #         gender = morphologyParser.parse(morph, "Gender")
    #         number = morphologyParser.parse(morph, "Number")
    #         person = morphologyParser.parse(morph, "Person")
    #
    #         print(f'{token} --> {lemma} : {morph}')
    #         print(f"Case = '{case}'")
    #         print(f"Gender = '{gender}'")
    #         print(f"Number = '{number}'")
    #         print(f"Person = '{person}'\n")
