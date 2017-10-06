# -*- encoding: utf-8 -*-

import pygame, math

class Stage:
    def __init__(self, manager,  data, player, platformGroup):
        self.manager = manager
        self.data = data
        self.player = player

        self.backgroundStack = self.platformStack = self.itemStack = self.enemyStack = []

        self.platformGroup = platformGroup

        self.setup()


    def setup(self):

        self.stageWidth = int(self.data["dimensions"][0])
        self.stageHeight = int(self.data["dimensions"][1])

        self.gravityX = int(self.data["gravity"][0])
        self.gravityY = int(self.data["gravity"][1])

        self.platforms_z = int(self.data["platforms_z"])

        # Fondo
        for l in self.data["bglayers"]:
            bglayer = BgLayer(self.manager, l, self.stageWidth, self.stageHeight, self.player)
            self.backgroundStack.append(bglayer)

        # Plataformas
        for p in self.data["platforms"]:
            platform = Platform(self.manager,p,self.stageWidth,self.stageHeight,self.player,  self.platforms_z)
            #self.platformGroup.add(platform)
            self.platformStack.append(platform)
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
    def updateScroll(self):
        return 0,0

    def update(self,clock):
        self.manager.getScreen().fill(int(self.data["bgColor"],16))
        for l in self.backgroundStack:
            l.update(clock)
        for p in self.platformStack:
            p.update(clock)

    def draw(self):
        for layer in self.backgroundStack:
            layer.draw()
        for p in self.platformStack:
            p.draw()

    def events(self, *args):
        raise NotImplemented("Tiene que implementar el metodo eventos.")


class BgLayer(pygame.sprite.Sprite):
    def __init__(self,manager,layer,stageWidth,stageHeight, player):

        self.scrollX = self.scrollY = 0 # desplazamiento por el scroll
        self.manager = manager
        self.layer = layer
        self.player = player
        self.stageWidth = stageWidth
        self.stageHeight = stageHeight
        self.x = int(self.layer["origin_x"]) # origen en el mapa de la capa
        self.y = int(self.layer["origin_y"])
        self.z = int(self.layer["origin_z"])
        self.w, self.h = self.manager.getScreen().get_size() # Tamaño de la pantalla
        self.image = self.manager.getLibrary().load(self.layer["image"],self.layer["color_key"])
        self.imageW, self.imageH = self.image.get_size()


        # Si se repite Horizontalmente
        if self.layer["repeat_x"]=="True": # Si se repite horizontalmente
            self.timesX = int(math.ceil(float( self.z*self.stageWidth)/ self.imageW))
        else:
            self.timesX = 1

        # Si se repite verticalmente
        if self.layer["repeat_y"] == "True":
            self.timesY = int(math.ceil(float( self.z * self.stageHeight) / self.imageH))
        else:
            self.timesY = 1

    def update(self ,clock):

        delay = .2
        self.scrollX -= math.ceil(self.player.getVelocidad()[0] * self.z * clock * delay)
        self.scrollY -= math.ceil(self.player.getVelocidad()[1] * self.z * clock * delay)


        # me aseguro de que no se salga la pantalla
        if self.scrollX < self.stageWidth - self.w:
            self.scrollX = self.stageWidth - self.w
        elif self.scrollX > 0 :
            self.scrollX = 0


        if self.scrollY > 0 :
            self.scrollY = 0
        elif self.scrollY < -self.stageHeight+self.h :
            self.scrollY =  -self.stageHeight+self.h


    def draw(self):
        for i in range(0,self.timesX):
            for j in range(0,self.timesY):
                self.manager.getScreen().blit(self.image,(self.scrollX+self.x+self.imageW*i,self.scrollY+self.y+self.imageH*j))


class Platform(pygame.sprite.Sprite):
    def __init__(self,manager,layer,stageWidth,stageHeight, player, origin_z):
        self.scrollX = self.scrollY = 0 # desplazamiento por el scroll
        self.manager = manager
        self.layer = layer
        self.player = player
        self.stageWidth = stageWidth
        self.stageHeight = stageHeight
        self.x = int(self.layer["origin_x"]) # origen en el mapa de la capa
        self.y = int(self.layer["origin_y"])
        self.z = origin_z
        self.w, self.h = self.manager.getScreen().get_size() # Tamaño de la pantalla
        self.image = self.manager.getLibrary().load(self.layer["image"],self.layer["color_key"])
        self.imageW, self.imageH = self.image.get_size()


    def update(self ,clock):
        delay = .2
        self.scrollX -= math.ceil(self.player.getVelocidad()[0] * self.z * clock * delay)
        self.scrollY -= math.ceil(self.player.getVelocidad()[1] * self.z * clock * delay)

       # me aseguro de que no se salga la pantalla
        if self.scrollX < self.stageWidth - self.w:
            self.scrollX = self.stageWidth - self.w
        elif self.scrollX > 0 :
            self.scrollX = 0

        if self.scrollY > 0 :
            self.scrollY = 0
        elif self.scrollY < -self.stageHeight+self.h :
            self.scrollY =  -self.stageHeight+self.h

    def draw(self):
        self.manager.getScreen().blit(self.image,(self.scrollX+self.x,self.scrollY+self.y))


'''
class Item(pygame.sprite.Sprite):
    def __init__(self,manager,layer,stageWidth,stageHeight, player):
        self.scrollX = self.scrollY = 0 # desplazamiento por el scroll
        self.manager = manager
        self.layer = layer
        self.player = player
        self.stageWidth = stageWidth
        self.stageHeight = stageHeight
        self.x = int(self.layer["origin_x"]) # origen en el mapa de la capa
        self.y = int(self.layer["origin_y"])
        self.w, self.h = self.manager.getScreen().get_size() # Tamaño de la pantalla
        self.image = self.manager.getLibrary().load(self.layer["image"],self.layer["color_key"])
        self.imageW, self.imageH = self.image.get_size()


    def update(self ,clock):
        delay = .2
        self.scrollX -= math.ceil(self.player.getVelocidad()[0] * self.z * clock * delay)
        self.scrollY -= math.ceil(self.player.getVelocidad()[1] * self.z * clock * delay)

    def draw(self):
        self.manager.getScreen().blit(self.image,(self.scrollX+self.x+self.imageW,self.scrollY+self.y+self.imageH))



class Enemy(pygame.sprite.Sprite):
    def __init__(self,manager,layer,stageWidth,stageHeight, player):
        self.scrollX = self.scrollY = 0 # desplazamiento por el scroll
        self.manager = manager
        self.layer = layer
        self.player = player
        self.stageWidth = stageWidth
        self.stageHeight = stageHeight
        self.x = int(self.layer["origin_x"]) # origen en el mapa de la capa
        self.y = int(self.layer["origin_y"])
        self.w, self.h = self.manager.getScreen().get_size() # Tamaño de la pantalla
        self.image = self.manager.getLibrary().load(self.layer["image"],self.layer["color_key"])
        self.imageW, self.imageH = self.image.get_size()


    def update(self ,clock):
        delay = .2
        self.scrollX -= math.ceil(self.player.getVelocidad()[0] * self.z * clock * delay)
        self.scrollY -= math.ceil(self.player.getVelocidad()[1] * self.z * clock * delay)

    def draw(self):
        self.manager.getScreen().blit(self.image,(self.scrollX+self.x+self.imageW,self.scrollY+self.y+self.imageH))


'''