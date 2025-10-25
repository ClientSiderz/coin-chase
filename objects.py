import pygame, random
from settings import COIN_IMG, BOMB_IMG, SCREEN

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = COIN_IMG
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = random.randint(2, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN.get_height():
            self.kill()

class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = BOMB_IMG
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = random.randint(2, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN.get_height():
            self.kill()

ALL_COINS = pygame.sprite.Group()
ALL_BOMBS = pygame.sprite.Group()
