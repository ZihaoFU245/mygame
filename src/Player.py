import pygame
from pygame import Vector2
from .Paddle import Paddle

class Player(Paddle):
    """Player class with automatic positioning and setup"""

    def __init__(self, side: str, screen_width: int, screen_height: int, 
                 paddle_width: int = 20, paddle_height: int = 100, 
                 paddle_margin: int = 20, speed: int = 400, 
                 color = "black", wall_thickness: int = 20):
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
        
        # Initialize paddle
        super().__init__(x, y, paddle_width, paddle_height, speed, color)
        self.order = order
        
        # Set screen bounds automatically
        self.set_screen_bounds(screen_width, screen_height, wall_thickness)

    def keyListen(self, keys: pygame.key.ScancodeWrapper, dt: float):
        """Handle keyboard input for paddle movement"""
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
        
        # Only update if there's movement
        if direction.length() > 0:
            self.update(dt, direction=direction)

        