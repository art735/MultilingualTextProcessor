from enum import Enum


class Mode(Enum):
    SEARCH_ONLY = 1
    FIND_AND_REPLACE = 2


class NextTagSearchDirection(Enum):
    INWARDS = 1
    OUTWARDS = 2
