# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from tela import Tela
from myutils import Spritesheet, Animacao

# Definições das opções do menu
NOVO_JOGO = 0
AJUDA     = 1
SAIR      = 2

# Variáveis globais
DELAY = 200
DISTANCIA_OPCOES = 28

class Menu(Tela):
    def __init__(self, jogo):
        super(Menu, self).__init__(jogo)
        self.bg_image = pygame.image.load('imagens/menubg.png')
        
        x = 0
        y = 0
        frames_animacao = []
        
        for linha in range(4):
            for coluna in range(8):
                frames_animacao.append((x, y, 32, 32))
                x += 32
            y += 32
            x = 0
        
        self.bola = Animacao(Spritesheet('imagens/bola.png'), 60, frames_animacao)
        self.pos_bola = [190, 243]
        self.ultimo_tempo = -1
        self.ignora_delay = False
        self.opcao_atual  = NOVO_JOGO
    
    def processa_eventos(self, eventos):
        for event in eventos:
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if self.opcao_atual == NOVO_JOGO:
                        self.jogo.irParaTela(self.jogo.FASE_1)
                    elif self.opcao_atual == AJUDA:
                        pass
                    elif self.opcao_atual == SAIR:
                        self.jogo.sair()
                if event.key == K_ESCAPE:
                    self.jogo.sair()
                    
        teclas = pygame.key.get_pressed()
        
        if not teclas[K_DOWN] and not teclas[K_UP]:
            self.ignora_delay = True
            
        delta_t = pygame.time.get_ticks() - self.ultimo_tempo
        
        if delta_t > DELAY or self.ignora_delay:
            self.ultimo_tempo = pygame.time.get_ticks()
            if teclas[K_DOWN]:
                self.pos_bola[1] += DISTANCIA_OPCOES
                self.ignora_delay = False
                self.opcao_atual  += 1
            if teclas[K_UP]:
                self.pos_bola[1] -= DISTANCIA_OPCOES
                self.ignora_delay = False
                self.opcao_atual  -= 1
            
            if self.pos_bola[1] > 359:
                self.pos_bola[1] = 243
                self.opcao_atual = 0
            if self.pos_bola[1] < 243:
                self.pos_bola[1] = 359
                self.opcao_atual = 2
            
                    
    def renderiza(self):
        self.jogo.screen.blit(self.bg_image, self.bg_image.get_rect())
        
        rect_bola = self.bola.rect
        rect_bola.left = self.pos_bola[0]
        rect_bola.top  = self.pos_bola[1]
        
        self.bola.atualiza(pygame.time.get_ticks())
        self.jogo.screen.blit(self.bola.frame, rect_bola)