# -*- coding: utf-8 -*-
from view.Character import *


class Item(Character):
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

    def getDoUpdateScroll(self):
        return True

class Heart(Item):
    def __init__(self, manager, data):
        Item.__init__(self, manager, data, "heart")
