# -*- encoding: utf-8 -*-
import re

from characters.Player import Player
from stage.regular.Stage import *


class GameLevel:
    def __init__(self, manager, data, id, player_stats):
        # Guardamos variables
        self.id = id
        self.manager = manager
        self.data = data
        self.level = data.getLevel(id)

        # Level text
        self.display_level_time = time() + 5
        self.opacity = 50

        # Creación de grupos de sprites
        self.spriteGroup = pygame.sprite.Group()
        self.platformGroup = pygame.sprite.Group()
        self.itemGroup = pygame.sprite.Group()
        self.enemyGroup = pygame.sprite.Group()
        self.deadBodiesGroup = pygame.sprite.Group()

        if self.level:
            self.player = Player(manager, data, 'player', player_stats)
            self.player.setPosition(data.getPlayerPositionAt(id))
            self.spriteGroup.add(self.player)

            self.stage = Stage(self.manager, self.level, self.player, self.platformGroup, self.spriteGroup,
                               self.enemyGroup, self.itemGroup, self.deadBodiesGroup)
            self.player.setStage(self.stage)
        else:
            print "Error no existe nivel con id ", id

    def display_level_name(self, opacity):
        try:
            # Variables
            if int(self.getNumericId()) == len(self.data.getLevels()):
                text = "Final Level"
            else:
                text = "Level " + str(self.getNumericId())
            color = (200, 200, 200)
            font_size = opacity
            # # Display text
            font = pygame.font.Font(self.data.getHudFontType(), font_size)
            text = font.render(text, True, color)
            text_rect = text.get_rect(center=(self.data.getWidth() / 2, self.data.getHeight() / 3))
            self.manager.getScreen().blit(text, text_rect)
        except Exception, e:
            raise e

    def getId(self):
        return self.id

    def getNumericId(self):
        levelid = self.getId()
        result = re.sub('[^0-9]', '', levelid)
        return result

    def getPlayerStats(self):
        return self.player.getLives(), self.player.getMaxHealth(), self.player.getHealth(), self.player.getPoints()

    def update(self, clock):
        self.stage.update(clock)
        # self.player.update(self.platformGroup, clock)

    def events(self, events_list):
        self.stage.events(events_list)

    def draw(self):
        self.stage.draw()
        if time() < self.display_level_time:
            self.display_level_name(self.opacity)
        elif self.opacity >= 0:
            self.display_level_name(self.opacity)
            self.opacity -= 9

    def getSpriteGroup(self):
        return self.spriteGroup

    def getPlatformGroup(self):
        return self.platformGroup

    def getItemGroup(self):
        return self.itemGroup

    def getEnemyGroup(self):
        return self.enemyGroup

    def getDeadBodiesGroup(self):
        return self.deadBodiesGroup
