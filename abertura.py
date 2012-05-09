import pygame
from pygame.locals import *
from tela import Tela

DELAY      = 2000
N_FRAMES   = 3
CONTANDO   = 0
PASSANDO   = 1
VELOCIDADE = 4

class Abertura(Tela):
    def __init__(self, jogo):
        self.jogo   = jogo
        self.imagem = pygame.image.load('garfield.png')
        self.rect   = self.imagem.get_rect()
        self.frame_atual  = 0
        self.ultimo_tempo = pygame.time.get_ticks()
        self.estado_atual = CONTANDO
        self.inicio_quadro(0)
        
    def inicio_quadro(self, n_quadro):
        print "inicio_quadro", n_quadro
        
    def fim_quadro(self, n_quadro):
        print "fim_quadro", n_quadro
        
    def processa_eventos(self, eventos):
        for event in eventos:
            if event.type == KEYDOWN:
                self.jogo.irParaTela(self.jogo.MENU)

    def renderiza(self):
        self.jogo.screen.blit(self.imagem, self.rect)
        
        if self.estado_atual == CONTANDO:
            tempo_atual = pygame.time.get_ticks()
            self.contador = self.jogo.tamanho_tela[0]
        
            if tempo_atual - self.ultimo_tempo > DELAY:
                self.estado_atual = PASSANDO
            
                self.fim_quadro(self.frame_atual)
                self.frame_atual += 1
                
                if self.frame_atual == N_FRAMES:
                    self.jogo.irParaTela(self.jogo.MENU)
        elif self.estado_atual == PASSANDO:
            if self.contador > 0:
                self.contador -= VELOCIDADE
                self.rect.left -= VELOCIDADE
            else:
                self.ultimo_tempo = pygame.time.get_ticks()
                self.estado_atual = CONTANDO
                self.inicio_quadro(self.frame_atual)