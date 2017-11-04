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
                           data.getCharacterSpeed("player"),
                           data.getCharacterJumpSpeed("player"),
                           data.getPlayerAnimationDelay())
        self.numPostura = SPRITE_JUMPING  # En que postura esta inicialmente
        self.data = data
        self.collision_rect = None
        self.manager = manager
        # Variables propias del jugador
        self.lives = 3
        self.health = 100
        self.maxHealth = 100
        self.attack = 50
        self.alive = True

    def getCollisionRect(self):
        return self.collision_rect

    def updateCollisionRect(self):
        # pygame.Rect(left, top, width, height)
        self.collision_rect = pygame.Rect(self.getRect().left + self.getRect().width / 2 - 3,
                                          self.getRect().bottom - 5,
                                          6, 5)

    def getLives(self):
        return self.lives

    def increaseLives(self):
        self.lives = self.lives + 1

    def decreaseLives(self):
        self.lives = self.lives - 1
        if self.lives <= 0:
            self.lives = 0
            # TODO GameOver menu
            print "Game Over!"
            self.alive = False
        else:
            self.stage.resetScroll()
            self.setPosition(self.data.getPlayerPositionAt("level_1"))
            self.setHealth(100)

    def getHealth(self):
        return self.health

    def setStage(self,s): self.stage = s

    def setHealth(self, value):
        self.health = value
        # Check for overflow in players health
        if self.health <= 0:
            self.health = 0
            # TODO matar al jugador
        if self.health >= self.maxHealth:
            self.health = self.maxHealth

    def increaseHealth(self):
        self.health = self.health + 5

    def decreaseHealth(self):
        if self.tiempo_colision < time():
            self.health = self.health - 10
            # TODO mover jugador hacia un lado, pegar un salto, o algo similar
            if self.health <= 0:
                self.decreaseLives()
            pygame.mixer.Sound('../bin/assets/sounds/player/enemy_hit_1.wav').play()
            self.tiempo_colision = time() + 1

    def getMaxHealth(self):
        return self.maxHealth

    def setMaxHealth(self, value):
        self.maxHealth = value

    def attack(self, pressedKeys):
        if pressedKeys[self.data.getSpace()]:
            print "test"
            Character.attack(self, ATTACK)

    def move(self, pressedKeys):
        # TODO Cuando el jugador está cayendo en diagonal, mantiene dirección a pesar de que no haya teclas pulsadas

        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
        if self.alive:
            if pressedKeys[self.data.getKeyUp()] and pressedKeys[self.data.getKeyLeft()]:
                Character.move(self, UPLEFT)
            elif pressedKeys[self.data.getKeyUp()] and pressedKeys[self.data.getKeyRight()]:
                Character.move(self, UPRIGHT)
            elif pressedKeys[self.data.getKeyUp()]:
                Character.move(self, UP)
            elif pressedKeys[self.data.getKeyDown()] and pressedKeys[self.data.getKeyLeft()]:
                Character.move(self, DOWNLEFT)
            elif pressedKeys[self.data.getKeyDown()] and pressedKeys[self.data.getKeyRight()]:
                Character.move(self, DOWNRIGHT)
            elif pressedKeys[self.data.getKeyDown()]:
                Character.move(self, DOWN)
            elif pressedKeys[self.data.getKeyLeft()]:
                Character.move(self, LEFT)
            elif pressedKeys[self.data.getKeyRight()]:
                Character.move(self, RIGHT)
            else:
                Character.move(self, STOPPED)
        else:
            # Crear animación de jugador muerto
            Character.move(self, STOPPED)

    def update(self,  clock, playerDisplacement, platformGroup,enemyGroup, itemGroup):
        if self.alive:
            enemyCol = pygame.sprite.spritecollideany(self, enemyGroup)
            itemCol = pygame.sprite.spritecollideany(self, itemGroup)

            if enemyCol is not None:
                enemyCol.behave(self, itemGroup)  # cada item realiza una accion propia

            if  itemCol is not None:
                itemCol.behave(self,itemGroup) # cada item realiza una accion propia


            # Call update in the super class
            Character.update(self, platformGroup, clock, playerDisplacement)

            # Update collision rect
            self.updateCollisionRect()
