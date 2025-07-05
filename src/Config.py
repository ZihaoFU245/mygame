"""
Game Configuration Settings
============================

This file contains all configurable parameters for the Pong game.
Adjust these values to fine-tune gameplay mechanics and physics.

Key Features:
- Reduced Magnus effect strength (15.0 instead of 50.0) for more balanced gameplay
- Updated speed boost levels: Easy (10%), Medium (25%), Hard (50%) 
- Consistent type handling (int for sizes, float for physics values)
- RGB color tuples for better performance
"""

class Config:
    """Configuration class for Pong game parameters"""
    
    # Ball Physics Configuration
    BALL_BASE_SPEED = 300.0
    BALL_SIZE = 15  # Changed to int for consistency
    BALL_MASS = 1.0
    BALL_MAX_BOUNCE_ANGLE = 75  # Maximum angle in degrees for paddle bounces
    
    # Magnus Effect (spin-induced curve) Configuration
    MAGNUS_EFFECT_STRENGTH = 0.5  # Reduced from 50.0 - how much spin affects trajectory
    MAGNUS_MIN_SPIN_THRESHOLD = 0.1  # Minimum spin to apply Magnus effect
    
    # Air and Angular Friction Configuration
    AIR_FRICTION = 0.99  # Air resistance factor (0.98 = 2% friction per second)
    ANGULAR_FRICTION = 0.8  # Angular velocity decay
    
    # Paddle Physics Configuration
    PADDLE_WIDTH = 20  # Changed to int for consistency
    PADDLE_HEIGHT = 100  # Changed to int for consistency
    PADDLE_MASS = 5.0
    PADDLE_ACCELERATION = 800.0  # Paddle acceleration rate
    PADDLE_DECELERATION = 600.0  # Deceleration force when no input (was incorrectly set to 0.85)
    PADDLE_MAX_SPEED = 600.0  # Maximum paddle speed
    PADDLE_FRICTION_COEFFICIENT = 0.15  # How much spin paddle imparts to ball
    
    # Speed Boost Configuration (Difficulty Levels)
    SPEED_BOOST_EASY = 1.10    # 10% speed increase per collision
    SPEED_BOOST_MEDIUM = 1.25  # 25% speed increase per collision  
    SPEED_BOOST_HARD = 1.50    # 50% speed increase per collision
    
    # Spin Configuration
    MAX_BALL_SPIN = 3.0  # Maximum angular velocity for ball
    SPIN_TRANSFER_EFFICIENCY = 1.0  # How efficiently paddle transfers spin to ball
    WALL_SPIN_REDUCTION = 0.7  # How much spin is reduced on wall bounce
    
    # Game Configuration
    WINNING_SCORE = 11
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    WALL_THICKNESS = 20
    
    # Visual Configuration
    BALL_COLOR = (255, 0, 0)  # Red
    PADDLE_COLOR = (75, 75, 75)  # White
    WALL_COLOR = (75, 75, 75)  # White
    BACKGROUND_COLOR = (255, 255, 255)  # Black
    TEXT_COLOR = (255, 255, 255)  # White
    SPIN_INDICATOR_MIN_THRESHOLD = 0.5  # Minimum spin to show visual indicator
    
    @classmethod
    def get_speed_boost_factor(cls, difficulty: str) -> float:
        """Get speed boost factor based on difficulty level"""
        difficulty_map = {
            "Easy": cls.SPEED_BOOST_EASY,
            "Medium": cls.SPEED_BOOST_MEDIUM,
            "Hard": cls.SPEED_BOOST_HARD
        }
        return difficulty_map.get(difficulty, cls.SPEED_BOOST_MEDIUM)
    
    @classmethod
    def get_difficulty_display_text(cls, difficulty: str) -> str:
        """Get display text for difficulty including speed boost percentage"""
        boost_factor = cls.get_speed_boost_factor(difficulty)
        percentage = int((boost_factor - 1.0) * 100)
        return f"{difficulty} (+{percentage}% speed/hit)"
