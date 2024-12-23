import sys
import pygame
from pygame.locals import K_ESCAPE, K_SPACE, K_UP, K_b, KEYDOWN, QUIT

class EventHandler:
    def __init__(self):
        super().__init__()

    @staticmethod
    def check_quit_event(event):
        """Handles quit events"""
        if event.type == QUIT or (
                event.type == KEYDOWN and event.key == K_ESCAPE
        ):
            pygame.quit()
            sys.exit()

    @staticmethod
    def is_tap_event(event):
        """Checks if event is tap event"""
        m_left, _, _ = pygame.mouse.get_pressed()
        space_or_up = event.type == KEYDOWN and (
                event.key == K_SPACE or event.key == K_UP
        )
        screen_tap = event.type == pygame.FINGERDOWN
        return m_left or space_or_up or screen_tap

    @staticmethod
    def is_blast_event(event):
        """Checks if the event is a blast event"""
        return event.type == KEYDOWN and event.key == K_b