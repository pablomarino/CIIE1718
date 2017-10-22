# -*- coding: utf-8 -*-
from view.Character import *


class Player(Character):
    "Cualquier personaje del juego"

    def __init__(self, manager, data, id):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        # TODO cambiar el constructor de Character por (self, data, id)
        # Dentro del propio constructor elige el sprite y demás valores buscando en el dataRetriever
        Character.__init__(self,
                           manager,
                           data,
                           data.getPlayerSheet(id),
                           data.getPlayerSheetCoords(id),
                           [5, 9, 5, 3],
                           data.getPlayerSpeed(),
                           data.getPlayerJumpSpeed(),
                           data.getPlayerAnimationDelay());

    def move(self, pressedKeys):
        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
        if pressedKeys[self.data.getKeyUp()]:
            Character.move(self, UP)
            pygame.mixer.Sound('../bin/assets/sounds/player/salto.wav').play()
        elif pressedKeys[self.data.getKeyLeft()]:
            Character.move(self, LEFT)
        elif pressedKeys[self.data.getKeyRight()]:
            Character.move(self, RIGHT)
        else:
            Character.move(self, STOPPED)
