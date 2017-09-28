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
            print ("Singleton already instantiated.")

    def getResources(self):
        return self.instance.resources
    def Load(self, file, colorkey = None):
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
            imagen = imagen.convert()
            if colorkey is not None:
                if colorkey is -1:
                    colorkey = imagen.get_at((0, 0))
                imagen.set_colorkey(colorkey, RLEACCEL)
            # Se almacena
            self.instance.resources[file] = imagen
            # Se devuelve
            return imagen
