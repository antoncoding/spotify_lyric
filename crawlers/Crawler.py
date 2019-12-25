class Crawler:
    def __init__(self, name):
        self.name = name

    def search_for_lyrics(self, artist, song):
        raise Exception('Not Implemented.')

    def raise_not_found(self):
        raise AttributeError('Not result found from {}'.format(self.name))
