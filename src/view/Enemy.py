# -*- coding: utf-8 -*-

from random import randint

from view.Character import *


class Enemy(Character):
    def __init__(self, manager, data, id):
        # TODO invertir el sprite de los enemigos
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

    def update(self, platformGroup, clock, playerDisplacement):
        # TODO implementar en cada tipo de enemigo si es necesario, al menos la parte de las plataformas
        if self.alive:

            # Comprobamos si está en colisión con una plataformas
            platform = pygame.sprite.spritecollideany(self, platformGroup)

            # Si el enemigo se sale de la pantalla, invertir velocidad X
            if self.posicion[0] == self.screen_width - self.getRect().width or self.posicion[0] == 0:
                self.invertXSpeed()

            # Comprobamos que el enemigo no se salga de su plataforma
            elif platform is not None:

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


class Belcebu(Enemy):
    def __init__(self, manager, data):
        Enemy.__init__(self, manager, data, "asmodeo")


class Mammon(Enemy):
    def __init__(self, manager, data):
        Enemy.__init__(self, manager, data, "mammon")
