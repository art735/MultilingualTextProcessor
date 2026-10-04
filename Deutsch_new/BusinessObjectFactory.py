import AppContext
from A000_MorphDictGeneratorAndToFileSaver import A000_MorphDictGeneratorAndToFileSaver
from A010_NewLemmasFinder import A010_NewLemmasFinder
from DeuLemmaResolver import DeuLemmaResolver
from DeuSpaCyOrStanzaWrapper import DeuSpaCyOrStanzaWrapper
from EllLemmaResolver import EllLemmaResolver
from EllSpaCyOrStanzaWrapper import EllSpaCyOrStanzaWrapper
from EngLemmaResolver import EngLemmaResolver
from EngSpaCyOrStanzaWrapper import EngSpaCyOrStanzaWrapper
from GrcSpaCyEngineWrapper import GrcSpaCyOrStanzaWrapper
from MD1_ChurchSlavonic_MorphDictWithoutLemmasMaker import MD1_ChurchSlavonic_MorphDictWithoutLemmasMaker
from MD1_MorphDictWithoutLemmasMaker import MD1_MorphDictWithoutLemmasMaker
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
    def create_md1_MorphDictWithoutLemmasMaker():
        morphDictService = BusinessObjectFactory.get_MorphDictService()
        spaCyOrStanzaWrapper = BusinessObjectFactory.get_spaCyOrStanzaWrapper()
        return MD1_MorphDictWithoutLemmasMaker(morphDictService, spaCyOrStanzaWrapper)

    @staticmethod
    def create_md1_ChurchSlavonic_MorphDictWithoutLemmasMaker():
        morphDictService = BusinessObjectFactory.get_MorphDictService()
        return MD1_ChurchSlavonic_MorphDictWithoutLemmasMaker(morphDictService)

    @staticmethod
    def create_a000_MorphDictGeneratorAndToFileSaver():
        morphDictService = BusinessObjectFactory.get_MorphDictService()
        return A000_MorphDictGeneratorAndToFileSaver(morphDictService)

    @staticmethod
    def get_MorphDictService():
        spaCyEngineWrapper = BusinessObjectFactory.get_spaCyOrStanzaWrapper()
        return MorphDictService(spaCyEngineWrapper)

    # @staticmethod
    # def get_morphDictToFileWriter():
    #     morphDictToStrConverter = BusinessObjectFactory.get_MorphDictToStrConverter()
    #     morphDictToFileWriter = MorphDictToFileWriter(morphDictToStrConverter)
    #     return morphDictToFileWriter

    # @staticmethod
    # def get_MorphDictToStrConverter():
    #     return MorphDictToStrConverter()


    @staticmethod
    def create_a010_NewLemmasFinder():
        morphDictService = BusinessObjectFactory.get_MorphDictService()
        lemmaResolver = BusinessObjectFactory.get_lemmaResolver()
        return A010_NewLemmasFinder(morphDictService, lemmaResolver)



    @staticmethod
    def get_spaCyOrStanzaWrapper():
        if AppContext.is_language_german():
            spaCyOrStanzaWrapper = DeuSpaCyOrStanzaWrapper()
        elif AppContext.is_language_modern_greek():
            spaCyOrStanzaWrapper = EllSpaCyOrStanzaWrapper()
        elif AppContext.is_language_ancient_greek():
            spaCyOrStanzaWrapper = GrcSpaCyOrStanzaWrapper()
        elif AppContext.is_language_english():
            spaCyOrStanzaWrapper = EngSpaCyOrStanzaWrapper()
        elif AppContext.is_language_church_slavonic():
            spaCyOrStanzaWrapper = None
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
        elif AppContext.is_language_english():
            lemmaResolver = EngLemmaResolver()
        elif AppContext.is_language_church_slavonic():
            lemmaResolver = None
        else:
            raise Exception(f"Current language is not supported.")
        return lemmaResolver

