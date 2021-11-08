import sys
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры"""

    def __init__(self):
        """Инициализирует игру и создаёт игровые ресурсы"""
        pygame.init()
        # Импортировали ранее, создали элемент класса Settings и сохранили
        self.settings = Settings()
        # Задаем поверхность, по настройкам Settings и заголовок окна
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alexey Invasion")

        # Создание экземпляра для хранения игровой статистики
        self.stats = GameStats(self)

        # Инициализируем статистику
        self.sb = Scoreboard(self)

        # Инициализация корабля
        self.ship = Ship(self)

        # Изменим цвет фона
        self.bg_color = self.settings.bg_color

        # Инициализация пуль
        self.bullets = pygame.sprite.Group()

        # Инициализация пришельцев
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # Инициализация кнопки Play
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Запуск основного цикла игры"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        """Вспомогательный метод"""
        """Обрабатывает нажатия клавиш и события мыши"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        # Нажал правую или левую кнопку
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        # Отпустил правую или левую кнопку
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Создание нового снаряда и включение в группу bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """Созданеи флота пришельцев"""
        # Создание пришельцов и вычисление кол-ва их в ряду
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Определяем кол-во рядов, попадающих в экран
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (2 * alien_height) - ship_height)
        #если 3
        #y=1080 -3*148- 148 =488
        #488 // (2*148_) = 1.6
        number_rows = available_space_y // (2 * alien_height)

        # Создание всего флота
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцев края экрана"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_alien(self, alien_number, row_number):
        # Создание пришельца и размещение его в ряду
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_bullet_alien_collisons(self):
        """Обработка коллизий снарядов и пришельце"""
        # Удаление снарядов и пришельце, участвующих в коллизиях
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()


        if not self.aliens:
            # Уничтожение существующих снарядов и создание нового флота
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """Проверяет достиг ли флот края,
        с последующим обновлением позиций всех пришельцев
        """
        self._check_fleet_edges()
        self.aliens.update()
        # Проверка коллизий пришелец-корабль
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("Лживые подонки. Все прочли? Запомнили? Ждите")
            self._ship_hit()

        # Проверка, добрались ли пришельцы до нижнего края экрана
        self._check_aliens_bottom()


    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # Отображение пришельцев
        self.aliens.draw(self.screen)

        # Вывод информации о счёте
        self.sb.show_score()

        # Кнопка Play отображается, если игра неактивна
        if not self.stats.game_active:
            self.play_button.draw_button()
        # Отображение последнего прорисованного экрана"""
        pygame.display.flip()

    def _update_bullets(self):
        """Обновление позиции снаряда и удаление снарядов, вышедших за край экрана"""
        # Обновление позиций снаряда
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisons()

        if not self.aliens:
            # Уничтожение существующих снарядов и нового флота
            self.bullets.empty()
            self._create_fleet()
    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пришельцем"""
        if self.stats.ships_left > 0:
            # Уменьшение ship_left
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # Очистка списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()
            # Создание нового флота и размещения корабля в центре
            self._create_fleet()
            self.ship.center_ship()
            # Пауза
            sleep(0.5)
        else:
            self.stats.game_active = False

    def _check_aliens_bottom(self):
        """Проверяет, добрались ли пришельцы до нижнего края экрана"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break
    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Сброс
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            # Очистка списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()
            # Создание нового флота и размещение корабля в цетре
            self._create_fleet()
            self.ship.center_ship()
            # Скрыть мышь
            #pygame.mouse.set_visible(False)
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()



if __name__ == "__main__":
    """Создание экземпляра и запуск игры"""
    ai = AlienInvasion()
    ai.run_game()
