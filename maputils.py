from pygame.locals import Rect
import pygame
from pygame.locals import *
from pygame import Rect
from xml import sax

class MapObject(object):
    def __init__(self, name, type, x, y, width, height):
        self.name = name
        self.type = type
        self.x    = x
        self.y    = y
        self.rect = Rect(x, y, width, height)
        self.properties = {}

class Tileset(object):
    def __init__(self, file, tile_width, tile_height):
        image = pygame.image.load(file).convert_alpha()
        if not image:
            print "Error creating new Tileset: file %s not found" % file
        self.tile_width  = tile_width
        self.tile_height = tile_height
        self.tiles = []
        for line in xrange(image.get_height()/self.tile_height):
            for column in xrange(image.get_width()/self.tile_width):
                pos = Rect(
                        column * self.tile_width,
                        line * self.tile_height,
                        self.tile_width,
                        self.tile_height)
                self.tiles.append(image.subsurface(pos))

    def get_tile(self, gid):
        return self.tiles[gid]

class TMXHandler(sax.ContentHandler):
    def __init__(self):
        self.width         = 0
        self.height        = 0
        self.tile_width    = 0
        self.tile_height   = 0
        self.columns       = 0
        self.lines         = 0
        self.properties    = {}
        self.image         = None
        self.tileset       = None
        self.layers        = {}
        self.objects       = []
        self.readingMap    = False
        self.readingObject = False

    def startElement(self, name, attrs):
        # get most general map informations and create a surface
        if name == 'map':
            self.columns     = int(attrs.get('width', None))
            self.lines       = int(attrs.get('height', None))
            self.tile_width  = int(attrs.get('tilewidth', None))
            self.tile_height = int(attrs.get('tileheight', None))
            self.width       = self.columns * self.tile_width
            self.height      = self.lines * self.tile_height
            self.image       = pygame.Surface([self.width, self.height]).convert()
            self.readingMap  = True
        # create a tileset
        elif name == "image":
            source = attrs.get('source', None)
            self.tileset = Tileset(source, self.tile_width, self.tile_height)
        # store additional properties.
        elif name == 'property':
            if self.readingMap:
                self.properties[attrs.get('name', None)] = attrs.get('value', None)
            if self.readingObject:
                self.currentObject.properties[attrs.get('name', None)] = attrs.get('value', None)
        # starting counting
        elif name == 'layer':
            self.line   = 0
            self.column = 0
            self.currentLayer = attrs.get('name', None)
            self.layers[self.currentLayer] = []
        # get information of each tile and put on the surface using the tileset
        elif name == 'tile':
            gid = int(attrs.get('gid', None)) - 1
            if gid < 0 : gid = 0

            if gid > 0:
                tile = self.tileset.get_tile(gid)
                pos = (self.column * self.tile_width, self.line * self.tile_height)
                self.image.blit(tile, pos)
                self.layers[self.currentLayer].append(Rect(pos[0], pos[1], self.tile_width, self.tile_height))
                
                if self.currentLayer in ('city', 'plants'):
                    pygame.draw.rect(self.image, (0, 0, 255), Rect(pos[0], pos[1], self.tile_width, self.tile_height), 1)

            self.column += 1
            if(self.column >= self.columns):
                self.column = 0
                self.line  += 1
        elif name == 'objectgroup':
            self.currentObjectGroup = attrs.get('name', None)
            self.object_width       = int(attrs.get('width', None))
            self.object_height      = int(attrs.get('height', None))
        elif name == 'object':
            self.readingMap    = False
            self.readingObject = True
            
            name  = attrs.get('name', None)
            _type = attrs.get('type', None)
            x     = int(attrs.get('x', None))
            y     = int(attrs.get('y', None))
            
            self.currentObject = MapObject(name, _type, x, y, self.object_width, self.object_height)
            self.objects.append(self.currentObject)

    # just for debugging
    def endDocument(self):
        print self.width, self.height, self.tile_width, self.tile_height
        print self.properties
        print self.image

class Mapa(object):
    def __init__(self, arquivo_mapa):
        parser = sax.make_parser()
        self.tmxhandler = TMXHandler()
        parser.setContentHandler(self.tmxhandler)
        print 'Carregando o mapa %s ...' % (arquivo_mapa,)
        parser.parse(arquivo_mapa)
        print 'Pronto !'

    def get_image(self):
        return self.tmxhandler.image

    def get_camada(self, nome_camada):
        return self.tmxhandler.layers[nome_camada]

    def colide(self, jogador_rect, camadas_obstaculos):
        for camada in camadas_obstaculos:
            for obstaculo in self.get_camada(camada):
                if obstaculo.colliderect(jogador_rect):
                    return True
        return False
    
    def get_collision_rects(self, jogador_rect, camadas_obstaculos):
        for camada in camadas_obstaculos:
            for obstaculo in self.get_camada(camada):
                if obstaculo.colliderect(jogador_rect):
                    return (jogador_rect, obstaculo)
        return None
    
    def get_collision_objects(self, jogador_rect):
        for objeto in self.tmxhandler.objects:
            if objeto.rect.colliderect(jogador_rect):
                return objeto
        return None