import pygame as pg
import traceback
import time
from tile import Tile, initialize_grid, draw_drag
from move_checker import is_valid_move, game_is_over, player_has_no_moves
from menus import difficulty_menu, start_menu, end_menu, no_move_popup
from game_mode import game_mode_menu
from game_state import Game_State
from inventory_frame import Inventory_Frame
from turn_panel import Turn_Panel
from ai_player import AIPlayer
from settings import BACKGROUND, WIDTH, HEIGHT, PIECE_WHITE, PIECE_BLACK


def Hive():
    pg.font.init()

    # Create the screen
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    background = pg.Surface(screen.get_size())

    # Title and Icon
    pg.display.set_caption("Hive")
    icon = pg.image.load("images/icon.png")
    pg.display.set_icon(icon)

    # Create inventories first
    white_inventory = Inventory_Frame((0, 158), 0, white=True)
    black_inventory = Inventory_Frame((440, 158), 1, white=False)

    # Initialize the grid with board tiles
    board_tiles = initialize_grid(HEIGHT - 200, WIDTH, radius=20)

    state = Game_State(
        tiles=board_tiles,
        white_inventory=white_inventory,
        black_inventory=black_inventory,
    )

    # Track the last AI move time
    last_ai_move_time = 0
    AI_MOVE_DELAY = 1.0  # 1 second delay between AI moves

    while state.running:
        while state.menu_loop:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    state.quit()
                    break
                start_menu(screen, state, event)

        # Game mode selection
        while not state.game_mode:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    state.quit()
                    break
                game_mode_menu(screen, state, event)

        # Difficulty selection for AI players
        while state.difficulty_selection_needed:
            current_ai = state.difficulty_selection_needed[0]
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    state.quit()
                    break
                if difficulty_menu(screen, state, event, current_ai):
                    state.difficulty_selection_needed.pop(0)
                    break

        while state.move_popup_loop:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    state.quit()
                    break
                no_move_popup(screen, background, state, event)

        while state.main_loop:
            pos = pg.mouse.get_pos()
            current_time = time.time()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    state.quit()
                    break
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        state.quit()
                        break

                # Enhanced AI Move Logic with Delay and Error Handling
                try:
                    if state.game_mode == "Human vs AI":
                        if state.turn % 2 == 0:  # AI's turn (Black)
                            # Check if enough time has passed since last AI move
                            if current_time - last_ai_move_time >= AI_MOVE_DELAY:
                                print(f"Preparing AI move. Turn: {state.turn}")
                                old_tile, new_tile = (
                                    state.ai_player_black.get_best_move(state)
                                )

                                if old_tile is None or new_tile is None:
                                    print(
                                        "Invalid move generated by AI. Skipping turn."
                                    )
                                    state.next_turn()
                                    last_ai_move_time = current_time
                                    continue

                                if is_valid_move(state, old_tile, new_tile):
                                    state.add_moving_piece(old_tile.pieces[-1])
                                    old_tile.move_piece(new_tile)
                                    print(
                                        f"AI move successful. Next turn: {state.turn + 1}"
                                    )
                                    state.next_turn()
                                    last_ai_move_time = current_time
                                    if player_has_no_moves(state):
                                        state.open_popup()

                                state.remove_moving_piece()

                    elif state.game_mode == "AI vs AI":
                        # Check if enough time has passed since last AI move
                        if current_time - last_ai_move_time >= AI_MOVE_DELAY:
                            # Alternate between white and black AI players
                            ai_to_move = (
                                state.ai_player_white
                                if state.turn % 2 == 1
                                else state.ai_player_black
                            )
                            print(
                                f"Preparing AI move for {ai_to_move.color}. Turn: {state.turn}"
                            )
                            old_tile, new_tile = ai_to_move.get_best_move(state)

                            if old_tile is None or new_tile is None:
                                print("Invalid move generated by AI. Skipping turn.")
                                state.next_turn()
                                last_ai_move_time = current_time
                                continue

                            if is_valid_move(state, old_tile, new_tile):
                                state.add_moving_piece(old_tile.pieces[-1])
                                old_tile.move_piece(new_tile)
                                print(
                                    f"AI move successful. Next turn: {state.turn + 1}"
                                )
                                state.next_turn()
                                last_ai_move_time = current_time
                                if player_has_no_moves(state):
                                    state.open_popup()

                            state.remove_moving_piece()

                except Exception as e:
                    print(f"Unexpected error during AI move: {e}")
                    traceback.print_exc()
                    state.next_turn()
                    last_ai_move_time = current_time  # Update time even on error

                # Human Move Logic
                if state.game_mode in ["Human vs Human", "Human vs AI"] and (
                    state.game_mode == "Human vs Human" or state.turn % 2 == 1
                ):
                    if event.type == pg.MOUSEBUTTONDOWN:
                        state.click()
                    if event.type == pg.MOUSEBUTTONUP:
                        state.unclick()
                        if state.moving_piece and state.is_player_turn():
                            old_tile = next(
                                tile
                                for tile in state.board_tiles
                                if tile.has_pieces()
                                and tile.pieces[-1] == state.moving_piece
                            )
                            new_tile = next(
                                (
                                    tile
                                    for tile in state.board_tiles
                                    if tile.under_mouse(pos)
                                ),
                                None,
                            )
                            if is_valid_move(state, old_tile, new_tile):
                                old_tile.move_piece(new_tile)
                                state.next_turn()
                                if player_has_no_moves(state):
                                    state.open_popup()

                            state.remove_moving_piece()

            # Drawing Logic
            background.fill(BACKGROUND)
            white_inventory.draw(background, pos)
            black_inventory.draw(background, pos)
            for tile in state.board_tiles:
                if state.clicked:
                    tile.draw(background, pos, state.clicked)
                    if (
                        tile.under_mouse(pos)
                        and state.moving_piece is None
                        and tile.has_pieces()
                    ):
                        state.add_moving_piece(tile.pieces[-1])
                else:
                    tile.draw(background, pos)
            if state.moving_piece:
                draw_drag(background, pos, state.moving_piece)
            state.turn_panel.draw(background, state.turn)
            screen.blit(background, (0, 0))
            pg.display.flip()

            if game_is_over(state):
                state.end_game()

        while state.end_loop:
            end_menu(screen, state, event)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    state.quit()
                    break
    return state.play_new_game


def main():
    run_game = True
    while run_game:
        run_game = Hive()


if __name__ == "__main__":
    main()