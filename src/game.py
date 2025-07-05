import pygame
from .Wall import Wall
from .Player import Player
from .Ball import Ball
from .GameUI import GameUI
from enum import Enum

class GameState(Enum):
    START_SCREEN = "start"
    PLAYING = "playing"
    FINISH_SCREEN = "finish"

class Game:
    """Main game class focused on game logic only"""

    def __init__(self, width: int = 1280, height: int = 720, fps: int = 120):
        """Game initialization"""
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.width = width
        self.height = height
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.running = True
        
        # Game state management
        self.state = GameState.START_SCREEN
        
        # Game configuration
        self.dark_grey = (64, 64, 64)
        self.white = (255, 255, 255)
        self.scores = [0, 0]  # [left_player_score, right_player_score]
        self.winning_score = 7
        self.winner = None
        
        # Difficulty system
        self.difficulty_levels = [1.25, 1.5, 2.0]  # 25%, 50%, 100% speed boost
        self.difficulty_names = ["Easy", "Medium", "Hard"]
        self.selected_difficulty = 1  # Default to Medium (50%)
        self.speed_increase_factor = self.difficulty_levels[self.selected_difficulty]
        
        # Initialize UI and game objects
        self.ui = GameUI(width, height)
        self._initialize_game_objects()

    def _initialize_game_objects(self):
        """Initialize all game objects"""
        self.topWall = Wall(0, 0, self.width, 20, color=self.dark_grey)
        self.bottomWall = Wall(0, self.height - 20, self.width, 20, color=self.dark_grey)
        
        self.playerLeft = Player("left", self.width, self.height, color=self.dark_grey)
        self.playerRight = Player("right", self.width, self.height, color=self.dark_grey)
        
        self.ball = Ball(self.width // 2, self.height // 2, color="red")
        

    def handle_events(self) -> None:
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)

    def _handle_keydown(self, key: int):
        """Handle keyboard input based on game state"""
        if self.state == GameState.START_SCREEN:
            if key == pygame.K_SPACE:
                self._start_game()
            elif key == pygame.K_1:
                self.selected_difficulty = 0
                self._update_speed_factor()
            elif key == pygame.K_2:
                self.selected_difficulty = 1
                self._update_speed_factor()
            elif key == pygame.K_3:
                self.selected_difficulty = 2
                self._update_speed_factor()
        elif self.state == GameState.FINISH_SCREEN:
            if key == pygame.K_SPACE:
                self._restart_game()
            elif key == pygame.K_ESCAPE:
                self.running = False
            elif key == pygame.K_1:
                self.selected_difficulty = 0
                self._update_speed_factor()
            elif key == pygame.K_2:
                self.selected_difficulty = 1
                self._update_speed_factor()
            elif key == pygame.K_3:
                self.selected_difficulty = 2
                self._update_speed_factor()

    def _update_speed_factor(self):
        """Update speed increase factor based on selected difficulty"""
        self.speed_increase_factor = self.difficulty_levels[self.selected_difficulty]

    def _start_game(self):
        """Start a new game"""
        self.state = GameState.PLAYING
        self.scores = [0, 0]
        self.winner = None
        self.ball.reset_ball()

    def _restart_game(self):
        """Restart the game from finish screen"""
        self.state = GameState.START_SCREEN
        self.scores = [0, 0]
        self.winner = None
        self.ball.reset_ball()

    def update(self, dt: float) -> None:
        """Update game logic"""
        if self.state != GameState.PLAYING:
            return
            
        keys = pygame.key.get_pressed()
        
        # Update game objects
        self.topWall.update(dt)
        self.bottomWall.update(dt)
        self.playerLeft.keyListen(keys, dt)
        self.playerRight.keyListen(keys, dt)
        
        # Update ball and check for wall collisions
        wall_hit = self.ball.update(dt, screen_height=self.height, wall_thickness=20)
        if wall_hit:
            self.ball.increase_speed(self.speed_increase_factor)
        
        # Handle game events
        self._handle_ball_collisions()
        self._check_ball_off_screen()

    def _handle_ball_collisions(self):
        """Handle collisions between ball and paddles"""
        if self.ball.collide(self.playerLeft) or self.ball.collide(self.playerRight):
            self.ball.increase_speed(self.speed_increase_factor)

    def _check_ball_off_screen(self):
        """Check if ball went off screen and handle scoring"""
        side = self.ball.is_off_screen(self.width)
        if not side:
            return
            
        # Update scores
        if side == "left":
            self.scores[1] += 1  # Right player scores
        elif side == "right":
            self.scores[0] += 1  # Left player scores
        
        # Check for winner
        if self.scores[0] >= self.winning_score:
            self.winner = "Left Player"
            self.state = GameState.FINISH_SCREEN
        elif self.scores[1] >= self.winning_score:
            self.winner = "Right Player"
            self.state = GameState.FINISH_SCREEN
        else:
            self.ball.reset_ball()

    def draw(self) -> None:
        """Draw based on current game state"""
        if self.state == GameState.START_SCREEN:
            self.ui.draw_start_screen(self.screen, self.winning_score, self.selected_difficulty)
        elif self.state == GameState.PLAYING:
            self._draw_game()
        elif self.state == GameState.FINISH_SCREEN:
            self.ui.draw_finish_screen(self.screen, self.winner, self.scores, self.selected_difficulty)
        
        pygame.display.flip()

    def _draw_game(self):
        """Draw the main game screen"""
        self.screen.fill(self.white)
        
        # Draw UI elements
        self.ui.draw_net(self.screen)
        self.ui.draw_scores(self.screen, self.scores)
        
        # Draw game objects
        self.topWall.draw(self.screen)
        self.bottomWall.draw(self.screen)
        self.playerLeft.draw(self.screen)
        self.playerRight.draw(self.screen)
        self.ball.draw(self.screen)

    def run(self) -> None:
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()




        