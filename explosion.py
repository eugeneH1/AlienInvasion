import pygame
from pygame.sprite import Sprite


class Explosion(Sprite):
    def __init__(self, ai_game, rect_x, rect_y, bomb_size):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.bomb_size = bomb_size
        # Create a bomb rect at the top of the ship
        self.images = []
        for num in range(1, self.bomb_size):
            img = pygame.image.load(f"/Users/eugeneheynike/Desktop/Alien_Invasion/Explosion{num}.png")
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.collision_rect = (rect_x, rect_y)
        self.rect.center = self.collision_rect
        self.counter = 0

    def update(self):
        explosion_speed = 15
        self.counter += 1
        if self.counter >= explosion_speed and self.index <= len(self.images) - 1:
            self.counter = 0
            if self.index < self.bomb_size:
                self.index += 1
            print(self.bomb_size)
            print(f" index: {self.index}")
            self.image = self.images[self.index]
            #self.rect = self.image.get_rect()
            self.rect.y -= 100
            self.rect.x -= 100

        if self.index >= self.bomb_size:
            self.kill()
