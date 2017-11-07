# -*- coding: utf-8 -*-

from characters.MySprite import *

# Estados
STOPPED = 0
LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4
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

    def actualizarPostura(self):
        self.retardoMovimiento -= 1
        if self.retardoMovimiento < 0:
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

            # Si esta mirando a la izquiera, cogemos la porcion de la hoja
            if self.mirando == LEFT:
                if not self.invertedSpriteSheet:
                    self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
                else:
                    self.image = pygame.transform.flip(
                        self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0)
            # Si no, si mira a la derecha, invertimos esa imagen
            elif self.mirando == RIGHT:
                if not self.invertedSpriteSheet:
                    self.image = pygame.transform.flip(
                        self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0)
                else:
                    self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])

    def getVelocidad(self):
        return self.velocidad

    def setVelocidad(self,v):
        self.velocidad = v

    def getDoUpdateScroll(self):
        # Si se añade animación de caida habra que añadirlo aqui
        return self.numPostura == SPRITE_JUMPING

    def invertXSpeed(self):
        self.velocidad = (-self.velocidad[0], self.velocidad[1])
        if self.mirando == RIGHT:
            self.move(LEFT)
        elif self.mirando == LEFT:
            self.move(RIGHT)

    # Función move en la clase Character
    def move(self, movimiento):
        (vx, vy) = self.velocidad

        # Saltar
        if movimiento == UP:
            if vy == 0:
                self.numPostura = SPRITE_JUMPING
                vy = -self.velocidadSalto
                pygame.mixer.Sound('../bin/assets/sounds/player/salto.wav').play()

        # Moverse a la derecha
        elif movimiento == RIGHT:
            self.mirando = RIGHT
            vx = self.velocidadCarrera

        # Moverse a la izquierda
        elif movimiento == LEFT:
            self.mirando = LEFT
            vx = -self.velocidadCarrera

        # Parado
        elif movimiento == STOPPED:
            vx = 0

        # Atacar
        elif movimiento == ATTACK:
            # TODO implementar función de ataque
            print "Aqui debería atacar"

        self.velocidad = (vx, vy)

    # Función update de la clase Character
    def update(self, grupoPlataformas, tiempo, scroll):
        vx, vy = self.velocidad

        platform_collided = pygame.sprite.spritecollideany(self, grupoPlataformas)

        # Si tenía postura STOPPED
        if self.numPostura == SPRITE_STOPPED:
            if vx > 0 or vx < 0:
                self.numPostura = SPRITE_WALKING

        # Si tenía postura WALKING
        if self.numPostura == SPRITE_WALKING:
            if vx == 0:
                self.numPostura = SPRITE_STOPPED

            if platform_collided is not None:
                if not self.getCollisionRect().colliderect(platform_collided.getRect()):
                    self.numPostura = SPRITE_JUMPING
            else:
                self.numPostura = SPRITE_JUMPING

        if self.numPostura == SPRITE_JUMPING:
            plataforma = pygame.sprite.spritecollideany(self, grupoPlataformas)

            if (plataforma is not None) and (vy > 0) and (plataforma.rect.bottom > self.rect.bottom):
                if not self.getCollisionRect().colliderect(plataforma.getRect()):
                    vy += GRAVITY * tiempo
                    if vy > 0.25: vy = 0.25
                else:
                    # Lo situamos con la parte de abajo colisionando con la plataforma para detectar cuando se cae
                    self.setPosition((self.posicion[0], plataforma.posicion[1] - plataforma.rect.height + 10))
                    self.numPostura = SPRITE_WALKING
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

    def printPostura(self):
        if self.numPostura == SPRITE_STOPPED:
            return "SPRITE_STOPPED"
        elif self.numPostura == SPRITE_WALKING:
            return "SPRITE_WALKING"
        elif self.numPostura == SPRITE_JUMPING:
            return "SPRITE_JUMPING"
        elif self.numPostura == SPRITE_DYING:
            return "SPRITE_DYING"
        elif self.numPostura == SPRITE_FALLING:
            return "SPRITE_FALLING"
        elif self.numPostura == SPRITE_ATTACKING:
            return "SPRITE_ATTACKING"

    def printMirando(self):
        if self.mirando == RIGHT:
            return "MIRANDO RIGHT"
        elif self.mirando == LEFT:
            return "MIRANDO LEFT"

    def setInvertedSpriteSheet(self, b):
        self.invertedSpriteSheet = b
