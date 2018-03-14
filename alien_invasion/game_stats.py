import os.path

from settings import Settings


class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_settings: Settings):

        self.ai_settings = ai_settings
        self.ships_left = self.ai_settings.ship_left
        self.score = 0
        self.level = 1
        self.time_to_blit = None
        self.broke_highscore = False
        self.game_active = False

        filename = os.path.join('.', 'save/highscore.txt')
        try:
            with open(filename, 'r') as f:
                self.prev_high_score = int(f.read())
        except FileNotFoundError:
            print('no save file found.')
            self.prev_high_score = 0

        self.high_score = self.prev_high_score
        self.time_passed = 0.0

    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_left
        self.score = 0
        self.level = 1
        self.time_to_blit = None
        self.broke_highscore = False
