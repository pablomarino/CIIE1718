# -*- coding: utf-8 -*-
from characters.Character import *


class Item(Character):
    def __init__(self, manager, data, id):
        self.manager = manager

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

    def behave(self, player, itemGroup):
        pass


class heart(Item):
    def __init__(self, manager, data):
        Item.__init__(self, manager, data, "heart")
        self.sound = data.getItemSound("heart")

    def behave(self, player, itemGroup):
        # Eliminamos el item
        for i in itemGroup:
            if i == self: itemGroup.remove(i)
        # Sonido
        player.increaseLives()
        pygame.mixer.Sound(self.sound).play()

class salud(Item):
    def __init__(self, manager, data):
        Item.__init__(self, manager, data, "salud")
        self.sound = data.getItemSound("salud")

    def behave(self, player, itemGroup):
        # Eliminamos el item
        for i in itemGroup:
            if i == self: itemGroup.remove(i)
        # Sonido
        player.increaseHealth()

class moneda(Item):
    def __init__(self, manager, data):
        Item.__init__(self, manager, data, "moneda")
        self.sound = data.getItemSound("moneda")

    def behave(self, player, itemGroup):
        # Eliminamos el item
        for i in itemGroup:
            if i == self: itemGroup.remove(i)
        # Sonido
        player.increasePoints()


class fire(Item):
    def __init__(self, manager, data):
        Item.__init__(self, manager, data, "fire")

    def behave(self, player, itemGroup):
        # TODO añadir sonido
        player.decreaseHealth(self)


class door(Item):
    def __init__(self, manager, data):
        self.active = True
        Item.__init__(self, manager, data, "door")

    # TODO modificar el rect para que el jugador tenga que tocar la parte inferior de la puerta, no los bordes

    def behave(self, player, itemGroup):
        if self.active:
            self.active = False
            print "Player health : " + str(player.getHealth())
            self.manager.addNextLevel()
            self.manager.changeScene()


class chandelier(Item):
    def __init__(self, manager, data):
        Item.__init__(self, manager, data, "chandelier")

    def behave(self, player, itemGroup):
        pass


class wardrove(Item):
    def __init__(self, manager, data):
        Item.__init__(self, manager, data, "wardrove")

    def behave(self, player, itemGroup):
        pass



class dante(Item):
    def __init__(self, manager, data):
        Item.__init__(self, manager, data, "dante")

    def behave(self, player, itemGroup):
        player.die()
