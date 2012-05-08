import pygame
from pygame.locals import *
from maputils import Mapa

ARQUIVO_MAPA = 'mapa.tmx'
FPS          = 60
TAMANHO_TELA = (640, 480)
OBSTACULOS   = ('city', 'plants')

def main():
    pygame.init()
    screen  = pygame.display.set_mode(TAMANHO_TELA)
    clock   = pygame.time.Clock()
    mapa    = Mapa(ARQUIVO_MAPA)
    rodando = True
    mapa_x  = 0
    mapa_y  = 0

    from personagens import Jogador

    jogador = Jogador([320, 200])

    while rodando:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                rodando = False

        #Obtem a lista de teclas pressionadas
        teclas  = pygame.key.get_pressed()
        andando = False
        old_pos = (jogador.posicao[0], jogador.posicao[1])

        if teclas[K_LEFT]:
            #mapa_x += 1
            if jogador.posicao[0] > jogador.rect.width / 2:
                jogador.posicao[0] -= 1
            jogador.direcao  = Jogador.ESQUERDA
            jogador.animacao = Jogador.ANDANDO
            andando = True
        if teclas[K_RIGHT]:
            #mapa_x -= 1
            jogador.posicao[0] += 1
            jogador.direcao  = Jogador.DIREITA
            jogador.animacao = Jogador.ANDANDO
            andando = True
        if teclas[K_UP]:
            #mapa_y += 1
            if jogador.posicao[1] > jogador.rect.height:
                jogador.posicao[1] -= 1
            jogador.direcao  = Jogador.CIMA
            jogador.animacao = Jogador.ANDANDO
            andando = True
        if teclas[K_DOWN]:
            #mapa_y -= 1
            jogador.posicao[1] += 1
            jogador.direcao  = Jogador.BAIXO
            jogador.animacao = Jogador.ANDANDO
            andando = True
        if teclas[K_ESCAPE]:
            rodando = False

        if not andando:
            jogador.animacao = Jogador.PARADO

        #Atualizando as variaveis do jogador
        jogador.update()
        #Atualizando a posicao do jogador de acordo com o deslocamento do mapa
        jogador_rect = jogador.rect.move(mapa_x, mapa_y)

        #Verificando as colisoes com os obstaculos
        if mapa.colide(jogador_rect, OBSTACULOS):
            jogador.posicao = [old_pos[0], old_pos[1]]

        #Logica de deslocamento do mapa na tela
        if jogador.posicao[0] + mapa_x > TAMANHO_TELA[0] * 0.75:
            mapa_x -= 1
        if jogador.posicao[0] + mapa_x < TAMANHO_TELA[0] * 0.25 and mapa_x < 0:
            mapa_x += 1
        if jogador.posicao[1] + mapa_y > TAMANHO_TELA[1] * 0.75:
            mapa_y -= 1
        if jogador.posicao[1] + mapa_y < TAMANHO_TELA[1] * 0.25 and mapa_y < 0:
            mapa_y += 1

        #Desenho do jogo na tela
        screen.blit(mapa.get_image(), (mapa_x, mapa_y))
        screen.blit(jogador.image, jogador_rect)
        pygame.display.flip()

if __name__ == "__main__": main()
