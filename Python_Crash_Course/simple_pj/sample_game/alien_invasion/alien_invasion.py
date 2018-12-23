import pygame
import game_functions as gf
from settings import Settings
from ship import Ship
from pygame.sprite import Group
from game_stats import Gmaestats
from button import Button
from scoreboard import Scoreboard

def run_game():
    #初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #创建Play按钮
    play_button = Button(ai_settings, screen, "Play")

    # 创建用于存储游戏统计信息的实例
    stats = Gmaestats(ai_settings)

    # 创建记分牌
    sb = Scoreboard(ai_settings, screen, stats)

    #设置背景颜色
    bg_clr = ai_settings.bg_clr

    #创建一个飞船
    ship = Ship(ai_settings, screen)

    #创建一组外星人
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)

    #创建一组子弹
    bullets = Group()

    # 开始游戏的主循环
    while True:
        #监视事件
        gf.check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens, sb)

        if stats.game_active:
            # 隐藏光标
            pygame.mouse.set_visible(False)
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb)

         # 更新屏幕
        gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button, sb)

run_game()