# -*- encoding: utf-8 -*-

# -------------------------------------------------
# Clase Escena con lo metodos abstractos
import pygame
from pygame.locals import *
from control.Stage import Stage
from data.DataRetriever import DataRetriever
from character.Player import Player


class GameLevel:
    def __init__(self, manager, data, id):
        self.manager = manager
        self.data = data
        self.level = data.getLevel(id)
        if self.level:
            self.stage = Stage(self.manager, self.level)

            ## Modificado para probar jugador
            self.player = Player()
            self.player.setPosition((200, 551))
            self.grupoSprites = pygame.sprite.Group( self.player)
            self.grupoPlataformas = pygame.sprite.Group()

        else:
           print "Error no existe nivel con id ",id

    def update(self, clock):
        self.stage.update(clock)
        # Update character
        self.player.update(self.grupoPlataformas, clock)
      

    def events(self):
        pressedKeys = pygame.key.get_pressed()
        self.player.move(pressedKeys, K_UP, K_LEFT, K_RIGHT)
        # raise NotImplemented("Tiene que implementar el metodo eventos.")

    def draw(self):
        self.stage.draw()
        ## Draw character
        self.grupoSprites.draw(self.manager.getScreen())

