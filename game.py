import pygame
from pygame.locals import *
import sys
import myplane
import enemy
import bullet
import supply

from consts import GlobalVar


class Game():
    def init_game(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(GlobalVar.SYSTEM_GAME_NAME)

        self.init_game_resources()
        self.define_game_vars()

        self.process_game()


    def init_game_resources(self):
        self.screen = pygame.display.set_mode((GlobalVar.SYSTEM_SCREEN_WIDTH, GlobalVar.SYSTEM_SCREEN_HEIGHT))

        # bg
        self.background = pygame.image.load(GlobalVar.PROJECT_PATH + '/images/background.png').convert()

        # bgm
        pygame.mixer.music.load(GlobalVar.PROJECT_PATH + '/sound/game_music.ogg')
        pygame.mixer.music.set_volume(GlobalVar.SYSTEM_MUSIC_VOL)

        # bullet sound
        self.bullet_sound = pygame.mixer.Sound(GlobalVar.PROJECT_PATH + '/sound/bullet.wav')
        self.bullet_sound.set_volume(GlobalVar.SYSTEM_MUSIC_VOL)

        # bomb sound
        self.bomb_sound = pygame.mixer.Sound(GlobalVar.PROJECT_PATH + '/sound/use_bomb.wav')
        self.bomb_sound.set_volume(GlobalVar.SYSTEM_MUSIC_VOL)

        # supply sound
        self.supply_sound = pygame.mixer.Sound(GlobalVar.PROJECT_PATH + '/sound/supply.wav')
        self.supply_sound.set_volume(GlobalVar.SYSTEM_MUSIC_VOL)

        # get bomb sound
        self.get_bomb_sound = pygame.mixer.Sound(GlobalVar.PROJECT_PATH + '/sound/get_bomb.wav')
        self.get_bomb_sound.set_volume(GlobalVar.SYSTEM_MUSIC_VOL)

        # get bullet sound
        self.get_bullet_sound = pygame.mixer.Sound(GlobalVar.PROJECT_PATH + '/sound/get_bullet.wav')
        self.get_bullet_sound.set_volume(GlobalVar.SYSTEM_MUSIC_VOL)

        # upgrade sound
        self.upgrade_sound = pygame.mixer.Sound(GlobalVar.PROJECT_PATH + '/sound/upgrade.wav')
        self.upgrade_sound.set_volume(GlobalVar.SYSTEM_MUSIC_VOL)

        # fly souund
        self.enemy1_down_sound = pygame.mixer.Sound(GlobalVar.PROJECT_PATH + '/sound/enemy1_down.wav')
        self.enemy1_down_sound.set_volume(GlobalVar.SYSTEM_MUSIC_VOL)
        self.enemy2_down_sound = pygame.mixer.Sound(GlobalVar.PROJECT_PATH + '/sound/enemy2_down.wav')
        self.enemy2_down_sound.set_volume(GlobalVar.SYSTEM_MUSIC_VOL)
        self.enemy3_down_sound = pygame.mixer.Sound(GlobalVar.PROJECT_PATH + '/sound/enemy3_down.wav')
        self.enemy3_down_sound.set_volume(GlobalVar.SYSTEM_MUSIC_VOL)
        self.enemy3_fly_sound = pygame.mixer.Sound(GlobalVar.PROJECT_PATH + '/sound/enemy3_flying.wav')
        self.enemy3_fly_sound.set_volume(GlobalVar.SYSTEM_MUSIC_VOL)
        self.me_down_sound = pygame.mixer.Sound(GlobalVar.PROJECT_PATH + '/sound/me_down.wav')
        self.me_down_sound.set_volume(GlobalVar.SYSTEM_MUSIC_VOL)

        # play sound
        pygame.mixer.music.play(-1)

        # score font
        self.score_font = pygame.font.Font(GlobalVar.PROJECT_PATH + "/font/font.ttf", GlobalVar.FONT_SCORE_SIZE)

        # pause images and font
        self.paused_nor_image = pygame.image.load(GlobalVar.PROJECT_PATH + "/images/pause_nor.png").convert_alpha()
        self.paused_pressed_image = pygame.image.load(GlobalVar.PROJECT_PATH + "/images/pause_pressed.png").convert_alpha()
        self.resume_nor_image = pygame.image.load(GlobalVar.PROJECT_PATH + '/images/resume_nor.png').convert_alpha()
        self.resume_pressed_image = pygame.image.load(GlobalVar.PROJECT_PATH + '/images/resume_pressed.png').convert_alpha()

        # super bomb
        self.bomb_image = pygame.image.load(GlobalVar.PROJECT_PATH + '/images/bomb.png').convert_alpha()
        self.bomb_font = pygame.font.Font(GlobalVar.PROJECT_PATH + "/font/font.ttf", GlobalVar.FONT_BOMB_SIZE)

        # life
        self.life_image = pygame.image.load(GlobalVar.PROJECT_PATH + "/images/life.png").convert_alpha()

        # game over
        self.gameover_font = pygame.font.Font(GlobalVar.PROJECT_PATH + "/font/font.TTF", GlobalVar.FONT_GAME_OVER_SIZE)
        self.again_image = pygame.image.load(GlobalVar.PROJECT_PATH + "/images/again.png").convert_alpha()
        self.gameover_image = pygame.image.load(GlobalVar.PROJECT_PATH + "/images/gameover.png").convert_alpha()


    def define_game_vars(self):
        # 实例我方飞机
        self.me = myplane.MyPlane()

        # 实例敌方飞机
        self.enemies = pygame.sprite.Group()

        # 实例敌方小型飞机
        self.small_enemies = pygame.sprite.Group()
        add_small_enemies(self.small_enemies, self.enemies, 15)

        # 实例敌方中型飞机
        self.mid_enemies = pygame.sprite.Group()
        add_mid_enemies(self.mid_enemies, self.enemies, 4)

        # 实例敌方大型飞机
        self.big_enemies = pygame.sprite.Group()
        add_big_enemies(self.big_enemies, self.enemies, 2)

        # 实例普通子弹
        self.bullet_normal = []
        self.bullet_normal_index = 0
        self.bullet_normal_num = GlobalVar.BULLET_NORMAL_NUMBER
        for i in range(self.bullet_normal_num):
            self.bullet_normal.append(bullet.Bullet1(self.me.rect.midtop))

        # 实例超级子弹
        self.bullet_super = []
        self.bullet_super_index = 0
        self.bullet_super_num = GlobalVar.BULLET_SUPER_NUMBER
        for i in range(self.bullet_super_num // 2):
            self.bullet_super.append(bullet.Bullet2((self.me.rect.centerx - 33, self.me.rect.centery)))
            self.bullet_super.append(bullet.Bullet2((self.me.rect.centerx + 30, self.me.rect.centery)))

        # 中弹图片索引
        self.e1_destroy_index = 0
        self.e2_destroy_index = 0
        self.e3_destroy_index = 0
        self.me_destroy_index = 0

        # 统计得分
        self.score = 0

        # 标志是否暂停游戏
        self.paused = False
        self.paused_rect = self.paused_nor_image.get_rect()
        self.paused_rect.left = GlobalVar.SYSTEM_SCREEN_WIDTH - self.paused_rect.width - 10
        self.paused_rect.top = 10
        self.paused_image = self.paused_nor_image

        # 设置难度
        self.level = GlobalVar.LEVEL1

        # 全屏炸弹
        self.bomb_rect = self.bomb_image.get_rect()
        self.bomb_num = GlobalVar.SYSTEM_BOMB_NUMBER

        # 每30秒发放一个补给包
        self.bullet_supply = supply.BulletSupply()
        self.bomb_supply = supply.Bomb_Supply()

        self.supply_time = USEREVENT
        pygame.time.set_timer(self.supply_time, GlobalVar.SYSTEM_SUPPLY_TIME)

        # 超级子弹定时器
        self.double_bullet_time = USEREVENT + 1

        # 解除我方重生无敌定时器
        self.invincible_time = USEREVENT + 2

        # 标志是否使用超级子弹
        self.is_double_bullet = False

        # 生命数量
        self.life_rect = self.life_image.get_rect()
        self.life_num = GlobalVar.SYSTEM_LIFE_NUMBER

        # 用于切换我方飞机图片
        self.switch_plane = True

        # 游戏结束画面
        self.again_rect = self.again_image.get_rect()
        self.gameover_rect = self.gameover_image.get_rect()

        # 用于延迟切换
        self.delay = GlobalVar.SYSTEM_DELAY

        # 限制打开一次记录文件
        self.recorded = False

        self.clock = pygame.time.Clock()
        self.running = True


    def process_game(self):
        while self.running:
            self.listen_event()
            self.change_difficult_level()

            if self.life_num == 0:
                self.game_over()

    def listen_event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and self.paused_rect.collidepoint(event.pos):
                    self.paused = not self.paused
                    if self.paused:
                        pygame.time.set_timer(self.supply_time, 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(self.supply_time, GlobalVar.SYSTEM_SUPPLY_TIME)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()

            elif event.type == MOUSEMOTION:
                if self.paused_rect.collidepoint(event.pos):
                    if self.paused:
                        self.paused_image = self.resume_pressed_image
                    else:
                        self.paused_image = self.paused_pressed_image
                else:
                    if self.paused:
                        self.paused_image = self.resume_nor_image
                    else:
                        self.paused_image = self.paused_nor_image
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.bomb_num:
                        self.bomb_num -= 1
                        self.bomb_sound.play()
                        for each in self.enemies:
                            if each.rect.bottom > 0:
                                each.destroy()
            elif event.type == self.supply_time:
                self.supply_sound.play()
                if choice([True, False]):
                    self.bomb_supply.reset()
                else:
                    self.bullet_supply.reset()

            elif event.type == self.double_bullet_time:
                self.is_double_bullet = False
                pygame.time.set_timer(double_bullet_time, 0)

            elif event.type == self.invincible_time:
                self.me.invincible = False
                pygame.time.set_timer(self.invincible_time, 0)

        self.screen.blit(self.background, (0, 0))

        if self.life_num and not self.paused:
            # 检测键盘操作
            key_pressed = pygame.key.get_pressed()

            if key_pressed[K_w] or key_pressed[K_UP]:
                self.me.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                self.me.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                self.me.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                self.me.moveRight()

            # 绘制全屏炸弹补给
            if self.bomb_supply.active:
                self.bomb_supply.move()
                self.screen.blit(self.bomb_supply.image, self.bomb_supply.rect)
                if pygame.sprite.collide_mask(self.me, self.bomb_supply):
                    self.get_bomb_sound.play()
                    if self.bomb_num < 3:
                        self.bomb_num += 1
                        self.bomb_supply.active = False

            # 绘制超级子弹补给
            if self.bullet_supply.active:
                self.bullet_supply.move()
                self.screen.blit(self.bullet_supply.image, self.bullet_supply.rect)
                if pygame.sprite.collide_mask(self.me, self.bullet_supply):
                    self.get_bullet_sound.play()
                    # 发射超级子弹
                    self.is_double_bullet = True
                    pygame.time.set_timer(self.double_bullet_time, 18 * 1000)
                    self.bullet_supply.active = False

            # 发射子弹
            bullets = []
            if not (self.delay % 10):
                self.bullet_sound.play()
                if self.is_double_bullet:
                    bullets = self.bullet_super
                    bullets[self.bullet_super_index].reset(
                        (self.me.rect.centerx - 33, self.me.rect.centery))
                    bullets[self.bullet_super_index +
                            1].reset((self.me.rect.centerx + 30, self.me.rect.centery))
                    self.bullet_super_index = (self.bullet_super_index + 2) % self.bullet_super_num
                else:
                    bullets = self.bullet_normal
                    bullets[self.bullet_normal_index].reset(self.me.rect.midtop)
                    self.bullet_normal_index = (self.bullet_normal_index + 1) % self.bullet_normal_num

            # 检测子弹是否击中敌机
            for b in bullets:
                if b.active:
                    b.move()
                    self.screen.blit(b.image, b.rect)
                    enemy_hit = pygame.sprite.spritecollide(
                        b, self.enemies, False, pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for each in enemy_hit:
                            each.hit_for_one()

            # 绘制敌方大型机
            for each in self.big_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        self.screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        if self.switch_plane:
                            self.screen.blit(each.image1, each.rect)
                        else:
                            self.screen.blit(each.image2, each.rect)

                    # 绘制血槽
                    pygame.draw.line(self.screen, GlobalVar.BLACK,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.right, each.rect.top - 5),
                                     2)

                    # 当生命大于20%显示绿色, 否则显示红色
                    energy_remain = each.energy / enemy.BigEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GlobalVar.GREEN
                    else:
                        energy_color = GlobalVar.RED
                    pygame.draw.line(self.screen, energy_color,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.left + each.rect.width * energy_remain,
                                      each.rect.top - 5),
                                     2)

                    # 即将出现在画面, 播放音效
                    if each.rect.bottom == -10:
                        self.enemy3_fly_sound.play(-1)
                        each.appear = True
                    # 离开画面, 关闭音效
                    if each.rect.bottom < -10 and each.appear:
                        self.enemy3_fly_sound.stop()
                        each.appear = False
                else:
                    # 毁灭
                    if self.e3_destroy_index == 0:
                        self.enemy3_down_sound.play()
                    if not (self.delay % 2):
                        self.screen.blit(each.destroy_images[
                                        e3_destroy_index], each.rect)
                        self.e3_destroy_index = (self.e3_destroy_index + 1) % 6
                        if self.e3_destroy_index == 0:
                            self.enemy3_fly_sound.stop()
                            self.score += GlobalVar.SYSTEM_POINT_E3
                            each.reset()

            # 绘制敌方中型机
            for each in self.mid_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        self.screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        self.screen.blit(each.image, each.rect)

                    # 绘制血槽
                    pygame.draw.line(self.screen, GlobalVar.BLACK,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.right, each.rect.top - 5),
                                     2)

                    # 当生命大于20%显示绿色, 否则显示红色
                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GlobalVar.GREEN
                    else:
                        energy_color = GlobalVar.RED
                    pygame.draw.line(self.screen, energy_color,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.left + each.rect.width * energy_remain,
                                      each.rect.top - 5),
                                     2)
                else:
                    # 毁灭
                    if self.e2_destroy_index == 0:
                        self.enemy2_down_sound.play()
                    if not (self.delay % 2):
                        self.screen.blit(each.destroy_images[
                                             self.e2_destroy_index], each.rect)
                        self.e2_destroy_index = (self.e2_destroy_index + 1) % 4
                        if self.e2_destroy_index == 0:
                            self.score += GlobalVar.SYSTEM_POINT_E2
                            each.reset()

            # 绘制敌方小型机
            for each in self.small_enemies:
                if each.active:
                    each.move()
                    self.screen.blit(each.image, each.rect)
                else:
                    # 毁灭
                    if self.e1_destroy_index == 0:
                        self.enemy1_down_sound.play()
                    if not (self.delay % 2):
                        self.screen.blit(each.destroy_images[
                                             self.e1_destroy_index], each.rect)
                        self.e1_destroy_index = (self.e1_destroy_index + 1) % 4
                        if self.e1_destroy_index == 0:
                            self.score += GlobalVar.SYSTEM_POINT_E1
                            each.reset()

            # 检测我方飞机碰撞
            enemies_down = pygame.sprite.spritecollide(
                self.me, self.enemies, False, pygame.sprite.collide_mask)
            if enemies_down and not self.me.invincible:
                self.me.active = False
                for each in enemies_down:
                    each.destroy()

            # 绘制我方飞机
            if self.me.active:
                if self.switch_plane:
                    self.screen.blit(self.me.image1, self.me.rect)
                else:
                    self.screen.blit(self.me.image2, self.me.rect)
            else:
                # 毁灭
                if self.me_destroy_index == 0:
                    self.me_down_sound.play()
                if not (self.delay % 2):
                    self.screen.blit(self.me.destroy_images[self.me_destroy_index], self.me.rect)
                    self.me_destroy_index = (self.me_destroy_index + 1) % 4
                    if self.me_destroy_index == 0:
                        self.life_num -= 1
                        self.me.reset()
                        pygame.time.set_timer(self.invincible_time, 3 * 1000)

            # 绘制全屏炸弹数量
            bomb_text = self.bomb_font.render("× %d" % self.bomb_num, True, GlobalVar.WHITE)
            text_rect = bomb_text.get_rect()
            self.screen.blit(self.bomb_image, (10, GlobalVar.SYSTEM_SCREEN_HEIGHT - 10 - self.bomb_rect.height))
            self.screen.blit(bomb_text, (20 + self.bomb_rect.width,
                                    GlobalVar.SYSTEM_SCREEN_HEIGHT - 5 - text_rect.height))

            # 绘制剩余生命数量
            if self.life_num:
                for i in range(self.life_num):
                    self.screen.blit(self.life_image,
                                ((GlobalVar.SYSTEM_SCREEN_WIDTH - 10 - (i + 1) * self.life_rect.width),
                                 GlobalVar.SYSTEM_SCREEN_HEIGHT - 10 - self.life_rect.height))
            # 绘制得分
            score_text = self.score_font.render('Score : %d' % self.score, True, GlobalVar.WHITE)
            self.screen.blit(score_text, (10, 5))

        #  绘制游戏结束画面

        self.screen.blit(self.paused_image, self.paused_rect)

        # 用于切换图片
        if not (self.delay % 11):
            self.switch_plane = not self.switch_plane

        self.delay -= 1
        if not self.delay:
            self.delay = GlobalVar.SYSTEM_DELAY

        pygame.display.flip()
        self.clock.tick(60)

    # 根据用户得分增加难度
    def change_difficult_level(self):
        if self.level == GlobalVar.LEVEL1 and self.score > 50000:
            self.level = GlobalVar.LEVEL2
            self.upgrade_sound.play()
            # 增加3架小型敌机, 2架中型敌机和1架大型敌机
            add_small_enemies(self.small_enemies, self.enemies, 3)
            add_mid_enemies(self.mid_enemies, self.enemies, 2)
            add_big_enemies(self.big_enemies, self.enemies, 1)

            # 提升小型敌机的速度
            inc_speed(self.small_enemies, 1)
        elif self.level == GlobalVar.LEVEL2 and self.score > 300000:
            self.level = GlobalVar.LEVEL3
            self.upgrade_sound.play()
            # 增加5架小型敌机, 3架中型敌机和2架大型敌机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)

            # 提升小型敌机的速度
            inc_speed(self.small_enemies, 1)
            inc_speed(self.mid_enemies, 1)
        elif self.level == GlobalVar.LEVEL3 and self.score > 600000:
            self.level = GlobalVar.LEVEL4
            self.upgrade_sound.play()
            # 增加5架小型敌机, 3架中型敌机和2架大型敌机
            add_small_enemies(self.small_enemies, self.enemies, 5)
            add_mid_enemies(self.mid_enemies, self.enemies, 3)
            add_big_enemies(self.big_enemies, self.enemies, 2)

            # 提升小型敌机的速度
            inc_speed(target=self.small_enemies, inc=1)
            inc_speed(target=self.mid_enemies, inc=1)
        elif self.level == GlobalVar.LEVEL4 and self.score > 1000000:
            self.level = GlobalVar.LEVEL5
            self.upgrade_sound.play()
            # 增加5架小型敌机, 3架中型敌机和2架大型敌机
            add_small_enemies(self.small_enemies, self.enemies, 5)
            add_mid_enemies(self.mid_enemies, self.enemies, 3)
            add_big_enemies(self.big_enemies, self.enemies, 2)

            # 提升小型敌机的速度
            inc_speed(target=self.small_enemies, inc=1)
            inc_speed(target=self.mid_enemies, inc=1)
            inc_speed(target=self.big_enemies, inc=1)


    def pause_game(self):
        pass

    def unpause_game(self):
        pass

    def game_over(self):
        # 背景音乐停止
        pygame.mixer.music.stop()

        # 停止全部音效
        pygame.mixer.stop()

        # 停止发放补给
        pygame.time.set_timer(self.supply_time, 0)

        if not self.recorded:
            self.recorded = True
            # 读取历史最高分
            with open(GlobalVar.PROJECT_PATH + '/record.txt', 'r') as f:
                record_score = int(f.read())

            # 判断是否高于历史最高分
            if self.score > record_score:
                with open(GlobalVar.PROJECT_PATH + '/record.txt', 'w') as f:
                    f.write(str(self.score))

        # 绘制结束界面
        record_score_text = self.score_font.render("Best : %d" % record_score, True, (255, 255, 255))
        self.screen.blit(record_score_text, (50, 50))

        gameover_text1 = self.gameover_font.render("Your Score", True, (255, 255, 255))
        gameover_text1_rect = gameover_text1.get_rect()
        gameover_text1_rect.left, gameover_text1_rect.top = \
            (GlobalVar.SYSTEM_SCREEN_WIDTH - gameover_text1_rect.width) // 2, \
            GlobalVar.SYSTEM_SCREEN_HEIGHT // 3
        self.screen.blit(gameover_text1, gameover_text1_rect)

        gameover_text2 = self.gameover_font.render(str(self.score), True, (255, 255, 255))
        gameover_text2_rect = gameover_text2.get_rect()
        gameover_text2_rect.left, gameover_text2_rect.top = \
            (GlobalVar.SYSTEM_SCREEN_WIDTH - gameover_text2_rect.width) // 2, \
            gameover_text1_rect.bottom + 10
        self.screen.blit(gameover_text2, gameover_text2_rect)

        self.again_rect.left, self.again_rect.top = \
            (GlobalVar.SYSTEM_SCREEN_WIDTH - self.again_rect.width) // 2, \
            gameover_text2_rect.bottom + 50
        self.screen.blit(self.again_image, self.again_rect)

        self.gameover_rect.left, self.gameover_rect.top = \
            (GlobalVar.SYSTEM_SCREEN_WIDTH - self.again_rect.width) // 2, \
            self.again_rect.bottom + 10
        self.screen.blit(self.gameover_image, self.gameover_rect)

        # 检测用户的鼠标操作
        # 如果用户按下鼠标左键
        if pygame.mouse.get_pressed()[0]:
            # 获取鼠标坐标
            pos = pygame.mouse.get_pos()
            # 如果用户点击“重新开始”
            if self.again_rect.left < pos[0] < self.again_rect.right and \
                    self.again_rect.top < pos[1] < self.again_rect.bottom:
                # 调用main函数，重新开始游戏
                self.init_game()
            # 如果用户点击“结束游戏”
            elif self.gameover_rect.left < pos[0] < self.gameover_rect.right and \
                    self.gameover_rect.top < pos[1] < self.gameover_rect.bottom:
                # 退出游戏
                pygame.quit()
                sys.exit()


def add_small_enemies(g1, g2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy()
        g1.add(e1)
        g2.add(e1)


def add_mid_enemies(g1, g2, num):
    for i in range(num):
        e2 = enemy.MidEnemy()
        g1.add(e2)
        g2.add(e2)


def add_big_enemies(g1, g2, num):
    for i in range(num):
        e3 = enemy.BigEnemy()
        g1.add(e3)
        g2.add(e3)


def inc_speed(target, inc):
    for each in target:
        each.speed += inc
