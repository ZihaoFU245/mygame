import pygame
from .Wall import Wall
from .Player import Player
from .Ball import Ball
from enum import Enum

class GameState(Enum):
    START_SCREEN = "start"
    PLAYING = "playing"
    FINISH_SCREEN = "finish"

class Game:
    """Main game class."""

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
        
        # Colors
        self.dark_grey = (64, 64, 64)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        
        # Font setup
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        
        # Scoring system
        self.scores = [0, 0]  # [left_player_score, right_player_score]
        self.winning_score = 7  # First to 7 wins
        self.winner = None
        
        # Ball speed increase factor
        self.speed_increase_factor = 2  # x2 speed increase per collision
        
        self._initialize_game_objects()

    def _initialize_game_objects(self):
        """Initialize all game objects"""
        # === Game Objects ===
        self.topWall = Wall(0, 0, self.width, 20, color=self.dark_grey)
        self.bottomWall = Wall(0, self.height - 20, self.width, 20, color=self.dark_grey)
        
        # Initialize players with automatic positioning and setup
        self.playerLeft = Player(
            side="left",
            screen_width=self.width,
            screen_height=self.height,
            color=self.dark_grey
        )
        
        self.playerRight = Player(
            side="right", 
            screen_width=self.width,
            screen_height=self.height,
            color=self.dark_grey
        )

        self.ball = Ball(self.width // 2, self.height // 2, color="red")
        

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.state == GameState.START_SCREEN:
                    if event.key == pygame.K_SPACE:
                        self._start_game()
                elif self.state == GameState.FINISH_SCREEN:
                    if event.key == pygame.K_SPACE:
                        self._restart_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False

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
        """update game status"""
        if self.state != GameState.PLAYING:
            return
            
        keys = pygame.key.get_pressed()

        # === update game objects goes here ===
        self.topWall.update(dt)
        self.bottomWall.update(dt)

        self.playerLeft.keyListen(keys, dt)
        self.playerRight.keyListen(keys, dt)

        # Update ball with screen parameters for wall collision
        self.ball.update(dt, screen_height=self.height, wall_thickness=20)
        
        # Handle ball-paddle collisions
        self._handle_ball_collisions()
        
        # Check if ball went off screen for scoring
        self._check_ball_off_screen()

    def _handle_ball_collisions(self):
        """Handle collisions between ball and paddles"""
        # Check collision with left paddle
        if self.ball.collide(self.playerLeft):
            self.ball.increase_speed(self.speed_increase_factor)
            
        # Check collision with right paddle
        if self.ball.collide(self.playerRight):
            self.ball.increase_speed(self.speed_increase_factor)

    def _check_ball_off_screen(self):
        """Check if ball went off screen and handle scoring"""
        side = self.ball.is_off_screen(self.width)
        if side:
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
                # Continue playing - reset ball
                self.ball.reset_ball()

    def draw(self) -> None:
        """Draw based on current game state"""
        if self.state == GameState.START_SCREEN:
            self._draw_start_screen()
        elif self.state == GameState.PLAYING:
            self._draw_game()
        elif self.state == GameState.FINISH_SCREEN:
            self._draw_finish_screen()
        
        pygame.display.flip()

    def _draw_start_screen(self):
        """Draw the starting screen"""
        self.screen.fill(self.white)
        
        # Title
        title = self.font_large.render("PONG", True, self.black)
        title_rect = title.get_rect(center=(self.width // 2, self.height // 4))
        self.screen.blit(title, title_rect)
        
        # Rules
        rules = [
            "GAME RULES:",
            f"• First to {self.winning_score} points wins",
            "• Ball gets faster after each paddle hit",
            "• Left Player: W/S keys",
            "• Right Player: Arrow keys",
            "",
            "Press SPACE to start"
        ]
        
        y_offset = self.height // 2 - 100
        for rule in rules:
            if rule == "GAME RULES:":
                text = self.font_medium.render(rule, True, self.black)
            elif rule == "Press SPACE to start":
                text = self.font_medium.render(rule, True, self.dark_grey)
            else:
                text = self.font_small.render(rule, True, self.black)
            
            text_rect = text.get_rect(center=(self.width // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 50 if rule == "GAME RULES:" else 40

    def _draw_game(self):
        """Draw the main game screen"""
        self.screen.fill(self.white)
        
        # Draw net
        self._draw_net()
        
        # Draw game objects
        self.topWall.draw(self.screen)
        self.bottomWall.draw(self.screen)
        self.playerLeft.draw(self.screen)
        self.playerRight.draw(self.screen)
        self.ball.draw(self.screen)
        
        # Draw scores
        self._draw_scores()

    def _draw_finish_screen(self):
        """Draw the finish screen"""
        self.screen.fill(self.white)
        
        # Winner announcement
        winner_text = self.font_large.render(f"{self.winner} Wins!", True, self.black)
        winner_rect = winner_text.get_rect(center=(self.width // 2, self.height // 3))
        self.screen.blit(winner_text, winner_rect)
        
        # Final score
        score_text = self.font_medium.render(f"Final Score: {self.scores[0]} - {self.scores[1]}", True, self.dark_grey)
        score_rect = score_text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(score_text, score_rect)
        
        # Instructions
        restart_text = self.font_small.render("Press SPACE to play again", True, self.black)
        restart_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 80))
        self.screen.blit(restart_text, restart_rect)
        
        quit_text = self.font_small.render("Press ESC to quit", True, self.black)
        quit_rect = quit_text.get_rect(center=(self.width // 2, self.height // 2 + 120))
        self.screen.blit(quit_text, quit_rect)

    def _draw_scores(self):
        """Draw the current scores during gameplay"""
        # Left player score
        left_score = self.font_large.render(str(self.scores[0]), True, self.dark_grey)
        left_rect = left_score.get_rect(center=(self.width // 4, 60))
        self.screen.blit(left_score, left_rect)
        
        # Right player score
        right_score = self.font_large.render(str(self.scores[1]), True, self.dark_grey)
        right_rect = right_score.get_rect(center=(3 * self.width // 4, 60))
        self.screen.blit(right_score, right_rect)

    def _draw_net(self) -> None:
        """Draw a dotted line in the middle of the screen to represent the net"""
        middle_x = self.width // 2
        dash_height = 15
        dash_gap = 10
        dash_width = 3
        
        y = 0
        while y < self.height:
            # Draw dash if it doesn't overlap with walls
            if y > 20 and y + dash_height < self.height - 20:
                pygame.draw.rect(self.screen, self.dark_grey, 
                               (middle_x - dash_width // 2, y, dash_width, dash_height))
            y += dash_height + dash_gap

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0

            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()




        