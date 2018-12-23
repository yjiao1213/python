class Gmaestats():

    def __init__(self, ai_settings):
        # 信息初始化
        self.ai_settings = ai_settings
        self.reset_stats()
        # 游戏刚启动时处于非活动状态
        self.game_active = False
        # 在任何情况下都不应重置最高得分
        self.write_high_score()
        #self.high_score = 0

    def reset_stats(self):
        # 初始化在游戏运行期间可能变化的统计信息
        self.ships_left = self.ai_settings.ship_limit
        # 记分
        self.score = 0
        # 等级
        self.level = 1

    def write_high_score(self):
        try:
            with open("high_score.txt", "r") as f:
                self.high_score = int(f.readlines()[0])
        except:
            self.high_score = 0