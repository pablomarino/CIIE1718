import json

class DataRetriever:
    instance = None
    # LOADERS
    # TODO : ERRORES LOAD
    def __init__(self):
        if not self.instance:
            self.instance = self.__DataRetriever()
        else:
            print ("Singleton already instantiated.")


    class __DataRetriever:

        def __init__(self):
            preferences = None
            levels = None
            players = None

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
    
    # GETTERS
    # TODO : Errores GETTERS

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

    def getKeyQuit(self):
        return self.instance.preferences['keys']['quit']

    def getKeyUp(self):
        return self.instance.preferences['keys']['up']

    def getKeyDown(self):
        return self.instance.preferences['keys']['down']

    def getKeyLeft(self):
        return self.instance.preferences['keys']['left']

    def getKeyRight(self):
        return self.instance.preferences['keys']['right']

    def getKeyBt1(self):
        return self.instance.preferences['keys']['bt1']

    def getKeyBt2(self):
        return self.instance.preferences['keys']['bt2']

    def getmedia_suffixes(self):
        return self.instance.preferences['media_suffixes']


    def getLevels(self):
        return self.instance.levels

    def getLevelSheet(self,id):
        return self.instance.levels['world'][id]


    def getPlayers(self):
        return self.instance.players

    def getPlayerSheet(self,id):
        return self.instance.players["roster"][id]



    # SETTERS
