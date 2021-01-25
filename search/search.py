from search.engines.google.google import Google

class Search():
    def __init__(self): 
        self.engine = Google()

    def search(self, term):
        result = {}
        result['engine'] = 'Google'
        result['result'] = self.engine.search(term)

        return result
