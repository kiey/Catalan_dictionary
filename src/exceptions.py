class CatalanDictionaryException(Exception):
    pass


class WordNotFoundError(CatalanDictionaryException):
    def __init__(self, word):
        self.message = f'{word} not found'

    def __str__(self):
        return self.message


class ConnectionError(CatalanDictionaryException):
    def __init__(self):
            self.message = 'Unable to stablish internet connection'

    def __str__(self):
        return self.message
