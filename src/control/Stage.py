import pygame

class Stage:
    def __init__(self, manager,  data):
        self.manager = manager
        self.data = data
        self.setup()

    def setup(self):
        self.manager.getScreen().fill(int(self.data["bgColor"],16))
        self.stageWidth = self.data["dimensions"][0]
        self.stageHeight = self.data["dimensions"][1]

        self.gravityX = self.data["gravity"][0]
        self.gravityY = self.data["gravity"][1]

        self.friction = self.data["friction"]

        for layer in self.data["bglayers"]:
            Layer(self.manager,layer)

        pygame.display.update()

    def update(self, *args):
        raise NotImplemented("Tiene que implementar el metodo update.")

    def events(self, *args):
        raise NotImplemented("Tiene que implementar el metodo eventos.")

    def draw(self, pantalla):
        raise NotImplemented("Tiene que implementar el metodo dibujar.")


class Layer:
    def __init__(self,manager,layer):
        self.manager = manager
        self.layer = layer
        image =  self.manager.getLibrary().load(self.layer["image"])
        self.manager.getScreen().blit(image,(int(self.layer["origin_x"]),int(self.layer["origin_y"])))
