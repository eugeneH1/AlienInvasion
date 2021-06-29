import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullets import Bullet
from alien import Alien
from gamestats import GameStats
from button import Button
from scoreboard import Scoreboard
from bomb import Bomb
from explosion import Explosion


class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.bg_colour = (230, 230, 230)
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.bomb = pygame.sprite.Group()
        self.explosion = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, "Play")

    def run_game(self):
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self.bomb.update()
                self._update_aliens()
                self.explosion.update()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            if self.stats.level % 2 == 0 and self.stats.bomb > 0:
                self._fire_bomb()
            else:
                self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.stats.reset_stats()
            self.settings.initialise_dynamic_settings()
            self.stats.game_active = True

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        if len(self.bullets.copy()) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _fire_bomb(self):
        new_bomb = Bomb(self)
        self.bomb.add(new_bomb)

    def _update_bullets(self):
        self.bullets.update()
        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))
        self._check_bullet_collisions()
        self._check_bomb_collisions()
        self._check_exp_collisions()

    def _check_bullet_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for alien in collisions.values():
                self.stats.score += self.settings.alien_points * len(alien)
                self.sb.prep_score()
                self.sb.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()
            self.stats.bomb = 1

    def _check_bomb_collisions(self):
        bomb_coll = pygame.sprite.groupcollide(self.bomb, self.aliens, True, True)
        if bomb_coll:
            for collision in bomb_coll.keys():
                self.stats.score += self.settings.alien_points * len(bomb_coll) * 5
                self.sb.prep_score()
                self.sb.check_high_score()
                self.stats.bomb -= 1
                x = collision.rect.x
                y = collision.rect.y
                if self.stats.level <= 6:
                    print("level: " + str(self.stats.level))
                    bomb_size = self.stats.level
                else:
                    bomb_size = 7
                exp = Explosion(self, x, y, bomb_size)
                self.explosion.add(exp)

    def _check_exp_collisions(self):
        collisions = pygame.sprite.groupcollide(self.explosion, self.aliens, False, True)
        if collisions:
            for alien in collisions:
                self.stats.score += self.settings.alien_points * len(collisions) * 15
                self.sb.prep_score()
                self.sb.check_high_score()

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.screen.get_rect().width - (2 * alien_width)
        number_of_aliens = available_space_x // (2 * alien_width)
        # Determine number of rows of aliens that fit onto screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_of_rows = (available_space_y // alien_height) - 1
        # Create fleet
        for row_number in range(number_of_rows):
            for alien_number in range(number_of_aliens):
                self._create_alien(alien_number, row_number)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            print("Ship hit!!!")
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        self.bomb.draw(self.screen)
        self.explosion.draw(self.screen)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
