class Intent():
    def getIntent(self, term):
        if term in ['busca', 'buscar', 'search', 'find']:
            return 'search'

        if term in ['download', 'baixar', 'página', 'pagina']:
            return 'download'

        if term in ['summary', 'resumo']:
            return 'summary'

        return False