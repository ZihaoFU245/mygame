import pygame
from .Wall import Wall
from .Player import Player

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
        self.dark_grey = (64, 64, 64)

        # === Other Components Goes here ===
        self.topWall = Wall(0, 0, self.width, 20, color=self.dark_grey)
        self.bottomWall = Wall(0, self.height - 20, self.width, 20, color=self.dark_grey)
        
        # Paddle dimensions
        paddle_width = 20
        paddle_height = 100
        paddle_margin = 20  # Distance from screen edge
        
        # Initialize players (paddles) at correct positions
        self.playerLeft = Player(
            x=paddle_margin, 
            y=(self.height - paddle_height) // 2,  # Center vertically
            width=paddle_width,
            height=paddle_height,
            speed=400,
            color=self.dark_grey,
            order=0  # Left player (WASD keys)
        )
        
        self.playerRight = Player(
            x=self.width - paddle_margin - paddle_width,  # Right side
            y=(self.height - paddle_height) // 2,  # Center vertically
            width=paddle_width,
            height=paddle_height,
            speed=400,
            color=self.dark_grey,
            order=1  # Right player (Arrow keys)
        )
        
        # Set screen bounds for both players
        self.playerLeft.set_screen_bounds(self.width, self.height, wall_thickness=20)
        self.playerRight.set_screen_bounds(self.width, self.height, wall_thickness=20)

        

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self, dt: float) -> None:
        """update game status"""
        keys = pygame.key.get_pressed()

        # === update game objects goes here ===
        self.topWall.update(dt)
        self.bottomWall.update(dt)

        self.playerLeft.keyListen(keys, dt)
        self.playerRight.keyListen(keys, dt)

    def draw(self) -> None:
        self.screen.fill("white")
        keys = pygame.key.get_pressed()
        self._draw_net()

        # === Other game objects drawing goes here ===
        self.topWall.draw(self.screen)
        self.bottomWall.draw(self.screen)

        self.playerLeft.draw(self.screen)
        self.playerRight.draw(self.screen)

        pygame.display.flip()

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




        