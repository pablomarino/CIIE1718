import pygame
import sys
from src.data.DataRetriever import DataRetriever

clock = pygame.time.Clock()
screenFlags = pygame.DOUBLEBUF | pygame.HWSURFACE
finished = False

# Cargo preferencias de la aplicacion
data = DataRetriever()
data.loadPreferences('../bin/config/preferences.json')
fps = data.getFps();

# Cargo datos de niveles
data.loadLevels('../bin/config/levels.json')

# Cargo datos de los jugadores
data.loadPlayers('../bin/config/players.json')
#print(data.getPlayerSheet('beatrice'))


# Inicializar la libreria de pygame
pygame.init()

# Creamos la pantalla
pygame.display.set_caption(data.getWindowTitle())
pygame.display.set_icon(pygame.image.load(data.getWindowIcon()))
screen = pygame.display.set_mode([data.getWidth(), data.getHeight()], screenFlags)

while not finished:
    clock.tick(fps)
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN and e.key == int(data.getKeyQuit()):
            finished = True

# Aqui ocurre la magia

    pygame.display.flip()
sys.exit()

