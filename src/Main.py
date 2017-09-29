#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importar modulos
import pygame
from src.control.GameManager import *
from src.control.GameLevel import *
from src.data.DataRetriever import DataRetriever
if __name__ == '__main__':
    # Instancio un Singleton para cargar configuraciones
    data = DataRetriever()
    data.loadPreferences('../bin/config/preferences.json')  # Cargo preferencias de la aplicacion
    data.loadLevels('../bin/config/levels.json')            # Cargo datos de niveles
    data.loadPlayers('../bin/config/players.json')          # Cargo datos de los jugadores


    # Inicializamos la libreria de pygame
    pygame.init()
    # Creamos el director
    manager = GameManager(data)
    # manager.add(manager, Menu())
    manager.add(GameLevel(manager, data,"level_1"))
    manager.run()
    # Cuando se termine la ejecución, finaliza la librería
    pygame.quit()
'''
import pygame
import sys

# Por ahora cargo aqui pero habria que montar un gestor de niveles
# Cargo el escenario
Level1 = data.getLevel('level_1')

# Cargo assets Jugador
playerSheet = library.Load(data.getPlayerSheet('player'))
# Las posiciones de los sprites para cada animacion se obtienen
playerAnimations = data.getPlayerAnimations('player')


while not finished:
    clock.tick(fps)
    for e in pygame.event.get():
        # Se sale al pulsar Esc
        if e.type == pygame.KEYDOWN and e.key == int(data.getKeyQuit()):
            finished = True

#   Aqui ocurre la magia

    pygame.display.flip()
sys.exit()
'''