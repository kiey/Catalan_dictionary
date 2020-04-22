class WordNotFoundError(Exception):
    def __init__(self, word):
        self.message = f'{word} not found'

    def __str__(self):
        return self.message
