import pygame
from pygame.sprite import Sprite


class Bomb(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Create a bomb rect at the top of the ship
        self.image = pygame.image.load("/Users/eugeneheynike/Desktop/Alien_Invasion/Bomb.png")
        self.rect = self.image.get_rect()
        self.rect.midtop = ai_game.ship.rect.midtop
        self.exists = True

        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)

    def update(self):
        """Move the bomb to the top of the screen"""
        self.y -= self.settings.bullet_speed
        # Update the rect position
        self.rect.y = self.y
