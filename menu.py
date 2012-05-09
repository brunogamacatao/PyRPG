import pygame
from pygame.locals import *

class Menu(object):
    def __init__(self, jogo):
        self.jogo = jogo

    def processa_eventos(self, eventos):
        for event in eventos:
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    self.jogo.irParaTela(self.jogo.FASE_1)
                if event.key == K_ESCAPE:
                    self.jogo.sair()
                    
    def renderiza(self):
        #Desenho do jogo na tela
        self.jogo.screen.fill((255, 0, 0))

    def processa(self, eventos):
        self.processa_eventos(eventos)
        self.renderiza()