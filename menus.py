import pygame as pg
import webbrowser
from settings import (
    WHITE,
    BLACK,
    PURPLE,
    HOVER_COLOR,
    PIECE_WHITE,
    PIECE_BLACK,
    CLEAR,
    START_COLOR,
    WIDTH,
    HEIGHT,
)

START = "START"
RULES = "RULES"
OPTIONS = "OPTIONS"
NEWGAME = "NEW GAME"
QUIT = "QUIT"

EASY = "Easy"
MEDIUM = "Medium"
HARD = "Hard"
IMPOSSIBLE = "Impossible"


class DifficultyButton:
    def __init__(self, text, rect):
        self.text = text
        self.rect = rect
        self.color = BLACK
        self.difficulty_map = {EASY: 1, MEDIUM: 2, HARD: 3, IMPOSSIBLE: 4}

    def run_if_clicked(self, pos, state, player_type):
        if self.rect.collidepoint(pos):
            difficulty = self.difficulty_map[self.text]
            if player_type == "white":
                state.ai_player_white.difficulty = difficulty
            elif player_type == "black":
                state.ai_player_black.difficulty = difficulty
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


def draw_title(screen, text):
    FONT = pg.font.SysFont("Times New Norman", 48)
    title = FONT.render(text, True, WHITE)
    title_rect = title.get_rect(center=(WIDTH / 2, HEIGHT / 4))
    screen.blit(title, title_rect)


def difficulty_menu(screen, state, event, player_type):
    """
    Display difficulty selection menu for AI players

    Args:
        screen: Pygame screen
        state: Game state
        event: Pygame event
        player_type: "white" or "black" to indicate which AI player to configure

    Returns:
        Boolean indicating if difficulty was selected
    """
    button_width = WIDTH / 3
    button_height = HEIGHT / 10
    button_pos = WIDTH / 2 - button_width / 2

    # Create buttons in a vertical layout
    rect1 = pg.Rect(button_pos, 3 / 8 * HEIGHT, button_width, button_height)
    rect2 = pg.Rect(button_pos, 4 / 8 * HEIGHT, button_width, button_height)
    rect3 = pg.Rect(button_pos, 5 / 8 * HEIGHT, button_width, button_height)
    rect4 = pg.Rect(button_pos, 6 / 8 * HEIGHT, button_width, button_height)

    buttons = [
        DifficultyButton(EASY, rect1),
        DifficultyButton(MEDIUM, rect2),
        DifficultyButton(HARD, rect3),
        DifficultyButton(IMPOSSIBLE, rect4),
    ]

    if event.type == pg.MOUSEMOTION:
        for button in buttons:
            button.highlight_if_hovered(event.pos)
    elif event.type == pg.MOUSEBUTTONDOWN:
        for button in buttons:
            if button.run_if_clicked(event.pos, state, player_type):
                return True

    screen.fill(START_COLOR)

    # Draw appropriate title based on game mode and player
    if state.game_mode == "Human vs AI":
        title_text = "Select AI Difficulty"
    else:  # AI vs AI
        title_text = f"Select {player_type.capitalize()} AI Difficulty"
    draw_title(screen, title_text)

    for button in buttons:
        button.draw(screen)

    pg.display.flip()
    return False


class StartButton:
    def __init__(self, text, rect):
        self.text = text
        self.rect = rect
        self.color = BLACK

    def run_if_clicked(self, pos, state):
        if self.rect.collidepoint(pos):
            if self.text == START:
                state.start_game()
                return
            elif self.text == RULES:
                open_rules()

    def highlight_if_hovered(self, pos):
        if self.rect.collidepoint(pos):
            self.color = HOVER_COLOR
        else:
            self.color = BLACK

    def draw(self, background):
        FONT = pg.font.SysFont("Times New Norman", 60)
        font = FONT.render(self.text, True, WHITE)
        font_rect = font.get_rect(
            center=self.rect.center
        )  # Center the text in the button

        pg.draw.rect(background, self.color, self.rect)
        background.blit(
            font, font_rect
        )  # Use the centered font_rect instead of self.rect


