import pygame

class Jyx():

    def __init__(self, screen):
        #初始化并设置初始位置
        self.screen = screen

        #加载图像
        self.image = pygame.image.load('images/1_-min.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        #放到屏幕中央
        self.rect.center = self.screen_rect.center
        self.rect.center = self.screen_rect.center

    def blitme(self):
        #绘制
        self.screen.blit(self.image, self.rect)