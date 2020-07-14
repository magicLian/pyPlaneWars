# -*- coding: utf-8 -*-
# @Author   : Sdite
# @DateTime : 2017-07-26 17:56:37

import pygame
from random import *
from consts import GlobalVar


class BulletSupply(pygame.sprite.Sprite):
    """docstring for Bullet_Supply"""

    def __init__(self):
        super(BulletSupply, self).__init__()

        self.image = pygame.image.load(GlobalVar.PROJECT_PATH + '/images/bullet_supply.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.reset()
        self.speed = GlobalVar.SUPPLY_SPEED
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top < GlobalVar.SYSTEM_SCREEN_HEIGHT:
            self.rect.top += self.speed
        else:
            self.active = False

    def reset(self):
        self.active = True
        self.rect.left = randint(0, GlobalVar.SYSTEM_SCREEN_WIDTH - self.rect.width)
        self.rect.bottom = -100


class Bomb_Supply(pygame.sprite.Sprite):
    """docstring for Bomb_Supply"""

    def __init__(self):
        super(Bomb_Supply, self).__init__()

        self.image = pygame.image.load(GlobalVar.PROJECT_PATH + '/images/bomb_supply.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.reset()
        self.speed = GlobalVar.SUPPLY_SPEED
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top < GlobalVar.SYSTEM_SCREEN_HEIGHT:
            self.rect.top += self.speed
        else:
            self.active = False

    def reset(self):
        self.active = True
        self.rect.left = randint(0, GlobalVar.SYSTEM_SCREEN_WIDTH - self.rect.width)
        self.rect.bottom = -100