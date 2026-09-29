import AppContext
from A010_NewLemmasFinder import A010_NewLemmasFinder
from DeuLemmaResolver import DeuLemmaResolver
from DeuSpaCyOrStanzaWrapper import DeuSpaCyOrStanzaWrapper
from EllLemmaResolver import EllLemmaResolver
from EllSpaCyOrStanzaWrapper import EllSpaCyOrStanzaWrapper
from GrcSpaCyEngineWrapper import GrcSpaCyOrStanzaWrapper
from MorphDictService import MorphDictService


class BusinessObjectFactory:
    # @staticmethod
    # def create(option: Option) -> BusinessObject:
    #     if option == Option.OPTION_A:
    #         return BusinessObjectA()
    #     elif option == Option.OPTION_B:
    #         return BusinessObjectB()
    #     else:
    #         raise ValueError(f"Unknown option: {option}")

    @staticmethod
    def create_a010_NewLemmasFinder():
        morphDictService = BusinessObjectFactory.get_MorphDictService()
        lemmaResolver = BusinessObjectFactory.get_lemmaResolver()
        return A010_NewLemmasFinder(morphDictService, lemmaResolver)

    @staticmethod
    def get_MorphDictService():
        spaCyEngineWrapper = BusinessObjectFactory.get_spaCyOrStanzaWrapper()
        return MorphDictService(spaCyEngineWrapper)

    @staticmethod
    def get_spaCyOrStanzaWrapper():
        if AppContext.is_language_german():
            spaCyOrStanzaWrapper = DeuSpaCyOrStanzaWrapper()
        elif AppContext.is_language_modern_greek():
            spaCyOrStanzaWrapper = EllSpaCyOrStanzaWrapper()
        elif AppContext.is_language_ancient_greek():
            spaCyOrStanzaWrapper = GrcSpaCyOrStanzaWrapper()
        else:
            raise Exception(f"Current language is not supported.")
        return spaCyOrStanzaWrapper

    @staticmethod
    def get_lemmaResolver():
        if AppContext.is_language_german():
            lemmaResolver = DeuLemmaResolver()
        elif AppContext.is_language_modern_greek():
            lemmaResolver = EllLemmaResolver()
        elif AppContext.is_language_ancient_greek():
            # TODO
            lemmaResolver = None
        else:
            raise Exception(f"Current language is not supported.")
        return lemmaResolver

