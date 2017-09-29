import pygame
import src.control.GameLevel
from src.data.DataRetriever import DataRetriever
import sys

class GameManager:

    def __init__(self,data):
        self.data = data
        self.screenFlags = pygame.DOUBLEBUF | pygame.HWSURFACE
        self.finished = False
        self.clock = None
        self.fps = None

        # Inicializamos la pantalla y el modo grafico
        pygame.display.set_caption(self.data.getWindowTitle())
        pygame.display.set_icon(pygame.image.load(self.data.getWindowIcon()))
        self.screen = pygame.display.set_mode([self.data.getWidth(), self.data.getHeight()], self.screenFlags)
        self.clock = pygame.time.Clock()
        self.finished = False

        # Accedo a los metodos del singleton para obtener las configuraciones
        self.fps = self.data.getFps()

    def run(self):
        while not self.finished:
            self.clock.tick(self.fps)
            for e in pygame.event.get():
                # Se sale al pulsar Esc
                if e.type == pygame.KEYDOWN and e.key == int(self.data.getKeyQuit()):
                    self.finished = True

                    #   Aqui ocurre la magia

            pygame.display.flip()
        sys.exit()