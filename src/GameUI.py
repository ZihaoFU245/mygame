import pygame
from typing import Tuple, List
from .Config import Config

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
    
    def draw_start_screen(self, screen: pygame.Surface, winning_score: int):
        """Draw the starting screen with title and mode selection"""
        screen.fill(self.white)
        
        # Title
        title = self.font_large.render("PONG", True, self.black)
        title_rect = title.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
        screen.blit(title, title_rect)
        
        # Game mode selection
        mode_title = self.font_medium.render("SELECT GAME MODE:", True, self.black)
        mode_rect = mode_title.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 40))
        screen.blit(mode_title, mode_rect)
        
        # Mode options
        single_player = self.font_small.render("1. Single Player (vs AI)", True, self.black)
        single_rect = single_player.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 20))
        screen.blit(single_player, single_rect)
        
        two_player = self.font_small.render("2. Two Player (vs Human)", True, self.black)
        two_rect = two_player.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 60))
        screen.blit(two_player, two_rect)
        
        # Instructions
        instruction = self.font_small.render("Press 1 or 2 to select mode", True, self.dark_grey)
        instruction_rect = instruction.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 120))
        screen.blit(instruction, instruction_rect)

    
    def draw_finish_screen(self, screen: pygame.Surface, winner: str, scores: List[int], selected_difficulty: int, is_single_player: bool = False):
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
        
        # Use appropriate difficulty display text based on game mode
        if is_single_player:
            difficulties = [
                (f"1. {Config.get_bot_difficulty_display_text('Easy')}", 0),
                (f"2. {Config.get_bot_difficulty_display_text('Medium')}", 1),
                (f"3. {Config.get_bot_difficulty_display_text('Hard')}", 2)
            ]
        else:
            difficulties = [
                (f"1. {Config.get_difficulty_display_text('Easy')}", 0),
                (f"2. {Config.get_difficulty_display_text('Medium')}", 1),
                (f"3. {Config.get_difficulty_display_text('Hard')}", 2)
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
    
    def draw_scores(self, screen: pygame.Surface, scores: List[int], is_single_player: bool = False):
        """Draw the current scores during gameplay"""
        # Left player score
        left_label = "PLAYER" if is_single_player else "LEFT"
        left_score = self.font_large.render(str(scores[0]), True, self.blue)
        left_rect = left_score.get_rect(center=(self.screen_width // 4, 60))
        screen.blit(left_score, left_rect)
        
        # Left player label
        left_label_text = self.font_small.render(left_label, True, self.dark_grey)
        left_label_rect = left_label_text.get_rect(center=(self.screen_width // 4, 90))
        screen.blit(left_label_text, left_label_rect)
        
        # Right player score
        right_label = "BOT" if is_single_player else "RIGHT"
        right_score = self.font_large.render(str(scores[1]), True, self.blue)
        right_rect = right_score.get_rect(center=(3 * self.screen_width // 4, 60))
        screen.blit(right_score, right_rect)
        
        # Right player label
        right_label_text = self.font_small.render(right_label, True, self.dark_grey)
        right_label_rect = right_label_text.get_rect(center=(3 * self.screen_width // 4, 90))
        screen.blit(right_label_text, right_label_rect)
    
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
    
    def draw_mode_selection_screen(self, screen: pygame.Surface, is_single_player: bool, selected_difficulty: int):
        """Draw the mode selection screen with difficulty settings"""
        screen.fill(self.white)
        
        # Title
        mode_text = "SINGLE PLAYER" if is_single_player else "TWO PLAYER"
        title = self.font_large.render(mode_text, True, self.black)
        title_rect = title.get_rect(center=(self.screen_width // 2, self.screen_height // 6))
        screen.blit(title, title_rect)
        
        # Difficulty selection (for both single and two player modes)
        if is_single_player:
            difficulty_title = self.font_medium.render("SELECT AI DIFFICULTY:", True, self.black)
        else:
            difficulty_title = self.font_medium.render("SELECT DIFFICULTY:", True, self.black)
        
        difficulty_rect = difficulty_title.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
        screen.blit(difficulty_title, difficulty_rect)
        
        # Use appropriate difficulty display text based on game mode
        if is_single_player:
            difficulties = [
                (f"1. {Config.get_bot_difficulty_display_text('Easy')}", 0),
                (f"2. {Config.get_bot_difficulty_display_text('Medium')}", 1),
                (f"3. {Config.get_bot_difficulty_display_text('Hard')}", 2)
            ]
        else:
            difficulties = [
                (f"1. {Config.get_difficulty_display_text('Easy')}", 0),
                (f"2. {Config.get_difficulty_display_text('Medium')}", 1),
                (f"3. {Config.get_difficulty_display_text('Hard')}", 2)
            ]
        
        y_offset = self.screen_height // 3 
        for i, (text, index) in enumerate(difficulties):
            color = self.blue if index == selected_difficulty else self.black
            # Use slightly larger font for difficulty options to make them more prominent
            font_to_use = self.font_medium if index == selected_difficulty else self.font_small
            diff_text = font_to_use.render(text, True, color)
            diff_rect = diff_text.get_rect(center=(self.screen_width // 2, y_offset))
            screen.blit(diff_text, diff_rect)
            y_offset += 45  # Increased spacing for better visibility
        
        # Game mode specific rules
        if is_single_player:
            rules = [
                "SINGLE PLAYER RULES:",
                "• You control the left paddle (W/S keys)",
                "• AI Bot controls the right paddle",
                "• Ball speed increases after each hit",
                "• Higher difficulty = faster ball + smarter bot",
                "",
                "Use 1/2/3 keys to select difficulty"
            ]
        else:
            rules = [
                "TWO PLAYER RULES:",
                "• Left Player: W/S keys",
                "• Right Player: Arrow keys", 
                "• Ball speed increases after each hit",
                "• First to 11 points wins",
                "",
                "Use 1/2/3 keys to select difficulty"
            ]
        
        # Draw rules
        y_offset = self.screen_height // 2 + 40
        for rule in rules:
            if rule.endswith("RULES:"):
                text = self.font_medium.render(rule, True, self.black)
            else:
                text = self.font_small.render(rule, True, self.black)
            
            text_rect = text.get_rect(center=(self.screen_width // 2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 35 if rule.endswith("RULES:") else 30
        
        # Instructions
        y_offset += 20
        start_text = self.font_small.render("Press SPACE to start", True, self.dark_grey)
        start_rect = start_text.get_rect(center=(self.screen_width // 2, y_offset))
        screen.blit(start_text, start_rect)
        
        back_text = self.font_small.render("Press ESC to go back", True, self.dark_grey)
        back_rect = back_text.get_rect(center=(self.screen_width // 2, y_offset + 35))
        screen.blit(back_text, back_rect)
