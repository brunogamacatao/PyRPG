import pygame
from pygame.locals import *
from tela import Tela

class Menu(Tela):
    def __init__(self, jogo):
        super(Menu, self).__init__(jogo)
        self.bg_image = pygame.image.load('imagens/menubg.png')
    
    def processa_eventos(self, eventos):
        for event in eventos:
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    self.jogo.irParaTela(self.jogo.FASE_1)
                if event.key == K_ESCAPE:
                    self.jogo.sair()
                    
    def renderiza(self):
        self.jogo.screen.blit(self.bg_image, self.bg_image.get_rect())