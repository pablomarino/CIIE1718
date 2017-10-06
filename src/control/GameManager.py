import pygame,sys
from utils.AssetLoader import AssetLoader


class GameManager:

    def __init__(self,data):
        self.data = data
        self.stack = []
        self.screenFlags = pygame.DOUBLEBUF | pygame.HWSURFACE
        self.finished = False
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

    def add(self, level):
        self.stack.append(level)

    def run(self):
        while not self.finished:
            time = self.clock.tick(self.fps)
            for e in pygame.event.get():
                # Se sale al pulsar Esc
                if e.type == pygame.KEYDOWN and e.key == int(self.data.getKeyQuit()):
                    self.finished = True
                # Call 'events' function in the current level
                self.stack[0].events()

            #   Aqui ocurre la magia (HardCoded)
            self.stack[0].update(time)
            self.stack[0].draw()

            pygame.display.flip()
        pygame.quit()
        sys.exit()

    def getScreen(self):
        return self.screen

    def getLibrary(self):
        return self.library