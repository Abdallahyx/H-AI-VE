from tile import Inventory_Tile
from pieces import Queen, Grasshopper, Spider, Beetle, Ant
from inventory_frame import Inventory_Frame
from turn_panel import Turn_Panel
from settings import PIECE_WHITE, PIECE_BLACK


class Game_State:
    def __init__(self, tiles=[], white_inventory=None, black_inventory=None):
        # Existing initialization code...
        self.running = True
        self.menu_loop = True
        self.main_loop = False
        self.end_loop = False
        self.play_new_game = False
        self.move_popup_loop = False

        # board
        self.white_inventory = white_inventory
        self.black_inventory = black_inventory
        self.board_tiles = (
            tiles + white_inventory.tiles + black_inventory.tiles
            if white_inventory and black_inventory
            else []
        )

        self.turn_panel = Turn_Panel()

        # action attributes
        self.clicked = False
        self.moving_piece = None
        self.turn = 1

        # game mode and AI
        self.game_mode = None
        self.ai_player_white = None
        self.ai_player_black = None
        self.difficulty_selection_needed = (
            []
        )  # List of AI players needing difficulty selection

        # other
        self.winner = None

    def start_game(self):
        self.menu_loop = False
        self.main_loop = True

    def end_game(self):
        self.main_loop = False
        self.end_loop = True

    def new_game(self):
        # Reset all game state attributes
        self.main_loop = True
        self.end_loop = False
        self.turn = 1
        self.clicked = False
        self.moving_piece = None
        self.winner = None
        self.game_mode = None
        self.ai_player_white = None
        self.ai_player_black = None
        self.difficulty_selection_needed = []

    def quit(self):
        self.running = False
        self.menu_loop = False
        self.main_loop = False
        self.end_loop = False

    def play_again(self):
        self.play_new_game = True
        self.quit()

    def open_popup(self):
        self.main_loop = False
        self.move_popup_loop = True

    def close_popup(self):
        self.main_loop = True
        self.move_popup_loop = False
        self.next_turn()

    def add_moving_piece(self, piece):
        self.moving_piece = piece

    def remove_moving_piece(self):
        self.moving_piece = None

    def click(self):
        self.clicked = True

    def unclick(self):
        self.clicked = False

    def add_tiles(self, tiles):
        self.board_tiles.extend(tiles)

    def next_turn(self):
        self.turn += 1

    def is_player_turn(self):
        if self.moving_piece.color == PIECE_WHITE and self.turn % 2 == 1:
            return True
        elif self.moving_piece.color == PIECE_BLACK and self.turn % 2 == 0:
            return True
        else:
            return False

    def get_tiles_with_pieces(self, include_inventory=False):
        tiles = []
        for tile in self.board_tiles:
            if include_inventory:
                if tile.has_pieces():
                    tiles.append(tile)
            elif tile.has_pieces() and type(tile) is not Inventory_Tile:
                tiles.append(tile)
        return tiles

    def get_current_player_color(self):
        """
        Determine the current player's color based on the turn
        """
        return PIECE_WHITE if self.turn % 2 == 1 else PIECE_BLACK

    def get_ai_player(self):
        """
        Get the current AI player based on the turn
        """
        if self.game_mode == "Human vs AI":
            return self.ai_player_white if self.turn % 2 == 0 else None
        elif self.game_mode == "AI vs AI":
            return self.ai_player_white if self.turn % 2 == 1 else self.ai_player_black
        return None
