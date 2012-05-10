# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from maputils import Mapa

FPS          = 60
TAMANHO_TELA = (640, 480)
OBSTACULOS   = ('city', 'plants')

class Jogo(object):
    # Definição dos estados do jogo
    ABERTURA = 0
    MENU     = 1
    FASE_1   = 2
    FASE_2   = 3
    
    def __init__(self, tamanho_tela = TAMANHO_TELA, fps = FPS):
        pygame.init()
        
        self.tamanho_tela = tamanho_tela
        self.fps          = fps
        self.screen       = pygame.display.set_mode(self.tamanho_tela)
        self.clock        = pygame.time.Clock()
        self.rodando      = True
        
        self.irParaTela(Jogo.ABERTURA)
        
    def irParaTela(self, tela):
        if hasattr(self, 'estadoAtual'):
            self.estadoAnterior = self.estadoAtual
            self.telaAnterior   = self.telaAtual
        
        self.estadoAtual = tela
        
        if tela == Jogo.ABERTURA:
            from abertura import Abertura
            self.telaAtual = Abertura(self)
        elif tela == Jogo.MENU:
            from menu import Menu
            self.telaAtual = Menu(self)
        elif tela == Jogo.FASE_1:
            from fase_1 import Fase1
            self.telaAtual = Fase1(self)
        elif tela == Jogo.FASE_2:
            from fase_2 import Fase2
            self.telaAtual = Fase2(self)
            
        self.exibe_transicao()
        
    def exibe_transicao(self):
        from transicoes import blinds
        blinds(pygame.surfarray.array2d(self.screen), self.tamanho_tela, self.screen, 6)
            
    def voltar(self, dx = 0, dy = 0):
        self.estadoAtual = self.estadoAnterior
        self.telaAtual   =  self.telaAnterior
        
        delattr(self, 'estadoAnterior')
        delattr(self, 'telaAnterior')
        
        self.telaAtual.jogador.posicao[0] += dx
        self.telaAtual.jogador.posicao[1] += dy
            
    def sair(self):
        self.rodando = False

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
