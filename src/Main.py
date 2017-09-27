import pygame
import sys
from src.data.DataRetriever import DataRetriever

clock = pygame.time.Clock()
screenFlags = pygame.DOUBLEBUF | pygame.HWSURFACE
finished = False

# Instancio un objeto para cargar configuraciones
data = DataRetriever()
data.loadPreferences('../bin/config/preferences.json')# Cargo preferencias de la aplicacion
data.loadLevels('../bin/config/levels.json')# Cargo datos de niveles
data.loadPlayers('../bin/config/players.json')# Cargo datos de los jugadores
fps = data.getFps()

# print(data.getPlayerSheet('beatrice')) # para acceder al spritesheet y posiciones de los sprites de un jugador


# Inicializar la libreria de pygame
pygame.init()

# Creamos la pantalla
pygame.display.set_caption(data.getWindowTitle())
pygame.display.set_icon(pygame.image.load(data.getWindowIcon()))
screen = pygame.display.set_mode([data.getWidth(), data.getHeight()], screenFlags)

while not finished:
    clock.tick(fps)
    for e in pygame.event.get():
        # Se sale al pulsar Esc
        if e.type == pygame.KEYDOWN and e.key == int(data.getKeyQuit()):
            finished = True

# Aqui ocurre la magia

    pygame.display.flip()
sys.exit()
