import pygame
import math

class Stage:
    def __init__(self, manager,  data, player):
        self.manager = manager
        self.data = data
        self.player = player
        self.layersStack = []
        self.setup()


    def setup(self):

        self.stageWidth = int(self.data["dimensions"][0])
        self.stageHeight = int(self.data["dimensions"][1])

        self.gravityX = int(self.data["gravity"][0])
        self.gravityY = int(self.data["gravity"][1])

        self.friction = int(self.data["friction"])

        for layer in self.data["bglayers"]:
            self.layersStack.append(Layer(self.manager,layer,self.stageWidth,self.stageHeight,self.player))

        pygame.display.update()

    def update(self,clock):
        self.manager.getScreen().fill(int(self.data["bgColor"],16))
        for layer in self.layersStack:
            layer.update(clock)

    def draw(self):
        for layer in self.layersStack:
            layer.draw()

'''
    def events(self, *args):
        raise NotImplemented("Tiene que implementar el metodo eventos.")

    def draw(self, pantalla):
        raise NotImplemented("Tiene que implementar el metodo dibujar.")

'''

class Layer(pygame.sprite.Sprite):
    def __init__(self,manager,layer,stageWidth,stageHeight, player):
        self.scrollX = 0# desplazamiento por el scroll
        self.scrollY = 0
        self.manager = manager
        self.layer = layer
        self.player = player
        self.stageWidth = stageWidth
        self.stageHeight = stageHeight
        self.x = int(self.layer["origin_x"]) # origen en el mapa de la capa
        self.y = int(self.layer["origin_x"])
        self.z = int(self.layer["origin_z"])
        self.image = self.manager.getLibrary().load(self.layer["image"],self.layer["color_key"])
        self.imageW, self.imageH = self.image.get_size()
        self.w, self.h = self.manager.getScreen().get_size()

        # Si se repite Horizontalmente
        if self.layer["repeat_x"]=="True": # Si se repite horizontalmente
            self.timesX = int(math.ceil(float(self.w*self.stageWidth)/ self.imageW))
        else:
            self.timesX = 1

        # Si se repite verticalmente ademas multiplico por origin_z
        if self.layer["repeat_y"] == "True":
            self.timesY = int(math.ceil(float(self.h* self.z * self.stageHeight) / self.imageH))
        else:
            self.timesY = 1

    def update(self,clock):
        self.scrollY -= math.ceil((self.player.getVelocidad()[1]*self.z*clock)/1)
        #self.scrollY = 0 # -= math.ceil(float(self.z*clock)/40)

    def draw(self):
        for i in range(0,self.timesX):
            for j in range(0,self.timesY):
                self.manager.getScreen().blit(self.image,(self.scrollX+self.x+self.imageW*i,self.scrollY+self.y+self.imageH*j))


