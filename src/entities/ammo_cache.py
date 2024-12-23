import pygame
import pygame.time

from ..utils import GameConfig
from .entity import Entity
from .groups import ammo_cache_group


class AmmoCache(Entity):
    def __init__(self, config: GameConfig, player) -> None:
        # Initialize the parent class
        super().__init__(
            config,
            image=config.images.egg_cache.convert_alpha(),
            x=config.window.width,  # Start off-screen on the right
            y=(config.window.height - config.images.egg_cache.get_height())
            // 2,  # Center vertically
        )
        self.player = player
        self.last_ammo_time = 0
        self.ammo_spawn_interval = 3000
        self.speed = 5

    def maybe_spawn_ammo(self):
        """Spawns ammo if the player has less than 5 ammo and the cooldown has passed."""

        current_time = pygame.time.get_ticks()
        if self.player.ammo < 5:
            if current_time - self.last_ammo_time > self.ammo_spawn_interval:
                self.last_ammo_time = current_time
                new_ammo = AmmoCache(self.config, self.player)
                ammo_cache_group.add(new_ammo)

    def check_collision(self):
        """Check collision with the player."""
        if self.collide(self.player):
            self.player.ammo += 1
            self.config.sounds.collect.play()
            ammo_cache_group.empty()

    def update(self):
        """Updates sprite image and deletes it if it goes off-screen"""

        self.x -= self.speed
        self.rect.x = self.x
        if self.rect.right < 0:
            self.kill()
