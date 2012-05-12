import pygame
from pygame.locals import *
from fase import Fase

ARQUIVO_MAPA = 'mapas/mapasfuturo/futuro1.tmx'
OBSTACULOS   = ('casas',)
DELAY_PARA_EXPLICACAO = 100

class Fase1(Fase):
    def __init__(self, jogo):
        super(Fase1, self).__init__(jogo, ARQUIVO_MAPA, OBSTACULOS, [10, 32 * 6])
        self.inicio_fase = pygame.time.get_ticks()
        self.exibiu_explicacao = False
        
    def processa_eventos(self, eventos):
        super(Fase1, self).processa_eventos(eventos)
        teclas = pygame.key.get_pressed()
        
        if not self.exibiu_explicacao:
            if pygame.time.get_ticks() - self.inicio_fase > DELAY_PARA_EXPLICACAO:
                self.exibir_texto("Historia Historia Historia Historia Historia Historia Historia Historia Historia Historia Historia Historia Historia")
                self.exibiu_explicacao = True
        