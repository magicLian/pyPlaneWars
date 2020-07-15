import pygame
import traceback
from game import Game


if __name__ == '__main__':
    try:
        Game().init_game()

    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
