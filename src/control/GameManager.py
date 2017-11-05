# -*- coding: utf-8 -*-
import sys

import pygame

from utils.AssetLoader import AssetLoader


class GameManager:
    def __init__(self, data):
        self.data = data
        self.stack = []
        self.screenFlags = pygame.DOUBLEBUF | pygame.HWSURFACE
        self.finished_scene = False
        self.clock = None
        self.fps = None
        # Instancio el cargador de medios
        self.library = AssetLoader()

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

    # TODO Crear función para incrementar nivel

    def changeScene(self):
        self.finished_scene = True
        if len(self.stack) > 0:
            self.stack.pop()

    def endGame(self):
        self.stack = []
        self.finished = True

    def addScene(self, scene):
        self.finished_scene = True
        self.stack.append(scene)

    def run(self):
        while not self.finished:
            time = self.clock.tick(self.fps)
            self.events_list = pygame.event.get()
            for e in self.events_list:
                # Se sale al pulsar Esc
                if e.type == pygame.KEYDOWN and e.key == int(self.data.getKeyQuit()):
                    self.endGame()

                # if e.type == pygame.KEYDOWN and e.key == int(self.data.getKeyReturn()):
                #     self.changeScene()
                #     self.add(GameLevel(self, self.data, "level_2"))
                #     pass

                # Call 'events' function in the current level
                if len(self.stack) > 0:
                    self.stack[len(self.stack) - 1].events(self.events_list)

            # Update and draw the stack items
            if len(self.stack) > 0:
                self.stack[len(self.stack) - 1].update(time)
                self.stack[len(self.stack) - 1].draw()

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
