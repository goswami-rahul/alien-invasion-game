class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game settings."""
        # Screen settings
        self.screen_width = 1360
        self.screen_height = 768
        self.bg_color = (10, 5, 50)

        # Ship settings
        self.ship_size = (100, 80)
        self.ship_speed_factor = 2
        self.ship_left = 3

        # Bullet settings.
        self.bullet_speed_factor = 3.5
        self.bullet_width = 4
        self.bullet_height = 20
        self.bullet_color = (255, 255, 255)
        self.bullets_allowed = 5   # bullets allowed in the same time on screen

        # Alien settings.
        self.alien_size = (80, 50)
        self.alien_drop_dist = 10
        self.alien_ship_dist_factor = 5

        # Score card settings.
        self.score_ship_size = (50, 40)
        self.score_font_size = 35
        self.score_font_color = (255, 255, 255)

        # Initialize dynamic settings.
        self.initialize_dynamic_settings()

        # Randomize alien fleet.
        self.alien_random_x = 0
        self.alien_random_y = 0

        # How quickly game speeds up.
        self.speedup_scale = 1.2
        self.score_scale = 1.5

    def initialize_dynamic_settings(self):
        """Initialize settings that change during the game."""

        self.set_default_alien_directions()
        self.ship_speed_factor = 400
        self.bullet_speed_factor = 800
        self.alien_speed_factor_x = 250
        self.alien_speed_factor_y = 100
        self.alien_density_factor_x = 3
        self.alien_density_factor_y = 3

        # Points gained by shooting alien.
        self.alien_points = 50
        self.ship_left = 2

    def set_default_alien_directions(self):
        """Set alien's direction to right."""

        # Settings not to be changed.
        self.alien_direction_x = 1
        self.alien_direction_y = 0

    def increase_speed(self):
        """Increase the tempo of the game."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor_x *= self.speedup_scale
        self.alien_speed_factor_y *= self.speedup_scale

        self.alien_density_factor_x = 1 + (self.alien_density_factor_x - 1) / self.speedup_scale
        self.alien_density_factor_y = 1 + (self.alien_density_factor_y - 1) / self.speedup_scale

        # Increase alien points.
        self.alien_points = int(self.alien_points * self.score_scale)
