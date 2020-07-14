import pygame
from random import *
from consts import GlobalVar


class SmallEnemy(pygame.sprite.Sprite):
    """docstring for SmallEnemy"""
    energy = 1

    def __init__(self):
        super(SmallEnemy, self).__init__()

        self.image = pygame.image.load(GlobalVar.PROJECT_PATH
                                       + '/images/enemy1.png').convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend(
            [pygame.image.load(GlobalVar.PROJECT_PATH + '/images/enemy1_down1.png').convert_alpha(),
             pygame.image.load(GlobalVar.PROJECT_PATH + '/images/enemy1_down2.png').convert_alpha(),
             pygame.image.load(GlobalVar.PROJECT_PATH + '/images/enemy1_down3.png').convert_alpha(),
             pygame.image.load(GlobalVar.PROJECT_PATH + '/images/enemy1_down4.png').convert_alpha()])
        self.rect = self.image.get_rect()
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 2
        self.reset()
        self.hit = False

    def move(self):
        if self.rect.top < GlobalVar.SYSTEM_SCREEN_HEIGHT:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.rect.left = randint(0, GlobalVar.SYSTEM_SCREEN_WIDTH - self.rect.width)
        self.rect.top = randint(-5 * GlobalVar.SYSTEM_SCREEN_HEIGHT, 0)
        self.active = True
        self.energy = SmallEnemy.energy

    def hit_for_one(self):
        self.hit = True
        self.energy -= 1
        if self.energy == 0:
            self.destroy()

    def destroy(self):
        self.active = False


class MidEnemy(pygame.sprite.Sprite):
    """docstring for MidEnemy"""

    energy = 8

    def __init__(self):
        super(MidEnemy, self).__init__()

        self.image = pygame.image.load(GlobalVar.PROJECT_PATH + '/images/enemy2.png').convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load(GlobalVar.PROJECT_PATH + '/images/enemy2_down1.png').convert_alpha(),
            pygame.image.load(GlobalVar.PROJECT_PATH + '/images/enemy2_down2.png').convert_alpha(),
            pygame.image.load(GlobalVar.PROJECT_PATH + '/images/enemy2_down3.png').convert_alpha(),
            pygame.image.load(GlobalVar.PROJECT_PATH + '/images/enemy2_down4.png').convert_alpha()
        ])
        self.image_hit = pygame.image.load(GlobalVar.PROJECT_PATH + '/images/enemy2_hit.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.active = True
        self.speed = 1
        self.mask = pygame.mask.from_surface(self.image)
        self.reset()
        self.hit = False

    def move(self):
        if self.rect.top < GlobalVar.SYSTEM_SCREEN_HEIGHT:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.rect.left = randint(0, GlobalVar.SYSTEM_SCREEN_WIDTH - self.rect.width)
        self.rect.top = randint(-10 * GlobalVar.SYSTEM_SCREEN_HEIGHT, -GlobalVar.SYSTEM_SCREEN_HEIGHT)
        self.active = True
        self.energy = MidEnemy.energy

    def hit_for_one(self):
        self.hit = True
        self.energy -= 1
        if self.energy == 0:
            self.destroy()

    def destroy(self):
        self.active = False


class BigEnemy(pygame.sprite.Sprite):
    """docstring for BigEnemy"""
    energy = 20

    def __init__(self):
        super(BigEnemy, self).__init__()

        self.image1 = pygame.image.load(GlobalVar.PROJECT_PATH + '/images/enemy3_n1.png').convert_alpha()
        self.image2 = pygame.image.load(GlobalVar.PROJECT_PATH + '/images/enemy3_n2.png').convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load(GlobalVar.PROJECT_PATH + '/images/enemy3_down1.png').convert_alpha(),
            pygame.image.load(GlobalVar.PROJECT_PATH + '/images/enemy3_down2.png').convert_alpha(),
            pygame.image.load(GlobalVar.PROJECT_PATH + '/images/enemy3_down3.png').convert_alpha(),
            pygame.image.load(GlobalVar.PROJECT_PATH + '/images/enemy3_down4.png').convert_alpha(),
            pygame.image.load(GlobalVar.PROJECT_PATH + '/images/enemy3_down5.png').convert_alpha(),
            pygame.image.load(GlobalVar.PROJECT_PATH + '/images/enemy3_down6.png').convert_alpha()
        ])
        self.image_hit = pygame.image.load(GlobalVar.PROJECT_PATH + '/images/enemy3_hit.png').convert_alpha()
        self.rect = self.image1.get_rect()
        self.active = True
        self.speed = 1
        self.mask = pygame.mask.from_surface(self.image1)
        self.appear = False
        self.reset()
        self.hit = False

    def move(self):
        if self.rect.top < GlobalVar.SYSTEM_SCREEN_HEIGHT:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.rect.left = randint(0, GlobalVar.SYSTEM_SCREEN_WIDTH - self.rect.width)
        self.rect.top = randint(-20 * GlobalVar.SYSTEM_SCREEN_HEIGHT, -10 * GlobalVar.SYSTEM_SCREEN_HEIGHT)
        self.active = True
        self.energy = BigEnemy.energy

    def hit_for_one(self):
        self.hit = True
        self.energy -= 1
        if self.energy == 0:
            self.destroy()

    def destroy(self):
        self.active = False
