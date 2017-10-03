# -*- coding: utf-8 -*-
from character.personajes import Personaje

# Movimientos
QUIETO = 0
IZQUIERDA = 1
DERECHA = 2
ARRIBA = 3
ABAJO = 4

# Velocidades de los distintos personajes
VELOCIDAD_JUGADOR = 0.2 # Pixeles por milisegundo
VELOCIDAD_SALTO_JUGADOR = 0.3 # Pixeles por milisegundo
RETARDO_ANIMACION_JUGADOR = 5 # updates que durará cada imagen del personaje
                              # debería de ser un valor distinto para cada postura

class Player(Personaje):
    "Cualquier personaje del juego"
    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        # Personaje.__init__(self,'Jugador.png','coordJugador.txt', [6, 12, 6], VELOCIDAD_JUGADOR, VELOCIDAD_SALTO_JUGADOR, RETARDO_ANIMACION_JUGADOR);
        Personaje.__init__(self,'player_beatrice.png','player_beatrice_coords.txt', [6, 7, 6], VELOCIDAD_JUGADOR, VELOCIDAD_SALTO_JUGADOR, RETARDO_ANIMACION_JUGADOR);


    def move(self, pressedKeys, arriba, izquierda, derecha):
        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
        if pressedKeys[arriba]:
            Personaje.move(self,ARRIBA)
        elif pressedKeys[izquierda]:
            Personaje.move(self,IZQUIERDA)
        elif pressedKeys[derecha]:
            Personaje.move(self,DERECHA)
        else:
            Personaje.move(self,QUIETO)
