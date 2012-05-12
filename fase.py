import math
import pygame
from pygame.locals import *
from maputils import Mapa
from config import DEBUG
from tela import Tela

ESPACAMENTO_LINHAS = 10
OFFSET_X           = 10

class Fase(Tela):
    def __init__(self, jogo, arquivo_mapa, obstaculos, posicao_jogador):
        super(Fase, self).__init__(jogo)
        from personagens import Jogador
        
        self.obstaculos     = obstaculos
        self.mapa           = Mapa(arquivo_mapa)
        self.mapa_x         = 0
        self.mapa_y         = 0
        self.jogador        = Jogador(posicao_jogador)
        self.exibindo_texto = False
        self.font           = pygame.font.Font(None, 30)
        self.old_teclas     = {}
        
    def processa_eventos(self, eventos):
        from personagens import Jogador

        for event in eventos:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.jogo.irParaTela(self.jogo.MENU)
        
        #Obtem a lista de teclas pressionadas
        andando = False
        old_pos = (self.jogador.posicao[0], self.jogador.posicao[1])
        
        teclas = pygame.key.get_pressed()
        if self.old_teclas:
            self.process_key_typed(self.diferenca(teclas, self.old_teclas))
            self.process_key_released(self.diferenca(self.old_teclas, teclas))
        self.old_teclas = teclas
        
        if self.exibindo_texto:
            pass
        else:
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
            if teclas[K_p]:
                self.exibir_texto("Jogo Pausado - Pressione ENTER para continuar ...")

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

            if self.mapa_x < -160:
                self.mapa_x = -160

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
        
        if self.exibindo_texto:
            self.jogo.screen.fill((255, 255, 255, 0), Rect(OFFSET_X / 2, self.texto_y - OFFSET_X / 2, self.jogo.tamanho_tela[0] - OFFSET_X, self.altura_texto + OFFSET_X), BLEND_ADD)
            y = self.texto_y
            texto_to_draw = ' '.join(self.linhas[self.linha_atual])[0 : self.letra_atual + 1]
            
            for index, linha in enumerate(self.linhas):
                if index < self.linha_atual:
                    texto = self.font.render(' '.join(linha), True, (0, 0, 0))
                elif index == self.linha_atual:
                    texto = self.font.render(texto_to_draw, True, (0, 0, 0))
                    
                if index <= self.linha_atual:
                    self.jogo.screen.blit(texto, (OFFSET_X, y))
                    y += texto.get_rect().height + ESPACAMENTO_LINHAS
                
                if self.escrevendo_texto:
                    tempo_atual = pygame.time.get_ticks()
                    if tempo_atual - self.tempo_ultima_letra > 50:
                        self.letra_atual += 1
                        if self.letra_atual >= len(' '.join(self.linhas[self.linha_atual])):
                            self.letra_atual = 0
                            self.linha_atual += 1
                            if self.linha_atual >= len(self.linhas):
                                self.escrevendo_texto = False
                                self.linha_atual = len(self.linhas) - 1
                                self.letra_atual = len(' '.join(self.linhas[self.linha_atual])) - 1
                        self.tempo_ultima_letra = tempo_atual
        
        if DEBUG:
            pygame.draw.rect(self.jogo.screen, (0, 255, 0), self.jogador_col_rect, 1)
            
            if self.mapa.get_collision_rects(self.jogador.get_collision_rect(), self.obstaculos):
                rects = self.mapa.get_collision_rects(self.jogador.get_collision_rect(), self.obstaculos)
                pygame.draw.rect(self.jogo.screen, (255, 0, 0), rects[0].move(self.mapa_x, self.mapa_y), 1)
                pygame.draw.rect(self.jogo.screen, (255, 0, 0), rects[1].move(self.mapa_x, self.mapa_y), 1)
        
            for objeto in self.mapa.tmxhandler.objects:
                pygame.draw.rect(self.jogo.screen, (255, 0, 0), objeto.rect.move(self.mapa_x, self.mapa_y), 1)
                
    def exibir_texto(self, texto):
        self.exibindo_texto = True
        self.indice_texto   = 0
        
        tamanho_texto = self.font.size(texto)
        
        palavras = texto.split()
        linha    = []
        linhas   = [linha,]
        tmp_str  = ''
        
        for palavra in palavras:
            if OFFSET_X + self.font.size(' '.join([tmp_str, palavra]))[0] <= self.jogo.tamanho_tela[0] - OFFSET_X:
                linha.append(palavra)
                tmp_str = ' '.join([tmp_str, palavra])
            else:
                linha = [palavra, ]
                linhas.append(linha)
                tmp_str = palavra
        
        self.linhas       = linhas
        qtd_linhas        = len(linhas)
        self.altura_texto = qtd_linhas * tamanho_texto[1] + (qtd_linhas - 1) * ESPACAMENTO_LINHAS
        self.texto_y      = (self.jogo.tamanho_tela[1] - self.altura_texto) / 2
        self.letra_atual  = 0
        self.linha_atual  = 0
        self.tempo_ultima_letra = pygame.time.get_ticks()
        self.escrevendo_texto   = True

    def process_key_typed(self, teclas):
        if teclas[K_RETURN]:
            if self.exibindo_texto:
                if self.escrevendo_texto:
                    self.linha_atual = len(self.linhas) - 1
                    self.letra_atual = len(' '.join(self.linhas[self.linha_atual])) - 1
                    self.escrevendo_texto = False
                else:
                    self.exibindo_texto = False
        
    def process_key_released(self, teclas):
        pass

    def diferenca(self, tupla_1, tupla_2):
        resultado = []
        for i in range(len(tupla_1)): resultado.append(tupla_1[i] and not tupla_2[i])
        return tuple(resultado)