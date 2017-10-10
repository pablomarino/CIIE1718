# -*- coding: utf-8 -*-
from character.Character import *

# -------------------------------------------------
# Clase Enemy

class Enemy(Character):
    "Cualquier personaje del juego"
    def __init__(self, data, id):
       Character.__init__(self, data, id);

    def move_cpu(self, data, player):
        return

# -------------------------------------------------
# Asmodeo

class Asmodeo(Enemy):
    Character.__init__(self, 
            data, 
            data.getPlayerSheet(id),
            data.getPlayerSheetCoords(id),
            [5, 9, 5, 3], 
            data.getPlayerSpeed(), 
            data.getPlayerJumpSpeed(), 
            data.getPlayerAnimationDelay());

    def move_cpu(self, data, player):
         if self.rect.left>0 and self.rect.right<data.getWidht() and self.rect.bottom>0 and self.rect.top<data.getHeight():
            if player.posicion[0]<self.posicion[0]:
                        player.move(self,LEFT)
                    else:
                        player.move(self,RIGHT)
                else:
                    player.move(self,STOPPED)
