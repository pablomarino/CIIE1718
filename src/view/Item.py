# -*- coding: utf-8 -*-
from view.Character import *


class Item():
    def __init__(self, manager, data, id):
        self.manager=manager
        self.data=data
        data.getPlayerSheet(id),
        data.getPlayerSheetCoords(id),

    def move_cpu(self, data, player):
        return

    def getDoUpdateScroll(self):
        return True

class Heart(Item):
    def __init__(self, manager, data):
        Item.__init__(self, manager, data, "heart")

class fire(Item):
    def __init__(self, manager, data):
        Item.__init__(self,manager,data,"fire")