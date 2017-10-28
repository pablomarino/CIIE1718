# -*- coding: utf-8 -*-

from view.MySprite import *

STOPPED = 0  # estados
LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4
UPLEFT = 5
UPRIGHT = 6
DOWNLEFT = 7
DOWNRIGHT = 8
ATTACK = 9
SPRITE_STOPPED = 0  # animaciones
SPRITE_WALKING = 1
SPRITE_JUMPING = 2
SPRITE_ATTACKING = 3
SPRITE_DYING = 4
SPRITE_FALLING = 5
SPRITE_ATTACKING = 3
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
        self.numPostura = 1
        self.numImagenPostura = 0
        self.coordenadasHoja = []
        self.retardoMovimiento = 0
        self.numPostura = SPRITE_JUMPING  # En que postura esta inicialmente
        self.velocidadCarrera = velocidadCarrera
        self.velocidadSalto = velocidadSalto
        self.retardoAnimacion = retardoAnimacion  # El retardo en la animacion del personaje
        self.tiempo_colision = 0

        datos = manager.getLibrary().loadCoordsFile(archivoCoordenadas)  # Leemos las coordenadas de un archivo de texto
        datos = datos.split()

        cont = 0;
        for linea in range(0, self.numberOfPostures):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for postura in range(1, numImagenes[linea] + 1):
                tmp.append(
                    pygame.Rect((int(datos[cont]), int(datos[cont + 1])), (int(datos[cont + 2]), int(datos[cont + 3]))))
                cont += 4
        self.rect = pygame.Rect(100, 100, self.coordenadasHoja[self.numPostura][self.numImagenPostura][2],
                                self.coordenadasHoja[self.numPostura][self.numImagenPostura][3])
        self.actualizarPostura()

    def move(self, movimiento):
        # actualizo el movimiento a menos que este en el aire y quiera actualizar a salto
        if (movimiento == UP or movimiento == UPRIGHT or movimiento == UPLEFT):
            if self.numPostura != SPRITE_JUMPING:
                self.movimiento = movimiento
                pygame.mixer.Sound('../bin/assets/sounds/player/salto.wav').play()
        else:
            self.movimiento = movimiento

    def attack(self, movimiento):
        self.movimiento = movimiento

    def actualizarPostura(self):
        self.retardoMovimiento -= 1
        if (self.retardoMovimiento < 0):
            self.retardoMovimiento = self.retardoAnimacion
            # Si ha pasado, actualizamos la postura
            self.numImagenPostura += 1
            if self.numImagenPostura >= len(self.coordenadasHoja[self.numPostura]):
                self.numImagenPostura = 0;
            if self.numImagenPostura < 0:
                self.numImagenPostura = len(self.coordenadasHoja[self.numPostura]) - 1
            self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
            # Si esta mirando a la izquiera, cogemos la porcion de la hoja
            if (self.mirando == LEFT or self.mirando == UPLEFT or self.mirando == DOWNLEFT):
                self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
            # Si no, si mira a la derecha, invertimos esa imagen
            elif (self.mirando == RIGHT or self.mirando == UPRIGHT or self.mirando == DOWNRIGHT):
                self.image = pygame.transform.flip(
                    self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0)

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
        # TODO cuando el jugador salta, todos los enemigos saltan también, solo que tienen jumpSpeed=0 y no se aprecia
        # (vx, vy) = self.velocidad
        (vx, vy) = self.velocidad
        self.printMovimiento()

        if self.movimiento == ATTACK:
            self.numPostura = SPRITE_ATTACKING

        if self.movimiento == UP:
            # La postura actual sera estar saltando
            self.numPostura = SPRITE_JUMPING
            # Le imprimimos una velocidad en el eje y
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

        if (self.movimiento == LEFT) or (self.movimiento == RIGHT):
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
                if pygame.sprite.spritecollideany(self, grupoPlataformas) == None:
                    self.numPostura = SPRITE_JUMPING
            '''
            # Si queremos saltar
            
            elif self.movimiento == UP:
                # La postura actual sera estar saltando
                self.numPostura = SPRITE_JUMPING
                # Le imprimimos una velocidad en el eje y
                vy = -self.velocidadSalto
                self.movimiento = STOPPED
            '''
        # Si no se ha pulsado ninguna tecla
        elif self.movimiento == STOPPED:
            # Si no estamos saltando, la postura actual será estar quieto
            if not self.numPostura == SPRITE_JUMPING:
                self.numPostura = SPRITE_STOPPED
                vx = 0

        # Además, si estamos en el aire
        if self.numPostura == SPRITE_JUMPING:
            # Miramos a ver si hay que parar de caer: si hemos llegado a una plataforma
            #  Para ello, miramos si hay colision con alguna plataforma del grupo
            plataforma = pygame.sprite.spritecollideany(self, grupoPlataformas)
            #  Ademas, esa colision solo nos interesa cuando estamos cayendo
            #  y solo es efectiva cuando caemos encima, no de lado, es decir,
            #  cuando nuestra posicion inferior esta por encima de la parte de abajo de la plataforma
            if (plataforma != None) and (vy > 0) and (plataforma.rect.bottom > self.rect.bottom):
                # Lo situamos con la parte de abajo un pixel colisionando con la plataforma
                #  para poder detectar cuando se cae de ella
                # print self.posicion[0], plataforma.posicion[1],plataforma.rect.height, plataforma.posicion[1]-plataforma.rect.height+1
                self.setPosition((self.posicion[0], plataforma.posicion[1] - plataforma.rect.height + 2))
                # Lo ponemos como quieto
                self.numPostura = SPRITE_STOPPED
                # Y estará quieto en el eje y
                vy = 0
            # Si no caemos en una plataforma, aplicamos el efecto de la gravedad
            else:
                vy += GRAVITY * tiempo
                if vy > 0.25: vy = 0.25

        # Actualizamos la imagen a mostrar
        self.actualizarPostura()

        # Aplicamos la velocidad en cada eje
        self.velocidad = (vx, vy)

        # Y llamamos al método de la superclase para que, según la velocidad y el tiempo
        #  calcule la nueva posición del Sprite
        MySprite.update(self, tiempo)

        if self.getDoUpdateScroll():
            self.establecerPosicionPantalla((scroll[0], -scroll[1]))

    def printPostura(self):
        pass
        # if self.numPostura == SPRITE_STOPPED:
        #     print "SPRITE_STOPPED"
        # elif self.numPostura == SPRITE_WALKING:
        #     print "SPRITE_WALKING"
        # elif self.numPostura == SPRITE_JUMPING:
        #     print "SPRITE_JUMPING"
        # elif self.numPostura == SPRITE_DYING:
        #     print "SPRITE_DYING"
        # elif self.numPostura == SPRITE_FALLING:
        #     print "SPRITE_FALLING"
        # elif self.numPostura == SPRITE_ATTACKING:
        #     print "SPRITE_ATTACKING"

    def printMovimiento(self):
