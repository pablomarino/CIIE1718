# -*- coding: utf-8 -*-
from time import time

from characters.Character import *


class Player(Character):
    def __init__(self, manager, data, id, player_stats):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Character.__init__(self,
                           manager,
                           data,
                           data.getPlayerSheet(id),
                           data.getPlayerSheetCoords(id),
                           [5, 6, 5, 1, 1],
                           data.getCharacterSpeed(id),
                           data.getCharacterJumpSpeed(id),
                           data.getPlayerAnimationDelay())
        # Variables generales
        self.data = data
        self.manager = manager

        # Variables de movimiento del jugador
        self.numPostura = SPRITE_JUMPING
        self.readyToJump = True
        self.collision_rect = pygame.Rect(self.getRect().left + self.getRect().width / 2 - 3,
                                          self.getRect().bottom - 5,
                                          6, 5)

        # Variables del ataque del jugador
        self.readyToAttack = True
        self.tiempo_ataque = 0
        self.attack = data.getCharacterAttack(id)

        # Variables propias del jugador
        self.lives = player_stats[0]
        self.points = player_stats[3]
        self.maxHealth = player_stats[1]
        self.health = player_stats[2]
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
            self.die()
        else:
            self.stage.resetScroll()
            self.setPosition(self.data.getPlayerPositionAt("level_1"))
            self.numPostura = SPRITE_JUMPING
            self.setHealth(self.getMaxHealth())

    def getHealth(self):
        return self.health

    def setHealth(self, value):
        self.health = value

    def increaseHealth(self, health_increase):
        self.health = self.health + health_increase
        if self.health >= self.getMaxHealth():
            self.health = self.getMaxHealth()

    def decreaseHealth(self, amount, e):
        # if self.tiempo_colision < time():
        self.health = self.health - amount
        self.backOff(e)
        if self.health <= 0:
            self.decreaseLives()
            # self.die()
            # self.tiempo_colision = time() + 1

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

            # Colisión con emeigos
            if enemyCol is not None:
                # TODO si hay un enemigo muerto en el suelo, comprueba la colisión con él
                if enemyCol.alive:
                    if self.attacking:
                        if not self.already_attacked:
                            enemyCol.decreaseHealth(self.attack)
                            pygame.mixer.Sound('../bin/assets/sounds/player/enemy_hit_2.wav').play()
                            # TODO enemyCol.backoff()
                            self.already_attacked = True
                        self.tiempo_ataque = time() + 1
                    else:
                        if self.tiempo_ataque < time():
                            # Colisión con enemigos sin estar atacando
                            enemyCol.onPlayerCollision(self)
                            self.tiempo_ataque = time() + 1

            # Colisión con items
            if itemCol is not None:
                # cada item realiza una accion propia
                itemCol.onPlayerCollision(self)

            self.updateCollisionRect()  # Update collision rect
        Character.update(self, platformGroup, clock, playerDisplacement)  # Call update in the super class
