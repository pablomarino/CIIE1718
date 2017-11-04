# -*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *


class AssetLoader:
    instance = None

    class __AssetLoader:
        def __init__(self):
            self.resources = {}

    def __init__(self):
        if not AssetLoader.instance:
            AssetLoader.instance = AssetLoader.__AssetLoader()
        else:
            print __name__, 'Singleton already instantiated.'

    def getResources(self):
        return self.instance.resources

    def load(self, file, colorkey=None):
        # Transparencia
        # -1 auto
        # metele un color que no haya si no quieres transparencia =P
        # 0x Hexadecimal

        # Si el fichero está entre los recursos ya cargados
        if file in self.instance.resources:
            # Se devuelve ese recurso
            return self.instance.resources[file]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga la imagen indicando la carpeta en la que está
            try:
                imagen = pygame.image.load(file)
            except pygame.error, message:
                print 'Cannot load image:', file
                raise SystemExit, message
            imagen = imagen.convert_alpha()#.convert()
            if colorkey is not 0:
                if colorkey is -1:
                    colorkey = imagen.get_at((0, 0))
                else:
                    colorkey = int(colorkey, 16)

                imagen.set_colorkey(colorkey, RLEACCEL)

            # Se almacena
            self.instance.resources[file] = imagen
            # Se devuelve
            return imagen

    def loadCoordsFile(self, file):
        # Si el nombre de archivo está entre los recursos ya cargados
        if file in self.instance.resources:
            # Se devuelve ese recurso
            return self.instance.resources[file]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga el recurso indicando el nombre de su carpeta
            # fullname = os.path.join('../bin/assets/sprites/main_characters', nombre)
            # fullname = os.path.join('', nombre)
            pfile = open(file, 'r')
            coords = pfile.read()
            pfile.close()
            # Se almacena
            self.instance.resources[file] = coords
            # Se devuelve
            return coords
