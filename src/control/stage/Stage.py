# -*- encoding: utf-8 -*-

import sys

from control.HUD import HUD
from control.stage.Background import *
from control.stage.Platform import Platform
from control.stage.Scene import Scene
from view.Enemy import *
from view.Item import *


def str_to_class(str):
    return getattr(sys.modules[__name__], str)


class Stage(Scene):
    def __init__(self, manager, data, player, platformGroup, spriteGroup, enemyGroup,itemGroup):
        Scene.__init__(self, manager)
        self.manager = manager
        self.data = data
        self.player = player
        self.playerStartPosition = self.player.getGlobalPosition()
        self.playerDisplacement = list((0, 0))
        self.spriteGroup = spriteGroup
        self.platformGroup = platformGroup
        self.enemyGroup = enemyGroup
        self.itemGroup = itemGroup
        self.setup()

    def setup(self):
        # Dimensiones de la pantalla
        self.levelDimensions = ((int(self.data["dimensions"][0]), int(self.data["dimensions"][1])))

        # Cordenada Z de la capa de plataformas
        self.platforms_z = int(self.data["platforms_z"])

        # Genero la capa del Fondo
        self.background = BackGround(self.manager, self.data["bglayers"], self.player, self.levelDimensions)

        self.mapFile = self.data["map_file"]
        # TODO los 3 tipos de plataforma tienen el miso sprite
        self.platformfiles = self.data["platform_files"]

        # Creamos el nivel a partir de fichero de texto
        self.create_level()

        # Creamos el HUD
        self.HUD = HUD(self.manager.getDataRetriever(), self.manager.getScreen(), self.player)

    def create_level(self):
        # Tamaño que representa cada letra del mapa.txt
        MAP_UNIT_WIDTH = 55
        MAP_UNIT_HEIGHT = 55
        # Variables
        column_number = 0
        row_number = 0
        # Asignación de letras a objetos
        platform_letter = "1"
        enemy_letter = "a"
        fire_letter = "f"
        heart_letter = "h"

        # Abrimos mapa en formato txt y lo leemos letra a letra
        with open(self.mapFile, "r") as f:
            for line in f:
                platform_size = 0
                prev_letter = " "

                for letter in line:
                    # Si hay la letra asignada a plataformas, aumentamos el tamaño de la plataforma a crear una posición
                    if letter == platform_letter:
                        platform_size = platform_size + 1

                    # Create enemies
                    if letter == enemy_letter:
                        tmp = str_to_class(self.data["enemies"][0])(self.manager, self.manager.getDataRetriever())
                        tmp.setPosition((column_number * MAP_UNIT_WIDTH, row_number * MAP_UNIT_HEIGHT))
                        self.enemyGroup.add(tmp)

                    # Create Items
                    if letter == fire_letter:
                        tmp = str_to_class("fire")(self.manager, self.manager.getDataRetriever())
                        tmp.setPosition((column_number * MAP_UNIT_WIDTH, row_number * MAP_UNIT_HEIGHT))
                        self.itemGroup.add(tmp)

                    if letter == heart_letter:
                        tmp= str_to_class("heart")(self.manager, self.manager.getDataRetriever())
                        tmp.setPosition((column_number * MAP_UNIT_WIDTH, row_number * MAP_UNIT_HEIGHT))
                        self.itemGroup.add(tmp)


                    # Creamos plataformas
                    if letter != platform_letter and prev_letter == platform_letter:
                        platform = Platform(
                            self.manager,
                            (column_number * MAP_UNIT_WIDTH, row_number * MAP_UNIT_HEIGHT),
                            self.platformfiles[0],
                            self.platforms_z,
                            platform_size)
                        self.platformGroup.add(platform)
                        platform_size = 0




                    # Incrementar el contador de columnas
                    column_number = column_number + 1

                    # Asignar el valor de la letra actual a la variable prev_letter
                    prev_letter = letter

                # Create last platform
                if prev_letter == platform_letter:
                    platform = Platform(
                        self.manager,
                        (column_number * MAP_UNIT_WIDTH, row_number * MAP_UNIT_HEIGHT),
                        self.platformfiles[0],
                        self.platforms_z,
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
        if (self.player.getDoUpdateScroll() & self.getDoUpdateScroll()):
            self.playerDisplacement = (
                0,  # int(math.ceil(self.playerStartPosition[0]-self.player.getPosition()[0])),
                int(math.ceil(self.playerStartPosition[1] - self.player.getGlobalPosition()[1]))
            )
        # print "player ", self.player.getGlobalPosition()[1], self.player.getLocalPosition()[1]
        self.background.update(clock, self.playerDisplacement)

        for p in self.platformGroup:
            p.update(clock, self.playerDisplacement)

        for i in self.itemGroup:
            i.update(self.platformGroup, clock, self.playerDisplacement)

        self.player.update(clock, self.playerDisplacement, self.platformGroup, self.enemyGroup, self.itemGroup)
        self.enemyGroup.update(self.platformGroup, clock, self.playerDisplacement)
        # self.player.enemy_coll(self.enemyGroup, self.player)
        self.HUD.update()

    def draw(self):
        self.background.draw()
        self.platformGroup.draw(self.manager.getScreen())
        self.spriteGroup.draw(self.manager.getScreen())
        self.enemyGroup.draw(self.manager.getScreen())
        self.itemGroup.draw(self.manager.getScreen())
        self.HUD.draw()
        self.draw_rects()

    def draw_rects(self):
        # Platform rects
        for item in self.itemGroup:
             self.draw_transparent_rect(item.getRect(), (255, 255, 255, 50))

        # Enemy rects
        for enemy in self.enemyGroup:
            self.draw_transparent_rect(enemy.getRect(), (255, 10, 10, 100))

        # Player rects
        self.draw_transparent_rect(self.player.getRect(), (23, 100, 255, 100))
        self.draw_transparent_rect(self.player.getCollisionRect(), (10, 255, 255, 100))

    def draw_transparent_rect(self, rect, colour):
        tmp = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA, 32)
        tmp.fill(colour)
        self.manager.getScreen().blit(tmp, (rect.left, rect.top))

    def events(self, events_list):
        self.player.move(pygame.key.get_pressed())

    def resetScroll(self):
        self.playerDisplacement = (0,0)

    def getDoUpdateScroll(self):
        # TODO Implementar
        '''
        retval = False

        if self.player.getPosition()[1] > self.manager.getScreen().get_size()[1]/2:
            retval = True
            print self.playerDisplacement
        '''
        retval = True
        return retval
