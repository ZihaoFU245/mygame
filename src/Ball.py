import pygame
import random
import math
from .GameObjectBase import GameObject
from .Config import Config

class Ball(GameObject):
    """Pong Ball Object with advanced physics"""
    
    def __init__(self, x: float, y: float, size: float = None, 
                 speed: float = None, mass: float = None, color: str = None):
        # Use config values as defaults
        size = size or Config.BALL_SIZE
        speed = speed or Config.BALL_BASE_SPEED
        mass = mass or Config.BALL_MASS
        color = color or Config.BALL_COLOR
        
        # Ball is square for collision, but we'll draw it as a circle
        super().__init__(x, y, size, size, mass)
        self.radius = size // 2  # Now both are ints, so this works correctly
        self.base_speed = speed  # Store original speed for resets
        self.speed = speed
        self.color = color
        self.initial_position = pygame.Vector2(x, y)
        self.max_bounce_angle = Config.BALL_MAX_BOUNCE_ANGLE
        
        # Advanced physics properties from config
        self.air_friction = Config.AIR_FRICTION
        self.angular_friction = Config.ANGULAR_FRICTION
        self.magnus_effect_strength = Config.MAGNUS_EFFECT_STRENGTH
        self.rotation_angle = 0.0  # Visual rotation for drawing
        
        # Initialize with random direction
        self.reset_ball()
    
    def reset_ball(self):
        """Reset ball to center with random direction and no spin"""
        self.position = self.initial_position.copy()
        self.angular_velocity = 0.0
        self.rotation_angle = 0.0
        
        # Reset speed to original base speed - this is critical!
        self.speed = self.base_speed
        
        # Random direction (left or right)
        direction = random.choice([-1, 1])
        angle = random.uniform(-30, 30)  # Random angle between -30 and 30 degrees
        angle_rad = math.radians(angle)
        
        self.velocity.x = direction * self.speed * math.cos(angle_rad)
        self.velocity.y = self.speed * math.sin(angle_rad)
    
    def update(self, dt: float, **kwargs):
        """Update ball position with advanced physics
        
        Returns:
            bool: True if ball hit a wall, False otherwise
        """
        # Apply Magnus effect (spin affects trajectory)
        self._apply_magnus_effect(dt)
        
        # Apply air friction
        self._apply_air_friction(dt)
        
        # Update angular properties
        self._update_angular_properties(dt)
        
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
            # Reverse some of the spin when hitting walls
            self.angular_velocity *= -Config.WALL_SPIN_REDUCTION
            wall_hit = True
            # Keep ball within bounds
            if self.position.y <= wall_thickness:
                self.position.y = wall_thickness
            else:
                self.position.y = screen_height - wall_thickness - self.height
        
        return wall_hit
    
    def _apply_magnus_effect(self, dt: float):
        """Apply Magnus effect - spin creates a perpendicular force"""
        if abs(self.angular_velocity) > Config.MAGNUS_MIN_SPIN_THRESHOLD:  # Only apply if there's significant spin
            # Magnus force is perpendicular to velocity direction
            if self.velocity.length() > 0:
                # Get perpendicular direction (90 degrees to velocity)
                velocity_normalized = self.velocity.normalize()
                perpendicular = pygame.Vector2(-velocity_normalized.y, velocity_normalized.x)
                
                # Magnus force magnitude based on spin and speed
                magnus_force_magnitude = (self.angular_velocity * self.velocity.length() * 
                                        self.magnus_effect_strength / self.mass)
                
                # Apply Magnus force
                magnus_force = perpendicular * magnus_force_magnitude
                self.apply_force(magnus_force, dt)
    
    def _apply_air_friction(self, dt: float):
        """Apply air friction to slow down the ball"""
        friction_factor = self.air_friction ** dt
        self.velocity *= friction_factor
    
    def _update_angular_properties(self, dt: float):
        """Update angular velocity and rotation angle"""
        # Apply angular friction
        self.angular_velocity *= self.angular_friction ** dt
        
        # Update visual rotation
        self.rotation_angle += self.angular_velocity * dt
        
        # Keep rotation angle in reasonable range
        if self.rotation_angle > 2 * math.pi:
            self.rotation_angle -= 2 * math.pi
        elif self.rotation_angle < -2 * math.pi:
            self.rotation_angle += 2 * math.pi

    def draw(self, screen: pygame.Surface):
        """Draw the ball as a circle with rotation indicator"""
        center_x = int(self.position.x + self.radius)
        center_y = int(self.position.y + self.radius)
        
        # Draw main ball
        pygame.draw.circle(screen, self.color, (center_x, center_y), self.radius)
        
        # Draw a small indicator to show rotation
        if abs(self.angular_velocity) > Config.SPIN_INDICATOR_MIN_THRESHOLD:  # Only show if spinning significantly
            indicator_length = self.radius * 0.6
            end_x = center_x + indicator_length * math.cos(self.rotation_angle)
            end_y = center_y + indicator_length * math.sin(self.rotation_angle)
            pygame.draw.line(screen, (255, 255, 255), (center_x, center_y), 
                           (int(end_x), int(end_y)), 2)
    
    def collide(self, other: 'GameObject') -> bool:
        """Handle collision with other game objects (mainly paddles)"""
        if not self.get_rect().colliderect(other.get_rect()):
            return False
        
        # This is a paddle collision
        self._handle_paddle_collision(other)
        return True
    
    def _handle_paddle_collision(self, paddle):
        """Handle collision with paddle - realistic Pong physics with spin"""
        # Get collision point relative to paddle center
        paddle_center_y = paddle.position.y + paddle.height / 2
        ball_center_y = self.position.y + self.radius
        
        # Calculate relative intersection (-1 to 1, where 0 is center)
        relative_intersect_y = (ball_center_y - paddle_center_y) / (paddle.height / 2)
        relative_intersect_y = max(-1, min(1, relative_intersect_y))
        
        # Calculate bounce angle (max 75 degrees)
        bounce_angle = relative_intersect_y * math.radians(self.max_bounce_angle)
        
        # Determine direction based on which paddle was hit
        direction = 1 if self.velocity.x < 0 else -1  # Reverse horizontal direction
        
        # Set new velocity
        self.velocity.x = direction * self.speed * math.cos(bounce_angle)
        self.velocity.y = self.speed * math.sin(bounce_angle)
        
        # Apply spin from paddle if it has the method (advanced paddles)
        if hasattr(paddle, 'get_impact_spin'):
            spin_to_add = paddle.get_impact_spin(ball_center_y)
            self.angular_velocity += spin_to_add
            
            # Limit maximum spin
            self.angular_velocity = max(-Config.MAX_BALL_SPIN, min(Config.MAX_BALL_SPIN, self.angular_velocity))
        
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
        """Increase ball speed (for progressive difficulty)
        Only affects current velocity, not the base speed that's used for resets"""
        self.velocity *= factor
        # Update current speed for collision calculations, but don't modify base_speed
        self.speed = self.velocity.length() if self.velocity.length() > 0 else self.base_speed