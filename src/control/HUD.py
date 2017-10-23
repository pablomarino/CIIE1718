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

    def update(self):
        pass

    def events(self):
        # TODO implement events function in the HUD?
        pass

    def draw(self):
        # Player x position
        self.text_to_screen(
            self.text_pos_x.format(self.player.getGlobalPosition()[0]),
            150,
            self.pos_y
        )

        # Player health
        self.text_to_screen(
            self.text_health.format(self.player.getHealth(), self.player.getMaxHealth()),
            550,
            self.pos_y
        )

        # Player lives
        self.text_to_screen(
            self.text_lives.format(self.player.getLives()),
            self.data.getWidth() - 150,
            self.pos_y
        )

    def text_to_screen(self, text, x, y, color=(200, 200, 200)):

        # TODO add font size, color, and font type to levels.json
        try:

            text = str(text)
            font = pygame.font.Font(self.font_type, self.font_size)
            text = font.render(text, True, color)
            self.screen.blit(text, (x, y))

        except Exception, e:
            raise e
