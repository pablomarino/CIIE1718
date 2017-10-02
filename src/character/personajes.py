# -*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *
from GestorRecursos import *

# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

# Movimientos
QUIETO = 0
IZQUIERDA = 1
DERECHA = 2
ARRIBA = 3
ABAJO = 4

#Posturas
SPRITE_QUIETO = 0
SPRITE_ANDANDO = 1
SPRITE_SALTANDO = 2

# Velocidades de los distintos personajes
VELOCIDAD_JUGADOR = 0.2 # Pixeles por milisegundo
VELOCIDAD_SALTO_JUGADOR = 0.3 # Pixeles por milisegundo
RETARDO_ANIMACION_JUGADOR = 5 # updates que durará cada imagen del personaje
                              # debería de ser un valor distinto para cada postura

GRAVEDAD = 0.0007 # Píxeles / ms2

# -------------------------------------------------
# Clase MiSprite
class MiSprite(pygame.sprite.Sprite):
    "Los Sprites que tendra este juego"
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.posicion = (0, 0)
        self.velocidad = (0, 0)
        self.scroll   = (0, 0)

    def setPosition(self, posicion):
        self.posicion = posicion
        self.rect.left = self.posicion[0] - self.scroll[0]
        self.rect.bottom = self.posicion[1] - self.scroll[1]

    def establecerPosicionPantalla(self, scrollDecorado):
        self.scroll = scrollDecorado;
        (scrollx, scrolly) = self.scroll;
        (posx, posy) = self.posicion;
        self.rect.left = posx - scrollx;
        self.rect.bottom = posy - scrolly;

    def incrementarPosicion(self, incremento):
        (posx, posy) = self.posicion
        (incrementox, incrementoy) = incremento
        self.setPosition((posx+incrementox, posy+incrementoy))

    def update(self, tiempo):
        incrementox = self.velocidad[0]*tiempo
        incrementoy = self.velocidad[1]*tiempo
        self.incrementarPosicion((incrementox, incrementoy))


# -------------------------------------------------
# Clases Personaje

