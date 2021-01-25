from googlesearch import search as gsearch

class Google():
    def search(self, term):
        return gsearch(term=term, num_results=1, lang="pt")
