# -*- encoding: utf-8 -*-
from src.control.GameManager import GameManager
from src.data.DataRetriever import DataRetriever



# -------------------------------------------------
# Clase Escena con lo metodos abstractos

class Scene:

    def __init__(self, director):
        self.width= director.getDataRetriever().getWidth()
        self.height=director.getDataRetriever().getHeight()

