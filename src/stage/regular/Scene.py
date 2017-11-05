# -*- encoding: utf-8 -*-


class Scene:
    def __init__(self, director):
        self.width = director.getDataRetriever().getWidth()
        self.height = director.getDataRetriever().getHeight()
