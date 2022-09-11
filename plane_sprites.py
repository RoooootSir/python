#  这是一个为主程序提供工具的文件
import time
import threading
import pygame
import random
pygame.init()

# 屏幕大小的常量
GAME_CREEN = pygame.Rect(0,0,480,700)
game_screen = pygame.display.set_mode(GAME_CREEN.size)
# 刷新帧率的常量
TIME_TICK = 80
# 定义一个创建敌机事件，事件类型为用户自定义事件
CREATE_ENEMY_EVENT = pygame.USEREVENT  #  USEREVENT 这个方法就是产生一个事件常量
# 定义一个发射子弹事件
FIRE_EVENT = pygame.USEREVENT + 1
# 创建敌机类型2 事件
CREATE_ENEMY2_EVENT = pygame.USEREVENT +2
# 背景音乐
pygame.mixer.init()
bg_music = pygame.mixer.Sound("./bg_music/bg2.mp3")
fire_music = pygame.mixer.Sound("./bg_music/飞机游戏背景配乐和子弹、爆炸声/飞机游戏背景配乐和子弹、爆炸声/short_lazer.mp3")
fire_music2 = pygame.mixer.Sound("./bg_music/飞机游戏背景配乐和子弹、爆炸声/飞机游戏背景配乐和子弹、爆炸声/laser.mp3")
enemy_destory_music = pygame.mixer.Sound("./bg_music/飞机游戏背景配乐和子弹、爆炸声/飞机游戏背景配乐和子弹、爆炸声/destroyer_lazer2.mp3")
enemy2_destory_music = pygame.mixer.Sound("./bg_music/飞机游戏背景配乐和子弹、爆炸声/飞机游戏背景配乐和子弹、爆炸声/destroyer_lazer4.mp3")

class sprites(pygame.sprite.Sprite):
    """飞机大战游戏精灵类"""
    def __init__(self, image_name, speed=1):
        # 调用父类的初始化方法，这样就可以避免因为重写初始化的原因，而导致不能调用父类初始化内封装的方法
        super().__init__()
        #  定义对象属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        # 在屏幕的垂直方向上移动
        self.rect.y += self.speed

class Background(sprites):
    """游戏背景精灵"""

    def __init__(self):
        #  解析背景图像，方便创建对象。把背景图像直接封装在类中。
        super().__init__("./images/background.png")

    def update(self):
        # 1.调用父类方法实现
        super().update()
        # 2.判断图像是否移出幕布，如果移出幕布，则把图片位置重新定义在幕布顶端
        if self.rect.y >= GAME_CREEN.height:
            self.rect.y = -self.rect.height

class Enemy(sprites):
    """创建敌机类"""
    def __init__(self):
        # 1.调用父类初始化方法，创建敌机模型
        super().__init__("./images/enemy1.png")
        # 2.定义敌机初始速度
        self.speed = random.randint(1, 3)
        # 3.定义敌机初始位置
        self.rect.x = random.randint(0, GAME_CREEN.width-self.rect.width)
        self.rect.y = -self.rect.height
        self.clock = pygame.time.Clock()
        self.destory_images = [pygame.image.load("./images/enemy1.png"),
                               pygame.image.load("./images/enemy1_down1.png"),
                               pygame.image.load("./images/enemy1_down2.png"),
                               pygame.image.load("./images/enemy1_down3.png"),
                               pygame.image.load("./images/enemy1_down4.png")]

    def update(self):
        # 1.调用父类方法保持飞行
        super().update()
        # 2.判断敌机是否飞出屏幕，如果是，则从敌机组中删除敌机
        if self.rect.y >= 743:
            # 将精灵从组中删除，也就是将数据从内存中擦除
            self.kill()



    def __del__(self):
        """在敌机被移除内存之前，执行下面的动作"""
        enemy_destory_music.set_volume(0.3)
        enemy_destory_music.play()
        print("有敌机在坐标为%d.%d处销毁" % (self.rect.x, self.rect.y))
        if  self.rect.y > 700 :
            pass
        else:
            for i in self.destory_images:
                self.clock = pygame.time.Clock()
                self.clock.tick(120)
                game_screen.blit(i,(self.rect.x, self.rect.y))
                pygame.display.update()




