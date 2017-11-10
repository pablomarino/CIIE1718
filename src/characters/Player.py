# -*- coding: utf-8 -*-
from time import time

from characters.Character import *


class Player(Character):
    "Cualquier personaje del juego"

    def __init__(self, manager, data, id, player_stats):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Character.__init__(self,
                           manager,
                           data,
                           data.getPlayerSheet(id),
                           data.getPlayerSheetCoords(id),
                           [5, 6, 5, 4, 1],
                           data.getCharacterSpeed("player"),
                           data.getCharacterJumpSpeed("player"),
                           data.getPlayerAnimationDelay())
        # Variables generales
        self.data = data
        self.manager = manager

        # Variables de movimiento del jugador
        self.numPostura = SPRITE_JUMPING
        self.readyToJump = True
        self.readyToAttack = True
        self.collision_rect = pygame.Rect(self.getRect().left + self.getRect().width / 2 - 3,
                                          self.getRect().bottom - 5,
                                          6, 5)

        # Variables propias del jugador
        self.lives = player_stats[0]
        self.points = player_stats[3]
        self.maxHealth = player_stats[1]
        self.health = player_stats[2]
        self.attack = 50
        self.alive = True

    def getCollisionRect(self):
        return self.collision_rect

    def updateCollisionRect(self):
        self.collision_rect = pygame.Rect(self.getRect().left + self.getRect().width / 2 - 3,
                                          self.getRect().bottom - 5,
                                          6, 5)

    def setAttacking(self, value):
        self.attacking = value
        self.readyToAttack = not value

    def getLives(self):
        return self.lives

    def increaseLives(self):
        self.lives = self.lives + 1

    def getPoints(self):
        return self.points

    def increasePoints(self):
        self.points = self.points + 5

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
            self.numPostura = SPRITE_JUMPING
            self.setHealth(self.getMaxHealth())

    def getHealth(self):
        return self.health

    def setHealth(self, value):
        self.health = value

    def increaseHealth(self):
        if self.health < self.getMaxHealth():
            self.health = self.health + 10

    def decreaseHealth(self, e):
        if self.tiempo_colision < time():
            self.health = self.health - 10
            self.backOff(e)
            if self.health <= 0:
                self.decreaseLives()
                # self.die()
            # TODO mover el sonido para la colisión con el enemigo, no aquí
            pygame.mixer.Sound('../bin/assets/sounds/player/enemy_hit_1.wav').play()
            self.tiempo_colision = time() + 1

    def getMaxHealth(self):
        return self.maxHealth

    def setMaxHealth(self, value):
        self.maxHealth = value

    def setStage(self, s):
        self.stage = s

    def move(self, pressedKeys):
        # Indicamos la acción a realizar según la tecla pulsada para el jugador
        if self.alive:
            # Horizontal movement
            if pressedKeys[self.data.getKeyRight()] and pressedKeys[self.data.getKeyLeft()]:
                Character.move(self, STOPPED)
            elif pressedKeys[self.data.getKeyRight()]:
                Character.move(self, RIGHT)
            elif pressedKeys[self.data.getKeyLeft()]:
                Character.move(self, LEFT)
            else:
                Character.move(self, STOPPED)

            # Vertical movement
            if pressedKeys[self.data.getKeyUp()] and self.readyToJump:
                self.readyToJump = False
                Character.move(self, UP)
            elif not pressedKeys[self.data.getKeyUp()]:
                self.readyToJump = True

            # Attack
            if pressedKeys[self.data.getSpace()] and self.readyToAttack:
                self.readyToAttack = False
                Character.move(self, ATTACK)
            elif not pressedKeys[self.data.getSpace()]:
                self.readyToAttack = True
        else:
            # TODO Crear animación de jugador muerto
            Character.move(self, STOPPED)

    def backOff(self, enemy):
        pass
        '''
        # Player se retira para no colisionar con enemigo
        (vx,vy) = self.getVelocidad()
        (tx,ty) = self.getVelocidad()
        tPostura = self.numPostura
        if self.getCollisionRect().left < enemy.getCollisionRect().left:
            vx = -.15
        else:
            vx = +.15
        if self.numPostura != SPRITE_JUMPING:
            vy = -.25
        #t = threading.Timer(0.35, self.endBackOff(self.numPostura,vx,vy))
        #st.start()
        self.numPostura = SPRITE_JUMPING
        self.setVelocidad((vx, vy))
        pygame.time.wait(1)
        self.setVelocidad((tx, ty))
        self.numPostura = tPostura

        #t.cancel(10)


    def endBackOff(self,p,x,y):
        self.setVelocidad((x,y))
        self.numPostura = p
        '''

    def update(self, clock, playerDisplacement, platformGroup, enemyGroup, itemGroup):
        if self.alive:
            enemyCol = pygame.sprite.spritecollideany(self, enemyGroup)
            itemCol = pygame.sprite.spritecollideany(self, itemGroup)
            if enemyCol is not None:
                if self.attacking:
                    self.setAttacking(False)
                    enemyCol.decreaseHealth(self.attack, enemyGroup)
                else:
                    if enemyCol.alive:
                        # Colisión con enemigos
                        enemyCol.onPlayerCollision(self, enemyGroup)  # cada enemigo realiza una accion propia
            if itemCol is not None:
                itemCol.onPlayerCollision(self, itemGroup)  # cada item realiza una accion propia
            self.updateCollisionRect()  # Update collision rect
        Character.update(self, platformGroup, clock, playerDisplacement)  # Call update in the super class
