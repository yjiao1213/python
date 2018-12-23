import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        super().__init__()
        #初始化飞船并设置初始位置
        self.screen = screen
        self.ai_settings = ai_settings
        
        #加载飞船图像
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        #新飞船放到屏幕底部中央
        self.rect.center = self.screen_rect.center
        self.rect.bottom = self.screen_rect.bottom

        # 在飞船的属性center中存储小数值
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

        #移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        #控制移动
        if self.moving_right == True and self.rect.right < self.screen_rect.right:
            self.centerx += self.ai_settings.ship_speed_factor

        if self.moving_left == True and self.rect.left > 0:
            self.centerx -= self.ai_settings.ship_speed_factor

        if self.moving_down == True and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.ai_settings.ship_speed_factor

        if self.moving_up == True and self.rect.top > self.screen_rect.top:
            self.centery -= self.ai_settings.ship_speed_factor

        # 根据self.center更新rect对象
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery


    def blitme(self):
        #绘制飞船
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        #让飞船在屏幕上居中
        self.center = self.screen_rect.centerx