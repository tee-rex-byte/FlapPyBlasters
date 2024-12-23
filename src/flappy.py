import asyncio

import pygame


from .entities import (
    Background,
    Floor,
    GameOver,
    Pipes,
    Player,
    PlayerMode,
    Score,
    WelcomeMessage,
)
from src.utils import GameConfig, Images, Sounds, Window
from src.entities.groups import blasters_group, ammo_cache_group
from src.entities.ammo_cache import AmmoCache
from src.entities.event_handler import EventHandler


class Flappy:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Flappy Bird Blasters")
        window = Window(288, 512)
        self.screen = pygame.display.set_mode((window.width, window.height))
        images = Images()

        self.config = GameConfig(
            screen=self.screen,
            clock=pygame.time.Clock(),
            fps=30,
            window=window,
            images=images,
            sounds=Sounds(),
        )

        self.background = Background(self.config)
        self.floor = Floor(self.config)
        self.player = Player(self.config)
        self.welcome_message = WelcomeMessage(self.config)
        self.game_over_message = GameOver(self.config)
        self.score = Score(self.config)
        self.pipes = Pipes(self.config, self.score)
        self.blasters_group = blasters_group
        self.ammo_cache_group = ammo_cache_group

    async def start(self):
        while True:
            self.player = Player(self.config)
            self.pipes = Pipes(self.config, self.score)
            await self.splash()
            await self.play()
            await self.game_over()

    async def splash(self):
        """Shows welcome splash screen animation of flappy bird"""

        self.player.set_mode(PlayerMode.SHM)

        while True:
            for event in pygame.event.get():
                EventHandler.check_quit_event(event)
                if EventHandler.is_tap_event(event):
                    return

            self.background.tick()
            self.floor.tick()
            self.player.tick()
            self.welcome_message.tick()

            # update and draw groups
            self.update_draw_groups()

            pygame.display.update()
            await asyncio.sleep(0)
            self.config.tick()

    def update_draw_groups(self):
        self.blasters_group.update()
        self.blasters_group.draw(self.screen)
        self.ammo_cache_group.update()
        self.ammo_cache_group.draw(self.screen)

    async def play(self):
        self.player.ammo = 5
        self.score.reset()
        self.blasters_group.empty()
        self.ammo_cache_group.empty()
        self.player.set_mode(PlayerMode.NORMAL)

        ammo_cache = AmmoCache(self.config, self.player)

        while True:
            if self.player.collided(self.pipes, self.floor):
                return

            # Spawn Ammo if you can
            ammo_cache.maybe_spawn_ammo()

            for cache in self.ammo_cache_group:
                cache.check_collision()

            for i, pipe in enumerate(self.pipes.upper):
                if self.player.crossed(pipe):
                    self.score.add()

            for event in pygame.event.get():
                EventHandler.check_quit_event(event)
                if EventHandler.is_tap_event(event):
                    self.player.flap()
                if EventHandler.is_blast_event(event):
                    self.player.blast()

            self.background.tick()
            self.floor.tick()
            self.pipes.tick()
            self.score.tick()
            self.player.tick()

            # update and draw groups
            self.update_draw_groups()

            pygame.display.update()
            await asyncio.sleep(0)
            self.config.tick()

    async def game_over(self):
        """crashes the player down and shows game over image"""

        self.player.set_mode(PlayerMode.CRASH)
        self.pipes.stop()
        self.floor.stop()

        while True:
            for event in pygame.event.get():
                EventHandler.check_quit_event(event)
                if EventHandler.is_tap_event(event):
                    if self.player.y + self.player.h >= self.floor.y - 1:
                        return

            self.background.tick()
            self.floor.tick()
            self.pipes.tick()
            self.score.tick()
            self.player.tick()
            self.blasters_group.empty()
            self.ammo_cache_group.empty()

            self.game_over_message.tick()

            self.config.tick()
            pygame.display.update()
            await asyncio.sleep(0)