#class Personaje(pygame.sprite.Sprite):
class Personaje(MiSprite):
    "Cualquier personaje del juego"

    # Parametros pasados al constructor de esta clase:
    #  Archivo con la hoja de Sprites
    #  Archivo con las coordenadoas dentro de la hoja
    #  Numero de imagenes en cada postura
    #  Velocidad de caminar y de salto
    #  Retardo para mostrar la animacion del personaje
    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidadCarrera, velocidadSalto, retardoAnimacion):

        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self);

        # Se carga la hoja
        self.hoja = GestorRecursos.CargarImagen(archivoImagen, -1)

        self.hoja = self.hoja.convert_alpha()
        # El movimiento que esta realizando
        self.movimiento = QUIETO
        # Lado hacia el que esta mirando
        self.mirando = DERECHA

        # Leemos las coordenadas de un archivo de texto
        datos = GestorRecursos.CargarArchivoCoordenadas(archivoCoordenadas)
        datos = datos.split()
        self.numPostura = 1;
        self.numImagenPostura = 0;
        cont = 0;
        self.coordenadasHoja = [];
        for linea in range(0, 3):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for postura in range(1, numImagenes[linea]+1):
                tmp.append(pygame.Rect((int(datos[cont]), int(datos[cont+1])), (int(datos[cont+2]), int(datos[cont+3]))))
                cont += 4

        # El retardo a la hora de cambiar la imagen del Sprite (para que no se mueva demasiado rápido)
        self.retardoMovimiento = 0;

        # En que postura esta inicialmente
        self.numPostura = QUIETO

        # El rectangulo del Sprite
        self.rect = pygame.Rect(100,100,self.coordenadasHoja[self.numPostura][self.numImagenPostura][2],self.coordenadasHoja[self.numPostura][self.numImagenPostura][3])

        # Las velocidades de caminar y salto
        self.velocidadCarrera = velocidadCarrera
        self.velocidadSalto = velocidadSalto

        # El retardo en la animacion del personaje (podria y deberia ser distinto para cada postura)
        self.retardoAnimacion = retardoAnimacion

        # Y actualizamos la postura del Sprite inicial, llamando al metodo correspondiente
        self.actualizarPostura()


    # Metodo base para realizar el movimiento: simplemente se le indica cual va a hacer, y lo almacena
    def move(self, movimiento):
        if movimiento == ARRIBA:
            # Si estamos en el aire y el personaje quiere saltar, ignoramos este movimiento
            if self.numPostura == SPRITE_SALTANDO:
                self.movimiento = QUIETO
            else:
                self.movimiento = ARRIBA
        else:
            self.movimiento = movimiento


    def actualizarPostura(self):
        self.retardoMovimiento -= 1
        # Miramos si ha pasado el retardo para dibujar una nueva postura
        if (self.retardoMovimiento < 0):
            self.retardoMovimiento = self.retardoAnimacion
            # Si ha pasado, actualizamos la postura
            self.numImagenPostura += 1
            if self.numImagenPostura >= len(self.coordenadasHoja[self.numPostura]):
                self.numImagenPostura = 0;
            if self.numImagenPostura < 0:
                self.numImagenPostura = len(self.coordenadasHoja[self.numPostura])-1
            self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])

            # Si esta mirando a la izquiera, cogemos la porcion de la hoja
            if self.mirando == IZQUIERDA:
                self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
            #  Si no, si mira a la derecha, invertimos esa imagen
            elif self.mirando == DERECHA:
                self.image = pygame.transform.flip(self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0)


    def update(self, grupoPlataformas, tiempo):

        # Las velocidades a las que iba hasta este momento
        (velocidadx, velocidady) = self.velocidad

        # Si vamos a la izquierda o a la derecha        
        if (self.movimiento == IZQUIERDA) or (self.movimiento == DERECHA):
            # Esta mirando hacia ese lado
            self.mirando = self.movimiento

            # Si vamos a la izquierda, le ponemos velocidad en esa dirección
            if self.movimiento == IZQUIERDA:
                velocidadx = -self.velocidadCarrera
            # Si vamos a la derecha, le ponemos velocidad en esa dirección
            else:
                velocidadx = self.velocidadCarrera

            # Si no estamos en el aire
            if self.numPostura != SPRITE_SALTANDO:
                # La postura actual sera estar caminando
                self.numPostura = SPRITE_ANDANDO
                # Ademas, si no estamos encima de ninguna plataforma, caeremos
                if pygame.sprite.spritecollideany(self, grupoPlataformas) == None:
                    self.numPostura = SPRITE_SALTANDO

        # Si queremos saltar
        elif self.movimiento == ARRIBA:
            # La postura actual sera estar saltando
            self.numPostura = SPRITE_SALTANDO
            # Le imprimimos una velocidad en el eje y
            velocidady = -self.velocidadSalto

        # Si no se ha pulsado ninguna tecla
        elif self.movimiento == QUIETO:
            # Si no estamos saltando, la postura actual será estar quieto
            if not self.numPostura == SPRITE_SALTANDO:
                self.numPostura = SPRITE_QUIETO
            velocidadx = 0



        # Además, si estamos en el aire
        if self.numPostura == SPRITE_SALTANDO:

            # Miramos a ver si hay que parar de caer: si hemos llegado a una plataforma
            #  Para ello, miramos si hay colision con alguna plataforma del grupo
            plataforma = pygame.sprite.spritecollideany(self, grupoPlataformas)
            #  Ademas, esa colision solo nos interesa cuando estamos cayendo
            #  y solo es efectiva cuando caemos encima, no de lado, es decir,
            #  cuando nuestra posicion inferior esta por encima de la parte de abajo de la plataforma
            if (plataforma != None) and (velocidady>0) and (plataforma.rect.bottom>self.rect.bottom):
                # Lo situamos con la parte de abajo un pixel colisionando con la plataforma
                #  para poder detectar cuando se cae de ella
                self.setPosition((self.posicion[0], plataforma.posicion[1]-plataforma.rect.height+1))
                # Lo ponemos como quieto
                self.numPostura = SPRITE_QUIETO
                # Y estará quieto en el eje y
                velocidady = 0

            # Si no caemos en una plataforma, aplicamos el efecto de la gravedad
            else:
                velocidady += GRAVEDAD * tiempo

        # Actualizamos la imagen a mostrar
        self.actualizarPostura()

        # Aplicamos la velocidad en cada eje      
        self.velocidad = (velocidadx, velocidady)

        # Y llamamos al método de la superclase para que, según la velocidad y el tiempo
        #  calcule la nueva posición del Sprite
        MiSprite.update(self, tiempo)
        
        return


# -------------------------------------------------
# Clase Player

class Player(Personaje):
    "Cualquier personaje del juego"
    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        # Personaje.__init__(self,'Jugador.png','coordJugador.txt', [6, 12, 6], VELOCIDAD_JUGADOR, VELOCIDAD_SALTO_JUGADOR, RETARDO_ANIMACION_JUGADOR);
        Personaje.__init__(self,'player_beatrice.png','player_beatrice_coords.txt', [6, 7, 6], VELOCIDAD_JUGADOR, VELOCIDAD_SALTO_JUGADOR, RETARDO_ANIMACION_JUGADOR);


    def move(self, pressedKeys, arriba, izquierda, derecha):
        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
        if pressedKeys[arriba]:
            Personaje.move(self,ARRIBA)
        elif pressedKeys[izquierda]:
            Personaje.move(self,IZQUIERDA)
        elif pressedKeys[derecha]:
            Personaje.move(self,DERECHA)
        else:
            Personaje.move(self,QUIETO)
