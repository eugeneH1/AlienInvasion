class GameStats:

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False
        with open("/Users/eugeneheynike/Desktop/Alien_Invasion/high_score.txt") as file_object:
            self.high_score = file_object.readline()

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        self.bomb = self.settings.bombs_allowed


