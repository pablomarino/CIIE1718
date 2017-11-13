#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importar modulos
from control.GameManager import *
from data.DataRetriever import DataRetriever
from control.GameLevel import GameLevel
from stage.menu.Menu import Menu

if __name__ == '__main__':
    # Instancio un Singleton para cargar configuraciones
    data = DataRetriever()
    data.loadPreferences('../bin/config/preferences.json')  # Cargo preferencias de la aplicacion
    data.loadLevels('../bin/config/levels.json')  # Cargo datos de niveles
    data.loadPlayers('../bin/config/players.json')  # Cargo datos de los jugadores
    data.loadItems('../bin/config/items.json')  # Cargo datos de los items

    # Inicializamos la librería de pygame
    pygame.init()
    # Creamos el director
    manager = GameManager(data)

    # menu = Menu(manager)
    # manager.add(menu)

    # Playerstats (lives, maxHealth, health, score)
    lives = 1
    max_health = 100
    health = 100
    score = 0

    player_stats = (lives, max_health, health, score)
    manager.add(GameLevel(manager, data, "level_5", player_stats))
    manager.run()
