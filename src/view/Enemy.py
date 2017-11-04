# -*- coding: utf-8 -*-

from random import randint

from view.Character import *


class Enemy(Character):
    def __init__(self, manager, data, id):
        Character.__init__(self,
                           manager,
                           data,
                           data.getPlayerSheet(id),
                           data.getPlayerSheetCoords(id),
                           [3, 4, 5],
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
        self.speed_x = data.getCharacterSpeed(id)
        self.chasing_speed_x = data.getCharacterChasingSpeed(id)
        # TODO rename this variable
        self.y_margin = 20

    def chasePlayer(self, active):
        self.active = active
        if active:
            # self.changeXSpeed(self.chasing_speed_x)
            self.velocidadCarrera = self.chasing_speed_x
        else:
            self.velocidadCarrera = self.speed_x
            # self.changeXSpeed(self.speed_x)

    def behave(self, player, enemyGroup):
        pass

    def getCollisionRect(self):
        # TODO implementar esta función para los enemigos
        return self.getRect()

    def update(self, platformGroup, clock, player, playerDisplacement):
        if self.alive:

            # Si el enemigo se sale de la pantalla, invertir velocidad X
            if self.posicion[0] == self.screen_width - self.getRect().width or self.posicion[0] == 0:
                self.invertXSpeed()

            if self.active:
                myposition_x = self.getGlobalPosition()[0]
                myposition_y = self.getGlobalPosition()[1]
                playerposition_x = player.getGlobalPosition()[0]
                playerposition_y = player.getGlobalPosition()[1]

                # TODO perseguir al jugador, incluso bajarse de las plataformas
                if myposition_y < playerposition_y - self.y_margin:
                    # El enemigo baja el nivel hasta encontrar al jugador
                    pass
                elif myposition_y > playerposition_y + self.y_margin:
                    self.chasePlayer(False)
                else:
                    # TODO perseguir al jugador en el eje x
                    if playerposition_x > myposition_x:
                        Character.move(self, RIGHT)
                    elif playerposition_x < myposition_x:
                        Character.move(self, LEFT)
                    else:
                        Character.move(self, STOPPED)
                    pass
            else:
                # Comprobamos si está en colisión con una plataformas
                platform = pygame.sprite.spritecollideany(self, platformGroup)

                # Comprobamos si el jugador está a la misma altura que el enemigo
                if self.getGlobalPosition()[1] - self.y_margin <= player.getGlobalPosition()[1] <= \
                                self.getGlobalPosition()[1] + self.y_margin:
                    self.chasePlayer(True)
                    return

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
        Character.update(self, platformGroup, clock, playerDisplacement)

    def getDoUpdateScroll(self):
        return True


class Asmodeo(Enemy):
    def __init__(self, manager, data):
        Enemy.__init__(self, manager, data, "asmodeo")
        self.setInvertedSpriteSheet(True)

    def behave(self, player, enemyGroup):
        player.decreaseHealth()


class Belcebu(Enemy):
    def __init__(self, manager, data):
        Enemy.__init__(self, manager, data, "asmodeo")
        self.setInvertedSpriteSheet(True)

    def behave(self, player, enemyGroup):
        player.decreaseHealth()


class Mammon(Enemy):
    def __init__(self, manager, data):
        Enemy.__init__(self, manager, data, "mammon")
        self.setInvertedSpriteSheet(True)

    def behave(self, player, enemyGroup):
        player.decreaseHealth()
