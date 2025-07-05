import pygame
import math
from typing import Any, Tuple
from .GameObjectBase import GameObject

class Paddle(GameObject):
    """Paddle object for Pong game with physics"""

    def __init__(self, x: float, y: float, width: float, height: float, 
                 speed: float = 400.0, mass: float = 5.0, color: Any = "black"):
        super().__init__(x, y, width, height, mass)
        self.color = color
        self.max_speed = speed  # Maximum speed
        self.acceleration = 800.0  # Pixels per second squared
        self.deceleration = 600.0  # Deceleration when no input
        self.screen_bounds: Tuple[int, int] = (0, 0)
        self.friction_coefficient = 0.3  # Friction that affects ball spin
        self.is_moving = False

    def set_screen_bounds(self, width: int, height: int, wall_thickness: int = 20):
        """Set screen boundaries for paddle movement"""
        self.screen_bounds = (wall_thickness, height - wall_thickness)

    def update(self, dt: float, **kwargs):
        """Update the paddle with acceleration physics
        
        Args:
            dt: Delta time in seconds
            direction: Optional pygame.Vector2 for movement direction
        """
        direction = kwargs.get('direction')
        
        if direction and direction.length() > 0:
            # Apply acceleration in the direction of input
            acceleration_force = direction.normalize() * self.acceleration
            self.apply_force(acceleration_force * self.mass, dt)
            self.is_moving = True
        else:
            # Apply deceleration when no input
            if self.velocity.length() > 0:
                decel_direction = -self.velocity.normalize()
                decel_force = decel_direction * self.deceleration * self.mass
                self.apply_force(decel_force, dt)
                
                # Stop if velocity is very small
                if self.velocity.length() < 10:
                    self.velocity = pygame.Vector2(0, 0)
            self.is_moving = False
        
        # Limit to maximum speed
        if self.velocity.length() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed
        
        # Move and clamp to screen
        self.move(dt)
        self._clamp_to_screen()

    def _clamp_to_screen(self):
        """Keep paddle within screen boundaries"""
        if self.screen_bounds != (0, 0):
            min_y, max_y = self.screen_bounds
            old_y = self.position.y
            self.position.y = max(min_y, min(self.position.y, max_y - self.height))
            
            # Stop velocity if hitting boundary
            if self.position.y != old_y:
                self.velocity.y = 0

    def get_impact_spin(self, ball_contact_point_y: float) -> float:
        """Calculate spin to apply to ball based on paddle movement and contact point
        
        Args:
            ball_contact_point_y: Y position where ball contacts paddle
            
        Returns:
            Angular velocity to apply to ball (radians/second)
        """
        # Get relative contact point (-1 to 1, where 0 is center)
        paddle_center_y = self.position.y + self.height / 2
        relative_contact = (ball_contact_point_y - paddle_center_y) / (self.height / 2)
        relative_contact = max(-1, min(1, relative_contact))
        
        # Calculate spin based on paddle velocity and friction
        paddle_velocity_factor = self.velocity.y / self.max_speed  # -1 to 1
        
        # Combine contact point and paddle movement for spin
        spin_intensity = (relative_contact * 0.7 + paddle_velocity_factor * 0.3)
        max_spin = 15.0  # Maximum radians per second
        
        return spin_intensity * max_spin * self.friction_coefficient

    def draw(self, screen: pygame.Surface):
        """Draw the paddle at current position"""
        pygame.draw.rect(screen, self.color, self.get_rect())

    def collide(self, other: 'GameObject') -> bool:
        """Check collision with other game object"""
        return self.get_rect().colliderect(other.get_rect())