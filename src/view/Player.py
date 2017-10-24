# -*- coding: utf-8 -*-
from view.Character import *


class Player(Character):
    "Cualquier personaje del juego"

    def __init__(self, manager, data, id):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        # TODO cambiar el constructor de Character por (self, data, id)
        # Dentro del propio constructor elige el sprite y demás valores buscando en el dataRetriever
        Character.__init__(self,
                           manager,
                           data,
                           data.getPlayerSheet(id),
                           data.getPlayerSheetCoords(id),
                           [5, 6, 5, 4],
                           data.getPlayerSpeed(),
                           data.getPlayerJumpSpeed(),
                           data.getPlayerAnimationDelay())

        # TODO crear variables con los valores necesarios para el jugador (vidas, salud... etc)
        self.lives = 3
        self.health = 100
        self.maxHealth = 100
        self.attack = 50;

    def getLives(self):
        return self.lives

    def increaseLives(self, value):
        self.lives = self.lives + 1

    def decreaseLives(self):
        self.lives = self.lives - 1
        if self.lives <= 0:
            self.lives = 0
            # TODO GameOver

    def getHealth(self):
        return self.health

    def setHealth(self, value):
        self.health = value
        # Check for overflow in players health
        if self.health <= 0:
            self.health = 0
            # TODO matar al jugador
        if self.health >= self.maxHealth:
            self.health = self.maxHealth

    def getMaxHealth(self):
        return self.maxHealth

    def setMaxHealth(self, value):
        self.maxHealth = value

    def attack(self, pressedKeys):
        if pressedKeys[self.data.getSpace()]:
            print "test"

    def move(self, pressedKeys):
        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
        if pressedKeys[self.data.getKeyUp()]:
            Character.move(self, UP)
            # TODO esto está mal, se reproduce siempre el sonido, aunque el jugador no salte
            pygame.mixer.Sound('../bin/assets/sounds/player/salto.wav').play()
        elif pressedKeys[self.data.getKeyLeft()]:
            Character.move(self, LEFT)
        elif pressedKeys[self.data.getKeyRight()]:
            Character.move(self, RIGHT)
        else:
            Character.move(self, STOPPED)
