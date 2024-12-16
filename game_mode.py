import pygame as pg
from settings import (
    PIECE_BLACK,
    PIECE_WHITE,
    WHITE,
    BLACK,
    HOVER_COLOR,
    START_COLOR,
    WIDTH,
    HEIGHT,
)
from ai_player import AIPlayer

HUMAN_VS_HUMAN = "Human vs Human"
HUMAN_VS_AI = "Human vs AI"
AI_VS_AI = "AI vs AI"


class GameModeButton:
    def __init__(self, text, rect):
        self.text = text
        self.rect = rect
        self.color = BLACK
        self.mode = text

    def run_if_clicked(self, pos, state):
        if self.rect.collidepoint(pos):
            state.game_mode = self.mode
            if self.mode == HUMAN_VS_AI:
                state.ai_player_black = AIPlayer(
                    PIECE_BLACK
                )  # Initialize with default difficulty
                state.difficulty_selection_needed = ["black"]
            elif self.mode == AI_VS_AI:
                state.ai_player_white = AIPlayer(
                    PIECE_WHITE
                )  # Initialize with default difficulty
                state.ai_player_black = AIPlayer(
                    PIECE_BLACK
                )  # Initialize with default difficulty
                state.difficulty_selection_needed = ["white", "black"]
            return True
        return False

    def highlight_if_hovered(self, pos):
        self.color = HOVER_COLOR if self.rect.collidepoint(pos) else BLACK

    def draw(self, background):
        FONT = pg.font.SysFont("Times New Norman", 40)
        font = FONT.render(self.text, True, WHITE)
        pg.draw.rect(background, self.color, self.rect)
        font_rect = font.get_rect(center=self.rect.center)
        background.blit(font, font_rect)


def game_mode_menu(screen, state, event):
    button_width = WIDTH / 3
    button_height = HEIGHT / 10
    button_pos = WIDTH / 2 - button_width / 2

    rect1 = pg.Rect(button_pos, 3 / 9 * HEIGHT, button_width, button_height)
    rect2 = pg.Rect(button_pos, 4 / 9 * HEIGHT, button_width, button_height)
    rect3 = pg.Rect(button_pos, 5 / 9 * HEIGHT, button_width, button_height)

    buttons = [
        GameModeButton(HUMAN_VS_HUMAN, rect1),
        GameModeButton(HUMAN_VS_AI, rect2),
        GameModeButton(AI_VS_AI, rect3),
    ]

    if event.type == pg.MOUSEMOTION:
        for button in buttons:
            button.highlight_if_hovered(event.pos)
    elif event.type == pg.MOUSEBUTTONDOWN:
        for button in buttons:
            if button.run_if_clicked(event.pos, state):
                return True

    screen.fill(START_COLOR)

    # Draw title
    FONT = pg.font.SysFont("Times New Norman", 48)
    title = FONT.render("Select Game Mode", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH / 2, HEIGHT / 4))
    screen.blit(title, title_rect)

    for button in buttons:
        button.draw(screen)

    pg.display.flip()
    return False
