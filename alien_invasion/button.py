import pygame


class Button():
	"""Represents a button on the screen."""
	
	def __init__(self, screen: pygame.SurfaceType, msg: str, b_color: tuple=()):
		
		self.screen = screen
		self.screen_rect = screen.get_rect()
		
		# Dimensions and properties of button.
		self.width = 150
		self.height = 50
		self.button_transparency = 80
		self.button_color = b_color if b_color else (0, 255, 0, self.button_transparency)
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont("comicsansms", 48)
		
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = self.screen_rect.center
		
		self.prep_msg(msg)
		
	def prep_msg(self, msg: str):
		"""Prepares msg into rendered image and position it at button center."""
		self.msg_image = self.font.render(msg, True, self.text_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center
		
	def draw_button(self):
		"""Draw button with msg."""
		self.screen_alpha = self.screen.convert_alpha(self.screen)
		self.screen_alpha.fill(self.button_color, self.rect)
		self.screen_alpha.blit(self.msg_image, self.msg_image_rect)
		self.screen.blit(self.screen_alpha, self.screen_rect)
		
		