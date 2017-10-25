from view.MySprite import *


class Platform(MySprite):
    def __init__(self, manager, position, imageFile, origin_z):
        # Super
        MySprite.__init__(self)
        # Dimensiones de la pantalla
        self.stageDimensions = manager.getScreen().get_size()
        # Posicion de la plataforma
        # self.position = (int(data["origin_x"]), int(data["origin_y"]))
        self.z = origin_z
        # Obtengo la imagen
        # self.image = manager.getLibrary().load(data["image"], data["color_key"])
        self.image = manager.getLibrary().load(imageFile, -1)
        # Guardo sus dimensiones
        self.imageW, self.imageH = self.image.get_size()
        # El rectangulo del Sprite
        self.rect = pygame.Rect(position[0], position[1], self.imageW, self.imageH)
        self.setPosition(position)

        # TODO eliminar
        self.z = 1

    def update(self, clock, scroll):
        # print scroll
        # targetX = self.position[0]+scroll[0]* -self.z
        # targetY = self.position[1]+scroll[1]* -self.z
        # self.setPosition((targetX,targetY))
        self.establecerPosicionPantalla((-scroll[0] * self.z, -scroll[1] * self.z))
