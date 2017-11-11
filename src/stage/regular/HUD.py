# -*- encoding: utf-8 -*-

import pygame


class HUD:
    def __init__(self, manager, player):
        self.manager = manager
        self.screen = manager.getScreen()
        self.data = manager.getDataRetriever()
        self.assetloader = manager.getLibrary()
        self.player = player

        # Recuperar datos del DataRetriever
        self.font_type = self.data.getHudFontType()
        self.font_size = self.data.getHudFontSize()
        self.font_color = self.data.getHudFontColor()
        self.pos_y = self.data.getHudPosY()

        # Dimensiones
        self.healthbar_length = 200
        self.healthbar_height = 20
        self.healthbar_position = (self.data.getWidth() / 2 - self.healthbar_length / 2, self.pos_y)
        self.lives_position = (900, self.pos_y)
        self.score_position = (150, self.pos_y)
        self.score_image_position = (125, self.pos_y)
        self.images_size = (25, 25)

        # Imágenes
        self.coin_image = self.assetloader.load(self.data.getHudCoinFile(), -1).convert_alpha()
        self.coin_image = pygame.transform.scale(self.coin_image, self.images_size)
        self.lives_image = self.assetloader.load(self.data.getHudLivesFile(), -1).convert_alpha()
        self.lives_image = pygame.transform.scale(self.lives_image, self.images_size)

        # Color palette
        self.BLACK = (0, 0, 0)
        self.HEALTHBAR_FOREGROUND_NORMAL = (20, 200, 20)
        self.HEALTHBAR_FOREGROUNDTEXT_NORMAL = (255, 255, 255)
        self.HEALTHBAR_FOREGROUND_LOWLIFE = (255, 20, 20)
        self.HEALTHBAR_FOREGROUNDTEXT_LOWLIFE = (255, 255, 255)
        self.HEALTHBAR_BACKGROUND = (70, 70, 70)
        self.COLOR_NORMALTEXT = (255, 255, 255)

        # Create text variables
        self.text_points = 'x{0}'
        self.text_lives = 'x{0}'
        self.text_health = '{0}/{1}'

        # Game state variables
        self.gameOver = False

    def draw_health_bar(self, health):
        # Comprobar que es un valor válido
        if health < 0:
            health = 0

        # Guardamos en x y la posición
        x, y = self.healthbar_position
        y = y - self.healthbar_height / 2

        # Escogemos color para la barra de salud
        if health < 20:
            foreground_color = self.HEALTHBAR_FOREGROUND_LOWLIFE
            foregroundtext_color = self.HEALTHBAR_FOREGROUNDTEXT_LOWLIFE
        else:
            foreground_color = self.HEALTHBAR_FOREGROUND_NORMAL
            foregroundtext_color = self.HEALTHBAR_FOREGROUNDTEXT_NORMAL

        # Calculamos tamaño de la barra de salud
        health_value = (float(health) / 100 * self.healthbar_length)
        outline_rect = pygame.Rect(x, y, self.healthbar_length, self.healthbar_height)
        fill_rect = pygame.Rect(x, y, health_value, self.healthbar_height)

        # Dibujamos
        pygame.draw.rect(self.screen, self.HEALTHBAR_BACKGROUND, outline_rect)
        pygame.draw.rect(self.screen, foreground_color, fill_rect)
        pygame.draw.rect(self.screen, self.BLACK, outline_rect, 3)

        self.text_to_screen(
            self.text_health.format(int(self.player.getHealth()), self.player.getMaxHealth()),
            self.data.getWidth() / 2,
            y,
            self.font_size,
            foregroundtext_color,
            True, False
        )

    def draw_score(self, score):
        # Recuperamos posición
        x, y = self.score_position

        # Dibujamos text
        self.text_to_screen(
            self.text_points.format(score),
            self.score_position[0],
            self.score_position[1],
            self.font_size,
            self.COLOR_NORMALTEXT,
            False, True
        )

        # Calculamos posición de la imagen
        x = x - self.images_size[0] - 5
        y = y - self.images_size[1] / 2

        # Dibujar imagen
        self.screen.blit(self.coin_image, (x, y))

    def draw_lives(self, player_lives):
        # Recuperamos posición
        x, y = self.lives_position

        # Dibujamos text
        self.text_to_screen(
            self.text_points.format(player_lives),
            x, y,
            self.font_size,
            self.COLOR_NORMALTEXT,
            False, True
        )

        # Calculamos posición de la imagen
        x = x - self.images_size[0] - 5
        y = y - self.images_size[1] / 2

        # Dibujar imagen
        self.screen.blit(self.lives_image, (x, y))

    def text_to_screen(self, text, x, y, font_size, color, centered_x=False, centered_y=False):
        try:
            text = str(text)
            font = pygame.font.Font(self.font_type, font_size)
            text = font.render(text, True, color)
            if centered_x:
                x = x - text.get_width() / 2
            if centered_y:
                y = y - text.get_height() / 2
            self.screen.blit(text, (x, y))
        except Exception, e:
            raise e

    def centered_text_to_screen(self, text, font_size):
        try:
            color = (200, 200, 200)
            text = str(text)
            font = pygame.font.Font(self.font_type, font_size)
            text = font.render(text, True, color)
            text_rect = text.get_rect(center=(self.data.getWidth() / 2, self.data.getHeight() / 2))
            self.screen.blit(text, text_rect)
        except Exception, e:
            raise e

    def update(self):
        if (self.player.getHealth() == 0) & (self.player.getLives() == 0):
            self.gameOver = True

    def events(self):
        pass

    def draw(self):
        # Gameover alert
        if self.gameOver:
            self.centered_text_to_screen(
                "GAME OVER",
                150
            )
        else:
            # Dibujamos vidas del jugador
            self.draw_lives(self.player.getLives())

            # Dibujamos puntuación del jugador
            self.draw_score(self.player.getPoints())

            # Dibujamos la barra de salud
            self.draw_health_bar(self.player.getHealth())
