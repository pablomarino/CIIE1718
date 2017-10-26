# -*- coding: utf-8 -*-
from time import time

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

        self.data = data

        # Variables propias del jugador
        self.lives = 3
        self.health = 100
        self.maxHealth = 100
        self.attack = 50
        self.alive = True

    def getLives(self):
        return self.lives

    def increaseLives(self, value):
        self.lives = self.lives + 1

    def decreaseLives(self):
        self.lives = self.lives - 1
        if self.lives <= 0:
            self.lives = 0
            # TODO GameOver
            print "Game Over!"
            self.alive = False
        else:
            # TODO Actualizar el scroll cuando se reinicia la posición del jugador
            self.setPosition(self.data.getPlayerPositionAt("level_1"))
            self.setHealth(100)

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

    def decreaseHealth(self):
        self.health = self.health - 10
        # TODO reproducir sonido, y probablemente mover jugador hacia un lado, pegar un salto, o algo similar
        if self.health <= 0:
            self.decreaseLives()

    def getMaxHealth(self):
        return self.maxHealth

    def setMaxHealth(self, value):
        self.maxHealth = value

    def attack(self, pressedKeys):
        if pressedKeys[self.data.getSpace()]:
            print "test"
            Character.attack(self, ATTACK)

    def move(self, pressedKeys):
        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
        if self.alive:
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
        else:
            # Crear animación de jugador muerto
            Character.move(self, STOPPED)

    def update(self, platformGroup, clock, playerDisplacement, enemygroup):
        if self.alive:
            if pygame.sprite.spritecollideany(self, enemygroup) is not None:
                if self.tiempo_colision < time():
                    self.decreaseHealth()
                    pygame.mixer.Sound('../bin/assets/sounds/player/enemy_hit_1.wav').play()
                    self.tiempo_colision = time() + 1
        Character.update(self, platformGroup, clock, playerDisplacement)
