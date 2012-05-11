import pygame
from pygame.locals import *
from fase import Fase

ARQUIVO_MAPA = 'mapas/mapa.tmx'
OBSTACULOS   = ('city', 'plants')

class Fase1(Fase):
    def __init__(self, jogo):
        super(Fase1, self).__init__(jogo, ARQUIVO_MAPA, OBSTACULOS, [320, 200])
        
    def processa_eventos(self, eventos):
        super(Fase1, self).processa_eventos(eventos)
        teclas = pygame.key.get_pressed()
        if teclas[K_p]:
            self.exibir_texto("Jogo Pausado - Pressione ENTER para continuar ... Jogo Pausado - Pressione ENTER para continuar ... Jogo Pausado - Pressione ENTER para continuar ... Jogo Pausado - Pressione ENTER para continuar ...")