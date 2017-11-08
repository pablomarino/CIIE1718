#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importar modulos
from control.GameManager import *
from data.DataRetriever import DataRetriever
from control.GameLevel import GameLevel
from stage.menu.Menu2 import Menu

if __name__ == '__main__':
    # Instancio un Singleton para cargar configuraciones
    data = DataRetriever()
    data.loadPreferences('../bin/config/preferences.json')  # Cargo preferencias de la aplicacion
    data.loadLevels('../bin/config/levels.json')  # Cargo datos de niveles
    data.loadPlayers('../bin/config/players.json')  # Cargo datos de los jugadores
    data.loadItems('../bin/config/items.json')  # Cargo datos de los items

    # Inicializamos la libreria de pygame
    pygame.init()
    # Creamos el director
    manager = GameManager(data)

    #menu = Menu(manager)
    #manager.add(menu)

    player_stats = (3, 100, 100, 0)
    manager.add(GameLevel(manager, data, "level_1", player_stats))
    manager.run()
