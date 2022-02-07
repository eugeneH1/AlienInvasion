import pygame
from pygame.sprite import Sprite


class Miniship(Sprite):
    """A class to manage the ship."""
    def __init__(self, ai_game):
        super().__init__()
        """Initialize the ship and set its starting position."""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        # Load the ship image and get its rect.
        self.image = pygame.image.load("/Users/eugeneheynike/Desktop/Alien_Invasion/MiniRocket.png")
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
