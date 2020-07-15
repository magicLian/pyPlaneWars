import pygame
import sys
import traceback
import myplane
import enemy
import bullet
import supply
from game import Game
from consts import GlobalVar
from pygame.locals import *
from random import *


if __name__ == '__main__':
    try:
        Game().init_game()

    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
