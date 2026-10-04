from enum import Enum


class CurrentLanguageComboBoxEnum(Enum):
    GERMAN = 'German'
    MODERN_GREEK = 'Modern Greek'
    ANCIENT_GREEK = 'Ancient Greek'
    ENGLISH = 'English'
    CHURCH_SLAVONIC = 'Church Slavonic'


class MorphDictPolicyComboBoxEnum(Enum):
    READ_MORPH_DICT_FROM_LAST_FILE = 'Read morph_dict from last file'
    GENERATE_MORPH_DICT_ON_THE_FLY = 'Generate morph_dict on the fly'


class VocabFileComboBoxEnum(Enum):
    ALL_VOCAB_FILES = 'All [!Vocab]-files'
    LAST_VOCAB_FILE = 'Last [!Vocab]-file'


class PortraitFileComboBoxEnum(Enum):
    ALL_PORTRAIT_FILES = 'All [Portrait]-files'
