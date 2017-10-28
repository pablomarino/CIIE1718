#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importar modulos
from control.GameManager import *
from control.stage.Menu2 import Menu
from data.DataRetriever import DataRetriever

if __name__ == '__main__':
    # Instancio un Singleton para cargar configuraciones
    data = DataRetriever()
    data.loadPreferences('../bin/config/preferences.json')  # Cargo preferencias de la aplicacion
    data.loadLevels('../bin/config/levels.json')  # Cargo datos de niveles
    data.loadPlayers('../bin/config/players.json')  # Cargo datos de los jugadores

    # Inicializamos la libreria de pygame
    pygame.init()
    # Creamos el director
    manager = GameManager(data)

    menu = Menu(manager)
    manager.add(menu)

    # manager.add(GameLevel(manager, data, "level_1"))
    manager.run()
