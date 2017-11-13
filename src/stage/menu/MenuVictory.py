# -*- encoding: utf-8 -*-
import pygame
from pygame.locals import *

from stage.menu.Menu import Menu
from stage.regular.Scene import Scene


class MenuVictory(Scene):
    def __init__(self, manager, player_stats):
        Scene.__init__(self, manager)
        self.manager = manager
        self.pantalla = manager.getScreen()
        self.player_stats = player_stats

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

        # Variables de los elementos gráficos
        self.pos_y = self.height / 3
        self.font_type = self.data.getFontType()
        self.font_size = 30
        # Dimensiones
        self.score_image_position = (125, self.pos_y)
        self.images_size = (self.font_size, self.font_size)

        # Imágenes
        self.coin_image = self.assetloader.load(self.data.getHudCoinFile(), -1).convert_alpha()
        self.coin_image = pygame.transform.scale(self.coin_image, self.images_size)
        self.lives_image = self.assetloader.load(self.data.getHudLivesFile(), -1).convert_alpha()
        self.lives_image = pygame.transform.scale(self.lives_image, self.images_size)

        # Color palette
        self.COLOR_NORMALTEXT = (255, 255, 255)

        # Create text variables
        self.text_points = 'x{0}'
        self.text_lives = 'x{0}'

    def text_to_screen(self, text, x, y, font_size, color, centered_x=False, centered_y=False):
        try:
            text = str(text)
            font = pygame.font.Font(self.font_type, font_size)
            text = font.render(text, True, color)
            if centered_x:
                x = x - text.get_width() / 2
            if centered_y:
                y = y - text.get_height() / 2
            self.pantalla.blit(text, (x, y))
        except Exception, e:
            raise e

    def draw_score(self, score, type, y):
        # Recuperamos posición
        x = self.width / 2

        # Dibujamos text
        self.text_to_screen(
            self.text_points.format(score),
            x,
            y,
            self.font_size,
            self.COLOR_NORMALTEXT,
            False, True
        )

        # Calculamos posición de la imagen
        x = x - self.images_size[0] - 5
        y = y - self.images_size[1] / 2

        # Dibujar imagen
        if type == "score":
            self.pantalla.blit(self.coin_image, (x, y))
        elif type == "lives":
            self.pantalla.blit(self.lives_image, (x, y))

    def getPlatformGroup(self):
        return pygame.sprite.Group()

    def getEnemyGroup(self):
        return pygame.sprite.Group()

    def update(self, *args):
        pass

    def events(self, events_list):
        for evento in events_list:
            # If enter key is pressed go back to menu
            if evento.type == KEYDOWN and evento.key == int(self.data.getKeyReturn()):
                self.manager.changeScene()
                self.manager.add(Menu(self.manager))

    def draw(self):
        # Dibujamos primero la imagen de fondo
        # TODO añadir imagen de fondo al menú de victoria
        # self.pantalla.blit(self.imagen, self.imagen.get_rect())

        # Texto de victoria
        self.text_to_screen("VICTORIA", self.width / 2, self.pos_y, self.font_size * 2, self.COLOR_NORMALTEXT, True,
                            True)

        # Dibujamos vidas del jugador
        self.draw_score(self.player_stats[0], "lives", self.pos_y + 70)

        # Dibujamos puntuación del jugador
        self.draw_score(self.player_stats[3], "score", self.pos_y + 120)

        # Pulsar enter para salir
        self.text_to_screen(
            "Press ENTER",
            self.data.getWidth() / 2, self.data.getHeight() / 1.25,
            23, self.COLOR_NORMALTEXT,
            True, True
        )