def start_menu(screen, state, event):

    button_width = WIDTH / 4.5
    button_height = HEIGHT / 10
    button_pos = WIDTH / 2 - button_width / 2

    rect1 = pg.Rect(button_pos, 3 / 9 * HEIGHT, button_width, button_height)
    rect2 = pg.Rect(button_pos, 4 / 9 * HEIGHT, button_width, button_height)

    buttons = [StartButton(START, rect1), StartButton(RULES, rect2)]

    if event.type == pg.MOUSEMOTION:
        for button in buttons:
            button.highlight_if_hovered(event.pos)
    elif event.type == pg.MOUSEBUTTONDOWN:
        for button in buttons:
            button.run_if_clicked(event.pos, state)

    screen.fill(START_COLOR)

    for button in buttons:
        button.draw(screen)

    pg.display.flip()


class EndButton:

    def __init__(self, text, pos):
        self.text = text

        font = pg.font.SysFont("Times New Norman", 90)
        self.FONT = font.render(self.text, True, PURPLE)
        self.FONT.set_alpha(250)
        self.font_rect = self.FONT.get_rect(center=pos)

    def run_if_clicked(self, pos, state):
        if self.font_rect.collidepoint(pos):
            if self.text == NEWGAME:
                state.play_again()
                return
            elif self.text == QUIT:
                state.quit()
                return

    def draw(self, background):
        background.blit(self.FONT, self.font_rect)


def end_menu(screen, state, event):

    clear_surface = pg.Surface((WIDTH, HEIGHT))
    clear_surface.set_alpha(5)
    clear_surface.fill(WHITE)
    buttons = [
        EndButton(NEWGAME, (WIDTH / 2, HEIGHT / 2)),
        EndButton(QUIT, (WIDTH / 2, 0.65 * HEIGHT)),
    ]

    title_font = pg.font.SysFont("Times New Norman", 120)

    if state.winner == PIECE_WHITE:
        wins = title_font.render("White Wins!", True, PURPLE)
    elif state.winner == PIECE_BLACK:
        wins = title_font.render("Black Wins!", True, PURPLE)
    else:
        wins = title_font.render("Draw", True, PURPLE)
    wins.set_alpha(250)
    wins_rect = wins.get_rect(center=(WIDTH / 2, HEIGHT / 8))

    if event.type == pg.MOUSEBUTTONDOWN:
        for button in buttons:
            button.run_if_clicked(event.pos, state)

    for button in buttons:
        button.draw(clear_surface)

    clear_surface.blit(wins, wins_rect)

    screen.blit(clear_surface, (0, 0))

    pg.display.flip()


def open_rules():
    webbrowser.open("https://www.ultraboardgames.com/hive/game-rules.php")


def no_move_popup(
    screen,
    surface,
    state,
    event,
):

    window_width = WIDTH / 2
    window_height = HEIGHT / 3

    clear_surface = pg.Surface((window_width, window_height))
    clear_surface.set_alpha(5)
    clear_surface.fill(CLEAR)

    popup_font = pg.font.SysFont("Times New Norman", 32)

    if state.turn % 2 == 1:
        no_move = popup_font.render("White has no moves", True, PURPLE)
        turn_skipped = popup_font.render("White turn is skipped", True, PURPLE)
    else:
        no_move = popup_font.render("Black has no moves,", True, PURPLE)
        turn_skipped = popup_font.render("Black turn is skipped", True, PURPLE)
    close = popup_font.render("Press the space bar to close this message", True, PURPLE)

    close.set_alpha(250)
    no_move.set_alpha(250)
    turn_skipped.set_alpha(250)

    close_rect = close.get_rect(
        center=(window_width / 2, window_height / 2 + window_height / 4)
    )
    no_move_rect = no_move.get_rect(
        center=(window_width / 2, window_height / 2 - window_height / 3)
    )
    turn_skipped_rect = turn_skipped.get_rect(
        center=(window_width / 2, window_height / 2 - window_height / 5)
    )

    clear_surface.blit(no_move, no_move_rect)
    clear_surface.blit(turn_skipped, turn_skipped_rect)
    clear_surface.blit(close, close_rect)

    if event.type == pg.KEYDOWN:
        if event.key == pg.K_SPACE:
            state.close_popup()

    screen.blit(clear_surface, (WIDTH / 4, HEIGHT / 4))
    pg.display.flip()
