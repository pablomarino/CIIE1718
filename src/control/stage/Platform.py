# -*- coding: utf-8 -*-
from view.MySprite import *


class Platform(MySprite):
    def __init__(self, manager, position, imageFile, origin_z, size):
        # Super
        MySprite.__init__(self, manager)

        # Dimensiones de la pantalla
        self.stageDimensions = manager.getScreen().get_size()
        self.z = origin_z

        # Obtengo la imagen
        self.image = manager.getLibrary().load(imageFile, -1)

        # Guardo sus dimensiones
        self.imageW, self.imageH = self.image.get_size()

        # Creamos el rect de la plataforma
        self.rect = pygame.Rect(0, 0, self.imageW * size, self.imageH)  # self.image.get_rect()

        # Calculamos la posición inicial de la plataforma
        new_position = (position[0] - size * self.imageW, position[1])
        self.setPosition(new_position)

        comp = self.image.copy()
        self.image = pygame.transform.scale(self.image, (self.imageW * size, self.imageH))
        for i in range(0,size):
            self.image.blit(comp,(self.imageW*i,0))

    def draw(self):
        pass

    def update(self, clock, scroll):
        self.establecerPosicionPantalla((-scroll[0] * self.z, -scroll[1] * self.z))
