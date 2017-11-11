# -*- coding: utf-8 -*-
import pygame
from characters.Character import *
from pygame.transform import *
from random import randint
from characters.Item import *
from characters.Character import *


class Enemy(Character):
    def __init__(self, manager, data, id):

        Character.__init__(self,
                           manager,
                           data,
                           data.getPlayerSheet(id),
                           data.getPlayerSheetCoords(id),
                           [3, 4, 5, 0, 1],
                           data.getCharacterSpeed(id),
                           0,
                           data.getPlayerAnimationDelay())
        # Crear posición aleatoria para cada personaje
        if randint(0, 1) == 0:
            Character.move(self, LEFT)
        else:
            Character.move(self, RIGHT)
        # Variables del enemigo
        self.health = 100
        self.alive = True
        self.active = False
        self.attack_damage = data.getCharacterAttack(id)

        # Velocidades del enemigo
        self.speed_x = data.getCharacterSpeed(id)
        self.chasing_speed_x = data.getCharacterChasingSpeed(id)

        # Márgenes de ataque del enemigo
        self.y_activityrange = 30
        self.x_activityrange = 180

        # Altura a la que el jugador deja de estar a la vista del enemigo
        self.top_y_activityrange = 100

        # Custom rects
        self.collision_rect = pygame.Rect(self.getRect().left + self.getRect().width / 2 - 3,
                                          self.getRect().bottom - 5,
                                          6, 5)
        self.activity_range_rect = pygame.Rect(self.getRect().left - self.x_activityrange,
                                               self.getRect().top - self.y_activityrange,
                                               self.getRect().width + (self.x_activityrange * 2),
                                               self.getRect().height + (self.y_activityrange * 2))
        self.time = 0
        self.enemyState = None
        self.currentState = 0

    def decreaseHealth(self, player_attack):
        self.health = self.health - player_attack
        if self.health <= 0:
            self.die()
            self.manager.getCurrentLevel().getEnemyGroup().remove(self)
            self.manager.getCurrentLevel().getDeadBodiesGroup().add(self)

    def chasePlayer(self, chase):
        self.active = chase
        if chase:
            self.velocidadCarrera = self.chasing_speed_x
        else:
            self.velocidadCarrera = self.speed_x
            self.move(self.mirando)

    def backoff(self, player):
        y = -0.3
        # Saltar en dirección opuesta al jugador
        if self.posicion[0] - player.posicion[0] < 0:
            x = -0.3
        elif self.posicion[0] - player.posicion[0] >0:
            x = 0.3
        else:
            if self.mirando == RIGHT:
                x = -0.3
            else:
                x = 0.3
        # Asignar la nueva velocidad al enemigo
        self.velocidad = x, y

    def onPlayerCollision(self, player):
        pygame.mixer.Sound('../bin/assets/sounds/player/enemy_hit_1.wav').play()
        player.decreaseHealth(self.attack_damage, self)


    def updateCollisionRect(self):
        self.collision_rect = pygame.Rect(self.getRect().left + self.getRect().width / 2 - 3,
                                          self.getRect().bottom - 5,
                                          6, 5)
    def updateActivityRangeRect(self):
        # Creamos el rect que servirá para comprobar si el jugador está en su rango de visión
        self.activity_range_rect = pygame.Rect(self.getRect().left - self.x_activityrange,
                                               self.getRect().top - self.y_activityrange,
                                               self.getRect().width + (self.x_activityrange * 2),
                                               self.getRect().height + (self.y_activityrange * 2))

    def getCollisionRect(self):
        return self.collision_rect

    def checkScreenBounds(self):
        # Si el enemigo se sale de la pantalla, invertir velocidad X
        if self.posicion[0] == self.screen_width - self.getRect().width or self.posicion[0] == 0:
            self.invertXSpeed()

    def movement(self,player):
        myposition_x = self.getGlobalPosition()[0]
        myposition_y = self.getGlobalPosition()[1]
        playerposition_x = player.getGlobalPosition()[0]
        playerposition_y = player.getGlobalPosition()[1]
        # Primero, comprobar si el enemigo tiene que atacar
        if self.getRect().colliderect(player.getRect()):
            pass
        # Comprobar si el jugador está por debajo del enemigo
        elif myposition_y < playerposition_y - self.y_activityrange:
            # El enemigo baja el nivel hasta encontrar al jugador
            pass
        elif myposition_y - self.top_y_activityrange >= playerposition_y:
            # Si el jugador está por encima del enemigo, no perseguirle
            self.chasePlayer(False)
        else:
            # Perseguir al jugador en el eje x
            if playerposition_x > myposition_x:
                Character.move(self, RIGHT)
            elif playerposition_x < myposition_x:
                Character.move(self, LEFT)
            else:
                Character.move(self, STOPPED)
            pass
        pass

    def standOnPlatform(self):
        # Comprobamos si está en colisión con una plataformas
        platform = pygame.sprite.spritecollideany(self, self.manager.getCurrentLevel().getPlatformGroup())

        # Comprobamos que el enemigo no se salga de su plataforma
        if platform is not None:
            if self.getRect().left < platform.getRect().left:
                # Si se sale de la plataforma, invertir su velocidadX y situarlo en el borde de la plataforma
                self.invertXSpeed()
                new_pos = (platform.getRect().left, self.getGlobalPosition()[1])
                self.setPosition(new_pos)

            elif self.getRect().right > platform.getRect().right:
                # Si se sale de la plataforma, invertir su velocidadX y situarlo en el borde de la plataforma
                self.invertXSpeed()
                new_pos = (platform.getRect().right - self.getRect().width, self.getGlobalPosition()[1])
                self.setPosition(new_pos)

    def update(self, clock, player, playerDisplacement):
        # Actualizamos los rects del enemigo
        self.updateCollisionRect()
        self.updateActivityRangeRect()
        if self.alive:
            self.checkScreenBounds()
            if self.active:
                self.movement(player)
            else:
                # Comprobamos si el jugador está dentro del rango de visión del jugador
                if player.getRect().colliderect(self.activity_range_rect):
                    self.chasePlayer(True)
                    return
                self.standOnPlatform()
        # Llamada al update de la super clase
        Character.update(self, clock, playerDisplacement)

    def getDoUpdateScroll(self):
        return True


