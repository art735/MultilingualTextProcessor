from MorphologyParser import MorphologyParser


class BasePosService:
    def __init__(self):
        self.morphologyParser = MorphologyParser()
        self.err_msg = "spaCy has incorrectly defined morphology for '{}'"
