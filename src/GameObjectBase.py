import pygame
from abc import ABC, abstractmethod

class GameObject(ABC):
    def __init__(self, x: float, y: float, width: float, height: float, mass: float = 1.0):
        """Initialize game object with position, size, and physics properties"""
        self.position = pygame.Vector2(x, y)
        self.width = width
        self.height = height
        self.velocity = pygame.Vector2(0.0, 0.0)
        self.mass = mass
        self.angular_velocity = 0.0  # Radians per second
        self.friction_coefficient = 0.0  # Default no friction

    @abstractmethod
    def update(self, dt: float, **kwargs):
        """Update Game Object
        
        Args:
            dt: Delta time in seconds
            **kwargs: Additional parameters specific to each object type
        """
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface):
        """Draw the game object
        
        Args:
            screen: The pygame surface to draw on
        """
        pass

    def get_rect(self) -> pygame.Rect:
        """Return the pygame collision rect object"""
        return pygame.Rect(self.position.x, self.position.y, self.width, self.height)

    @abstractmethod
    def collide(self, other: 'GameObject'):
        """Handle collision with other game objects
        
        Args:
            other: The other game object that collided with this one
        """
        pass

    def move(self, dt: float):
        """Basic movement based on velocity"""
        self.position += self.velocity * dt

    def apply_force(self, force: pygame.Vector2, dt: float):
        """Apply force to object (F = ma, so acceleration = F/m)"""
        acceleration = force / self.mass
        self.velocity += acceleration * dt


