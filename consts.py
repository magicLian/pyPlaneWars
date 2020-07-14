import os


class GlobalVar():
    PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))

    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)

    LEVEL1 = 1
    LEVEL2 = 2
    LEVEL3 = 3
    LEVEL4 = 4

    ME_SPEED = 10
    ME_BOTTOM_REMAINING = 30

    FONT_SCORE_SIZE = 36
    FONT_BOMB_SIZE = 48
    FONT_GAME_OVER_SIZE = 48

    SYSTEM_GAME_NAME= "pyPlaneWars"
    SYSTEM_SCREEN_WIDTH = 480
    SYSTEM_SCREEN_HEIGHT = 700
    SYSTEM_MUSIC_VOL = 0.2
    SYSTEM_BOMB_NUMBER = 3
    SYSTEM_SUPPLY_TIME = 30 * 1000
    SYSTEM_LIFE_NUMBER = 3
    SYSTEM_DELAY = 100