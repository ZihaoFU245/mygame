import pygame
from pygame import Vector2
from .Paddle import Paddle
from .Config import Config

class Bot(Paddle):
    """AI Bot class for Pong with configurable difficulty"""

    def __init__(self, side: str, screen_width: int, screen_height: int,
                 difficulty: str = "Medium", paddle_width: int = None, 
                 paddle_height: int = None, paddle_margin: int = 20, 
                 speed: int = None, color = None, wall_thickness: int = None):
        """Initialize bot with automatic positioning and AI settings
        
        Args:
            side: "left" or "right" - which side of the screen
            screen_width: Width of the game screen
            screen_height: Height of the game screen
            difficulty: "Easy", "Medium", or "Hard" - affects AI behavior
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
        elif side == "right":
            x = screen_width - paddle_margin - paddle_width
        else:
            raise ValueError("Side must be 'left' or 'right'")
        
        # Center vertically
        y = (screen_height - paddle_height) // 2
        
        # Initialize paddle with physics properties
        super().__init__(x, y, paddle_width, paddle_height, speed, Config.PADDLE_MASS, color)
        
        # Set screen bounds automatically
        self.set_screen_bounds(screen_width, screen_height, wall_thickness)
        
        # AI settings based on difficulty
        self.difficulty = difficulty
        self.side = side
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Configure AI behavior based on difficulty
        self._configure_ai_difficulty()
    
    def _configure_ai_difficulty(self):
        """Configure AI behavior based on difficulty level"""
        if self.difficulty == "Easy":
            self.reaction_time = 0.3  # Slower reaction
            self.prediction_accuracy = 0.6  # 60% accuracy in prediction
            self.max_ai_speed = self.max_speed * 0.7  # Slower movement
            self.paddle_center_bias = 0.3  # Tendency to return to center
        elif self.difficulty == "Medium":
            self.reaction_time = 0.2  # Medium reaction
            self.prediction_accuracy = 0.8  # 80% accuracy in prediction
            self.max_ai_speed = self.max_speed * 0.85  # Medium movement speed
            self.paddle_center_bias = 0.2  # Some tendency to return to center
        elif self.difficulty == "Hard":
            self.reaction_time = 0.1  # Fast reaction
            self.prediction_accuracy = 0.95  # 95% accuracy in prediction
            self.max_ai_speed = self.max_speed  # Full speed
            self.paddle_center_bias = 0.1  # Minimal center bias
        else:
            # Default to Medium
            self.difficulty = "Medium"
            self._configure_ai_difficulty()
        
        # Internal AI state
        self.last_ball_position = Vector2(0, 0)
        self.target_y = self.position.y + self.height / 2
        self.reaction_timer = 0.0
    
    def update_ai(self, dt: float, ball):
        """Update AI logic to track and intercept the ball
        
        Args:
            dt: Delta time in seconds
            ball: Ball object to track
        """
        if ball is None:
            return
        
        # Update reaction timer
        self.reaction_timer += dt
        
        # Only react if enough time has passed (simulates human reaction time)
        if self.reaction_timer < self.reaction_time:
            return
        
        ball_pos = Vector2(ball.position.x, ball.position.y)
        ball_vel = Vector2(ball.velocity.x, ball.velocity.y)
        
        # Determine if ball is moving towards this paddle
        ball_moving_towards_us = False
        if self.side == "left" and ball_vel.x < 0:
            ball_moving_towards_us = True
        elif self.side == "right" and ball_vel.x > 0:
            ball_moving_towards_us = True
        
        if ball_moving_towards_us:
            # Predict where the ball will be when it reaches our x position
            paddle_center_x = self.position.x + self.width / 2
            time_to_reach = abs(ball_pos.x - paddle_center_x) / abs(ball_vel.x) if ball_vel.x != 0 else 0
            
            # Predict ball position with some inaccuracy based on difficulty
            predicted_y = ball_pos.y + ball_vel.y * time_to_reach
            
            # Add some randomness based on prediction accuracy
            if self.prediction_accuracy < 1.0:
                error_range = (1.0 - self.prediction_accuracy) * 100
                error = (hash(int(ball_pos.x + ball_pos.y)) % int(error_range * 2)) - error_range
                predicted_y += error
            
            # Account for wall bounces (simplified)
            while predicted_y < Config.WALL_THICKNESS or predicted_y > self.screen_height - Config.WALL_THICKNESS:
                if predicted_y < Config.WALL_THICKNESS:
                    predicted_y = Config.WALL_THICKNESS + (Config.WALL_THICKNESS - predicted_y)
                elif predicted_y > self.screen_height - Config.WALL_THICKNESS:
                    predicted_y = (self.screen_height - Config.WALL_THICKNESS) - (predicted_y - (self.screen_height - Config.WALL_THICKNESS))
            
            self.target_y = predicted_y
        else:
            # Ball moving away - return towards center with some bias
            screen_center_y = self.screen_height / 2
            current_center_y = self.position.y + self.height / 2
            center_offset = (screen_center_y - current_center_y) * self.paddle_center_bias
            self.target_y = current_center_y + center_offset
        
        # Calculate movement direction
        current_center_y = self.position.y + self.height / 2
        y_diff = self.target_y - current_center_y
        
        # Create movement direction with deadzone to prevent jittering
        direction = Vector2(0, 0)
        deadzone = 5  # pixels
        
        if abs(y_diff) > deadzone:
            direction.y = 1 if y_diff > 0 else -1
            
            # Scale movement intensity based on distance and difficulty
            intensity = min(1.0, abs(y_diff) / 50.0)  # Normalize to 0-1
            direction.y *= intensity
        
        # Apply movement with AI speed limitation
        if direction.length() > 0:
            # Temporarily adjust max speed for AI
            original_max_speed = self.max_speed
            self.max_speed = self.max_ai_speed
            
            # Update paddle movement
            self.update(dt, direction=direction)
            
            # Restore original max speed
            self.max_speed = original_max_speed
        else:
            # No movement input - let deceleration handle it
            self.update(dt)
        
        # Reset reaction timer periodically to simulate human-like periodic reactions
        if self.reaction_timer > self.reaction_time * 2:
            self.reaction_timer = 0.0
        
        # Store ball position for next frame
        self.last_ball_position = ball_pos.copy()
    
    def set_difficulty(self, difficulty: str):
        """Change the bot's difficulty level
        
        Args:
            difficulty: "Easy", "Medium", or "Hard"
        """
        self.difficulty = difficulty
        self._configure_ai_difficulty()
    
    def get_difficulty(self) -> str:
        """Get current difficulty level"""
        return self.difficulty

