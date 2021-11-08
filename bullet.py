import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Класс для управления снарядами, выпущенными кораблем"""
    def __init__(self, ai_game):
        # Обращаемся к родительскому конструктору Sprite
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Создание снарядов в позиции (0,0) и назначение правильной позиции
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                            self.settings.bullet_height)
        # Расположение пули на верху корабля
        self.rect.midtop = ai_game.ship.rect.midtop

        # Позиция снаряда хранится в вещественной форме
        self.y = float (self.rect.y)

    def update(self):
        """перемещает снаряд вверх по экрану"""
        # Обновление позиции снаряда в вещественном формате
        self.y -= self.settings.bullet_speed_factor
        # Обновление позиции прямоугольника
        self.rect.y = self.y

    def draw_bullet(self):
        """Вывод снаряда на экран"""
        pygame.draw.rect(self.screen, self.color, self.rect)

