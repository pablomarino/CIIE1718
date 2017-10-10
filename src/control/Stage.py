# -*- encoding: utf-8 -*-

import pygame, math

from view.MySprite import MySprite


class Stage:
    def __init__(self, manager,  data, player, platformGroup):
        self.manager = manager
        self.data = data
        self.player = player

        self.backgroundStack = self.itemStack = self.enemyStack = []

        self.platformGroup = platformGroup

        self.setup()

    def setup(self):
        # Dimensiones de la pantalla
        self.stageWidth = int(self.data["dimensions"][0])
        self.stageHeight = int(self.data["dimensions"][1])

        # Gravedad
        self.gravityX = int(self.data["gravity"][0])
        self.gravityY = int(self.data["gravity"][1])

        # Cordenada Z de la capa de plataformas
        self.platforms_z = int(self.data["platforms_z"])

        # Genero las capas del Fondo
        for l in self.data["bglayers"]:
            bglayer = BgLayer(self.manager, l,self.player,  (self.stageWidth, self.stageHeight))
            self.backgroundStack.append(bglayer)


        # Genero las Plataformas
        for p in self.data["platforms"]:
            platform = Platform(self.manager,p, self.player,(self.stageWidth,self.stageHeight),  self.platforms_z)
            self.platformGroup.add(platform)


        '''
        # Items
        for i in self.data["items"]:
            item =Item(self.manager,i,self.stageWidth,self.stageHeight,self.player)
            self.itemStack.append(item)

        # Enemies
        for e in self.data["enemies"]:
            enemy = Enemy(self.manager, e, self.stageWidth, self.stageHeight, self.player)
            self.enemyStack.append(enemy)

        # Jugador
        '''


    def update(self,clock):
        self.manager.getScreen().fill(int(self.data["bgColor"], 16))
        for l in self.backgroundStack:
            l.update(clock)
        for p in self.platformGroup:
            p.update(clock)

    def draw(self):
        for l in self.backgroundStack:
            l.draw()
        self.platformGroup.draw(self.manager.getScreen())

    def events(self, *args):
        raise NotImplemented("Tiene que implementar el metodo eventos.")

## BGLAYER

class BgLayer(MySprite):
    def __init__(self,manager, data, player, dimensions):
        # Super
        MySprite.__init__(self)

        # Ref. a Gamemanager
        self.manager = manager
        # JSON
        self.data = data
        # Dimensiones de la pantalla
        self.stageDimensions = self.manager.getScreen().get_size()
        ## puede que plataformas no lo necesite
        # Dimensiones del nivel
        self.levelDimensions = dimensions
        # valor del scroll
        self.scrollValue = list((0, 0))
        # Limites del scroll
        self.scrollLimits = ( self.levelDimensions[0] - self.stageDimensions[0],
                             -self.levelDimensions[1] + self.stageDimensions[1])

        # Posicion de la plataforma
        self.position = (int(self.data["origin_x"]), int(self.data["origin_y"]))
        self.z = int(self.data["origin_z"])
        # Jugador
        self.player = player
        # Posicion inicial del jugador
        self.startPos = self.player.getPosition()
        # Obtengo la imagen
        self.image = self.manager.getLibrary().load(self.data["image"],self.data["color_key"])
        # Guardo sus dimensiones
        self.imageW, self.imageH = self.image.get_size()
        # El rectangulo del Sprite
        self.rect = pygame.Rect(self.position[0],self.position[1],self.imageW,self.imageH)

        # Si se repite Horizontalmente
        if self.data["repeat_x"]=="True": # Si se repite horizontalmente
            self.timesX = int(math.ceil(float(self.z*self.levelDimensions[0]) / self.imageW))
        else:
            self.timesX = 1

        # Si se repite verticalmente
        if self.data["repeat_y"] == "True":
            self.timesY = int(math.ceil(float(self.z*self.levelDimensions[1]) / self.imageH))
        else:
            self.timesY = 1


    def update(self ,clock):
        tmpPV=self.player.getVelocidad()
        self.scrollValue[0] -= math.ceil(tmpPV[0] * self.z * clock)
        self.scrollValue[1] -= math.ceil(tmpPV[1] * self.z * clock)
        
       # me aseguro de que no se salga la pantalla

        if self.scrollValue[0] < self.scrollLimits[0]:
            self.scrollValue[0] = self.scrollLimits[0]
        elif self.scrollValue[0] > 0 :
            self.scrollValue[0] = 0

        if self.scrollValue[1] > 0:
            self.scrollValue[1] = 0
        elif self.scrollValue[1] < self.scrollLimits[1]:
            self.scrollValue[1] = self.scrollLimits[1]

    def draw(self):
        for i in range(0, self.timesX):
            for j in range(0, self.timesY):
                self.manager.getScreen().blit(self.image, (
                self.scrollValue[0] +self.position[0] + self.imageW * i,
                self.scrollValue[1] +self.position[1] + self.imageH * j)
                )

## PLATFORM

class Platform(MySprite):
    def __init__(self,manager, data, player, dimensions, origin_z):
        # Super
        MySprite.__init__(self)

        # Referencia a Gamemanager
        self.manager = manager
        # Datos del JSON
        self.data = data
        # Dimensiones de la pantalla
        self.stageDimensions = self.manager.getScreen().get_size()
        # Dimensiones del nivel
        self.levelDimensions = dimensions
        # valor del scroll
        self.scrollValue = list((0,0))
        # Limites del scroll
        self.scrollLimits=(self.levelDimensions[0] - self.stageDimensions[0], -self.levelDimensions[1] + self.stageDimensions[1])
        # Posicion de la plataforma
        self.position = (int(self.data["origin_x"]), int(self.data["origin_y"]))
        self.z = origin_z
        # Jugador
        self.player = player
        # Posicion inicial del jugador
        self.startPos = self.player.getPosition()
        # Obtengo la imagen
        self.image = self.manager.getLibrary().load(self.data["image"],self.data["color_key"])
        # Guardo sus dimensiones
        self.imageW, self.imageH = self.image.get_size()
        # El rectangulo del Sprite
        self.rect = pygame.Rect(self.position[0],self.position[1],self.imageW,self.imageH)
        self.setPosition(self.position)

    def update(self ,clock):
        pass
        # el no jugador esta en el centro de la pantalla
        # y no he superado el limite superior de la pantalla
        # y no he superado el limite inferior de la pantalla
        # Actualizo el scroll

        # self.setPosition((self.player.getPosition()[0]-self.startPos[0],self.player.getPosition()[1]-self.startPos[1]))
        # self.incrementarPosicion((0,math.ceil(self.player.getVelocidad()[1] *clock )))





