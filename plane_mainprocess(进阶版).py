import pygame

import plane_sprites
from  plane_sprites import *
import  random

class  PlaneGame(object):
    """飞机大战主游戏"""
    def __init__(self):
        # 创建游戏窗口
        self.screen = game_screen
        # 创建时钟对象
        self.clock = pygame.time.Clock()
        # 调用私有方法，精灵和精灵组的创建
        self.__create_sprites()
        # 设置定时器事件，每隔一段时间执行一个动作（事件） 1000单位时毫秒
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        # 设置定时器，定时执行开火事件，每0.5s开一次火
        pygame.time.set_timer(FIRE_EVENT,300)
        # 创建敌机2号事件
        pygame.time.set_timer(CREATE_ENEMY2_EVENT, 1000)
        bg_music.set_volume(0.3)
        bg_music.play()
    def __create_sprites(self):
        # 创建两个背景对象，并设置两张背景图的初始位置
        # 这里可以直接将图片解析的方法封装在初始化函数中，这样可以简化主程序的代码
        bg1 = Background()
        bg2 = Background()
        # bg1 = Background("./images/background.png",5)
        # bg2 = Background("./images/background.png",5)
        # 将第二张背景图的初始位置设置在幕布的上方
        bg2.rect.y = -bg2.rect.height
        # 设置个全局变量精灵组，并把两张背景加入组中
        self.bg_group = pygame.sprite.Group(bg1, bg2)
        # 创建敌机组，这里不用加入对象，后面会通过事件监听，做出相应的创建敌机对象动作，并加入到敌机组中
        self.enemy_group = pygame.sprite.Group()
        # 创建英雄战机和英雄战机组
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)
        self.hero.speed2 = 0
    def start(self):
        print("游戏开始")
        while True:
            # 循环内部
            # 1.设置刷新率
            self.clock.tick(TIME_TICK)
            # 2.事件监听
            self.__event_handler()
            # 3.碰撞检测
            self.__check_collide()
            # 4.更新/绘制精灵组
            self.__update_sprites()
            # 5.更新显示
            pygame.display.update()

    def __event_handler(self):
        """事件监听，根据不同事件，执行不同动作"""
        for event in pygame.event.get():
            # 监听退出事件
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            # 监听创建敌机事件
            elif event.type == CREATE_ENEMY_EVENT :
                # print("创建敌机")
                self.enemy = Enemy()
                self.enemy_group.add(self.enemy)

                print("还剩%d个敌机" % len(self.enemy_group))
            elif event.type == CREATE_ENEMY2_EVENT:
                # print("创建敌机")
                enemy = Enemy2()
                self.enemy_group.add(enemy)
                # print("还剩%d个敌机" % len(self.enemy_group))
            #  监听开火事件
            elif event.type == FIRE_EVENT:
                self.hero.fire()
            # # 移动英雄方法1.用户必须抬起键盘参能算一次键盘事件，操作灵活度不高
            # elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            #     print("向右移动。。。")
        # 移动英雄方法2.用户可以按住键盘不放，就能持续的想一个方向移动
        # key模块中的get_pressed方法可以返回所有按键的元组，如果某个按键被按下，对应的值为1
        keys_pressed = pygame.key.get_pressed()
        # 判断是否按下向右的方向键
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.speed = 3
        # 判断是否按下向左的方向键
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speed = -3
        # 判断是否按下向上的方向键
        elif keys_pressed[pygame.K_UP]:
            self.hero.speed2 = -3
        # 判断是否按下向下的方向键
        elif keys_pressed[pygame.K_DOWN]:
            self.hero.speed2 = 3
        elif keys_pressed[pygame.K_SPACE]:
            self.hero.fire_bule()
        # 如果按下其他按键或者没有按下任何按键则飞机速度为0，没有移动速度数据的飞机，就会静止在原地
        else :
            self.hero.speed = 0
            self.hero.speed2 = 0

    def __check_collide(self):
        """碰撞检测"""
        # 子弹摧毁敌机
        pygame.sprite.groupcollide(self.enemy_group,self.hero.bullet_group,True,True)

        #  英雄飞机碰撞敌机
        break_enemies = pygame.sprite.spritecollide(self.hero,self.enemy_group,True)
        if len(break_enemies) > 0 :
            PlaneGame.__game_over()

    def __update_sprites(self):
        """更新幕布"""
        # 调用精灵组对象，更新数据并绘制新图到幕布上
        # 1.更新背景的
        self.bg_group.update()
        self.bg_group.draw(self.screen)
        # 2.更新敌机的
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        # 3.更新英雄飞机
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        # 4.飞机发射子弹
        self.hero.bullet_group.update()
        self.hero.bullet_group.draw(self.screen)
    @staticmethod
    def __game_over():
        """游戏结束方法"""
        print("游戏结束")
        pygame.quit()
        exit()

    def destoty(self,images,x,y):
        for i in images:
            self.screen.blit(i,(x,y))
            pygame.display.update()

if __name__ == '__main__':
    game = PlaneGame()
    game.start()