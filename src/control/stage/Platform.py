from view.MySprite import *

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
        # Obtengo la imagen
        self.image = self.manager.getLibrary().load(self.data["image"],self.data["color_key"])
        # Guardo sus dimensiones
        self.imageW, self.imageH = self.image.get_size()
        # El rectangulo del Sprite
        self.rect = pygame.Rect(self.position[0],self.position[1],self.imageW,self.imageH)
        self.setPosition(self.position)

    def update(self ,clock, scrollValue):
        self.scrollValue = scrollValue*self.z
        #print scrollValue
        targetX = self.position[0]-self.scrollValue[0]*self.z
        targetY = self.position[1]-self.scrollValue[1]*self.z
        self.setPosition((targetX,targetY))
        
        # print self.player.getPosition(), self.scrollValue, self.position[0], self.position[1]
        # el no jugador esta en el centro de la pantalla
        # y no he superado el limite superior de la pantalla
        # y no he superado el limite inferior de la pantalla
        # Actualizo el scroll




