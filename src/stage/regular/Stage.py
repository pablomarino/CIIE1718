# -*- encoding: utf-8 -*-

import sys

from characters.Enemy import *
from characters.Item import *
from stage.regular.Background import *
from stage.regular.HUD import HUD
from stage.regular.Platform import Platform
from stage.regular.Scene import Scene


def str_to_class(str):
    return getattr(sys.modules[__name__], str)


class Stage(Scene):
    def __init__(self, manager, data, player, platformGroup, spriteGroup, enemyGroup, itemGroup, deadBodiesGroup):
        Scene.__init__(self, manager)

        self.MAP_UNIT_WIDTH = 55
        self.MAP_UNIT_HEIGHT = 55
        # Asignación de letras a objetos
        self.platform_letter = ["0", "1", "2"]
        self.enemy_letter = ["a", "b", "m", "n", "s"]
        self.fire_letter = "f"
        self.heart_letter = "h"
        self.door_letter = "d"
        self.wardrove_letter = "w"
        self.chandelier_letter = "c"
        self.coin_letter = "$"
        self.health_potion_letter = "p"
        self.manager = manager
        self.data = data
        self.screen = self.manager.getScreen()
        self.player = player
        self.playerStartPosition = self.player.getGlobalPosition()
        self.playerDisplacement = list((0, 0))

        # Initialize groups
        self.spriteGroup = spriteGroup
        self.platformGroup = platformGroup
        self.enemyGroup = enemyGroup
        self.itemGroup = itemGroup
        self.deadBodiesGroup = deadBodiesGroup

        self.initialize_lifebar_finalenemy()
        self.setup()

    def setup(self):

        # cargo el mapa
        self.map = self.data["map"]
        self.levelDimensions = (1024, (len(
            self.map) + 10) * self.MAP_UNIT_HEIGHT)  # ((int(self.data["dimensions"][0]), int(self.data["dimensions"][1])))
        # Genero la capa del Fondo
        self.background = BackGround(self.manager, self.data["bglayers"], self.player, self.levelDimensions)
        self.platformfiles = self.data["platform_files"]
        # Creamos el nivel a partir de fichero de texto
        self.create_level()
        # Creamos el HUD
        self.HUD = HUD(self.manager, self.player)

    def create_level(self):
        # Variables
        column_number = 0
        row_number = 0

        for line in self.map:
            platform_size = 0
            prev_letter = " "
            for letter in line:
                # Si hay la letra asignada a plataformas, aumentamos el tamaño de la plataforma a crear una posición
                if letter in self.platform_letter:
                    platform_size = platform_size + 1

                # Create enemies
                if letter in self.enemy_letter:
                    if letter == "a":
                        tmp = Asmodeo(self.manager, self.manager.getDataRetriever())
                    elif letter == "b":
                        tmp = Belcebu(self.manager, self.manager.getDataRetriever())
                    elif letter == "m":
                        tmp = Mammon(self.manager, self.manager.getDataRetriever())
                    elif letter == "n":
                        tmp = Dante(self.manager, self.manager.getDataRetriever())
                    elif letter == "s":
                        tmp = Satan(self.manager, self.manager.getDataRetriever())
                    tmp.enemyGroup = self.enemyGroup
                    tmp.setPosition((column_number * self.MAP_UNIT_WIDTH, row_number * self.MAP_UNIT_HEIGHT))
                    self.enemyGroup.add(tmp)

                # Create Items
                if letter == self.fire_letter:
                    tmp = Fire(self.manager, self.manager.getDataRetriever(), self.itemGroup)
                    tmp.setPosition((column_number * self.MAP_UNIT_WIDTH, row_number * self.MAP_UNIT_HEIGHT))
                    self.itemGroup.add(tmp)

                if letter == self.heart_letter:
                    tmp = Heart(self.manager, self.manager.getDataRetriever(), self.itemGroup)
                    tmp.setPosition((column_number * self.MAP_UNIT_WIDTH, row_number * self.MAP_UNIT_HEIGHT))
                    self.itemGroup.add(tmp)

                if letter == self.door_letter:
                    tmp = Door(self.manager, self.manager.getDataRetriever(), self.itemGroup)
                    tmp.setPosition((column_number * self.MAP_UNIT_WIDTH, row_number * self.MAP_UNIT_HEIGHT))
                    self.itemGroup.add(tmp)

                if letter == self.chandelier_letter:
                    tmp = Chandelier(self.manager, self.manager.getDataRetriever(), self.itemGroup)
                    tmp.setPosition((column_number * self.MAP_UNIT_WIDTH, row_number * self.MAP_UNIT_HEIGHT))
                    self.itemGroup.add(tmp)

                if letter == self.wardrove_letter:
                    tmp = Wardrove(self.manager, self.manager.getDataRetriever(), self.itemGroup)
                    tmp.setPosition((column_number * self.MAP_UNIT_WIDTH, row_number * self.MAP_UNIT_HEIGHT))
                    self.itemGroup.add(tmp)

                if letter == self.health_potion_letter:
                    tmp = HealthPotion(self.manager, self.manager.getDataRetriever(), self.itemGroup)
                    tmp.setPosition((column_number * self.MAP_UNIT_WIDTH, row_number * self.MAP_UNIT_HEIGHT))
                    self.itemGroup.add(tmp)

                if letter == self.coin_letter:
                    tmp = Coin(self.manager, self.manager.getDataRetriever(), self.itemGroup)
                    tmp.setPosition((column_number * self.MAP_UNIT_WIDTH, row_number * self.MAP_UNIT_HEIGHT))
                    self.itemGroup.add(tmp)

                # Creamos plataformas
                if not letter in self.platform_letter and prev_letter in self.platform_letter:
                    platform = Platform(
                        self.manager,
                        (column_number * self.MAP_UNIT_WIDTH, row_number * self.MAP_UNIT_HEIGHT),
                        self.platformfiles[int(prev_letter)],
                        platform_size)
                    self.platformGroup.add(platform)
                    platform_size = 0

                # Incrementar el contador de columnas
                column_number = column_number + 1

                # Asignar el valor de la letra actual a la variable prev_letter
                prev_letter = letter

            # Create last platform
            if prev_letter in self.platform_letter:
                platform = Platform(
                    self.manager,
                    (column_number * self.MAP_UNIT_WIDTH, row_number * self.MAP_UNIT_HEIGHT),
                    self.platformfiles[int(prev_letter)],
                    platform_size)
                self.platformGroup.add(platform)

            # Incrementar el contador de filas
            row_number = row_number + 1
            column_number = 0


    def update(self, clock):
        self.manager.getScreen().fill(int(self.data["bgColor"], 16))  # en windows es necesario =\ en mac no
        # Calculo la distancia entre la posicion inicial del jugador y la actual
        # Este valor se le pasa a Background y Platform para que realice el scroll
        # solo actualizo el scroll si el jugador esta saltando o cayendo
        if self.player.getDoUpdateScroll() & self.getDoUpdateScroll():
            self.playerDisplacement = (
                0,  # int(math.ceil(self.playerStartPosition[0]-self.player.getPosition()[0])),
                int(math.ceil(self.playerStartPosition[1] - self.player.getGlobalPosition()[1]))
            )
        # print "player ", self.player.getGlobalPosition()[1], self.player.getLocalPosition()[1]
        self.background.update(clock, self.playerDisplacement)

        for p in self.platformGroup:
            p.update(clock, self.playerDisplacement)

        for i in self.itemGroup:
            i.update(clock, self.playerDisplacement)

        self.player.update(clock, self.playerDisplacement, self.platformGroup, self.enemyGroup, self.itemGroup)
        self.enemyGroup.update(clock, self.player, self.playerDisplacement)
        self.deadBodiesGroup.update(clock, self.player, self.playerDisplacement)
        # self.player.enemy_coll(self.enemyGroup, self.player)
        self.HUD.update()

    def draw(self):
        self.background.draw()
        self.platformGroup.draw(self.manager.getScreen())
        self.itemGroup.draw(self.manager.getScreen())
        self.enemyGroup.draw(self.manager.getScreen())
        self.deadBodiesGroup.draw(self.manager.getScreen())
        self.spriteGroup.draw(self.manager.getScreen())
        self.HUD.draw()
        self.draw_lifebar_finalenemy()
        # self.draw_rects()

    def draw_rects(self):
        # Platform rects
        for item in self.itemGroup:
            self.draw_transparent_rect(item.getRect(), (255, 255, 255, 50))

        # Enemy rects
        for enemy in self.enemyGroup:
            self.draw_transparent_rect(enemy.getRect(), (255, 10, 10, 100))
            self.draw_transparent_rect(enemy.activity_range_rect, (10, 255, 255, 100))
            # self.draw_transparent_rect(enemy.getCollisionRect(), (0, 0, 0, 100))

        # Player rects
        self.draw_transparent_rect(self.player.getRect(), (23, 100, 255, 100))
        self.draw_transparent_rect(self.player.getCollisionRect(), (10, 255, 255, 100))

    def draw_transparent_rect(self, rect, colour):
        tmp = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA, 32)
        tmp.fill(colour)
        self.manager.getScreen().blit(tmp, (rect.left, rect.top))

    def initialize_lifebar_finalenemy(self):
        self.healthbar_length = 200
        self.healthbar_height = 20

    def draw_lifebar_finalenemy(self):
        for enemy in self.enemyGroup:
            if type(enemy).__name__ == "Satan":
                if not enemy.health == 500:
                    health = enemy.health
                    x = enemy.getRect().left + enemy.getRect().width / 2 - self.healthbar_length / 2
                    y = enemy.getRect().top - 50

                    # Escogemos color para la barra de salud
                    if health < 20:
                        foreground_color = (255, 0, 0)
                    else:
                        foreground_color = (0, 255, 0)

                    # Calculamos tamaño de la barra de salud
                    health_value = (float(health) / 500 * self.healthbar_length)
                    outline_rect = pygame.Rect(x, y, self.healthbar_length, self.healthbar_height)
                    fill_rect = pygame.Rect(x, y, health_value, self.healthbar_height)

                    # Dibujamos
                    pygame.draw.rect(self.screen, (70, 70, 70), outline_rect)
                    pygame.draw.rect(self.screen, foreground_color, fill_rect)
                    pygame.draw.rect(self.screen, (0, 0, 0), outline_rect, 3)

    def events(self, events_list):
        self.player.move(pygame.key.get_pressed())

    def resetScroll(self):
        self.playerDisplacement = (0, 0)

    def getDoUpdateScroll(self):
        return True