class Enemy2(sprites):
    """创建敌机类"""
    def __init__(self):
        # 1.调用父类初始化方法，创建敌机模型
        super().__init__("./images/enemy2.png")
        # 2.定义敌机初始速度
        self.speed = random.randint(1, 2)
        # 3.定义敌机初始位置
        self.rect.x = random.randint(0, GAME_CREEN.width - self.rect.width)
        self.rect.y = -self.rect.height
        self.clock = pygame.time.Clock()
        self.destory_images = [pygame.image.load("./images/enemy2.png"),
                               pygame.image.load("./images/enemy2_down1.png"),
                               pygame.image.load("./images/enemy2_down2.png"),
                               pygame.image.load("./images/enemy2_down3.png"),
                               pygame.image.load("./images/enemy2_down4.png")]
    def update(self):
        # 1.调用父类方法保持飞行
        super().update()
        # 2.判断敌机是否飞出屏幕，如果是，则从敌机组中删除敌机
        if self.rect.y >= 743:
            # 将精灵从组中删除，也就是将数据从内存中擦除
            self.kill()

    def __del__(self):
        """在敌机被移除内存之前，执行下面的动作"""
        enemy2_destory_music.set_volume(0.5)
        enemy2_destory_music.play()
        print("有敌机在坐标为%d.%d处销毁" % (self.rect.x ,self.rect.y))
        if self.rect.y > 700:
            pass
        else:
            for i in self.destory_images:
                self.clock = pygame.time.Clock()
                self.clock.tick(120)
                game_screen.blit(i, (self.rect.x, self.rect.y))
                pygame.display.update()


class Hero(sprites):
    """创建英雄类"""
    def __init__(self):
        # 创建英雄飞机图像和初始位置以及速度，这里这是飞机速度为0
        super().__init__("./images/me1.png",0)
        self.rect.centerx = GAME_CREEN.centerx
        self.rect.y = GAME_CREEN.height - 126
        # 定义一个纵向移动的速度
        self.speed2 = 0
        # 创建子弹的精灵组
        self.bullet_group = pygame.sprite.Group()
    def update(self):
        # 判断飞机位置是否超出屏幕左右两侧，如过超出屏幕，则飞机不可向屏幕外的方向移动
        if self.rect.x >= GAME_CREEN.width - self.rect.width:
            if self.speed >= 0:
                pass
            else:
                self.rect.x += self.speed
        elif self.rect.x <= 0:
            if self.speed <= 0:
                pass
            else:
                self.rect.x += self.speed
        else:
            self.rect.x += self.speed
        # 判断飞机位置是否超出屏幕上下两侧，如过超出屏幕，则飞机不可向屏幕外的方向移动
        if self.rect.y >= GAME_CREEN.height - self.rect.height:
            if self.speed2 >= 0:
                pass
            else:
                self.rect.y += self.speed2
        elif self.rect.y <= 0:
            if self.speed2 <= 0:
                pass
            else:
                self.rect.y += self.speed2
        else:
            self.rect.y += self.speed2
        # self.rect.y += self.speed2
    def fire(self):
        # 1.创建子弹精灵 三连发
        bullet1 = Bullet()
        bullet2 = Bullet()
        bullet3 = Bullet()
        # 2.设置子弹精灵位置
        bullet1.rect.y = self.rect.y - 10
        bullet2.rect.y = self.rect.y - 10
        bullet3.rect.y = self.rect.y - 10

        bullet1.rect.x = self.rect.centerx - 20
        bullet2.rect.x = self.rect.centerx
        bullet3.rect.x = self.rect.centerx + 20
        # 3.将子弹降入子弹精灵组
        self.bullet_group.add(bullet1,bullet2 ,bullet3)
        # 设置音量大小
        fire_music.set_volume(0.1)
        fire_music.play()

    def fire_bule(self):
        # 1.创建子弹精灵 三连发
        bullet1 = Bullet_bule()
        bullet2 = Bullet_bule()
        bullet3 = Bullet_bule()
        # 2.设置子弹精灵位置
        bullet1.rect.y = self.rect.y + 30
        bullet2.rect.y = self.rect.y + 30

        bullet1.rect.x = self.rect.centerx - 40
        bullet2.rect.x = self.rect.centerx + 40
        # 3.将子弹降入子弹精灵组qq
        self.bullet_group.add(bullet1, bullet2)
        fire_music2.set_volume(0.1)
        fire_music2.play()
class Bullet(sprites):
    """子弹精灵类"""
    def __init__(self):
        super().__init__("./images/bullet1.png", -2)

    def update(self):
        super().update()
        if self.rect.y < -self.rect.height:
            self.kill()

class Bullet_bule(sprites):
    """子弹精灵类"""
    def __init__(self):
        super().__init__("./images/bullet2.png", -5)

    def update(self):
        super().update()
        if self.rect.y < -self.rect.height:
            self.kill()