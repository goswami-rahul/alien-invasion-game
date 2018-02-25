import pygame
from pygame.sprite import Group

from alien_invasion.scorecard import Scorecard
from alien_invasion.settings import Settings
from alien_invasion.ship import Ship
from alien_invasion.button import Button
from alien_invasion.game_stats import GameStats
from typing import Union


class GameItems:
	"""A class representing all game items."""
	
	acceptable_game_items = ['screen', 'ship', 'aliens', 'bullets', 'play_button', 'restart_button', 'sb']
	game_items_annotations = Union[pygame.SurfaceType, Ship, Group, Button, Scorecard]
	
	def __init__(self, ai_settings: Settings, stats: GameStats, **kwargs: game_items_annotations):
		"""Initialize with default items unless specified in kwargs."""
		
		# Default initializations for game items.
		# Initialize screen.
		self.screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height)
			, pygame.HWSURFACE | pygame.FULLSCREEN | pygame.DOUBLEBUF)
		pygame.display.set_caption("Alien Invasion Game")
		
		# Initialize ship.
		self.ship = Ship(ai_settings, self.screen)
		
		# Initialize aliens group.
		self.aliens = Group()
		
		# Initialize bullets group.
		self.bullets = Group()
		
		# Initialize buttons.
		self.play_button = Button(self.screen, "Play !")
		# self.restart_button = Button(self.screen, "Restart")
		# self.cancel_button = Button(self.screen, "Cancel", (255, 0, 0, 80))
		# self.set_button_pos()
		
		# Initialize scorecard.
		self.sb = Scorecard(ai_settings, stats, self.screen)
		
		for game_item in kwargs:
			if game_item in self.acceptable_game_items:
				self.__setattr__(game_item, kwargs[game_item])