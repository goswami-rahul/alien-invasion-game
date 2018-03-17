import pygame
import pygame.font
import pygame.time
from pygame.sprite import Group

from game_stats import GameStats
from settings import Settings
from ship import Ship


class Scorecard:
    """A class to display scorecard."""

    def __init__(self, ai_settings: Settings, stats: GameStats, screen: pygame.SurfaceType):

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        self.score_ship_size = self.ai_settings.score_ship_size  # size of ship in the scoreboard.
        self.dur_highscore_msg = 3000        # duration of highscore msg = 3 sec

        # Font settings.
        font_name = 'fonts/PoiretOne.ttf'       # try changing the font
        self.font_color = self.ai_settings.score_font_color
        self.font = pygame.font.Font(font_name, self.ai_settings.score_font_size)

        # Prepare the initial score image.
        self.prep_images()

    def prep_images(self):
        """Prepare the scorecard."""
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Prepare the image of score."""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)

        self.score_image = self.font.render(score_str, True, self.font_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.top = 10
        self.score_rect.right = self.screen_rect.right - 20

    def show_score(self):
        """Display the score."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.ship_str_image, self.ship_str_rect)
        self.ships.draw(self.screen)
        self.print_high_score_msg()

    def print_high_score_msg(self):
        """Display the high score message when broken."""
        if self.stats.score > self.stats.prev_high_score and not self.stats.broke_highscore:
            self.stats.time_to_blit = pygame.time.get_ticks() + self.dur_highscore_msg
            self.stats.broke_highscore = True

        if self.stats.time_to_blit:
            self.screen.blit(self.new_high_score_image, self.new_high_score_rect)
            if pygame.time.get_ticks() >= self.stats.time_to_blit:
                self.stats.time_to_blit = None

    def prep_high_score(self):
        """Prepare the high score."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "High Score: {:,}".format(high_score)

        self.high_score_image = self.font.render(high_score_str, True, self.font_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.top = self.score_rect.top
        self.high_score_rect.centerx = self.screen_rect.centerx

        self.new_high_score_msg = "Congratulations! New High Score."
        self.new_high_score_image = self.font.render(self.new_high_score_msg, True, self.font_color)
        self.new_high_score_rect = self.new_high_score_image.get_rect()
        self.new_high_score_rect.centerx = self.high_score_rect.centerx
        self.new_high_score_rect.y = self.high_score_rect.bottom + 4

    def prep_level(self):
        """Prepare the image of current level."""
        level_str = "Level: {:d}".format(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.font_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.top = self.score_rect.top + 45
        self.level_rect.right = self.score_rect.right

    def prep_ships(self):
        """Show how many ships are left."""
        ship_str = "Ships left:  " if self.stats.ships_left > 0 else "No ships left."
        self.ship_str_image = self.font.render(ship_str, True, self.font_color)
        self.ship_str_rect = self.ship_str_image.get_rect()
        self.ship_str_rect.x = 10
        self.ship_str_rect.y = self.score_rect.top

        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen, self.score_ship_size)
            ship.rect.x = self.ship_str_rect.width + ship_number * ship.rect.width
            ship.rect.centery = self.ship_str_rect.centery
            self.ships.add(ship)
