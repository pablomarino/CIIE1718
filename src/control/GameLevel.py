# -*- encoding: utf-8 -*-

import pygame
from control.Stage import Stage
from character.Player import Player


class GameLevel:
    def __init__(self, manager, data, id):
        self.manager = manager

        self.data = data
        self.level = data.getLevel(id)

        self.spriteGroup = pygame.sprite.Group()
        self.platformGroup = pygame.sprite.Group()
        self.itemGroup = pygame.sprite.Group()
        self.enemyGroup = pygame.sprite.Group()
        
        if self.level:
            self.player = Player(data, 'player')
            self.player.setPosition(data.getPlayerPositionAt(id))
            self.spriteGroup.add(self.player)
            
            self.stage = Stage(self.manager, self.level, self.player,self.platformGroup)
        else:
           print "Error no existe nivel con id ",id

    def update(self, clock):
        self.player.update(self.platformGroup, clock)
        self.stage.update(clock)

    def events(self):
        self.player.move(pygame.key.get_pressed())

    def draw(self):
        self.stage.draw()
        self.spriteGroup.draw(self.manager.getScreen())

