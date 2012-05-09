# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from maputils import Mapa

FPS          = 60
TAMANHO_TELA = (640, 480)
OBSTACULOS   = ('city', 'plants')

class Jogo(object):
    # Definição dos estados do jogo
    MENU   = 0
    FASE_1 = 1
    
    def __init__(self, tamanho_tela = TAMANHO_TELA, fps = FPS):
        pygame.init()
        
        self.tamanho_tela = tamanho_tela
        self.fps          = fps
        self.screen       = pygame.display.set_mode(self.tamanho_tela)
        self.clock        = pygame.time.Clock()
        self.rodando      = True
        
        self.irParaTela(Jogo.MENU)
        
    def irParaTela(self, tela):
        self.estadoAtual = tela
        
        if tela == Jogo.MENU:
            from menu import Menu
            self.telaAtual = Menu(self)
        elif tela == Jogo.FASE_1:
            from fases import Fase
            self.telaAtual = Fase(self)

    def main(self):
        while self.rodando:
            self.clock.tick(self.fps)

            eventos = pygame.event.get()

            for event in eventos:
                if event.type == QUIT:
                    self.rodando = False

            self.telaAtual.processa(eventos)
            
            pygame.display.flip()

if __name__ == "__main__":
    jogo = Jogo()
    jogo.main()
