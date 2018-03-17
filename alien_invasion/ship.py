import os.path
import pygame
from pygame.sprite import Sprite

from game_stats import GameStats
from settings import Settings


class Ship(Sprite):
    def __init__(self, ai_settings: Settings, screen: pygame.SurfaceType
                 , size=(0, 0), image_name="images/ship1.png"):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the ship image and get its rect.
        # fullname = os.path.join(os.getcwd(), image_name
        try:
            self.image = pygame.image.load(image_name)
        except pygame.error as e:
            print('Cannot load image: ', image_name)
            print(e)
            raise SystemExit
        if size == (0, 0):
            size = ai_settings.ship_size
        self.image = pygame.transform.scale(self.image, size)

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a float value for the ship's center.
        self.center = float(self.rect.centerx)

        # Movement Flags.
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def update(self, stats: GameStats):
        """Update the ship's position based on the movement flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor * stats.time_passed
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor * stats.time_passed

        # Update rect object from self.center
        self.rect.centerx = self.center

    def center_ship(self):
        """Position the ship at center on screen."""
        self.center = float(self.screen_rect.centerx)
