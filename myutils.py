import os
import pygame

IMG_DIR = ''

def load_image(filename):
    return pygame.image.load(os.path.join(IMG_DIR, filename)).convert()

class Spritesheet:
    def __init__(self, filename):
        self.sheet = load_image(filename)
    def imgat(self, rect, colorkey = None):
        rect = pygame.Rect(rect)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    def imgsat(self, rects, colorkey = None):
        imgs = []
        for rect in rects:
            imgs.append(self.imgat(rect, colorkey))
        return imgs

class Animacao:
    def __init__(self, spritesheet, fps, rects, incremento=1):
        self.rects        = rects
        self.incremento   = incremento
        self.frameAtual   = 0
        self.delay        = 1000 / fps
        self.ultimoUpdate = 0
        self.frames       = spritesheet.imgsat(self.rects, -1)
        self.frame        = self.frames[self.frameAtual]
        self.rect         = pygame.Rect(self.rects[self.frameAtual])

    def atualiza(self, tempoAtual):
        if tempoAtual - self.ultimoUpdate > self.delay:
            self.ultimoUpdate = tempoAtual
            self.frameAtual   = (self.frameAtual + 1) % len(self.frames)
            self.frame        = self.frames[self.frameAtual]
            self.rect         = pygame.Rect(self.rects[self.frameAtual])