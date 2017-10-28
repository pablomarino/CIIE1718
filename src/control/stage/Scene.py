# -*- encoding: utf-8 -*-




# -------------------------------------------------
# Clase Escena con lo metodos abstractos

class Scene:

    def __init__(self, director):
        self.width= director.getDataRetriever().getWidth()
        self.height=director.getDataRetriever().getHeight()

