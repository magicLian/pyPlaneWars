import pygame
from consts import GlobalVar


class MyPlane(pygame.sprite.Sprite):
    """docstring for MyPlane"""

    def __init__(self):
        super(MyPlane, self).__init__()

        self.image1 = pygame.image.load(GlobalVar.PROJECT_PATH + '/images/me1.png').convert_alpha()
        self.image2 = pygame.image.load(GlobalVar.PROJECT_PATH + '/images/me2.png').convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load(GlobalVar.PROJECT_PATH + '/images/me_destroy_1.png').convert_alpha(),
            pygame.image.load(GlobalVar.PROJECT_PATH + '/images/me_destroy_2.png').convert_alpha(),
            pygame.image.load(GlobalVar.PROJECT_PATH + '/images/me_destroy_3.png').convert_alpha(),
            pygame.image.load(GlobalVar.PROJECT_PATH + '/images/me_destroy_4.png').convert_alpha()
        ])
        self.rect = self.image1.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.active = True
        self.invincible = False
        self.mask = pygame.mask.from_surface(self.image2)
        self.rect.left = (GlobalVar.SYSTEM_SCREEN_WIDTH - self.rect.width) // 2
        self.rect.top = GlobalVar.SYSTEM_SCREEN_HEIGHT - self.rect.height - GlobalVar.ME_BOTTOM_REMAINING
        self.speed = GlobalVar.ME_SPEED

    def moveUp(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def moveDown(self):
        if self.rect.bottom < GlobalVar.SYSTEM_SCREEN_HEIGHT - self.height - GlobalVar.ME_BOTTOM_REMAINING:
            self.rect.bottom += self.speed
        else:
            self.rect.bottom = GlobalVar.SYSTEM_SCREEN_HEIGHT - GlobalVar.ME_BOTTOM_REMAINING

    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def moveRight(self):
        if self.rect.right < GlobalVar.SYSTEM_SCREEN_WIDTH:
            self.rect.right += self.speed
        else:
            self.rect.right = GlobalVar.SYSTEM_SCREEN_WIDTH

    def reset(self):
        self.rect.left = (GlobalVar.SYSTEM_SCREEN_WIDTH - self.rect.width) // 2
        self.rect.right = self.rect.left + self.rect.width
        self.rect.top = GlobalVar.SYSTEM_SCREEN_HEIGHT - self.rect.height - GlobalVar.ME_BOTTOM_REMAINING
        self.rect.bottom = self.rect.top + self.rect.height
        self.active = True
        self.invincible = True
