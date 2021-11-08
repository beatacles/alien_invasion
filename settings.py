class Settings():
    """Класс для хранения настроек игры Alien Invasion"""

    def __init__(self):
        """Инициализирует настройки игры"""
        # Параметры экрана
        self.screen_width = 1920
        self.screen_height = 1080
        self.bg_color = (230, 230, 230)

        # Настройки корабля
        #self.ship_speed = 5
        self.ship_limit = 3


        # Параметры снаряда
        #self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 10

        #Параметры пришельцев
        #self.alien_speed = 5.0
        self.fleet_drop_speed = 10
        # fleet_direction = 1 обозначатет движение вправо, -1 - влево
        self.fleet_direction = 1

        #Параметры игры
        self.speedup_scale = 1.2
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициализирует динамические настройки игры"""
        self.ship_speed_factor = 5.0
        self.bullet_speed_factor = 5.0
        self.alien_speed_factor = 3.0
        self.fleet_direction = 1

        #Подсчёт очков
        self.alien_points = 50

    def increase_speed(self):
        """Увеличивает настройки скорости"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

