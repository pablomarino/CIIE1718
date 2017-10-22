# -*- encoding: utf-8 -*-

import pygame


class HUD:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.text_pos_x = 'Player posX : {0}'
        self.text_lives = 'Lives {0}'

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
            50,
            20
        )

        # Player lives
        self.text_to_screen(
            self.text_lives.format(3),
            550,
            50,
            20
        )

    def text_to_screen(self, text, x, y, size,
                       color=(200, 200, 200), font_type='../bin/assets/fonts/fast99.ttf'):

        # TODO add font size, color, and font type to levels.json
        try:

            text = str(text)
            font = pygame.font.Font(font_type, size)
            text = font.render(text, True, color)
            self.screen.blit(text, (x, y))

        except Exception, e:
            print 'Font Error, saw it coming'
            raise e
