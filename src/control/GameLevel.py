# -*- encoding: utf-8 -*-

import pygame
from characters.Enemy import *
from characters.Player import Player

from src.stage.regular.Stage import *


class GameLevel:
    def __init__(self, manager, data, id):
        self.manager = manager

        self.data = data
        self.level = data.getLevel(id)

        pygame.mixer.music.load(self.data.getMusicFile())
        # pygame.mixer.music.play()

        self.spriteGroup = pygame.sprite.Group()
        self.platformGroup = pygame.sprite.Group()
        self.itemGroup = pygame.sprite.Group()
        self.enemyGroup = pygame.sprite.Group()

        if self.level:
            # TODO tener en cuenta, valores de vida y demás se reinician al pasar de nivel,se crea un jugador nuevo
            self.player = Player(manager, data, 'player')
            self.player.setPosition(data.getPlayerPositionAt(id))
            self.spriteGroup.add(self.player)

            self.stage = Stage(self.manager, self.level, self.player, self.platformGroup, self.spriteGroup,
                               self.enemyGroup,self.itemGroup)
            self.player.setStage(self.stage)
        else:
            print "Error no existe nivel con id ", id

    def update(self, clock):
        self.stage.update(clock)
        # self.player.update(self.platformGroup, clock)

    def events(self, events_list):
        self.stage.events(events_list)

    def draw(self):
        self.stage.draw()
        # self.spriteGroup.draw(self.manager.getScreen())
        pass
