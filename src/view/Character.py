# -*- coding: utf-8 -*-

from view.MySprite import *

# Estados
STOPPED = 0
LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4
UPLEFT = 5
UPRIGHT = 6
DOWNLEFT = 7
DOWNRIGHT = 8
ATTACK = 9

# Animaciones
SPRITE_STOPPED = 0
SPRITE_WALKING = 1
SPRITE_JUMPING = 2
SPRITE_ATTACKING = 3
SPRITE_DYING = 4
SPRITE_FALLING = 5

# Variables movimiento
GRAVITY = 0.0007  # Píxeles / ms2


class Character(MySprite):
    def __init__(self, manager, data, archivoImagen, archivoCoordenadas, numImagenes, velocidadCarrera, velocidadSalto,
                 retardoAnimacion):
        MySprite.__init__(self, manager)
        self.numberOfPostures = len(numImagenes)
        self.manager = manager
        self.hoja = manager.getLibrary().load(archivoImagen, -1).convert_alpha()  # Se carga la hoja
        self.data = data
        self.movimiento = STOPPED  # El movimiento que esta realizando
        self.mirando = RIGHT  # Lado hacia el que esta mirando
        self.numImagenPostura = 0
        self.coordenadasHoja = []
        self.retardoMovimiento = 0
        self.numPostura = 0
        self.velocidadCarrera = velocidadCarrera
        self.velocidadSalto = velocidadSalto
        self.retardoAnimacion = retardoAnimacion  # El retardo en la animacion del personaje
        self.tiempo_colision = 0
        self.invertedSpriteSheet = False

        datos = manager.getLibrary().loadCoordsFile(archivoCoordenadas)  # Leemos las coordenadas de un archivo de texto
        datos = datos.split()
        cont = 0

        for linea in range(0, self.numberOfPostures):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]

            for postura in range(0, numImagenes[linea]):
                tmp.append(
                    pygame.Rect((int(datos[cont]), int(datos[cont + 1])), (int(datos[cont + 2]), int(datos[cont + 3]))))
                cont += 4
        # Creamos el rect
        self.rect = pygame.Rect(self.getGlobalPosition()[0],
                                self.getGlobalPosition()[1],
                                self.coordenadasHoja[self.numPostura][self.numImagenPostura].width,
                                self.coordenadasHoja[self.numPostura][self.numImagenPostura].height)
        # Actualizamos postura
        self.actualizarPostura()

    def move(self, movimiento):
        # todo mover a player??
        # actualizo el movimiento a menos que este en el aire y quiera actualizar a salto
        if (movimiento == UP or movimiento == UPRIGHT or movimiento == UPLEFT):
            if self.numPostura != SPRITE_JUMPING:
                self.movimiento = movimiento
                pygame.mixer.Sound('../bin/assets/sounds/player/salto.wav').play()
        else:
            self.movimiento = movimiento

    def attack(self, movimiento):
        # todo mover a player??
        self.movimiento = movimiento

    def actualizarPostura(self):
        self.retardoMovimiento -= 1
        if (self.retardoMovimiento < 0):
            self.retardoMovimiento = self.retardoAnimacion
            # Si ha pasado, actualizamos la postura
            self.numImagenPostura += 1

            if self.numImagenPostura >= len(self.coordenadasHoja[self.numPostura]):
                self.numImagenPostura = 0

            if self.numImagenPostura < 0:
                self.numImagenPostura = len(self.coordenadasHoja[self.numPostura]) - 1

            self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])

            # Actualizamos la variable rect para que se adapte al sprite
            self.rect = pygame.Rect(self.getGlobalPosition()[0], self.getGlobalPosition()[0],
                                    self.coordenadasHoja[self.numPostura][self.numImagenPostura].width,
                                    self.coordenadasHoja[self.numPostura][self.numImagenPostura].height)

            # Actualizamos el rect de colisión con plataformas

            # Si esta mirando a la izquiera, cogemos la porcion de la hoja
            if (self.mirando == LEFT or self.mirando == UPLEFT or self.mirando == DOWNLEFT):
                if self.invertedSpriteSheet == False:
                    self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
                else:
                    self.image = pygame.transform.flip(
                        self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0)
            # Si no, si mira a la derecha, invertimos esa imagen
            elif (self.mirando == RIGHT or self.mirando == UPRIGHT or self.mirando == DOWNRIGHT):
                if self.invertedSpriteSheet == False:
                    self.image = pygame.transform.flip(
                        self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0)
                else:
                    self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])

    def getVelocidad(self):
        return self.velocidad

    def getDoUpdateScroll(self):
        # Si se añade animacion de caida habra que añadirlo aqui
        return self.numPostura == SPRITE_JUMPING

    def invertXSpeed(self):
        self.velocidad = (-self.velocidad[0], self.velocidad[1])
        if self.movimiento == RIGHT:
            self.movimiento = LEFT
        elif self.movimiento == LEFT:
            self.movimiento = RIGHT

    def update(self, grupoPlataformas, tiempo, scroll):
        # todo mover a player??
        (vx, vy) = self.velocidad

        # Ataque
        if self.movimiento == ATTACK:
            self.numPostura = SPRITE_ATTACKING

        # Saltos
        if self.movimiento == UP:
            self.numPostura = SPRITE_JUMPING
            vy = -self.velocidadSalto
            self.movimiento = STOPPED
        elif self.movimiento == UPRIGHT or self.movimiento == UPLEFT:
            self.numPostura = SPRITE_JUMPING
            vy = -self.velocidadSalto
            if self.movimiento == UPLEFT:
                vx = -self.velocidadCarrera
                self.mirando = LEFT
            else:
                vx = self.velocidadCarrera
                self.mirando = RIGHT
            self.movimiento = STOPPED
        # Desplazamiento lateral
        elif (self.movimiento == LEFT) or (self.movimiento == RIGHT):
            # Esta mirando hacia ese lado
            self.mirando = self.movimiento

            # Si vamos a la izquierda, le ponemos velocidad en esa dirección
            if self.movimiento == LEFT:
                vx = -self.velocidadCarrera
            # Si vamos a la derecha, le ponemos velocidad en esa dirección
            else:
                vx = self.velocidadCarrera
            # Si no estamos en el aire
            if self.numPostura != SPRITE_JUMPING:
                # La postura actual sera estar caminando
                self.numPostura = SPRITE_WALKING
                # Ademas, si no estamos encima de ninguna plataforma, caeremos
                platform_collided = pygame.sprite.spritecollideany(self, grupoPlataformas)
                if platform_collided is not None:
                    if not self.getCollisionRect().colliderect(platform_collided.getRect()):
                        self.numPostura = SPRITE_JUMPING
                else:
                    self.numPostura = SPRITE_JUMPING
        elif self.movimiento == STOPPED:
            # Si no estamos saltando, la postura actual será estar quieto
            if not self.numPostura == SPRITE_JUMPING:
                self.numPostura = SPRITE_STOPPED
                vx = 0
            else:
                # si estoy saltando y no pulso derecha izda reduzco la velocidad lateral con easing exp
                if (vx > 0):
                    vx = vx + (-vx * 0.025)
                elif (vx < 0):
                    vx = vx + (-vx * 0.025)

        # Además, si estamos en el aire
        if self.numPostura == SPRITE_JUMPING:
            # Miramos a ver si hay que parar de caer: si hemos llegado a una plataforma
            #  Para ello, miramos si hay colision con alguna plataforma del grupo
            plataforma = pygame.sprite.spritecollideany(self, grupoPlataformas)
            #  Ademas, esa colision solo nos interesa cuando estamos cayendo
            #  y solo es efectiva cuando caemos encima, no de lado, es decir,
            #  cuando nuestra posicion inferior esta por encima de la parte de abajo de la plataforma
            if (plataforma is not None) and (vy > 0) and (plataforma.rect.bottom > self.rect.bottom):
                if not self.getCollisionRect().colliderect(plataforma.getRect()):
                    vy += GRAVITY * tiempo
                    if vy > 0.25: vy = 0.25
                else:
                    # Lo situamos con la parte de abajo colisionando con la plataforma para detectar cuando se cae
                    self.setPosition((self.posicion[0], plataforma.posicion[1] - plataforma.rect.height + 10))
                    self.numPostura = SPRITE_STOPPED
                    # Y estará quieto en el eje y
                    vy = 0
            # Si no caemos en una plataforma, aplicamos el efecto de la gravedad
            else:
                vy += GRAVITY * tiempo
                if vy > 0.25: vy = 0.25

        self.actualizarPostura()

        self.velocidad = (vx, vy)
        # Superclase calcula la nueva posición del Sprite con la velocidad
        MySprite.update(self, tiempo)

        if self.getDoUpdateScroll(): self.establecerPosicionPantalla((scroll[0], -scroll[1]))
        # if type(self).__name__ == "Asmodeo": print self.printMovimiento(), self.printPostura(), self.velocidad

    def printPostura(self):
        if self.numPostura == SPRITE_STOPPED:
            print "SPRITE_STOPPED"
        elif self.numPostura == SPRITE_WALKING:
            print "SPRITE_WALKING"
        elif self.numPostura == SPRITE_JUMPING:
            print "SPRITE_JUMPING"
        elif self.numPostura == SPRITE_DYING:
            print "SPRITE_DYING"
        elif self.numPostura == SPRITE_FALLING:
            print "SPRITE_FALLING"
        elif self.numPostura == SPRITE_ATTACKING:
            print "SPRITE_ATTACKING"

    def printMovimiento(self):
        if self.movimiento == UP:
            print "MOVE_UP"
        elif self.movimiento == UPLEFT:
            print "MOVE_UPLEFT"
        elif self.movimiento == UPRIGHT:
            print "MOVE_UPRIGHT"
        elif self.movimiento == STOPPED:
            print "MOVE_STOPPED"
        elif self.movimiento == LEFT:
            print "MOVE_LEFT"
        elif self.movimiento == RIGHT:
            print "MOVE_RIGHT"
        elif self.movimiento == DOWN:
            print "MOVE_DOWN"
        elif self.movimiento == ATTACK:
            print "MOVE_ATTACK"
        elif self.movimiento == DOWNLEFT:
            print "MOVE_DOWNLEFT"
        elif self.movimiento == DOWNRIGHT:
            print "MOVE_DOWNRIGHT"

    def setInvertedSpriteSheet(self, b):
        self.invertedSpriteSheet = b;
