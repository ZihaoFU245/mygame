import pygame
from pygame import Vector2
from .Paddle import Paddle
from .Config import Config

class Player(Paddle):
    """Player class with automatic positioning and setup"""

    def __init__(self, side: str, screen_width: int, screen_height: int, 
                 paddle_width: int = None, paddle_height: int = None, 
                 paddle_margin: int = 20, speed: int = None, 
                 color = None, wall_thickness: int = None):
        """Initialize player with automatic positioning
        
        Args:
            side: "left" or "right" - which side of the screen
            screen_width: Width of the game screen
            screen_height: Height of the game screen
            paddle_width: Width of the paddle
            paddle_height: Height of the paddle
            paddle_margin: Distance from screen edge
            speed: Movement speed
            color: Paddle color
            wall_thickness: Thickness of top/bottom walls
        """
        # Use config values as defaults
        paddle_width = paddle_width or Config.PADDLE_WIDTH
        paddle_height = paddle_height or Config.PADDLE_HEIGHT
        speed = speed or Config.PADDLE_MAX_SPEED
        color = color or Config.PADDLE_COLOR
        wall_thickness = wall_thickness or Config.WALL_THICKNESS
        
        # Calculate position based on side
        if side == "left":
            x = paddle_margin
            order = 0  # WASD keys
        elif side == "right":
            x = screen_width - paddle_margin - paddle_width
            order = 1  # Arrow keys
        else:
            raise ValueError("Side must be 'left' or 'right'")
        
        # Center vertically
        y = (screen_height - paddle_height) // 2
        
        # Initialize paddle with physics properties using new signature
        super().__init__(x, y, paddle_width, paddle_height, speed, Config.PADDLE_MASS, color)
        self.order = order
        
        # Set screen bounds automatically
        self.set_screen_bounds(screen_width, screen_height, wall_thickness)

    def keyListen(self, keys: pygame.key.ScancodeWrapper, dt: float):
        """Handle keyboard input for paddle movement with acceleration"""
        direction = Vector2(0, 0)
        
        if self.order == 0:  # Left player - WASD keys
            if keys[pygame.K_w]:
                direction.y = -1
            if keys[pygame.K_s]:
                direction.y = 1
        else:  # Right player - Arrow keys
            if keys[pygame.K_UP]:
                direction.y = -1
            if keys[pygame.K_DOWN]:
                direction.y = 1
        
        # Update paddle with direction (handles acceleration automatically)
        self.update(dt, direction=direction)

        