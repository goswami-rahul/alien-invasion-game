from typing import Union

import pygame
from pygame.sprite import Group

from button import Button
from game_stats import GameStats
from scorecard import Scorecard
from settings import Settings
from ship import Ship


class GameItems:
    """A class representing all game items."""

    acceptable_game_items = ['screen', 'ship', 'aliens', 'bullets', 'play_button', 'restart_button', 'sb']
    game_items_types = Union[pygame.SurfaceType, Ship, Group, Button, Scorecard]

    def __init__(self, ai_settings: Settings, stats: GameStats, **kwargs: game_items_types):
        """Initialize with default items unless specified in kwargs."""

        # Default initializations for game items.
        # Initialize screen.
        flags = pygame.HWSURFACE | pygame.DOUBLEBUF    # | pygame.FULLSCREEN
        self.screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height), flags)
        pygame.display.set_caption("Alien Invasion Game")

        # Initialize ship.
        self.ship = Ship(ai_settings, self.screen)

        # Initialize aliens group.
        self.aliens = Group()

        # Initialize bullets group.
        self.bullets = Group()

        # Initialize buttons.
        self.play_button = Button(self.screen, "Play!")

        # TODO implement Restart and Cancel buttons.
        # self.restart_button = Button(self.screen, "Restart")
        # self.cancel_button = Button(self.screen, "Cancel", (255, 0, 0, 80))
        # self.set_button_pos()

        # Initialize scorecard.
        self.sb = Scorecard(ai_settings, stats, self.screen)

        # Set the game items for those default values are given.
        for game_item in kwargs:
            if game_item in self.acceptable_game_items:
                self.__setattr__(game_item, kwargs[game_item])
