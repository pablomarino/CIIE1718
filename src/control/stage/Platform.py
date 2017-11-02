# -*- coding: utf-8 -*-
from view.MySprite import *


class Platform(MySprite):
    def __init__(self, manager, position, imageFile, origin_z, size):
        # Super
        MySprite.__init__(self, manager)
        # Dimensiones de la pantalla
        self.stageDimensions = manager.getScreen().get_size()
        self.z = origin_z

        # TODO cambiar el sprite de las plataformas para que no queden deformadas con el reescalamiento
        # Obtengo la imagen
        self.image = manager.getLibrary().load(imageFile, -1)
        # Guardo sus dimensiones
        self.imageW, self.imageH = self.image.get_size()
        # Alargamos la plataforma hasta el tamaño adecuado
        self.image = pygame.transform.scale(self.image, (self.imageW * size, self.imageH))

        # Calculamos la posición inicial de la plataforma
        new_position = (position[0] - size * self.imageW, position[1])
        # Creamos el rect de la plataforma
        self.rect = self.image.get_rect()
        # Asignamos la posición inicial como la posición de la plataforma
        self.setPosition(new_position)

    def update(self, clock, scroll):
        self.establecerPosicionPantalla((-scroll[0] * self.z, -scroll[1] * self.z))
