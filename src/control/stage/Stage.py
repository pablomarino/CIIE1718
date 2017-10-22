# -*- encoding: utf-8 -*-

import pygame, math

from control.stage.Background import *
from control.stage.Platform import *
from control.HUD import HUD
import math


class Stage:
    def __init__(self, manager, data, player, platformGroup, spriteGroup, enemyGroup):
        self.manager = manager
        self.data = data
        self.player = player
        self.playerStartPosition = self.player.getGlobalPosition()
        self.playerDisplacement = list((0, 0))
        self.spriteGroup = spriteGroup
        self.itemStack = self.enemyStack = []
        self.platformGroup = platformGroup
        self.enemyGroup = enemyGroup
        self.setup()

    def setup(self):
        # Dimensiones de la pantalla
        self.levelDimensions = ((int(self.data["dimensions"][0]), int(self.data["dimensions"][1])))

        # Cordenada Z de la capa de plataformas
        self.platforms_z = int(self.data["platforms_z"])

        # Genero la capa del Fondo
        self.background = BackGround(self.manager, self.data["bglayers"], self.player, self.levelDimensions)

        # Genero las Plataformas
        for p in self.data["platforms"]:
            platform = Platform(self.manager, p, self.platforms_z)
            self.platformGroup.add(platform)

        # Creamos el HUD
        self.HUD = HUD(self.manager.getDataRetriever(), self.manager.getScreen(), self.player)

        '''
        # Items
        for i in self.data["items"]:
            item =Item(self.manager,i,self.levelWidth,self.levelHeight,self.player)
            self.itemStack.append(item)
        '''
        '''
        # Enemies
        for e in self.data["enemies"]:
            enemy = Enemy(self.manager, e, self.levelWidth, self.levelHeight, self.player)
            self.enemyStack.append(enemy)
        '''

    def update(self, clock):
        self.manager.getScreen().fill(int(self.data["bgColor"], 16))  # en windows es necesario =\ en mac no
        # Calculo la distancia entre la posicion inicial del jugador y la actual
        # Este valor se le pasa a Background y Platform para que realice el scroll
        if (
                    self.player.getDoUpdateScroll() & self.getDoUpdateScroll()):  # solo actualizo el scroll si esta saltando o cayendo
            self.playerDisplacement = (
                0,  # int(math.ceil(self.playerStartPosition[0]-self.player.getPosition()[0])),
                int(math.ceil(self.playerStartPosition[1] - self.player.getGlobalPosition()[1]))
            )
        print "player ", self.player.getGlobalPosition()[1], self.player.getLocalPosition()[1]
        self.background.update(clock, self.playerDisplacement)

        for p in self.platformGroup:
            p.update(clock, self.playerDisplacement)

        self.player.update(self.platformGroup, clock, self.playerDisplacement)
        self.enemyGroup.update(self.platformGroup, clock, self.playerDisplacement)

    def draw(self):
        self.background.draw()
        self.platformGroup.draw(self.manager.getScreen())
        self.spriteGroup.draw(self.manager.getScreen())
        self.enemyGroup.draw(self.manager.getScreen())
        self.HUD.draw()

    def events(self, *args):
        raise NotImplemented("Tiene que implementar el metodo eventos.")

    def getDoUpdateScroll(self):
        # TODO Implementar
        '''
        retval = False

        if self.player.getPosition()[1] > self.manager.getScreen().get_size()[1]/2:
            retval = True
            print self.playerDisplacement
        '''
        retval = True
        return retval
