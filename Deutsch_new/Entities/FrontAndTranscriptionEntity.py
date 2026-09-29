class FrontAndTranscriptionEntity:
    def __init__(self):
        self.front = []
        self.transcription = []

    def to_str(self):
        front_str = '^^^'.join(self.front)
        transcription_str = '^^^'.join(self.transcription)
        result = '|'.join([front_str, transcription_str])
        return result

    def __str__(self):
        return f'{self.front}|{self.transcription}'
