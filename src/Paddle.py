import pygame
from typing import Any, Tuple
from .GameObjectBase import GameObject

class Paddle(GameObject):
    """Paddle object for Pong game"""

    def __init__(self, x: float, y: float, width: float, height: float, 
                 speed: float = 400.0, color: Any = "black"):
        super().__init__(x, y, width, height)
        self.color = color
        self.speed = speed  # Pixels per second
        self.screen_bounds: Tuple[int, int] = (0, 0)  # Will be set by game

    def set_screen_bounds(self, width: int, height: int, wall_thickness: int = 20):
        """Set screen boundaries for paddle movement"""
        self.screen_bounds = (wall_thickness, height - wall_thickness)

    def update(self, dt: float, **kwargs):
        """Update the paddle position based on input
        
        Args:
            dt: Delta time in seconds
            direction: Optional pygame.Vector2 for movement direction
            keys: Optional pygame key state for input handling
        """
        direction = kwargs.get('direction')
        if direction:
            # Move paddle based on direction and speed
            self.velocity = direction * self.speed
            self.move(dt)
            self._clamp_to_screen()

    def _clamp_to_screen(self):
        """Keep paddle within screen boundaries"""
        if self.screen_bounds != (0, 0):
            min_y, max_y = self.screen_bounds
            self.position.y = max(min_y, min(self.position.y, max_y - self.height))

    def draw(self, screen: pygame.Surface):
        """Draw the paddle at current position"""
        pygame.draw.rect(screen, self.color, self.get_rect())

    def collide(self, other: 'GameObject') -> bool:
        """Check collision with other game object"""
        return self.get_rect().colliderect(other.get_rect())