import pygame
from typing import Any
from .GameObjectBase import GameObject

class Wall(GameObject):
    """The Wall that on top and bottom of the game."""

    def __init__(self, x: float, y: float, width: float, height: float, color: Any = "black"):
        super().__init__(x, y, width, height)
        self.color = color
        
    def update(self, dt: float, direction: pygame.Vector2 = None):
        """Update of the Wall - walls are static so nothing to update"""
        pass

    def draw(self, screen: pygame.Surface):
        """Draw the wall"""
        pygame.draw.rect(screen, self.color, self.get_rect())

    def collide(self, other: 'GameObject'):
        """Handle collision - walls are static, collision response is handled by the other object"""
        # Wall collision is typically handled by the colliding object (like ball)
        # This could return collision info if needed
        return self.get_rect().colliderect(other.get_rect()) 