import pygame


class Button:
    """Represents a button on the screen."""

    def __init__(self, screen: pygame.SurfaceType, msg: str, size=48, b_color=(-1, -1, -1)):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Properties of button.
        self.button_transparency = 80
        self.button_color = (0, 255, 0) if b_color == (-1, -1, -1) else b_color
        if len(self.button_color) == 3:
            self.button_color += (self.button_transparency, )      # add alpha channel
        self.text_color = (255, 255, 255)

        self.font = pygame.font.Font('fonts/RussoOne.ttf', size)

        self.prep_msg(msg)

        button_width = self.msg_image_rect.width + 30
        button_height = self.msg_image_rect.height + 10

        self.rect = pygame.Rect(0, 0, button_width, button_height)
        self.rect.center = self.msg_image_rect.center

    def prep_msg(self, msg: str):
        """Prepare button text into rendered image and position it at button center."""
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.screen_rect.center

    def draw_button(self):
        """Draw button with msg."""
        screen_alpha = self.screen.convert_alpha(self.screen)
        screen_alpha.fill(self.button_color, self.rect)
        screen_alpha.blit(self.msg_image, self.msg_image_rect)
        self.screen.blit(screen_alpha, self.screen_rect)
