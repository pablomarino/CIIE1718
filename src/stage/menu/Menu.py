# -*- encoding: utf-8 -*-
import pygame
from pygame.locals import *

from control.GameLevel import GameLevel
from stage.regular.Scene import Scene


class ElementoGUI:
    def __init__(self, pantalla, manager, rectangulo):
        self.pantalla = pantalla
        self.manager = manager
        self.rect = rectangulo

    def establecerPosicion(self, posicion):
        (posicionx, posiciony) = posicion
        self.rect.left = posicionx
        self.rect.bottom = posiciony

    def posicionEnElemento(self, posicion):
        (posicionx, posiciony) = posicion
        if (posicionx >= self.rect.left) and (posicionx <= self.rect.right) \
                and (posiciony >= self.rect.top) and (posiciony <= self.rect.bottom):
            return True
        else:
            return False

    def draw(self):
        raise NotImplemented("Function not implemented yet.")

    def action(self):
        raise NotImplemented("Function not implemented yet.")

    def end_game(self):
        print "Ending game..."
        self.manager.endGame()
        pass

    def start_game(self):
        print "Starting game..."
        self.manager.changeScene()
        # Player stats (lives, maxHealth, health, score)
        lives = 3
        max_health = 100
        health = 100
        score = 0
        player_stats = (lives, max_health, health, score)
        self.manager.add(GameLevel(self.manager, self.manager.getDataRetriever(), "level_1", player_stats))
        # self.manager.add(GameLevel(self.manager, self.manager.getDataRetriever(), "level_1"))
        # pass


# -------------------------------------------------
# Clase Boton y los distintos botones

class Boton(ElementoGUI):
    def __init__(self, pantalla, posicion, manager):
        # Se carga la imagen del boton
        # self.imagen = GestorRecursos.CargarImagen(nombreImagen,-1)


        imagenFile = manager.getDataRetriever().getButtonFile()
        self.imagen = manager.getLibrary().load(imagenFile, -1)
        self.imagen = pygame.transform.scale(self.imagen, (30, 30))

        # self.imagen= DataRetriever.getButton(self)
        # self.imagen = pygame.transform.scale(self.imagen, (30, 30))
        # Se llama al método de la clase padre con el rectángulo que ocupa el botón
        ElementoGUI.__init__(self, pantalla, manager, self.imagen.get_rect())
        # Se coloca el rectangulo en su posicion
        self.establecerPosicion(posicion)

    def draw(self, pantalla):
        pantalla.blit(self.imagen, self.rect)


class BotonJugar(Boton):
    def __init__(self, pantalla, manager):
        Boton.__init__(self, pantalla, (860, 650), manager)

    def action(self):
        # print "Action BotonJugar"
        self.start_game()


class BotonSalir(Boton):
    def __init__(self, pantalla, manager):
        Boton.__init__(self, pantalla, (860, 700), manager)

    def action(self):
        # print "Action BotonSalir"
        self.end_game()


# -------------------------------------------------
# Clase TextoGUI y los distintos textos

class TextoGUI(ElementoGUI):
    def __init__(self, pantalla, manager, fuente, color, texto, posicion):
        # Se crea la imagen del texto
        self.imagen = fuente.render(texto, True, color)
        # Se llama al método de la clase padre con el rectángulo que ocupa el texto
        ElementoGUI.__init__(self, pantalla, manager, self.imagen.get_rect())
        # Se coloca el rectangulo en su posicion
        self.establecerPosicion(posicion)

    def draw(self, pantalla):
        pantalla.blit(self.imagen, self.rect)


class TextoJugar(TextoGUI):
    def __init__(self, pantalla, manager):
        self.font_size = 26
        self.font_type = manager.getDataRetriever().getFontType()
        self.font = pygame.font.Font(self.font_type, self.font_size)
        TextoGUI.__init__(self, pantalla, manager, self.font, (200, 200, 200), 'Jugar', (900, 650))

    def action(self):
        # print "Accion TextoJugar"
        self.start_game()


class TextoSalir(TextoGUI):
    def __init__(self, pantalla, manager):
        self.font_size = 26
        self.font_type = manager.getDataRetriever().getFontType()
        self.font = pygame.font.Font(self.font_type, self.font_size)
        TextoGUI.__init__(self, pantalla, manager, self.font, (200, 200, 200), 'Salir', (900, 700))

    def action(self):
        # print "Accion TextoGUI"
        self.end_game()


# -------------------------------------------------
# Class menu itself


class Menu(Scene):
    def __init__(self, manager):
        Scene.__init__(self, manager)
        self.manager = manager
        self.pantalla = manager.getScreen()

        # PantallaGUI
        self.data = manager.getDataRetriever()
        self.assetloader = manager.getLibrary()
        self.width = self.data.getWidth()
        self.heigth = self.data.getHeight()

        imagenFile = self.data.getBackgroundFile()
        self.imagen = self.assetloader.load(imagenFile, -1)
        self.imagen = pygame.transform.scale(self.imagen, (self.width, self.heigth))
        # Se tiene una lista de elementos GUI
        self.elementosGUI = []

        # PantallaInicialGUI
        botonJugar = BotonJugar(self, manager)
        botonSalir = BotonSalir(self, manager)
        self.elementosGUI.append(botonJugar)
        self.elementosGUI.append(botonSalir)
        # Creamos el texto y lo metemos en la lista
        textoJugar = TextoJugar(self, manager)
        textoSalir = TextoSalir(self, manager)
        self.elementosGUI.append(textoJugar)
        self.elementosGUI.append(textoSalir)

        self.clicked_element = None

    def getNumericId(self):
        return 0

    def getPlayerStats(self):
        return 3, 100, 100, 0

    def update(self, *args):
        pass

    def getPlatformGroup(self):
        return pygame.sprite.Group()

    def getEnemyGroup(self):
        return pygame.sprite.Group()

    def events(self, events_list):
        for evento in events_list:

            # If mouse is pressed
            if evento.type == MOUSEBUTTONDOWN:
                self.clicked_element = None
                for elemento in self.elementosGUI:
                    # print "elemento - " + str(elemento.rect.left) + str(elemento.rect.bottom)
                    if elemento.posicionEnElemento(evento.pos):
                        # print "Has pulsado en un elemento"
                        self.clicked_element = elemento

            # If mouse is raised
            if evento.type == MOUSEBUTTONUP:
                for elemento in self.elementosGUI:
                    if elemento.posicionEnElemento(evento.pos):
                        if elemento == self.clicked_element:
                            # print "Has de-pulsado en el mismo elemento"
                            elemento.action()

            # If enter key is pressed
            if evento.type == KEYDOWN and evento.key == int(self.data.getKeyReturn()):
                self.manager.addNextLevel()
                self.manager.changeScene()
                pass

    def draw(self):
        # Dibujamos primero la imagen de fondo
        self.pantalla.blit(self.imagen, self.imagen.get_rect())
        # Después los botones
        for elemento in self.elementosGUI:
            elemento.draw(self.pantalla)
