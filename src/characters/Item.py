# -*- coding: utf-8 -*-
from time import time

from characters.Character import *


class Item(Character):
    def __init__(self, manager, data, id, itemGroup):
        self.manager = manager
        self.itemGroup = itemGroup
        self.tiempo_colision = 0

        # LLamada a constructor de la super clase
        Character.__init__(self,
                           manager,
                           data,
                           data.getItemSheet(id),  # archivoImagen
                           data.getItemSheetCoords(id),  # archivoCoordenadas
                           [8],  # numImagenes
                           0,  # data.getCharacterSpeed(id),  #velocidadCarrera
                           0,  # velocidadSalto
                           10)  # data.getItemAnimationDelay())#retardo animacion

    def getCollisionRect(self):
        return self.getRect()

    def update(self, platformGroup, clock, playerDisplacement):
        self.numPostura = SPRITE_STOPPED
        self.actualizarPostura()
        Character.update(self, platformGroup, clock, playerDisplacement)

    def getDoUpdateScroll(self):
        return True

    def onPlayerCollision(self, player):
        pass


class heart(Item):
    def __init__(self, manager, data, itemGroup):
        Item.__init__(self, manager, data, "heart", itemGroup)
        self.sound = data.getItemSound("heart")

    def onPlayerCollision(self, player):
        pygame.mixer.Sound(self.sound).play()
        # Eliminamos el item
        self.itemGroup.remove(self)
        # Sonido
        player.increaseLives()



class health_potion(Item):
    def __init__(self, manager, data, itemGroup):
        Item.__init__(self, manager, data, "health_potion", itemGroup)
        self.sound = data.getItemSound("health_potion")

    def onPlayerCollision(self, player):
        pygame.mixer.Sound(self.sound).play()
        # Eliminamos el item
        self.itemGroup.remove(self)
        # Sonido
        player.increaseHealth(30)


class coin(Item):
    def __init__(self, manager, data, itemGroup):
        Item.__init__(self, manager, data, "coin", itemGroup)
        self.sound = data.getItemSound("coin")

    def onPlayerCollision(self, player):
        pygame.mixer.Sound(self.sound).play()
        # Eliminamos el item
        self.itemGroup.remove(self)
        # Sonido
        player.increasePoints()


class fire(Item):
    def __init__(self, manager, data, itemGroup):
        Item.__init__(self, manager, data, "fire", itemGroup)
        self.sound = data.getItemSound("fire")

    def onPlayerCollision(self, player):
        if self.tiempo_colision < time():
            pygame.mixer.Sound(self.sound).play()
            player.decreaseHealth(0.8, self)
            self.tiempo_colision = time() + 0.2


class door(Item):
    def __init__(self, manager, data, itemGroup):
        self.active = True
        Item.__init__(self, manager, data, "door", itemGroup)

    # TODO modificar el rect para que el jugador tenga que tocar la parte inferior de la puerta, no los bordes

    def onPlayerCollision(self, player):
        if self.active:
            self.active = False
            # TODO añadir sonido
            print "Player health : " + str(player.getHealth())
            self.manager.addNextLevel()
            self.manager.changeScene()


class chandelier(Item):
    def __init__(self, manager, data, itemGroup):
        Item.__init__(self, manager, data, "chandelier", itemGroup)

    def onPlayerCollision(self, player):
        pass


class wardrove(Item):
    def __init__(self, manager, data, itemGroup):
        Item.__init__(self, manager, data, "wardrove", itemGroup)

    def onPlayerCollision(self, player):
        pass


# TODO no usado de momento
class dante(Item):
    def __init__(self, manager, data, itemGroup):
        Item.__init__(self, manager, data, "dante", itemGroup)

    def onPlayerCollision(self, player):
        player.die()
