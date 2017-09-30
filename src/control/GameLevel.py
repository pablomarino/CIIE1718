# -*- encoding: utf-8 -*-

# -------------------------------------------------
# Clase Escena con lo metodos abstractos
from control.Stage import Stage
from data.DataRetriever import DataRetriever
class GameLevel:
    def __init__(self, manager, data, id):
        self.manager = manager
        self.level = data.getLevel(id)
        if self.level:
           self.stage = Stage(self.manager, self.level)
        else:
           print "Error no existe nivel con id ",id

    def update(self, *args):
        self.stage.update()
      

    def events(self, *args):
        raise NotImplemented("Tiene que implementar el metodo eventos.")

    def draw(self, pantalla):
        raise NotImplemented("Tiene que implementar el metodo dibujar.")
