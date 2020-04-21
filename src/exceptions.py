class WordNotFoundError(Exception):
    def __init__(self, word):
        self.message = f'{word} not found'

    def __str__(self):
        return self.message


class EmptyStrError(Exception):
    def __init__(self, message=''):
        self.message = 'Word parameter is an empty string'

    def __str__(self):
        return self.message
