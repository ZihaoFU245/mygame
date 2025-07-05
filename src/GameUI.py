import pygame
from typing import Tuple, List

class GameUI:
    """Utility class for handling all UI rendering and text display"""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Colors
        self.dark_grey = (64, 64, 64)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.blue = (0, 0, 255)
        
        # Fonts
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
    
    def draw_start_screen(self, screen: pygame.Surface, winning_score: int, selected_difficulty: int):
        """Draw the starting screen with title, rules, and difficulty selection"""
        screen.fill(self.white)
        
        # Title
        title = self.font_large.render("PONG", True, self.black)
        title_rect = title.get_rect(center=(self.screen_width // 2, self.screen_height // 6))
        screen.blit(title, title_rect)
        
        # Difficulty selection
        difficulty_title = self.font_medium.render("SELECT DIFFICULTY:", True, self.black)
        difficulty_rect = difficulty_title.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
        screen.blit(difficulty_title, difficulty_rect)
        
        difficulties = [
            ("1. Easy (25% speed boost)", 0),
            ("2. Medium (50% speed boost)", 1),
            ("3. Hard (100% speed boost)", 2)
        ]
        
        y_offset = self.screen_height // 3 
        for i, (text, index) in enumerate(difficulties):
            color = self.blue if index == selected_difficulty else self.black
            diff_text = self.font_small.render(text, True, color)
            diff_rect = diff_text.get_rect(center=(self.screen_width // 2, y_offset))
            screen.blit(diff_text, diff_rect)
            y_offset += 40
        
        # Rules
        rules = [
            "GAME RULES:",
            f"• First to {winning_score} points wins",
            "• Ball gets faster after each hit (paddle & wall)",
            "• Left Player: W/S keys",
            "• Right Player: Arrow keys",
            "",
            "Use 1/2/3 keys to select difficulty",
            "Press SPACE to start"
        ]
        
        y_offset = self.screen_height // 2 + 10
        for rule in rules:
            if rule == "GAME RULES:":
                text = self.font_medium.render(rule, True, self.black)
            elif rule.startswith("Use") or rule.startswith("Press"):
                text = self.font_small.render(rule, True, self.dark_grey)
            else:
                text = self.font_small.render(rule, True, self.black)
            
            text_rect = text.get_rect(center=(self.screen_width // 2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 35 if rule == "GAME RULES:" else 30
    
    def draw_finish_screen(self, screen: pygame.Surface, winner: str, scores: List[int], selected_difficulty: int):
        """Draw the finish screen with winner announcement, final score, and difficulty selection"""
        screen.fill(self.white)
        
        # Winner announcement
        winner_text = self.font_large.render(f"{winner} Wins!", True, self.black)
        winner_rect = winner_text.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
        screen.blit(winner_text, winner_rect)
        
        # Final score
        score_text = self.font_medium.render(f"Final Score: {scores[0]} - {scores[1]}", True, self.dark_grey)
        score_rect = score_text.get_rect(center=(self.screen_width // 2, self.screen_height // 3))
        screen.blit(score_text, score_rect)
        
        # Difficulty selection for next game
        difficulty_title = self.font_medium.render("SELECT DIFFICULTY FOR NEXT GAME:", True, self.black)
        difficulty_rect = difficulty_title.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        screen.blit(difficulty_title, difficulty_rect)
        
        difficulties = [
            ("1. Easy (25% speed boost)", 0),
            ("2. Medium (50% speed boost)", 1),
            ("3. Hard (100% speed boost)", 2)
        ]
        
        y_offset = self.screen_height // 2 + 50
        for i, (text, index) in enumerate(difficulties):
            color = self.blue if index == selected_difficulty else self.black
            diff_text = self.font_small.render(text, True, color)
            diff_rect = diff_text.get_rect(center=(self.screen_width // 2, y_offset))
            screen.blit(diff_text, diff_rect)
            y_offset += 35
        
        # Instructions
        y_offset += 20
        restart_text = self.font_small.render("Use 1/2/3 to select difficulty", True, self.dark_grey)
        restart_rect = restart_text.get_rect(center=(self.screen_width // 2, y_offset))
        screen.blit(restart_text, restart_rect)
        
        play_text = self.font_small.render("Press SPACE to play again", True, self.black)
        play_rect = play_text.get_rect(center=(self.screen_width // 2, y_offset + 35))
        screen.blit(play_text, play_rect)
        
        quit_text = self.font_small.render("Press ESC to quit", True, self.black)
        quit_rect = quit_text.get_rect(center=(self.screen_width // 2, y_offset + 70))
        screen.blit(quit_text, quit_rect)
    
    def draw_scores(self, screen: pygame.Surface, scores: List[int]):
        """Draw the current scores during gameplay"""
        # Left player score
        left_score = self.font_large.render(str(scores[0]), True, self.blue)
        left_rect = left_score.get_rect(center=(self.screen_width // 4, 60))
        screen.blit(left_score, left_rect)
        
        # Right player score
        right_score = self.font_large.render(str(scores[1]), True, self.blue)
        right_rect = right_score.get_rect(center=(3 * self.screen_width // 4, 60))
        screen.blit(right_score, right_rect)
    
    def draw_net(self, screen: pygame.Surface):
        """Draw a dotted line in the middle of the screen to represent the net"""
        middle_x = self.screen_width // 2
        dash_height = 15
        dash_gap = 10
        dash_width = 3
        
        y = 0
        while y < self.screen_height:
            # Draw dash if it doesn't overlap with walls
            if y > 20 and y + dash_height < self.screen_height - 20:
                pygame.draw.rect(screen, self.dark_grey, 
                               (middle_x - dash_width // 2, y, dash_width, dash_height))
            y += dash_height + dash_gap
