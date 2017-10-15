# -*- coding: utf-8 -*-
from character.Character import *


# -------------------------------------------------
# Clase Enemy

class Enemy(Character):
    def __init__(self, data, id):
        Character.__init__(self,
                           data,
                           data.getPlayerSheet(id),
                           data.getPlayerSheetCoords(id),
                           [3, 4, 5],
                           data.getPlayerSpeed(),
                           data.getPlayerJumpSpeed(),
                           data.getPlayerAnimationDelay());

    def move_cpu(self, data, player):
        return


# -------------------------------------------------
# Asmodeo

class Asmodeo(Enemy):
    def __init__(self, data):
        Enemy.__init__(self, data, "asmodeo")

    def move_cpu(self, data, player):
        pass
        '''if self.rect.bottom > 0 and self.rect.right < data.getWidht() and self.rect.bottom > 0 and self.rect.top < data.getHeight():
            if player.position[0] < self.position[0]:
                Character.move(self, LEFT)
            else:
                Character.move(self, RIGHT)
        else:
            Character.move(self, STOPPED)'''
