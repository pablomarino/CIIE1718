# -*- coding: utf-8 -*-
from character.Character import *

# Velocidades de los distintos personajes
VELOCIDAD_JUGADOR = 0.2 # Pixeles por milisegundo
VELOCIDAD_SALTO_JUGADOR = 0.3 # Pixeles por milisegundo
RETARDO_ANIMACION_JUGADOR = 5 # updates que durará cada imagen del personaje
                              # debería de ser un valor distinto para cada postura

class Player(Character):
    "Cualquier personaje del juego"
    def __init__(self, data, id):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        # TODO cambiar el constructor de Character por (self, data, id)
        # Dentro del propio constructor elige el sprite y demás valores buscando en el dataRetriever
        Character.__init__(self, data, data.getPlayerSheet(id),'player_beatrice_coords.txt', [6, 7, 6], VELOCIDAD_JUGADOR, VELOCIDAD_SALTO_JUGADOR, RETARDO_ANIMACION_JUGADOR);


    def move(self, pressedKeys, arriba, izquierda, derecha):
        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
        if pressedKeys[arriba]:
            Character.move(self,UP)
        elif pressedKeys[izquierda]:
            Character.move(self,LEFT)
        elif pressedKeys[derecha]:
            Character.move(self,RIGHT)
        else:
            Character.move(self,STOPPED)
