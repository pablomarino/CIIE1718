# -*- coding: utf-8 -*-
from view.Character import *
from random import randint


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

        self.health = 100
        self.alive = True
        # TODO cada enemigo debería moverse hacia un lado diferente al crearse el nivel

        if randint(0,1)==0 :
            Character.move(self, LEFT)
        else:
            Character.move(self, RIGHT)

    def update(self, platformGroup, clock, playerDisplacement):
        # TODO implementar en cada tipo de enemigo si es necesario, al menos la parte de las plataformas
        if self.alive:
            # Si el enemigo se sale de la pantalla, invertir velocidad X
            if self.posicion[0] == self.screen_width - self.getRect().width or self.posicion[0] == 0:
                self.invertXSpeed()
            # si el jugador ya no va a estar en contacto con una plataforma, invertir el eje X
            elif pygame.sprite.spritecollideany(self, platformGroup) is None:
                # TODO comprobar mejor si la parte derecha del enemigo y de la plataforma coinciden, y viceversa
                self.invertXSpeed()

            Character.update(self, platformGroup, clock, playerDisplacement)

    def getDoUpdateScroll(self):
        return True


class Asmodeo(Enemy):
    def __init__(self, manager, data):
        Enemy.__init__(self, manager, data, "asmodeo")

        # def move_cpu(self, data, player):
        #     pass
        '''if self.rect.bottom > 0 and self.rect.right < data.getWidht() and self.rect.bottom > 0 and self.rect.top < data.getHeight():
            if player.position[0] < self.position[0]:
                Character.move(self, LEFT)
            else:
                Character.move(self, RIGHT)
        else:
            Character.move(self, STOPPED)'''


class Belcebu(Enemy):
    def __init__(self, manager, data):
        Enemy.__init__(self, manager, data, "asmodeo")

        # def move_cpu(self, data, player):
        #     pass


class Mammon(Enemy):
    def __init__(self, manager, data):
        Enemy.__init__(self, manager, data, "mammon")

        # def move_cpu(self, data, player):
        #     pass
