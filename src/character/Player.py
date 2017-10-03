# -*- coding: utf-8 -*-
from character.Character import Character


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

class Player(Character):
    "Cualquier personaje del juego"
    def __init__(self, data):
        self.id = 'player'
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        # Character.__init__(self,'Jugador.png','coordJugador.txt', [6, 12, 6], VELOCIDAD_JUGADOR, VELOCIDAD_SALTO_JUGADOR, RETARDO_ANIMACION_JUGADOR);
        Character.__init__(self, data.getPlayerSheet(self.id),'player_beatrice_coords.txt', [6, 7, 6], VELOCIDAD_JUGADOR, VELOCIDAD_SALTO_JUGADOR, RETARDO_ANIMACION_JUGADOR);


    def move(self, pressedKeys, arriba, izquierda, derecha):
        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
        if pressedKeys[arriba]:
            Character.move(self,ARRIBA)
        elif pressedKeys[izquierda]:
            Character.move(self,IZQUIERDA)
        elif pressedKeys[derecha]:
            Character.move(self,DERECHA)
        else:
            Character.move(self,QUIETO)
