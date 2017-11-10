# -*- coding: utf-8 -*-

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
        self.enemyGroup = None
        self.health = 100
        self.alive = True
        self.active = False

        # Velocidades del enemigo
        self.speed_x = data.getCharacterSpeed(id)
        self.chasing_speed_x = data.getCharacterChasingSpeed(id)

        # Márgenes de ataque del enemigo
        self.y_activityrange = 30
        self.x_activityrange = 180

        # Altura a la que el jugador deja de estar a la vista del enemigo
        self.test_margin = 100  # TODO buscarle un nombre a esta variable

        # Custom rects
        self.collision_rect = pygame.Rect(self.getRect().left + self.getRect().width / 2 - 3,
                                          self.getRect().bottom - 5,
                                          6, 5)
        self.activity_range_rect = pygame.Rect(self.getRect().left - self.x_activityrange,
                                               self.getRect().top - self.y_activityrange,
                                               self.getRect().width + (self.x_activityrange * 2),
                                               self.getRect().height + (self.y_activityrange * 2))
        self.count = 0
        self.enemyState = ["wander"]
        self.currentState = 0

    def decreaseHealth(self, player_attack, enemyGroup):
        self.health = self.health - player_attack
        if self.health <= 0:
            self.die()
            # for i in enemyGroup:
            #     if i == self:
            #         enemyGroup.remove(i)

    def chasePlayer(self, chase):
        self.active = chase
        if chase:
            self.velocidadCarrera = self.chasing_speed_x
        else:
            self.velocidadCarrera = self.speed_x
            self.move(self.mirando)

    def onPlayerCollision(self, player, enemyGroup):
        pass

    def updateCollisionRect(self):
        # TODO intentar no crear un nuevo rect cada vez que se llama a la función update
        self.collision_rect = pygame.Rect(self.getRect().left + self.getRect().width / 2 - 3,
                                          self.getRect().bottom - 5,
                                          6, 5)

    def updateActivityRangeRect(self):
        # TODO intentar no crear un nuevo rect cada vez que se llama a la función update
        # Creamos el rect que servirá para comprobar si el jugador está en su rango de visión
        self.activity_range_rect = pygame.Rect(self.getRect().left - self.x_activityrange,
                                               self.getRect().top - self.y_activityrange,
                                               self.getRect().width + (self.x_activityrange * 2),
                                               self.getRect().height + (self.y_activityrange * 2))
        # x = self.rect.left - self.activity_range_rect.left - self.activity_range_rect.width / 2 + self.rect.width / 2
        # y = self.rect.top - self.activity_range_rect.top
        # self.activity_range_rect = self.activity_range_rect.move(x, y)

    def getCollisionRect(self):
        return self.collision_rect

    def update(self, platformGroup, clock, player, playerDisplacement):
        if self.alive:

            # Actualizamos los rects del enemigo
            self.updateCollisionRect()
            self.updateActivityRangeRect()

            # Si el enemigo se sale de la pantalla, invertir velocidad X
            if self.posicion[0] == self.screen_width - self.getRect().width or self.posicion[0] == 0:
                self.invertXSpeed()

            if self.active:
                myposition_x = self.getGlobalPosition()[0]
                myposition_y = self.getGlobalPosition()[1]
                playerposition_x = player.getGlobalPosition()[0]
                playerposition_y = player.getGlobalPosition()[1]

                # Primero, comprobar si el enemigo tiene que atacar
                if self.getRect().colliderect(player.getRect()):
                    # TODO enemigo pasa a movimiento ATTACK
                    # TODO poner velocidad a cero
                    pass

                # Comprobar si el jugador está por debajo del enemigo
                elif myposition_y < playerposition_y - self.y_activityrange:
                    # El enemigo baja el nivel hasta encontrar al jugador
                    pass
                elif myposition_y - self.test_margin >= playerposition_y:
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
            else:
                # Comprobamos si el jugador está dentro del rango de visión del jugador
                if player.getRect().colliderect(self.activity_range_rect):
                    self.chasePlayer(True)
                    return

                # Comprobamos si está en colisión con una plataformas
                platform = pygame.sprite.spritecollideany(self, platformGroup)

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

        # Llamada al update de la super clase
        Character.update(self, platformGroup, clock, playerDisplacement)

    def getDoUpdateScroll(self):
        return True


