import json

#@staticmethod
def loadPreferences(file):
    with open(file) as preferences_file:
        data = json.load(preferences_file)
    return data

#@staticmethod
def printPreferences(data):
    print('\nPreferences\n==================')
    print('Version     : ' + data['version'])
    print('Resolution  : ' + data['screen_res'][0] + 'x' + data['screen_res'][1])
    print('Screen Icon : ' + data['screen_icon'])
    print('Screen Title: ' + data['screen_title'])
    print('Fps         : ' + data['fps_target'])
    print('Keys quit   : ' + data['keys']['quit'][0] + ', ' + data['keys']['quit'][1])
    print('Keys up     : ' + data['keys']['up'][0] + ', ' + data['keys']['up'][1])
    print('Keys down   : ' + data['keys']['down'][0] + ', ' + data['keys']['down'][1])
    print('Keys left   : ' + data['keys']['left'][0] + ', ' + data['keys']['left'][1])
    print('Keys right  : ' + data['keys']['right'][0] + ', ' + data['keys']['right'][1])
    print('Keys bt1    : ' + data['keys']['bt1'][0] + ', ' + data['keys']['bt1'][1])
    print('Keys bt2    : ' + data['keys']['bt2'][0] + ', ' + data['keys']['bt2'][1])
