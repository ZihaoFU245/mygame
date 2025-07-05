import pygame
from pygame import Vector2
from .Paddle import Paddle

class Player(Paddle):
    """Player class"""

    def __init__(self, x, y, width, height, speed = 400, color = "black", order: int = 0):
        super().__init__(x, y, width, height, speed, color)
        self.order = order  # Two player could use arrow keys and wasd keys

    # Inherite from Paddle and add key board listener
    def keyListen(self, keys: pygame.key.ScancodeWrapper, dt: float):
        """Wrap Paddle class with keyboard listening"""
        if (self.order == 0):
            # WASD keys
            if keys[pygame.K_w]:
                d = Vector2(0, -1)
                self.update(dt, direction=d)
            if keys[pygame.K_s]:
                d = Vector2(0, 1)
                self.update(dt, direction=d)
        else:
            # Arrow keys
            if keys[pygame.K_UP]:
                d = Vector2(0, -1)
                self.update(dt, direction=d)
            if keys[pygame.K_DOWN]:
                d = Vector2(0, 1)
                self.update(dt, direction=d)

        