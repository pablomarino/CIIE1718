import pygame
import sys
import json


clock = pygame.time.Clock()
screenFlags = pygame.DOUBLEBUF | pygame.HWSURFACE;
finished = False

def loadPreferences(file):
    with open(file) as preferences_file:
        data = json.load(preferences_file)
    return data

def printPreferences(data):
    print('\nPreferences\n==================')
    print('Version     : ' + data['version'])
    print('Resolution  : ' + data['screen_res'][0] + 'x' + data['screen_res'][1])
    print('Screen Icon : ' + data['screen_icon'])
    print('Screen Title: ' + data['screen_title'])
    print('Fps         : ' + data['fps_target'])
    print('Keys quit   : ' + data['keys']['quit'][0] + ', ' + data['keys']['quit'][1])
    print('Keys up     : ' + data['keys']['up'][0] + ', ' + data['keys']['up'][1])
    print('Keys down   : ' + data['keys']['down'][0] + ', ' + data['keys']['down'][1])
    print('Keys left   : ' + data['keys']['left'][0] + ', ' + data['keys']['left'][1])
    print('Keys right  : ' + data['keys']['right'][0] + ', ' + data['keys']['right'][1])
    print('Keys bt1    : ' + data['keys']['bt1'][0] + ', ' + data['keys']['bt1'][1])
    print('Keys bt2    : ' + data['keys']['bt2'][0] + ', ' + data['keys']['bt2'][1])

# Preferencias
preferences = loadPreferences('config/preferences.json')
#printPreferences(preferences)
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
