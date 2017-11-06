# -*- coding: utf-8 -*-

import json

from pygame.locals import *


class DataRetriever:
    instance = None

    def __init__(self):
        if not DataRetriever.instance:
            DataRetriever.instance = DataRetriever.__DataRetriever()
        else:
            print __name__, 'Singleton already instantiated.'

    class __DataRetriever:

        def __init__(self):
            self.preferences = None
            self.levels = None
            self.players = None
            self.items = None
            # Keys are now added here for different locales support
            self.KEY_LEFT = K_LEFT
            self.KEY_UP = K_UP
            self.KEY_DOWN = K_DOWN
            self.KEY_RIGHT = K_RIGHT
            self.SPACE = K_SPACE
            self.RETURN = K_RETURN

    def __loadConfig(self, file):
        with open(file) as preferences_file:
            data = json.load(preferences_file)
        return data

    def loadPreferences(self, file):
        self.instance.preferences = self.__loadConfig(file)

    def loadLevels(self, file):
        self.instance.levels = self.__loadConfig(file)

    def loadPlayers(self, file):
        self.instance.players = self.__loadConfig(file)

    def loadItems(self, file):
        self.instance.items = self.__loadConfig(file)

    # GETTERS

    def getPreferences(self):
        return self.instance.preferences

    def getVersion(self):
        return self.instance.preferences['version']

    def getWidth(self):
        return int(self.instance.preferences['screen_res'][0])

    def getHeight(self):
        return int(self.instance.preferences['screen_res'][1])

    def getWindowIcon(self):
        return self.instance.preferences['window_icon']

    def getWindowTitle(self):
        return self.instance.preferences['window_title']

    def getFps(self):
        return float(self.instance.preferences['fps_target'])

    # TODO add different music to each level?
    def getMusicFile(self):
        return self.instance.preferences['music_file']

    def getHudPosY(self):
        return int(self.instance.preferences['hud_pos_y'])

    def getHudFontSize(self):
        return int(self.instance.preferences['hud_font_size'])

    def getHudFontColor(self):
        return self.instance.preferences['hud_font_color']

    def getHudFontType(self):
        return self.instance.preferences['hud_font_type']

    def getKeyQuit(self):
        return self.instance.preferences['keys']['quit']

    def getButtonFile(self):
        return self.instance.preferences['button']

    def getBackgroundFile(self):
        return self.instance.preferences['menu_background']

    # def getKeyUp(self):
    #     return self.instance.preferences['keys']['up']

    # def getKeyDown(self):
    #     return self.instance.preferences['keys']['down']

    # def getKeyLeft(self):
    #     return self.instance.preferences['keys']['left']

    # def getKeyRight(self):
    #     return self.instance.preferences['keys']['right']

    def getSpace(self):
        return self.instance.SPACE

    def getKeyUp(self):
        return self.instance.KEY_UP

    def getKeyDown(self):
        return self.instance.KEY_DOWN

    def getKeyLeft(self):
        return self.instance.KEY_LEFT

    def getKeyRight(self):
        return self.instance.KEY_RIGHT

    def getKeyReturn(self):
        return self.instance.RETURN

    def getKeyBt1(self):
        return self.instance.preferences['keys']['bt1']

    def getKeyBt2(self):
        return self.instance.preferences['keys']['bt2']

    def getmedia_suffixes(self):
        return self.instance.preferences['media_suffixes']

    def getLevels(self):
        return self.instance.levels

    def getLevel(self, id):
        return self.instance.levels[id]

    def getPlayerPositionAt(self, id):
        return (512,384)#(int(self.instance.levels[id]["player"]["x"]), int(self.instance.levels[id]["player"]["y"]))

    def getDimensions(self, id):
        return self.instance.levels[id]['dimensions']

    def getBgColor(self, id):
        return self.instance.levels[id]['bgColor']

    def getGravity(self, id):
        return self.instance.levels[id]['gravity']

    def getBgLayers(self, id):
        return self.instance.levels[id]['bgLayers']

    def getPlayers(self):
        return self.instance.players

    def getPlayer(self, id):
        return self.instance.players["roster"][id]

    def getPlayerSheet(self, id):
        return self.instance.players["roster"][id]['file']

    def getPlayerSheetCoords(self, id):
        return self.instance.players["roster"][id]['file_coords']

    def getItemSheet(self, id):
        return self.instance.items["items"][id]['file']

    def getItemSheetCoords(self, id):
        return self.instance.items["items"][id]['file_coords']

    def getItemSound(self, id):
        return self.instance.items["items"][id]['sound']

    def getPlayerAnchor(self, id):
        return self.instance.players["roster"][id]['anchor']

    def getPlayerAnimations(self, id):
        return self.instance.players["roster"][id]['animations']

    def getCharacterSpeed(self, id):
        return self.instance.players["roster"][id]['speed']

    def getCharacterChasingSpeed(self, id):
        return self.instance.players["roster"][id]['chasing_speed']

    def getCharacterJumpSpeed(self, id):
        return self.instance.players["roster"][id]['jump_speed']

    def getPlayerAnimationDelay(self):
        return self.instance.players["player_animation_delay"]
