class GameStats():
    """Отслеживание статистики для игры"""
    def __init__(self, ai_game):
        """Инициализируем статистику"""
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False
        #Рекорды не сбрасываются
        self.high_score = 0

    def reset_stats(self):
        """инициализирует статистику, изм-ся в ходе игры"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1