class Asmodeo(Enemy):
    def __init__(self, manager, data):
        Enemy.__init__(self, manager, data, "asmodeo")
        self.setInvertedSpriteSheet(True)

class Dante(Enemy):
    def __init__(self, manager, data):
        Enemy.__init__(self, manager, data, "dante")
        # self.setInvertedSpriteSheet(True)


class Belcebu(Enemy):
    def __init__(self, manager, data):
        Enemy.__init__(self, manager, data, "belcebu")
        self.setInvertedSpriteSheet(True)


class Mammon(Enemy):
    def __init__(self, manager, data):
        Enemy.__init__(self, manager, data, "mammon")
        self.setInvertedSpriteSheet(True)


class FireProjectile(Enemy):
    def __init__(self, manager, data):
        Enemy.__init__(self, manager, data, "fireprojectile")
        self.health = 500000
        self.time = 0
        self.ttl = 6000
        (self.sizeX,self.sizeY) = self.image.get_size()
    '''
    def movement(self, player):
        Character.move(self, LEFT)

    def standOnPlatform(self):
        # Comprobamos si está en colisión con una plataformas
        platform = pygame.sprite.spritecollideany(self, self.manager.getCurrentLevel().getPlatformGroup())
    '''
    def update(self, clock, player, playerDisplacement):
        # Actualizamos los rects del enemigo
        self.updateCollisionRect()
        self.time = self.time + clock
        '''
        if self.alive:

            self.checkScreenBounds()

            if self.active:
                self.movement(player)
            else:
                self.standOnPlatform()
        '''
        # elimino el sprite
        if self.time > self.ttl:
            if self.sizeX > 10 and self.sizeY > 10:
                self.sizeX = self.sizeX - 10
                self.sizeY = self.sizeY - 10
                pygame.transform.scale(self.image, (self.sizeX, self.sizeY))
                self.manager.getScreen().blit(self.image, (self.getCollisionRect().left, self.getCollisionRect().top))
            else:
                self.manager.getCurrentLevel().getEnemyGroup().remove(self)
        # Llamada al update de la super clase
        Character.update(self, clock, (0,0))#playerDisplacement)

