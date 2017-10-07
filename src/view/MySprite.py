# -*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *


class MySprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.posicion = (0, 0)
        self.velocidad = (0, 0)
        self.scroll   = (0, 0)

    def setPosition(self, posicion):
        self.posicion = posicion
        self.rect.left = self.posicion[0] - self.scroll[0]
        self.rect.bottom = self.posicion[1] - self.scroll[1]

    def getPosition(self):
        return self.posicion

    def establecerPosicionPantalla(self, scrollDecorado):
        self.scroll = scrollDecorado;
        (scrollx, scrolly) = self.scroll;
        (posx, posy) = self.posicion;
        self.rect.left = posx - scrollx;
        self.rect.bottom = posy - scrolly;

    def incrementarPosicion(self, incremento):
        (posx, posy) = self.posicion
        (incrementox, incrementoy) = incremento
        self.setPosition((posx+incrementox, posy+incrementoy))

    def update(self, clock):
        incrementox = self.velocidad[0]*clock
        incrementoy = self.velocidad[1]*clock
        self.incrementarPosicion((incrementox, incrementoy))