# -*- encoding: utf-8 -*-

from characters.Player import Player

from stage.regular.Stage import *


class GameLevel:
    def __init__(self, manager, data, id, player_stats):
        # Guardamos variables
        self.id = id
        self.manager = manager
        self.data = data
        self.level = data.getLevel(id)

        # Creación de grupos de sprites
        self.spriteGroup = pygame.sprite.Group()
        self.platformGroup = pygame.sprite.Group()
        self.itemGroup = pygame.sprite.Group()
        self.enemyGroup = pygame.sprite.Group()

        if self.level:
            # TODO pasar los valores de vida del jugador para que no se pierdan de un nivel a otro
            self.player = Player(manager, data, 'player', player_stats)
            self.player.setPosition(data.getPlayerPositionAt(id))
            self.spriteGroup.add(self.player)

            self.stage = Stage(self.manager, self.level, self.player, self.platformGroup, self.spriteGroup,
                               self.enemyGroup, self.itemGroup)
            self.player.setStage(self.stage)
        else:
            print "Error no existe nivel con id ", id

    def getId(self):
        return self.id

    def getPlayerStats(self):
        return self.player.getLives(), self.player.getMaxHealth(), self.player.getHealth(), self.player.getPoints()

    def update(self, clock):
        self.stage.update(clock)
        # self.player.update(self.platformGroup, clock)

    def events(self, events_list):
        self.stage.events(events_list)

    def draw(self):
        self.stage.draw()
        # self.spriteGroup.draw(self.manager.getScreen())
        pass
