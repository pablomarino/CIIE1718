import json

class DataRetriever:

    # LOADERS
    # TODO : ERRORES LOAD
    def __init__(self):
        self.__preferences = ''
        self.__levels = ''
        self.__players = ''

    def __loadConfig(self, file):
        with open(file) as preferences_file:
            data = json.load(preferences_file)
        return data

    def loadPreferences(self,file):
        self.__preferences = self.__loadConfig(file)

    def loadLevels(self,file):
        self.__levels = self.__loadConfig(file)

    def loadPlayers(self,file):
        self.__players = self.__loadConfig(file)


    # GETTERS
    # TODO : Errores GETTERS

    def getPreferences(self):
        return self.__preferences

    def getVersion(self):
        return self.__preferences['version']

    def getWidth(self):
        return int(self.__preferences['screen_res'][0])

    def getHeight(self):
        return int(self.__preferences['screen_res'][1])

    def getWindowIcon(self):
        return self.__preferences['window_icon']

    def getWindowTitle(self):
        return self.__preferences['window_title']

    def getFps(self):
        return float(self.__preferences['fps_target'])

    def getKeyQuit(self):
        return self.__preferences['keys']['quit']

    def getKeyUp(self):
        return self.__preferences['keys']['up']

    def getKeyDown(self):
        return self.__preferences['keys']['down']

    def getKeyLeft(self):
        return self.__preferences['keys']['left']

    def getKeyRight(self):
        return self.__preferences['keys']['right']

    def getKeyBt1(self):
        return self.__preferences['keys']['bt1']

    def getKeyBt2(self):
        return self.__preferences['keys']['bt2']

    def getmedia_suffixes(self):
        return self.__preferences['media_suffixes']


    def getLevels(self):
        return self.__levels

    def getLevelSheet(self,id):
        return self.__levels['world'][id]



    def getPlayers(self):
        return self.__players

    def getPlayerSheet(self,id):
        return self.__players["roster"][id]



    # SETTERS


    # UTILS


    def printPreferences(self):
        print('\nPreferences\n==================')
        print('Version     : ' +  self.__preferences['version'])
        print('Resolution  : ' +  self.__preferences['screen_res'][0] + 'x' +  self.__preferences['screen_res'][1])
        print('Screen Icon : ' +  self.__preferences['screen_icon'])
        print('Screen Title: ' +  self.__preferences['screen_title'])
        print('Fps         : ' +  self.__preferences['fps_target'])
        print('Keys quit   : ' +  self.__preferences['keys']['quit'][0] + ', ' +  self.__preferences['keys']['quit'][1])
        print('Keys up     : ' +  self.__preferences['keys']['up'][0] + ', ' +  self.__preferences['keys']['up'][1])
        print('Keys down   : ' +  self.__preferences['keys']['down'][0] + ', ' +  self.__preferences['keys']['down'][1])
        print('Keys left   : ' +  self.__preferences['keys']['left'][0] + ', ' +  self.__preferences['keys']['left'][1])
        print('Keys right  : ' +  self.__preferences['keys']['right'][0] + ', ' +  self.__preferences['keys']['right'][1])
        print('Keys bt1    : ' +  self.__preferences['keys']['bt1'][0] + ', ' +  self.__preferences['keys']['bt1'][1])
        print('Keys bt2    : ' +  self.__preferences['keys']['bt2'][0] + ', ' +  self.__preferences['keys']['bt2'][1])
