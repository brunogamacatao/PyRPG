class Tela(object):
    def __init__(self, jogo):
        self.jogo = jogo

    def processa_eventos(self, eventos):
        pass
                    
    def renderiza(self):
        pass

    def processa(self, eventos):
        self.processa_eventos(eventos)
        self.renderiza()