import pygame

from ..utils import GameConfig, clamp
from .entity import Entity
from .floor import Floor
from .pipe import Pipe, Pipes

blasters_group = pygame.sprite.Group()

class Blasters(pygame.sprite.Sprite):
    def __init__(self, x, y, config: GameConfig):
        self.group = blasters_group
        pygame.sprite.Sprite.__init__(self, blasters_group)
        self.config = config
        self.speed = 12
        image = config.images.egg
        self.image = pygame.transform.scale(image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.config.sounds.shoot.play()

    def update(self):
        self.rect.x += self.speed
        if self.rect.right > self.config.window.width:
            self.kill()

    #draws egg sprite
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)