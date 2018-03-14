import os.path

import pygame
from pygame.sprite import Sprite

from game_stats import GameStats
from settings import Settings


class Alien(Sprite):
    """A class to represent a single alien in a fleet."""

    def __init__(self, ai_settings: Settings, screen: pygame.SurfaceType,
                 image_name='images/alien1.png'):
        """Initialize the alien and set its starting position."""

        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.screen_rect = screen.get_rect()

        # Load the alien image and set its rect attribute.
        fullname = os.path.join('.', image_name)
        try:
            self.image = pygame.image.load(fullname)
        except pygame.error:
            print('Cannot load image:', image_name)
            raise SystemExit
        self.image = pygame.transform.scale(self.image, ai_settings.alien_size)
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.drop_dist = self.y + self.ai_settings.alien_drop_dist

    def blitme(self):
        """Draw the alien at its current position."""
        self.screen.blit(self.image, self.rect)

    def update(self, stats: GameStats):
        """Move the alien."""
        self.x += self.ai_settings.alien_speed_factor_x * self.ai_settings.alien_direction_x * stats.time_passed
        self.rect.x = self.x
        if self.y > self.drop_dist:
            self.drop_dist += self.ai_settings.alien_drop_dist
        self.y += self.ai_settings.alien_speed_factor_y * self.ai_settings.alien_direction_y * stats.time_passed
        self.rect.y = self.y

    def check_edges(self, edge='both'):
        """Returns True if alien is at edge of screen."""

        left_edge = self.rect.left <= self.screen_rect.left
        right_edge = self.rect.right >= self.screen_rect.right
        if edge == 'left':
            return left_edge
        elif edge == 'right':
            return right_edge
        else:
            return left_edge or right_edge
