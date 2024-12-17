import sys

import pygame


class Sounds:
    collect: pygame.mixer.Sound
    die: pygame.mixer.Sound
    empty: pygame.mixer.Sound
    explosion: pygame.mixer.Sound
    hit: pygame.mixer.Sound
    point: pygame.mixer.Sound
    shoot: pygame.mixer.Sound
    swoosh: pygame.mixer.Sound
    wing: pygame.mixer.Sound

    def __init__(self) -> None:
        if "win" in sys.platform:
            ext = "wav"
        else:
            ext = "ogg"

        self.collect = pygame.mixer.Sound(f"assets/audio/collect.{ext}")
        self.die = pygame.mixer.Sound(f"assets/audio/die.{ext}")
        self.empty = pygame.mixer.Sound(f"assets/audio/empty.{ext}")
        self.explosion = pygame.mixer.Sound(f"assets/audio/explosion.{ext}")
        self.hit = pygame.mixer.Sound(f"assets/audio/hit.{ext}")
        self.point = pygame.mixer.Sound(f"assets/audio/point.{ext}")
        self.shoot = pygame.mixer.Sound(f"assets/audio/shoot.{ext}")
        self.swoosh = pygame.mixer.Sound(f"assets/audio/swoosh.{ext}")
        self.wing = pygame.mixer.Sound(f"assets/audio/wing.{ext}")

