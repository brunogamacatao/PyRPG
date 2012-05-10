import pygame
from pygame.locals import *
from maputils import Mapa
from config import DEBUG
from tela import Tela

class Fase(Tela):
    def __init__(self, jogo, arquivo_mapa, obstaculos, posicao_jogador):
        super(Fase, self).__init__(jogo)
        from personagens import Jogador
        
        self.obstaculos = obstaculos
        self.mapa       = Mapa(arquivo_mapa)
        self.mapa_x     = 0
        self.mapa_y     = 0
        self.jogador    = Jogador(posicao_jogador)
        
    def processa_eventos(self, eventos):
        from personagens import Jogador

        for event in eventos:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.jogo.irParaTela(self.jogo.MENU)

        
        #Obtem a lista de teclas pressionadas
        teclas  = pygame.key.get_pressed()
        andando = False
        old_pos = (self.jogador.posicao[0], self.jogador.posicao[1])

        if teclas[K_LEFT]:
            if self.jogador.posicao[0] > 0:
                self.jogador.posicao[0] -= 1
            self.jogador.direcao  = Jogador.ESQUERDA
            self.jogador.animacao = Jogador.ANDANDO
            andando = True
        if teclas[K_RIGHT]:
            self.jogador.posicao[0] += 1
            self.jogador.direcao  = Jogador.DIREITA
            self.jogador.animacao = Jogador.ANDANDO
            andando = True
        if teclas[K_UP]:
            if self.jogador.posicao[1] > 0:
                self.jogador.posicao[1] -= 1
            self.jogador.direcao  = Jogador.CIMA
            self.jogador.animacao = Jogador.ANDANDO
            andando = True
        if teclas[K_DOWN]:
            self.jogador.posicao[1] += 1
            self.jogador.direcao  = Jogador.BAIXO
            self.jogador.animacao = Jogador.ANDANDO
            andando = True

        if not andando:
            self.jogador.animacao = Jogador.PARADO

        #Atualizando as variaveis do jogador
        self.jogador.update()
        #Atualizando a posicao do jogador de acordo com o deslocamento do mapa
        self.jogador_img_rect = self.jogador.rect.move(self.mapa_x, self.mapa_y)
        self.jogador_col_rect = self.jogador.get_collision_rect().move(self.mapa_x, self.mapa_y)

        #Verificando as colisoes com os obstaculos
        if self.mapa.colide(self.jogador.get_collision_rect(), self.obstaculos):
            self.jogador.posicao = [old_pos[0], old_pos[1]]

        # Logica de deslocamento do mapa na tela
        if self.jogador.posicao[0] + self.mapa_x > self.jogo.tamanho_tela[0] * 0.75:
            self.mapa_x -= 1
        if self.jogador.posicao[0] + self.mapa_x < self.jogo.tamanho_tela[0] * 0.25 and self.mapa_x < 0:
            self.mapa_x += 1
        if self.jogador.posicao[1] + self.mapa_y > self.jogo.tamanho_tela[1] * 0.75:
            self.mapa_y -= 1
        if self.jogador.posicao[1] + self.mapa_y < self.jogo.tamanho_tela[1] * 0.25 and self.mapa_y < 0:
            self.mapa_y += 1

        objeto = self.mapa.get_collision_objects(self.jogador.get_collision_rect())
        if objeto:
            if objeto.properties.has_key('para'):
                self.jogo.irParaTela(getattr(self.jogo, objeto.properties['para']))
            elif objeto.properties.has_key('voltar'):
                dx = int(objeto.properties['dx'])
                dy = int(objeto.properties['dy'])
                self.jogo.voltar(dx, dy)

    def renderiza(self):
        #Desenho do jogo na tela
        self.jogo.screen.blit(self.mapa.get_image(), (self.mapa_x, self.mapa_y))
        self.jogo.screen.blit(self.jogador.image, self.jogador_img_rect)
        
        if DEBUG:
            pygame.draw.rect(self.jogo.screen, (0, 255, 0), self.jogador_col_rect, 1)
            
            if self.mapa.get_collision_rects(self.jogador.get_collision_rect(), self.obstaculos):
                rects = self.mapa.get_collision_rects(self.jogador.get_collision_rect(), self.obstaculos)
                pygame.draw.rect(self.jogo.screen, (255, 0, 0), rects[0].move(self.mapa_x, self.mapa_y), 1)
                pygame.draw.rect(self.jogo.screen, (255, 0, 0), rects[1].move(self.mapa_x, self.mapa_y), 1)
        
            for objeto in self.mapa.tmxhandler.objects:
                pygame.draw.rect(self.jogo.screen, (255, 0, 0), objeto, 1)
