import pygame

from ..utils import GameConfig
from .entity import Entity


class Blasters(Entity):
    def __init__(self, x, y, config: GameConfig):
        image = pygame.transform.scale(config.images.egg, (50, 50))
        super().__init__(config, image, x, y)
        self.hit = False
        self.crashed = False
        self.speed = 7
        self.config.sounds.shoot.play()

    def update(self):
        """Updates sprite image and deletes it if it goes off-screen"""
        self.x += self.speed
        self.rect.x = self.x
        if self.rect.right > self.config.window.width:
            self.kill()

    def draw(self):
        """Draws egg sprite on screen"""
        super().draw()