class Satan(Enemy):
    def __init__(self, manager, data):
        Enemy.__init__(self, manager, data, "satan")
        self.health = 500
        self.setInvertedSpriteSheet(True)
        self.enemyState = ["wander", "attack", "wander", "berserk"]
        self.playerDisplacement = None

    def update(self, clock, player, playerDisplacement):
        self.time = self.time + clock
        if self.playerDisplacement == None:
            self.playerDisplacement = playerDisplacement
        if self.alive:
            # Actualizamos los rects del enemigo
            self.updateCollisionRect()
            self.updateActivityRangeRect()

            # Cambio el comportamiento del enemigo cada 8 segundos
            if self.time>8000:
                self.time = 0
                self.currentState = self.currentState + 1
                if self.currentState > len(self.enemyState) - 1:
                    self.currentState = 0

            if self.enemyState[self.currentState] == "wander":
                self.wander()
            elif self.enemyState[self.currentState] == "attack":
                # realiza 3 ataques lanzando fuego  se coloca sobre la puerta
                self.attack()
                pass
            elif self.enemyState[self.currentState] == "berserk":
                # Cae fuego del cielo se coloca en el centro de la pantalla
                self.berserk()

            if self.active:
                myposition_x = self.getGlobalPosition()[0]
                myposition_y = self.getGlobalPosition()[1]
                playerposition_x = player.getGlobalPosition()[0]
                playerposition_y = player.getGlobalPosition()[1]

            #evito que el jugador supere al enemigo
            if player.getCollisionRect().left >= (self.getCollisionRect().centerx):
                player.setPosition((player.getCollisionRect().left - 75, player.getGlobalPosition()[1]))
        else:
            self.manager.getCurrentLevel().getEnemyGroup().remove(self)

        # Llamada al update de la super clase
        Character.update(self, clock, playerDisplacement)

    def wander(self):
        if self.getVelocidad()[0] == 0:
            Character.move(self,LEFT)
        if (self.posicion[0] <= (self.screen_width/3) or self.posicion[0]>=(self.screen_width-self.getRect().width)):
            self.invertXSpeed()


    def attack(self):
        if (self.posicion[0] < ((self.screen_width-self.getRect().width)/2)-20):
            Character.move(self, RIGHT)
        elif(self.posicion[0] > ((self.screen_width+self.getRect().width)/2)+20):
            Character.move(self, LEFT)
        else:
            Character.move(self,STOPPED)
            if self.time % 1000 < 50:
                self.fireArrow(self)


    def berserk(self):
        if (self.posicion[0] < ((self.screen_width - self.getRect().width)) - 20):
            Character.move(self, RIGHT)
        else:
            Character.move(self, STOPPED)
            if self.time % 1000 < 100:
                self.piroclasto()

    def chasePlayer(self, chase):
        pass

    def piroclasto(self):
        tmp = FireProjectile(self.manager, self.manager.getDataRetriever())
        tmp.setPosition((randint(55, (self.screen_width - 55)), 0))
        self.manager.getCurrentLevel().getEnemyGroup().add(tmp)

    def fireArrow(self, p):
        tmp = FireProjectile(self.manager, self.manager.getDataRetriever())
        tmp.setPosition((p.getRect().x-15+p.getRect().width/2, p.getRect().y+p.getRect().height/2))
        self.manager.getCurrentLevel().getEnemyGroup().add(tmp)
