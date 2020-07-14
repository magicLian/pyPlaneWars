import pygame
from pygame.locals import *
import myplane
import enemy
import bullet
import supply
import consts


class Game(None):
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode(consts.globalMap["screenWH"])
        pygame.display.set_caption(consts.globalMap["gameName"])

        self.background = pygame.image.load(consts.globalMap["projectPath"] + '/images/background.png').convert()

        # 载入音乐
        pygame.mixer.music.load(consts.globalMap["projectPath"] + '/sound/game_music.ogg')
        pygame.mixer.music.set_volume(consts.globalMap["musicVol"])

        self.bullet_sound = pygame.mixer.Sound(consts.globalMap["projectPath"] + '/sound/bullet.wav')
        self.bullet_sound.set_volume(consts.globalMap["musicVol"])

        self.bomb_sound = pygame.mixer.Sound(consts.globalMap["projectPath"] + '/sound/use_bomb.wav')
        self.bomb_sound.set_volume(consts.globalMap["musicVol"])

        self.supply_sound = pygame.mixer.Sound(consts.globalMap["projectPath"] + '/sound/supply.wav')
        self.supply_sound.set_volume(consts.globalMap["musicVol"])

        self.get_bomb_sound = pygame.mixer.Sound(consts.globalMap["projectPath"] + '/sound/get_bomb.wav')
        self.get_bomb_sound.set_volume(consts.globalMap["musicVol"])

        self.get_bullet_sound = pygame.mixer.Sound(consts.globalMap["projectPath"] + '/sound/get_bullet.wav')
        self.get_bullet_sound.set_volume(consts.globalMap["musicVol"])

        self.upgrade_sound = pygame.mixer.Sound(consts.globalMap["projectPath"] + '/sound/upgrade.wav')
        self.upgrade_sound.set_volume(consts.globalMap["musicVol"])

        self.enemy3_fly_sound = pygame.mixer.Sound(consts.globalMap["projectPath"] + '/sound/enemy3_flying.wav')
        self.enemy3_fly_sound.set_volume(consts.globalMap["musicVol"])

        self.enemy1_down_sound = pygame.mixer.Sound(consts.globalMap["projectPath"] + '/sound/enemy1_down.wav')
        self.enemy1_down_sound.set_volume(consts.globalMap["musicVol"])

        self.enemy2_down_sound = pygame.mixer.Sound(consts.globalMap["projectPath"] + '/sound/enemy2_down.wav')
        self.enemy2_down_sound.set_volume(consts.globalMap["musicVol"])

        self.enemy3_down_sound = pygame.mixer.Sound(consts.globalMap["projectPath"] + '/sound/enemy3_down.wav')
        self.enemy3_down_sound.set_volume(consts.globalMap["musicVol"])

        self.me_down_sound = pygame.mixer.Sound(consts.globalMap["projectPath"] + '/sound/me_down.wav')
        self.me_down_sound.set_volume(consts.globalMap["musicVol"])

        # 播放音乐
        pygame.mixer.music.play(-1)

        # 实例我方飞机
        self.me = myplane.MyPlane()

        # 实例敌方飞机
        self.enemies = pygame.sprite.Group()

        # 实例敌方小型飞机
        self.small_enemies = pygame.sprite.Group()
        self.add_small_enemies(15)

        # 实例敌方中型飞机
        self.mid_enemies = pygame.sprite.Group()
        self.add_mid_enemies(4)

        # 实例敌方大型飞机
        self.big_enemies = pygame.sprite.Group()
        self.add_big_enemies(2)

        # 实例普通子弹
        self.bullet1 = []
        self.bullet1_index = 0
        self.bullet1_num = 4
        for i in range(self.bullet1_num):
            self.bullet1.append(self.bullet.Bullet1(self.me.rect.midtop))

        # 实例超级子弹
        self.bullet2 = []
        self.bullet2_index = 0
        self.bullet2_num = 8
        for i in range(self.bullet2_num // 2):
            self.bullet2.append(self.bullet.Bullet2((self.me.rect.centerx - 33, self.me.rect.centery)))
            self.bullet2.append(self.bullet.Bullet2((self.me.rect.centerx + 30, self.me.rect.centery)))

        # 中弹图片索引
        self.e1_destroy_index = 0
        self.e2_destroy_index = 0
        self.e3_destroy_index = 0
        self.me_destroy_index = 0

        # 统计得分
        self.score = 0
        self.score_font = pygame.font.Font(consts.globalMap["projectPath"] + "/font/font.ttf",
                                           consts.globalMap["scoreFontSize"])

        # 标志是否暂停游戏
        self.paused = False
        self.paused_nor_image = pygame.image.load(
            consts.globalMap["projectPath"] + "/images/pause_nor.png").convert_alpha()
        self.paused_pressed_image = pygame.image.load(
            consts.globalMap["projectPath"] + "/images/pause_pressed.png").convert_alpha()
        self.resume_nor_image = pygame.image.load(
            consts.globalMap["projectPath"] + '/images/resume_nor.png').convert_alpha()
        self.resume_pressed_image = pygame.image.load(
            consts.globalMap["projectPath"] + '/images/resume_pressed.png').convert_alpha()
        self.paused_rect = self.paused_nor_image.get_rect()
        self.paused_rect.left, self.paused_rect.top = consts.globalMap["screenWH"][0] - self.paused_rect.width - 10, 10
        self.paused_image = self.paused_nor_image

        # 设置难度
        self.level = consts.LEVEL1

        # 全屏炸弹
        self.bomb_image = pygame.image.load(consts.globalMap["projectPath"] + '/images/bomb.png').convert_alpha()
        self.bomb_rect = self.bomb_image.get_rect()
        self.bomb_font = pygame.font.Font(consts.globalMap["projectPath"] + "/font/font.ttf", consts.globalMap["bombFontSize"])
        self.bomb_num = consts.globalMap["bombNum"]

        # 每30秒发放一个补给包
        self.bullet_supply = supply.BulletSupply((consts.globalMap["screenWH"][0], consts.globalMap["screenWH"][1]))
        self.bomb_supply = supply.Bomb_Supply((consts.globalMap["screenWH"][0], consts.globalMap["screenWH"][1]))

        supply_time = USEREVENT
        pygame.time.set_timer(supply_time, consts.globalMap["supplyTimer"])

        # 超级子弹定时器
        self.double_bullet_time = USEREVENT + 1

        # 解除我方重生无敌定时器
        self.invincible_time = USEREVENT + 2

        # 标志是否使用超级子弹
        self.is_double_bullet = False

        # 生命数量
        self.life_image = pygame.image.load(consts.globalMap["projectPath"] + "/images/life.png").convert_alpha()
        self.life_rect = self.life_image.get_rect()
        self.life_num = consts.globalMap["lifeNum"]

        # 用于切换我方飞机图片
        self.switch_plane = True

        # 游戏结束画面
        self.gameover_font = pygame.font.Font(consts.globalMap["projectPath"] + "/font/font.TTF",
                                              consts.globalMap["gameOverFontSize"])
        self.again_image = pygame.image.load(consts.globalMap["projectPath"] + "/images/again.png").convert_alpha()
        self.again_rect = self.again_image.get_rect()
        self.gameover_image = pygame.image.load(consts.globalMap["projectPath"] + "/images/gameover.png").convert_alpha()
        self.gameover_rect = self.gameover_image.get_rect()

        # 用于延迟切换
        self.delay = consts.globalMap["delay"]

        # 限制打开一次记录文件
        self.recorded = False

        self.clock = pygame.time.Clock()
        self.running = True

    def add_small_enemies(self, num):
        for i in range(num):
            e1 = enemy.SmallEnemy(consts.globalMap["screenWH"])
            self.enemies.add(e1)
            self.small_enemies.add(e1)

    def add_mid_enemies(self, num):
        for i in range(num):
            e2 = enemy.MidEnemy(consts.globalMap["screenWH"])
            self.enemies.add(e2)
            self.mid_enemies.add(e2)

    def add_big_enemies(self, num):
        for i in range(num):
            e3 = enemy.BigEnemy(consts.globalMap["screenWH"])
            self.enemies.add(e3)
            self.big_enemies.add(e3)

    def init_game(self, screen):
        pass

    def listen_event(self):
        pass

    def end_game(self):
        pass

    def pause_game(self):
        pass

    def unpause_game(self):
        pass

    def game_over(self):
        pass
