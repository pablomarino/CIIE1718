# -*- coding: utf-8 -*-
from view.Character import *


class Item(Character):
    def __init__(self, manager, data, id):
        Character.__init__(self,
                            manager,
                            data,
                            data.getItemSheet(id),          #archivoImagen
                            data.getItemSheetCoords(id),    #archivoCoordenadas
                            [3],                            # numImagenes
                            0,#data.getCharacterSpeed(id),  #velocidadCarrera
                            0,                              #velocidadSalto
                            5)#data.getItemAnimationDelay())#retardo animacion


    def getCollisionRect(self):
        # TODO implementar esta función para los enemigos
        return self.getRect()

    def update(self, platformGroup, clock, playerDisplacement):
        # Comprobamos si está en colisión con una plataformas
        Character.update(self, platformGroup, clock, playerDisplacement)

    def getDoUpdateScroll(self):
        return False

class heart(Item):
    def __init__(self, manager, data):
        Item.__init__(self, manager, data, "heart")

class fire(Item):
    def __init__(self, manager, data):
        Item.__init__(self,manager,data,"fire")