import pygame
from pygame.locals import *
import pygame.sprite
from myutils import Spritesheet, Animacao

class Jogador(pygame.sprite.Sprite):
    #Carregamento do spritesheet
    spritesheet = Spritesheet('imagens/personagem.png')

    #Definicao das direcoes
    CIMA     = 0
    DIREITA  = 1
    BAIXO    = 2
    ESQUERDA = 3

    #Definicao das animacoes
    PARADO  = 'parado'
    ANDANDO = 'andando'

    def __init__(self, posicaoInicial, fps = 15):
        pygame.sprite.Sprite.__init__(self)
        self.posicao = posicaoInicial

        self.animacoes = {
            'parado' : [
                Animacao(Jogador.spritesheet, fps, [(0,   7, 32, 48),]),
                Animacao(Jogador.spritesheet, fps, [(0,  55, 32, 48),]),
                Animacao(Jogador.spritesheet, fps, [(0, 102, 32, 48),]),
                Animacao(Jogador.spritesheet, fps, [(0, 151, 32, 48),]),
            ],
            'andando' : [
                Animacao(Jogador.spritesheet, fps, [(0,   7, 32, 48), (36,   7, 32, 48), (73,   7, 32, 48)]),
                Animacao(Jogador.spritesheet, fps, [(0,  55, 32, 48), (36,  55, 32, 48), (73,  55, 32, 48)]),
                Animacao(Jogador.spritesheet, fps, [(0, 102, 32, 48), (36, 102, 32, 48), (73, 102, 32, 48)]),
                Animacao(Jogador.spritesheet, fps, [(0, 151, 32, 48), (36, 151, 32, 48), (73, 151, 32, 48)]),
            ],
        }

        self.direcao  = Jogador.DIREITA
        self.animacao = Jogador.PARADO

    def update(self):
        animacao = self.animacoes[self.animacao][self.direcao]
        animacao.atualiza(pygame.time.get_ticks())
        self.image  = animacao.frame
        self.rect   = animacao.rect
        self.rect.x = self.posicao[0]
        self.rect.y = self.posicao[1]
        
        
    def get_collision_rect(self):
        return Rect(self.rect.x, self.rect.y + self.rect.height / 2, self.rect.width, self.rect.height / 2)