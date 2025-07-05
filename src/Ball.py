import pygame
import random
import math
from .GameObjectBase import GameObject

class Ball(GameObject):
    """Pong Ball Object"""
    
    def __init__(self, x: float, y: float, size: float = 15, 
                 speed: float = 300, color: str = "black"):
        # Ball is square for simplicity, but we'll draw it as a circle
        super().__init__(x, y, size, size)
        self.radius = size // 2
        self.speed = speed
        self.color = color
        self.initial_position = pygame.Vector2(x, y)
        self.max_bounce_angle = 75  # Maximum angle in degrees for paddle bounces
        
        # Initialize with random direction
        self.reset_ball()
    
    def reset_ball(self):
        """Reset ball to center with random direction"""
        self.position = self.initial_position.copy()
        
        # Random direction (left or right)
        direction = random.choice([-1, 1])
        angle = random.uniform(-30, 30)  # Random angle between -30 and 30 degrees
        angle_rad = math.radians(angle)
        
        self.velocity.x = direction * self.speed * math.cos(angle_rad)
        self.velocity.y = self.speed * math.sin(angle_rad)
    
    def update(self, dt: float, **kwargs):
        """Update ball position and handle wall collisions
        
        Returns:
            bool: True if ball hit a wall, False otherwise
        """
        # Move the ball
        self.move(dt)
        
        # Get screen dimensions and walls from kwargs
        screen_height = kwargs.get('screen_height', 720)
        wall_thickness = kwargs.get('wall_thickness', 20)
        
        # Check for wall collisions
        wall_hit = False
        
        # Bounce off top and bottom walls
        if self.position.y <= wall_thickness or self.position.y + self.height >= screen_height - wall_thickness:
            self.velocity.y *= -1
            wall_hit = True
            # Keep ball within bounds
            if self.position.y <= wall_thickness:
                self.position.y = wall_thickness
            else:
                self.position.y = screen_height - wall_thickness - self.height
        
        return wall_hit
    
    def draw(self, screen: pygame.Surface):
        """Draw the ball as a circle"""
        center_x = int(self.position.x + self.radius)
        center_y = int(self.position.y + self.radius)
        pygame.draw.circle(screen, self.color, (center_x, center_y), self.radius)
    
    def collide(self, other: 'GameObject') -> bool:
        """Handle collision with other game objects (mainly paddles)"""
        if not self.get_rect().colliderect(other.get_rect()):
            return False
        
        # This is a paddle collision
        self._handle_paddle_collision(other)
        return True
    
    def _handle_paddle_collision(self, paddle):
        """Handle collision with paddle - realistic Pong physics"""
        # Get collision point relative to paddle center
        paddle_center_y = paddle.position.y + paddle.height / 2
        ball_center_y = self.position.y + self.radius
        
        # Calculate relative intersection (-1 to 1, where 0 is center)
        relative_intersect_y = (ball_center_y - paddle_center_y) / (paddle.height / 2)
        
        # Clamp to prevent extreme angles
        relative_intersect_y = max(-1, min(1, relative_intersect_y))
        
        # Calculate bounce angle (max 75 degrees)
        bounce_angle = relative_intersect_y * math.radians(self.max_bounce_angle)
        
        # Determine direction based on which paddle was hit
        direction = 1 if self.velocity.x < 0 else -1  # Reverse horizontal direction
        
        # Set new velocity
        self.velocity.x = direction * self.speed * math.cos(bounce_angle)
        self.velocity.y = self.speed * math.sin(bounce_angle)
        
        # Move ball away from paddle to prevent sticking
        if direction > 0:  # Hit left paddle, move right
            self.position.x = paddle.position.x + paddle.width + 1
        else:  # Hit right paddle, move left
            self.position.x = paddle.position.x - self.width - 1
    
    def is_off_screen(self, screen_width: int) -> str:
        """Check if ball is off screen and return which side"""
        if self.position.x + self.width < 0:
            return "left"
        elif self.position.x > screen_width:
            return "right"
        return ""
    
    def increase_speed(self, factor: float = 1.05):
        """Increase ball speed (for progressive difficulty)"""
        self.velocity *= factor