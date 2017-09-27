import pygame
import sys
from src.data.DataRetriever import loadPreferences, printPreferences

clock = pygame.time.Clock()
screenFlags = pygame.DOUBLEBUF | pygame.HWSURFACE;
finished = False


# Preferencias
preferences = loadPreferences('../bin/config/preferences.json')
printPreferences(preferences)
screenSize = w, h = int(preferences['screen_res'][0]), int(preferences['screen_res'][1])
screenIcon = preferences['screen_icon']
screenTitle = preferences['screen_title']
fps = int(preferences['fps_target'])

# Inicializar la libreria de pygame
pygame.init()

# Creamos la pantalla
pygame.display.set_caption(screenTitle)
pygame.display.set_icon(pygame.image.load(screenIcon))
screen = pygame.display.set_mode(screenSize, screenFlags)

while not finished:
    now = clock.tick(fps)
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN and e.key == int(preferences['keys']['quit']):
            finished = True
#
    pygame.display.flip()
sys.exit()
