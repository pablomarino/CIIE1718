# -*- encoding: utf-8 -*-

import pygame, math

from control.stage.Background import *
from control.stage.Platform import *
import math


class Stage:
    def __init__(self, manager, data, player, platformGroup, spriteGroup, enemy1):
        self.manager = manager
        self.data = data
        self.player = player
        self.playerStartPosition = self.player.getPosition()
        self.scrollValue = list((0, 0))

        self.spriteGroup = spriteGroup

        self.itemStack = self.enemyStack = []

        self.platformGroup = platformGroup

        # TODO esto está metido a lo bestia para hacer pruebas
        self.enemy1 = enemy1
        self.enemyGroup = pygame.sprite.Group()
        self.enemyGroup.add(self.enemy1)

        self.setup()

    def setup(self):
        # Dimensiones de la pantalla
        self.stageWidth = int(self.data["dimensions"][0])
        self.stageHeight = int(self.data["dimensions"][1])

        # Gravedad
        self.gravityX = int(self.data["gravity"][0])
        self.gravityY = int(self.data["gravity"][1])

        # Cordenada Z de la capa de plataformas
        self.platforms_z = int(self.data["platforms_z"])

        # Genero la capa del Fondo
        self.background = BackGround(self.manager, self.data["bglayers"], self.player,
                                     (self.stageWidth, self.stageHeight))

        # Genero las Plataformas
        for p in self.data["platforms"]:
            platform = Platform(self.manager, p, self.player, (self.stageWidth, self.stageHeight), self.platforms_z)
            self.platformGroup.add(platform)

        '''
        # Items
        for i in self.data["items"]:
            item =Item(self.manager,i,self.stageWidth,self.stageHeight,self.player)
            self.itemStack.append(item)

        # Enemies
        for e in self.data["enemies"]:
            enemy = Enemy(self.manager, e, self.stageWidth, self.stageHeight, self.player)
            self.enemyStack.append(enemy)

        # Jugador
        '''

    def update(self, clock):
        self.manager.getScreen().fill(int(self.data["bgColor"], 16))  # en windows es necesario =\
        # Calculo la distancia entre la posicion inicial del jugador y la actual
        # Este valor se le pasa a Background y Platform para que realice el scroll
        # la componente x es 0 pq no hacemos scroll horizontal
        if self.player.getDoUpdateScroll():  # solo actualizo el scroll si esta saltando
            self.scrollValue = (
                0,  # (self.player.getPosition()[0]-self.playerStartPosition[0]),
                int(math.ceil(self.player.getPosition()[1] - self.playerStartPosition[1])))
        self.background.update(clock, self.scrollValue)
        for p in self.platformGroup:
            p.update(clock, self.scrollValue)
        self.player.update(self.platformGroup, clock)
        self.enemy1.update(self.platformGroup, clock)

    def draw(self):
        self.background.draw()
        self.platformGroup.draw(self.manager.getScreen())
        self.spriteGroup.draw(self.manager.getScreen())
        self.enemyGroup.draw(self.manager.getScreen())

    def events(self, *args):
        raise NotImplemented("Tiene que implementar el metodo eventos.")
