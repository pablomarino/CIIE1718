# -*- coding: utf-8 -*-
from view.MySprite import MySprite
from GestorRecursos import *


# Movimientos
STOPPED = 0
LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4

#Posturas
SPRITE_STOPPED = 0
SPRITE_WALKING = 1
SPRITE_JUMPING = 2
SPRITE_DYING = 3

GRAVITY = 0.0007 # Píxeles / ms2


class Character(MySprite):
    "Cualquier personaje del juego"

    # Parametros pasados al constructor de esta clase:
    #  Archivo con la hoja de Sprites
    #  Archivo con las coordenadoas dentro de la hoja
    #  Numero de imagenes en cada postura
    #  Velocidad de caminar y de salto
    #  Retardo para mostrar la animacion del personaje
    def __init__(self, data, archivoImagen, archivoCoordenadas, numImagenes, velocidadCarrera, velocidadSalto, retardoAnimacion):

        # Primero invocamos al constructor de la clase padre
        MySprite.__init__(self);

        # Guardamos el número de posturas del personaje
        self.numberOfPostures = len(numImagenes)

        # Se carga la hoja
        self.hoja = GestorRecursos.CargarImagen(archivoImagen, -1)

        # Guardamos instancia del dataRetriever
        self.data = data

        self.hoja = self.hoja.convert_alpha()
        # El movimiento que esta realizando
        self.movimiento = STOPPED
        # Lado hacia el que esta mirando
        self.mirando = RIGHT

        # Leemos las coordenadas de un archivo de texto
        datos = GestorRecursos.CargarArchivoCoordenadas(archivoCoordenadas)
        datos = datos.split()
        self.numPostura = 1;
        self.numImagenPostura = 0;
        cont = 0;
        self.coordenadasHoja = [];
        for linea in range(0, self.numberOfPostures):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for postura in range(1, numImagenes[linea]+1):
                tmp.append(pygame.Rect((int(datos[cont]), int(datos[cont+1])), (int(datos[cont+2]), int(datos[cont+3]))))
                cont += 4

        # El retardo a la hora de cambiar la imagen del Sprite (para que no se mueva demasiado rápido)
        self.retardoMovimiento = 0;

        # En que postura esta inicialmente
        self.numPostura = SPRITE_JUMPING

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
        if movimiento == UP:
            # Si estamos en el aire y el personaje quiere saltar, ignoramos este movimiento
            if self.numPostura == SPRITE_JUMPING:
                self.movimiento = STOPPED
            else:
                self.movimiento = UP
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
            if self.mirando == LEFT:
                self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
            #  Si no, si mira a la derecha, invertimos esa imagen
            elif self.mirando == RIGHT:
                self.image = pygame.transform.flip(self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0)


    def update(self, grupoPlataformas, tiempo):

        print(pygame.sprite.spritecollideany(self, grupoPlataformas))

        # Las velocidades a las que iba hasta este momento
        (velocidadx, velocidady) = self.velocidad

        # Si vamos a la izquierda o a la derecha        
        if (self.movimiento == LEFT) or (self.movimiento == RIGHT):
            # Esta mirando hacia ese lado
            self.mirando = self.movimiento

            # Si vamos a la izquierda, le ponemos velocidad en esa dirección
            if self.movimiento == LEFT:
                velocidadx = -self.velocidadCarrera
            # Si vamos a la derecha, le ponemos velocidad en esa dirección
            else:
                velocidadx = self.velocidadCarrera

            # Si no estamos en el aire
            if self.numPostura != SPRITE_JUMPING:
                # La postura actual sera estar caminando
                self.numPostura = SPRITE_WALKING
                # Ademas, si no estamos encima de ninguna plataforma, caeremos
                if pygame.sprite.spritecollideany(self, grupoPlataformas) == None:
                    self.numPostura = SPRITE_JUMPING

        # Si queremos saltar
        elif self.movimiento == UP:
            # La postura actual sera estar saltando
            self.numPostura = SPRITE_JUMPING
            # Le imprimimos una velocidad en el eje y
            velocidady = -self.velocidadSalto
            self.movimiento = STOPPED

        # Si no se ha pulsado ninguna tecla
        elif self.movimiento == STOPPED:
            # Si no estamos saltando, la postura actual será estar quieto
            if not self.numPostura == SPRITE_JUMPING:
                self.numPostura = SPRITE_STOPPED
            velocidadx = 0
            # TODO decidir si poner velocidadY = 0



        # Además, si estamos en el aire
        if self.numPostura == SPRITE_JUMPING:

            # Miramos a ver si hay que parar de caer: si hemos llegado a una plataforma
            #  Para ello, miramos si hay colision con alguna plataforma del grupo
            plataforma = pygame.sprite.spritecollideany(self, grupoPlataformas)
            #  Ademas, esa colision solo nos interesa cuando estamos cayendo
            #  y solo es efectiva cuando caemos encima, no de lado, es decir,
            #  cuando nuestra posicion inferior esta por encima de la parte de abajo de la plataforma
            if (plataforma != None) and (velocidady>0) and (plataforma.rect.bottom>self.rect.bottom):
                # Lo situamos con la parte de abajo un pixel colisionando con la plataforma
                #  para poder detectar cuando se cae de ella
                # print self.posicion[0], plataforma.posicion[1],plataforma.rect.height, plataforma.posicion[1]-plataforma.rect.height+1
                self.setPosition((self.posicion[0], plataforma.posicion[1]-plataforma.rect.height+2))
                # Lo ponemos como quieto
                self.numPostura = SPRITE_STOPPED
                # Y estará quieto en el eje y
                velocidady = 0

            # Si no caemos en una plataforma, aplicamos el efecto de la gravedad
            else:
                velocidady += GRAVITY * tiempo
                ###
                ###
                ### todo Hay que limitar la velocidad de caida y al llegar al maximo si choca con plataforma muere
                ###
                ###
                if velocidady>0.01:velocidady=0.05

        # Actualizamos la imagen a mostrar
        self.actualizarPostura()

        # Aplicamos la velocidad en cada eje      
        self.velocidad = (velocidadx, velocidady)

        # Y llamamos al método de la superclase para que, según la velocidad y el tiempo
        #  calcule la nueva posición del Sprite
        MySprite.update(self, tiempo)
        
        return


    def getVelocidad(self):
        return self.velocidad

    def getDoUpdateScroll(self):
        return self.numPostura == SPRITE_JUMPING
