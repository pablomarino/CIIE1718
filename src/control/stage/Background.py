from view.MySprite import *
import math

class BackGround():

    def __init__(self, manager, data, player, levelDimensions):
        self.scroll = list((0, 0))
        self.backgroundStack = []
        self.manager = manager
        self.data = data
        self.player = player
        self.levelDimensions = levelDimensions

        for l in self.data:
            bglayer = BgLayer(self, l)
            self.backgroundStack.append(bglayer)

    def getScrollValue(self):
        return self.scroll

    def update(self, clock, scroll):
        for l in self.backgroundStack:
            l.update(clock,scroll)


    def draw(self):
        for l in self.backgroundStack:
            l.draw()

    def events(self, *args):
        raise NotImplemented("Tiene que implementar el metodo eventos.")



## BGLAYER

class BgLayer(MySprite):
    def __init__(self,parent, data):
        # Super
        MySprite.__init__(self)

        # Ref. a Gamemanager
        self.manager = parent.manager
        # JSON
        self.data = data
        # Dimensiones de la pantalla
        self.stageDimensions = self.manager.getScreen().get_size()
        ## puede que plataformas no lo necesite
        # Dimensiones del nivel
        self.levelDimensions = parent.levelDimensions
        # valor del scroll
        self.scroll = list((0, 0))
        '''
        # Limites del scroll
        self.scrollLimits = ( self.levelDimensions[0] - self.stageDimensions[0],
                             -self.levelDimensions[1] + self.stageDimensions[1])
        '''
        # Posicion de la plataforma
        self.position = (int(self.data["origin_x"]), int(self.data["origin_y"]))
        self.z = int(self.data["origin_z"])
        # Jugador
        self.player = parent.player
        # Posicion inicial del jugador
        self.startPos = self.player.getGlobalPosition()
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
        self.z = 1

    def update(self ,clock, scroll):
        # Todo comprobar valores a partir de los que es necesario realizar el scroll
        # me aseguro de que no se salga la pantalla
        '''
        if self.scroll[0] < self.scrollLimits[0]:
            self.scroll[0] = self.scrollLimits[0]
        elif self.scroll[0] > 0 :
            self.scroll[0] = 0

        if self.scroll[1] > 0:
            self.scroll[1] = 0
        elif self.scroll[1] < self.scrollLimits[1]:
            self.scroll[1] = self.scrollLimits[1]
        '''
        #self.targetX = self.position[0] + scroll[0] * self.z
        #self.targetY = self.position[1] + scroll[1] * self.z
        self.establecerPosicionPantalla((-scroll[0]* self.z, -scroll[1]* self.z))


    def draw(self):
        for i in range(0, self.timesX):
            for j in range(0, self.timesY):
                #self.manager.getScreen().blit(self.image, (self.targetX + self.imageW * i,self.targetY + self.imageH * j))
                self.manager.getScreen().blit(self.image,(self.rect.left*self.z + self.imageW * i, self.rect.bottom*self.z  + self.imageH * j))
