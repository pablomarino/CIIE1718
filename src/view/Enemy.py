# -*- coding: utf-8 -*-
from view.Character import *


class Enemy(Character):
    def __init__(self, manager, data, id):
        Character.__init__(self,
                           manager,
                           data,
                           data.getPlayerSheet(id),
                           data.getPlayerSheetCoords(id),
                           [3, 4, 5],
                           data.getPlayerSpeed(),
                           data.getPlayerJumpSpeed(),
                           data.getPlayerAnimationDelay());

        self.health = 100;

    def move_cpu(self, data, player):
        return

    def getDoUpdateScroll(self):
        return True

class Asmodeo(Enemy):
    def __init__(self, manager, data):
        Enemy.__init__(self, manager, data, "asmodeo")

    def move_cpu(self, data, player):
        pass
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

    def move_cpu(self, data, player):
        pass


class Mammon(Enemy):
    def __init__(self, manager, data):
        Enemy.__init__(self, manager, data, "mammon")

    def move_cpu(self, data, player):
        pass
