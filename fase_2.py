import pygame
from pygame.locals import *
from fase import Fase

ARQUIVO_MAPA = 'mapas/mapa2.tmx'
OBSTACULOS   = ('obstaculos',)

class Fase2(Fase):
    def __init__(self, jogo):
        super(Fase2, self).__init__(jogo, ARQUIVO_MAPA, OBSTACULOS, [320, 200])