import pygame
from pygame.sprite import Sprite

from game_stats import GameStats
from settings import Settings
from ship import Ship


class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_settings: Settings, screen: pygame.SurfaceType, ship: Ship):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = screen

        # Create a bullet rect at (0, 0) and then set its position.
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.centery

        # Store the bullet's position as float.
        self.y = float(self.rect.y)
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self, stats: GameStats):
        """Move the bullet up the screen."""
        self.y -= self.speed_factor * stats.time_passed
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw bullet on the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
