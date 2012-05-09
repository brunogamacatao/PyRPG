import pygame
from pygame.locals import *

class Fase2(object):
    def __init__(self, jogo):
        self.jogo = jogo

    def processa_eventos(self, eventos):
        for event in eventos:
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    self.jogo.irParaTela(self.jogo.FASE_1)
                    
    def renderiza(self):
        #Desenho do jogo na tela
        self.jogo.screen.fill((0, 0, 255))

    def processa(self, eventos):
        self.processa_eventos(eventos)
        self.renderiza()