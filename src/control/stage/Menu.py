# -*- encoding: utf-8 -*-

import pygame
from pygame.locals import *
from src.control.GameLevel import *
#from gestorRecursos import *
from src.data.DataRetriever import DataRetriever
from src.control.GameManager import *
#from fase import Fase


# ANCHO_PANTALLA = 1024
# ALTO_PANTALLA = 768

# -------------------------------------------------
# Clase abstracta ElementoGUI

class ElementoGUI:
    def __init__(self, pantalla, rectangulo):
        self.pantalla = pantalla
        self.rect = rectangulo

    def establecerPosicion(self, posicion):
        (posicionx, posiciony) = posicion
        self.rect.left = posicionx
        self.rect.bottom = posiciony

    def posicionEnElemento(self, posicion):
        (posicionx, posiciony) = posicion
        if (posicionx>=self.rect.left) and (posicionx<=self.rect.right) and (posiciony>=self.rect.top) and (posiciony<=self.rect.bottom):
            return True
        else:
            return False

    # def dibujar(self):
    #     raise NotImplemented("Tiene que implementar el metodo dibujar.")
    # def accion(self):
    #     raise NotImplemented("Tiene que implementar el metodo accion.")


# -------------------------------------------------
# Clase Boton y los distintos botones

class Boton(ElementoGUI):
    def __init__(self, pantalla, posicion, manager):
        # Se carga la imagen del boton
        #self.imagen = GestorRecursos.CargarImagen(nombreImagen,-1)

        self.imagenFile = manager.getDataRetriever().getButtonFile()
        self.imagen = manager.getLibrary().load(self.imagenFile, -1)
        self.imagen = pygame.transform.scale(self.imagen, (30, 30))

        #self.imagen= DataRetriever.getButton(self)
        #self.imagen = pygame.transform.scale(self.imagen, (30, 30))
        # Se llama al método de la clase padre con el rectángulo que ocupa el botón
        ElementoGUI.__init__(self, pantalla, self.imagen.get_rect())
        # Se coloca el rectangulo en su posicion
        self.establecerPosicion(posicion)
    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

class BotonJugar(Boton):
    def __init__(self, pantalla, manager):
        Boton.__init__(self, pantalla, (860,650), manager)
    def accion(self):
        self.pantalla.menu.ejecutarJuego()


class BotonSalir(Boton):
    def __init__(self, pantalla, manager):
        Boton.__init__(self,pantalla,(860, 650),manager)
    def accion(self):
        self.pantalla.menu.salirPrograma()

# -------------------------------------------------
# Clase TextoGUI y los distintos textos

class TextoGUI(ElementoGUI):
    def __init__(self, pantalla, fuente, color, texto, posicion):
        # Se crea la imagen del texto
        self.imagen = fuente.render(texto, True, color)
        # Se llama al método de la clase padre con el rectángulo que ocupa el texto
        ElementoGUI.__init__(self, pantalla, self.imagen.get_rect())
        # Se coloca el rectangulo en su posicion
        self.establecerPosicion(posicion)
    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

class TextoJugar(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.SysFont('arial', 26);
        TextoGUI.__init__(self, pantalla, fuente, (224, 224, 224), 'Jugar', (900, 650))
    def accion(self):
        self.pantalla.menu.ejecutarJuego()

class TextoSalir(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.SysFont('arial', 26);
        TextoGUI.__init__(self, pantalla, fuente, (224, 224, 224), 'Salir', (900, 700))
    def accion(self):
        self.pantalla.menu.salirPrograma()

# -------------------------------------------------
# Clase PantallaGUI y las distintas pantallas

class PantallaGUI:
    def __init__(self,manager):
        #self.menu = menu
        # Se carga la imagen de fondo
        self.data = manager.getDataRetriever()
        self.assetloader=manager.getLibrary()
        self.width= self.data.getWidth()
        self.heigth= self.data.getHeight()

        self.imagenFile = self.data.getBackgroundFile()
        self.imagen = self.assetloader.load(self.imagenFile, -1)
        self.imagen = pygame.transform.scale(self.imagen, (self.width, self.heigth))
        # Se tiene una lista de elementos GUI
        self.elementosGUI = []

    def eventos(self, lista_eventos):
        for evento in lista_eventos:
            if evento.type == MOUSEBUTTONDOWN:
                self.elementoClic = None
                for elemento in self.elementosGUI:
                    if elemento.posicionEnElemento(evento.pos):
                        self.elementoClic = elemento
            if evento.type == MOUSEBUTTONUP:
                for elemento in self.elementosGUI:
                    if elemento.posicionEnElemento(evento.pos):
                        if (elemento == self.elementoClic):
                            elemento.accion()

    def dibujar(self, pantalla):
        # Dibujamos primero la imagen de fondo
        pantalla.blit(self.imagen, self.imagen.get_rect())
        # Después los botones
        for elemento in self.elementosGUI:
            elemento.dibujar(pantalla)

class PantallaInicialGUI(PantallaGUI):
    def __init__(self, manager):
        PantallaGUI.__init__(self, manager)
        # Creamos los botones y los metemos en la lista
        botonJugar = BotonJugar(self, manager)
        botonSalir = BotonSalir(self, manager)
        self.elementosGUI.append(botonJugar)
        self.elementosGUI.append(botonSalir)
        # Creamos el texto y lo metemos en la lista
        textoJugar = TextoJugar(self)
        textoSalir = TextoSalir(self)
        self.elementosGUI.append(textoJugar)
        self.elementosGUI.append(textoSalir)

# -------------------------------------------------
# Clase Menu, la escena en sí

class Menu(Scene):

    def __init__(self, manager):
        # Llamamos al constructor de la clase padre
        Scene.__init__(self, manager);
        self.pantalla=manager.getScreen()

        # Creamos la lista de pantallas
        self.listaPantallas = []
        # Creamos las pantallas que vamos a tener
        #   y las metemos en la lista
        self.listaPantallas.append(PantallaInicialGUI(manager))
        # En que pantalla estamos actualmente
        self.mostrarPantallaInicial()

    def update(self, *args):
        return

    def events(self):
        #self.player.move(pygame.key.get_pressed())

        for evento in pygame.event.get():
            # Si se quiere salir, se le indica al director
            if evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                    self.salirPrograma()
            elif evento.type == pygame.QUIT:
                self.director.salirPrograma()

        # Se pasa la lista de eventos a la pantalla actual
        #self.listaPantallas[self.pantallaActual].eventos(lista_eventos)

    def draw(self):
        self.listaPantallas[self.pantallaActual].dibujar(self.pantalla)

    #--------------------------------------
    # Metodos propios del menu

    def salirPrograma(self):
        self.director.salirPrograma()

    def ejecutarJuego(self):
        #fase = Fase(self.director)
        #self.director.apilarEscena(fase)
        raise NotImplemented("Tiene que implementar el metodo ejecutar.")

    def mostrarPantallaInicial(self):
        self.pantallaActual = 0

    
