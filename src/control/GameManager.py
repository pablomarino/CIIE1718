# -*- coding: utf-8 -*-

import re
import sys

import pygame

from stage.menu.Menu import Menu
from utils.AssetLoader import AssetLoader


class GameManager:
    def __init__(self, data):
        self.data = data
        self.stack = list()
        self.screenFlags = pygame.DOUBLEBUF | pygame.HWSURFACE
        self.finished_scene = False
        self.clock = None
        self.fps = None

        # Instancio el cargador de medios
        self.library = AssetLoader()

        # Música de fondo
        pygame.mixer.music.load(self.data.getMusicFile())
        # pygame.mixer.music.play()

        # Inicializamos la pantalla y el modo grafico
        pygame.display.set_caption(self.data.getWindowTitle())
        pygame.display.set_icon(pygame.image.load(self.data.getWindowIcon()))
        self.screen = pygame.display.set_mode([self.data.getWidth(), self.data.getHeight()], self.screenFlags)
        self.clock = pygame.time.Clock()
        self.finished = False

        # Accedo a los metodos del singleton para obtener las configuraciones
        self.fps = self.data.getFps()

        # Prueba para corregir la función events del juego
        self.events_list = []

    def add(self, level):
        self.stack.append(level)

    def addNextLevel(self):
        from control.GameLevel import GameLevel

        # Get numeric id of the new level
        actual_level = self.stack.__getitem__(0)
        levelid = actual_level.getId()
        result = re.sub('[^0-9]', '', levelid)
        levelnumber = int(result) + 1

        # Check if the new level exists
        if levelnumber <= self.data.getNumberOfLevels():
            self.add(
                GameLevel(self, self.getDataRetriever(), "level_" + str(levelnumber), actual_level.getPlayerStats()))
        else:
            print "Victoria"
            # TODO crear un menú de victoria
            self.add(Menu(self))

    def changeScene(self):
        self.finished_scene = True
        if len(self.stack) > 0:
            self.stack.pop(0)

    def endGame(self):
        self.stack = list()
        self.finished = True

    def run(self):
        while not self.finished:
            time = self.clock.tick(self.fps)
            self.events_list = pygame.event.get()
            for e in self.events_list:
                # Se sale al pulsar Esc
                if e.type == pygame.KEYDOWN and e.key == int(self.data.getKeyQuit()):
                    self.endGame()

                # Call 'events' function in the current level
                if len(self.stack) > 0:
                    self.stack[0].events(self.events_list)

            # Update and draw the stack items
            if len(self.stack) > 0:
                self.stack[0].update(time)
                self.stack[0].draw()

            pygame.display.flip()
        pygame.quit()
        sys.exit()

    def getScreen(self):
        return self.screen

    def getLibrary(self):
        return self.library

    def getDataRetriever(self):
        return self.data

    def getStack(self):
        return self.stack
