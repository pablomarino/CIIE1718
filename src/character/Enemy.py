# -*- coding: utf-8 -*-
from character.Character import *


# -------------------------------------------------
# Clase Enemy

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

    def move_cpu(self, data, player):
        return

# -------------------------------------------------
# Asmodeo (fase 1)

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

# -------------------------------------------------
# Belcebu (fase 2)

class Belcebu(Enemy):
    def __init__(self, manager, data):
        Enemy.__init__(self, manager, data, "asmodeo")

    def move_cpu(self, data, player):
        pass

# -------------------------------------------------
# Mammon (fase 3)

class Mammon(Enemy):
    def __init__(self, manager, data):
        Enemy.__init__(self, manager, data, "mammon")

    def move_cpu(self, data, player):
        pass