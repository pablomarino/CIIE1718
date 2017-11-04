# -*- coding: utf-8 -*-
from view.Character import *


class Item(Character):
    def __init__(self, manager, data, id):
        Character.__init__(self,
                            manager,
                            data,
                            data.getItemSheet(id),          #archivoImagen
                            data.getItemSheetCoords(id),    #archivoCoordenadas
                            [8],                            # numImagenes
                            0,#data.getCharacterSpeed(id),  #velocidadCarrera
                            0,                              #velocidadSalto
                            10)#data.getItemAnimationDelay())#retardo animacion


    def getCollisionRect(self):
        # TODO implementar esta función para los enemigos
        return self.getRect()

    def update(self, platformGroup, clock, playerDisplacement):
        self.numPostura = SPRITE_STOPPED
        self.actualizarPostura()
        Character.update(self, platformGroup, clock, playerDisplacement)

    def getDoUpdateScroll(self):
        return True

    def behave(self,player,itemGroup):
        pass


class heart(Item):
    def __init__(self, manager, data):
        Item.__init__(self, manager, data, "heart")
    def behave(self,player,itemGroup):
        # eliminar
        for i in itemGroup:
            if i == self: itemGroup.remove(i)
        player.increaseLives()

class fire(Item):
    def __init__(self, manager, data):
        Item.__init__(self,manager,data,"fire")

    def behave(self,player,itemGroup):
        player.decreaseHealth()

class door(Item):
    def __init__(self, manager, data):
        self.active = True
        Item.__init__(self,manager,data,"door")

    def behave(self,player,itemGroup):
        if self.active:
            self.active = False
            player.nextLevel()

class dante(Item):
    def __init__(self, manager, data):
        Item.__init__(self,manager,data,"dante")

    def behave(self,player,itemGroup):
        player.die()
