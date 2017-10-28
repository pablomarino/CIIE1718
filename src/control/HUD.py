# -*- encoding: utf-8 -*-

import pygame


class HUD:
    def __init__(self, data, screen, player):
        self.data = data
        self.screen = screen
        self.player = player

        # Initialize variables
        self.font_type = data.getHudFontType()
        self.font_size = data.getHudFontSize()
        self.font_color = data.getHudFontColor()
        self.pos_y = data.getHudPosY();

        # Create text variables
        self.text_pos_x = 'Player posX : {0}'
        self.text_lives = 'Lives {0}'
        self.text_health = 'Health {0}/{1}'

        # Game state variables
        self.gameOver = False

    def update(self):
        if (self.player.getHealth() == 0) & (self.player.getLives() == 0):
            self.gameOver = True

    def events(self):
        pass

    def draw(self):
        # TODO finish the HUD properly
        # Gameover alert
        if self.gameOver:
            self.centered_text_to_screen(
                "GAME OVER",
                150
            )
        else:
            # Player x position
            self.text_to_screen(
                self.text_pos_x.format(self.player.getGlobalPosition()[0]),
                150,
                self.pos_y,
                self.font_size
            )

            # Player health
            self.text_to_screen(
                self.text_health.format(self.player.getHealth(), self.player.getMaxHealth()),
                550,
                self.pos_y,
                self.font_size
            )

            # Player lives
            self.text_to_screen(
                self.text_lives.format(self.player.getLives()),
                self.data.getWidth() - 150,
                self.pos_y,
                self.font_size
            )

    def text_to_screen(self, text, x, y, font_size):

        try:
            color = (200, 200, 200)
            text = str(text)
            font = pygame.font.Font(self.font_type, font_size)
            text = font.render(text, True, color)
            self.screen.blit(text, (x, y))

        except Exception, e:
            raise e

    def centered_text_to_screen(self, text, font_size):
        try:
            color = (200, 200, 200)
            text = str(text)
            font = pygame.font.Font(self.font_type, font_size)
            text = font.render(text, True, color)
            text_rect = text.get_rect(center=(1024 / 2, 768 / 2))
            self.screen.blit(text, text_rect)

        except Exception, e:
            raise e
