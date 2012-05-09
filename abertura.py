import pygame
from pygame.locals import *
from tela import Tela

DELAY = 2000

class Abertura(Tela):
    def __init__(self, jogo):
        self.jogo    = jogo
        self.imagens = []
        self.imagens.append(pygame.image.load('garfield1.png')) 
        self.imagens.append(pygame.image.load('garfield2.png')) 
        self.imagens.append(pygame.image.load('garfield3.png'))
        self.frame_atual  = 0
        self.ultimo_tempo = pygame.time.get_ticks()
        
    def processa_eventos(self, eventos):
        for event in eventos:
            if event.type == KEYDOWN:
                self.jogo.irParaTela(self.jogo.MENU)

    def renderiza(self):
        frame = self.imagens[self.frame_atual]
        self.jogo.screen.blit(frame, frame.get_rect())
        
        tempo_atual = pygame.time.get_ticks()
        
        if tempo_atual - self.ultimo_tempo > DELAY:
            self.ultimo_tempo = tempo_atual
            self.frame_atual += 1
            if self.frame_atual == len(self.imagens):
                self.jogo.irParaTela(self.jogo.MENU)