<<<<<<< HEAD
        if self.movimiento == UP:
            print "MOVE_UP"
        elif self.movimiento == UPLEFT:
            print "MOVE_UPLEFT"
        elif self.movimiento == UPRIGHT:
            print "MOVE_UPRIGHT"
        # elif self.movimiento == STOPPED:
        #     print "MOVE_STOPPED"
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
=======
        pass
        # if self.movimiento == UP:
        #     print "MOVE_UP"
        # elif self.movimiento == UPLEFT:
        #     print "MOVE_UPLEFT"
        # elif self.movimiento == UPRIGHT:
        #     print "MOVE_UPRIGHT"
        # elif self.movimiento == STOPPED:
        #     print "MOVE_STOPPED"
        # elif self.movimiento == LEFT:
        #     print "MOVE_LEFT"
        # elif self.movimiento == RIGHT:
        #     print "MOVE_RIGHT"
        # elif self.movimiento == DOWN:
        #     print "MOVE_DOWN"
        # elif self.movimiento == ATTACK:
        #     print "MOVE_ATTACK"
        # elif self.movimiento == DOWNLEFT:
        #     print "MOVE_DOWNLEFT"
        # elif self.movimiento == DOWNRIGHT:
        #     print "MOVE_DOWNRIGHT"
>>>>>>> 733b4d9c2424b1f3fe2b2a9769507eeeb5476a14
