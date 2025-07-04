import pygame


class Game:
    """Main game class."""

    def __init__(self, width: int = 1280, height: int = 720, fps: int = 120):
        """Game initialization"""
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.running = True

        # === Other Components Goes here ===

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self, dt: float) -> None:
        """update game status"""
        keys = pygame.key.get_pressed()

        # === update game objects goes here ===

    def draw(self) -> None:
        self.screen.fill("black")
        keys = pygame.key.get_pressed()

        # === Other game objects drawing goes here ===

        pygame.display.flip()

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0

            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()




        