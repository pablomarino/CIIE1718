# -*- encoding: utf-8 -*-

from stage.Stage import *
from view.Enemy import *
from view.Player import Player


class GameLevel:
    def __init__(self, manager, data, id):
        self.manager = manager

        self.data = data
        self.level = data.getLevel(id)

        # Add music to the game
        pygame.mixer.music.load(self.data.getMusicFile())
        # pygame.mixer.music.play()

        self.spriteGroup = pygame.sprite.Group()
        self.platformGroup = pygame.sprite.Group()
        self.itemGroup = pygame.sprite.Group()
        self.enemyGroup = pygame.sprite.Group()

        if self.level:
            # TODO tener en cuenta, valores de vida y demás se reinician al pasar de nivel,se crea un jugador nuevo
            self.player = Player(manager, data, 'player')
            self.player.setPosition(data.getPlayerPositionAt(id))
            self.spriteGroup.add(self.player)

            # for e in self.level["enemies"]:
            #     tmp = str_to_class(e["kind"])(manager, data)
            #     tmp.setPosition((int(e["x"]), int(e["y"])))
            #     self.enemyGroup.add(tmp)
            # self.enemy1 = Asmodeo(manager, data)
            # self.enemy1.setPosition(data.getPlayerPositionAt(id))

            self.stage = Stage(self.manager, self.level, self.player, self.platformGroup, self.spriteGroup,
                               self.enemyGroup)
        else:
            print "Error no existe nivel con id ", id

    def update(self, clock):
        self.stage.update(clock)
        # self.player.update(self.platformGroup, clock)

    def events(self):
        self.stage.events()

    def draw(self):
        self.stage.draw()
        # self.spriteGroup.draw(self.manager.getScreen())
        pass
