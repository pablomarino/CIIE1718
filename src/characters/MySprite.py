# -*- coding: utf-8 -*-

import pygame


class MySprite(pygame.sprite.Sprite):
    def __init__(self, manager):
        pygame.sprite.Sprite.__init__(self)
        self.manager = manager
        self.posicion = (0, 0)
        self.velocidad = (0, 0)
        self.scroll = (0, 0)
        self.screen_width = self.manager.getDataRetriever().getWidth()

    def setPosition(self, posicion):
        self.posicion = posicion
        self.rect.left = self.posicion[0] - self.scroll[0]
        self.rect.bottom = self.posicion[1] - self.scroll[1]

    def establecerPosicionPantalla(self, scrollDecorado):
        self.scroll = scrollDecorado
        (scrollx, scrolly) = self.scroll
        (posx, posy) = self.posicion
        self.rect.left = posx - scrollx
        self.rect.bottom = posy - scrolly

    def incrementarPosicion(self, incremento):
        (posx, posy) = self.posicion
        (incrementox, incrementoy) = incremento
        newposx = posx + incrementox
        if newposx <= 0:
            newposx = 0
        if newposx >= self.screen_width - self.getRect().width:
            # print self.getRect().width
            newposx = self.screen_width - self.getRect().width
        self.setPosition((newposx, posy + incrementoy))

    def update(self, clock):
        incrementox = self.velocidad[0] * clock
        incrementoy = self.velocidad[1] * clock
        self.incrementarPosicion((incrementox, incrementoy))

    def getGlobalPosition(self):
        return self.posicion

    def getLocalPosition(self):
        return self.rect.left, self.rect.bottom

    def getRect(self):
        return self.rect
