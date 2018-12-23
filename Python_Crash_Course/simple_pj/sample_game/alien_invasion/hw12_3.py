import pygame
from settings import Settings


def run_game():
    #初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #设置背景颜色
    bg_clr = ai_settings.bg_clr

    # 开始游戏的主循环
    while True:
        #监视事件
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print(event.key)



run_game()

