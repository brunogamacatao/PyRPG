import pygame
from pygame.locals import *
from fase import Fase

ARQUIVO_MAPA = 'mapa.tmx'
OBSTACULOS   = ('city', 'plants')

class Fase1(Fase):
    def __init__(self, jogo):
        super(Fase1, self).__init__(jogo, ARQUIVO_MAPA, OBSTACULOS, [320, 200])