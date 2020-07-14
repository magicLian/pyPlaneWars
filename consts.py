import os

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

LEVEL1 = 1
LEVEL2 = 2
LEVEL3 = 3
LEVEL4 = 4

MyPlane = {
    "speed": 10,
    "bottomRemaining": 30
}

globalMap = {
    "screenWH": [480, 700],
    "gameName": "pyPlaneWars",
    "musicVol": 0.2,
    "bombNum": 3,
    "supplyTimer": 30 * 1000,
    "lifeNum": 3,
    "scoreFontSize": 36,
    "bombFontSize": 48,
    "gameOverFontSize": 48,
    "delay": 100,
    "projectPath": os.path.dirname(os.path.realpath(__file__))
}