class Asmodeo(Enemy):
    def __init__(self, manager, data):
        Enemy.__init__(self, manager, data, "asmodeo")
        self.setInvertedSpriteSheet(True)

    def onPlayerCollision(self, player, enemyGroup):
        player.decreaseHealth(self)


class Dante(Enemy):
    def __init__(self, manager, data):
        Enemy.__init__(self, manager, data, "dante")
        #self.setInvertedSpriteSheet(True)

    def onPlayerCollision(self, player, enemyGroup):
        player.decreaseHealth(self)




class Belcebu(Enemy):
    def __init__(self, manager, data):
        Enemy.__init__(self, manager, data, "belcebu")
        self.setInvertedSpriteSheet(True)

    def onPlayerCollision(self, player, enemyGroup):
        player.decreaseHealth(self)


class Mammon(Enemy):
    def __init__(self, manager, data):
        Enemy.__init__(self, manager, data, "mammon")
        self.setInvertedSpriteSheet(True)

    def onPlayerCollision(self, player, enemyGroup):
        player.decreaseHealth(self)

class FireProjectile(Enemy):
    def __init__(self, manager, data):
        Enemy.__init__(self, manager, data, "fireprojectile")

    def onPlayerCollision(self, player, itemGroup):
        # TODO añadir sonido
        player.decreaseHealth(self)

    def update(self, platformGroup, clock, player, playerDisplacement):
        pass


class Satan(Enemy):
    def __init__(self, manager, data):
        Enemy.__init__(self, manager, data, "satan")
        self.setInvertedSpriteSheet(True)
        self.enemyState = ["wander", "attack", "wander", "berserk"]
        self.playerDisplacement = None

    def update(self, platformGroup, clock, player, playerDisplacement):
        self.count = self.count + clock
        if self.playerDisplacement == None:
            self.playerDisplacement = playerDisplacement
        if self.alive:
            # Actualizamos los rects del enemigo
            self.updateCollisionRect()
            self.updateActivityRangeRect()

            # Cambio el comportamiento del enemigo
            if self.count>8000:
                self.count = 0
                self.currentState = self.currentState + 1
                if self.currentState > len(self.enemyState)-1:
                    self.currentState = 0

            print self.enemyState[self.currentState]

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

        # Llamada al update de la super clase
        Character.update(self, platformGroup, clock, playerDisplacement)

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
            self.fireArrow(self)


    def berserk(self):
        if (self.posicion[0] < ((self.screen_width - self.getRect().width)) - 20):
            Character.move(self, RIGHT)
        else:
            Character.move(self, STOPPED)
            self.piroclasto()

    def chasePlayer(self, chase):
        pass

    def onPlayerCollision(self, player, enemyGroup):
        player.decreaseHealth(self)

    def piroclasto(self):
        tmp = FireProjectile(self.manager, self.manager.getDataRetriever())
        tmp.setPosition((randint(55, (self.screen_width - 55)), 0))
        self.enemyGroup.add(tmp)
        #p.playerDisplacement[1]

    def fireArrow(self, p):
        tmp = FireProjectile(self.manager, self.manager.getDataRetriever())
        tmp.setPosition((p.getRect().x, p.getRect().y))
        self.enemyGroup.add(tmp)

class EnemyTest(Enemy):
    def __init__(self, manager, data):
        Enemy.__init__(self, manager, data, "mammon")
        self.setInvertedSpriteSheet(True)

    def onPlayerCollision(self, player, enemyGroup):
        player.decreaseHealth(self)
