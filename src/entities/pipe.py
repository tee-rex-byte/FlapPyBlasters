import random
import pygame.time
from typing import List

from ..utils import GameConfig
from .entity import Entity
from .groups import blasters_group
from .score import Score


class Pipe(Entity):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.vel_x = -5

    def draw(self) -> None:
        self.x += self.vel_x
        super().draw()


class Pipes(Entity):
    upper: List[Pipe]
    lower: List[Pipe]

    def __init__(self, config: GameConfig, score: Score) -> None:
        super().__init__(config)
        self.score = score
        self.last_explosion_time = 0
        self.explosion_cooldown = 500
        self.pipe_gap = 120
        self.top = 0
        self.bottom = self.config.window.viewport_height
        self.upper = []
        self.lower = []
        self.spawn_initial_pipes()

    def tick(self) -> None:
        if self.can_spawn_pipes():
            self.spawn_new_pipes()

        self.remove_old_pipes()

        pipes_to_remove = []
        current_time = pygame.time.get_ticks()

        for up_pipe, low_pipe in zip(self.upper, self.lower):
            up_pipe.tick()
            low_pipe.tick()

            # Handles pipe and blaster collision
            for blaster in blasters_group.sprites():
                if up_pipe.collide(blaster) or low_pipe.collide(blaster):
                    if (
                        current_time - self.last_explosion_time
                        >= self.explosion_cooldown
                    ):
                        self.last_explosion_time = current_time
                        self.config.sounds.explosion.play()
                        pipes_to_remove.append((up_pipe, low_pipe))

                        # Remove Blaster
                        blasters_group.remove(blaster)

                        # Increment Score
                        self.score.add()

        # Remove Pipes AFTER iteration
        self.upper = [
            pipe
            for pipe in self.upper
            if (pipe not in [p[0] for p in pipes_to_remove])
        ]
        self.lower = [
            pipe
            for pipe in self.lower
            if (pipe not in [p[1] for p in pipes_to_remove])
        ]

    def stop(self) -> None:
        for pipe in self.upper + self.lower:
            pipe.vel_x = 0

    def can_spawn_pipes(self) -> bool:
        if not self.upper:
            return True
        last = self.upper[-1]

        return self.config.window.width - (last.x + last.w) > last.w * 2.5

    def spawn_new_pipes(self):
        # add new pipe when first pipe is about to touch left of screen
        if not self.upper or self.can_spawn_pipes():
            upper, lower = self.make_random_pipes()
            if self.upper:
                last_upper_pipe = self.upper[-1]
                if upper.x - last_upper_pipe.x < last_upper_pipe.w * 3.5:
                    # Adjust spawn difference
                    upper.x = last_upper_pipe.x + last_upper_pipe.w * 3.5
                    lower.x = last_upper_pipe.x + last_upper_pipe.w * 3.5
            self.upper.append(upper)
            self.lower.append(lower)

    def remove_old_pipes(self):
        # remove first pipe if it's out of the screen
        self.upper = [pipe for pipe in self.upper if pipe.x >= -pipe.w]
        self.lower = [pipe for pipe in self.lower if pipe.x >= -pipe.w]

    def spawn_initial_pipes(self):
        upper_1, lower_1 = self.make_random_pipes()
        upper_1.x = self.config.window.width + upper_1.w * 3
        lower_1.x = self.config.window.width + upper_1.w * 3
        self.upper.append(upper_1)
        self.lower.append(lower_1)

        upper_2, lower_2 = self.make_random_pipes()
        upper_2.x = upper_1.x + upper_1.w * 3.5
        lower_2.x = upper_1.x + upper_1.w * 3.5
        self.upper.append(upper_2)
        self.lower.append(lower_2)

    def make_random_pipes(self):
        """returns a randomly generated pipe"""
        # y of gap between upper and lower pipe
        base_y = self.config.window.viewport_height

        gap_y = random.randrange(0, int(base_y * 0.6 - self.pipe_gap))
        gap_y += int(base_y * 0.2)
        pipe_height = self.config.images.pipe[0].get_height()
        pipe_x = self.config.window.width + 10

        upper_pipe = Pipe(
            self.config,
            self.config.images.pipe[0],
            pipe_x,
            gap_y - pipe_height,
        )

        lower_pipe = Pipe(
            self.config,
            self.config.images.pipe[1],
            pipe_x,
            gap_y + self.pipe_gap,
        )

        return upper_pipe, lower_pipe
