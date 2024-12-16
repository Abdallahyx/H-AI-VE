import pygame as pg
from pieces import Queen, Grasshopper, Spider, Beetle, Ant
from tile import Inventory_Tile
from settings import PIECE_WHITE, PIECE_BLACK, WHITE, BLACK, PANEL, WIDTH, HEIGHT


class Inventory_Frame:

    def __init__(
        self,
        pos,
        player,
        white=True,
    ):
        left = pos[0]
        top = HEIGHT - pos[1]

        inventory_width = WIDTH / 2
        inventory_height = 160

        inner_left = left + 5
        inner_top = top + 5
        inner_width = inventory_width - 10
        inner_height = inventory_height - 10

        self.back_panel = pg.Rect(left, top, inventory_width, inventory_height)
        self.inner_panel = pg.Rect(inner_left, inner_top, inner_width, inner_height)

        title_height = inner_height / 10
        stock_height = inner_height * (9 / 10)
        stock_width = inner_width / 5

        self.tile_rects = []
        self.tiles = []

        if white:
            self.color = PIECE_WHITE
        else:
            self.color = PIECE_BLACK

        # Track available pieces by type
        self.available_pieces = {
            "Queen": 1,
            "Beetle": 2,
            "Spider": 2,
            "Grasshopper": 3,
            "Ant": 3,
        }

        for i in range(0, 5):
            self.tile_rects.append(
                pg.Rect(
                    inner_left + i * stock_width + 2,
                    inner_top + title_height + 2,
                    stock_width - 4,
                    stock_height - 4,
                )
            )

            if i == 0:
                tile_pos = (
                    inner_left + i * stock_width + stock_width / 2,
                    inner_top + title_height + stock_height / 2,
                )
                self.tiles.append(
                    Inventory_Tile(
                        tile_pos, (99, 99), 20, self.color, piece=Queen(self.color)
                    )
                )
            if i == 1:
                for j in range(1, 3):
                    tile_pos = (
                        inner_left + i * stock_width + stock_width / 2,
                        inner_top + title_height + j * stock_height / 3,
                    )
                    self.tiles.append(
                        Inventory_Tile(
                            tile_pos, (99, 99), 20, self.color, piece=Beetle(self.color)
                        )
                    )
            if i == 2:
                for j in range(1, 3):
                    tile_pos = (
                        inner_left + i * stock_width + stock_width / 2,
                        inner_top + title_height + j * stock_height / 3,
                    )
                    self.tiles.append(
                        Inventory_Tile(
                            tile_pos, (99, 99), 20, self.color, piece=Spider(self.color)
                        )
                    )
            if i == 3:
                for j in [25, 67, 109]:
                    tile_pos = (
                        inner_left + i * stock_width + stock_width / 2,
                        inner_top + title_height + j * stock_height / 135,
                    )
                    self.tiles.append(
                        Inventory_Tile(
                            tile_pos,
                            (99, 99),
                            20,
                            self.color,
                            piece=Grasshopper(self.color),
                        )
                    )
            if i == 4:
                for j in [25, 67, 109]:
                    tile_pos = (
                        inner_left + i * stock_width + stock_width / 2,
                        inner_top + title_height + j * stock_height / 135,
                    )
                    self.tiles.append(
                        Inventory_Tile(
                            tile_pos, (99, 99), 20, self.color, piece=Ant(self.color)
                        )
                    )

        for tile in self.tiles:
            for piece in tile.pieces:
                piece.update_pos(tile.coords)

        FONT = pg.font.SysFont("Times New Norman", 24)
        if player == 0:
            self.font = FONT.render("Player 1 Inventory", True, WHITE)
        else:
            self.font = FONT.render("Player 2 Inventory", True, WHITE)
        self.title_rect = self.font.get_rect(
            center=(inner_left + inner_width / 2, inner_top + title_height / 2)
        )

    def draw(self, background, pos):
        pg.draw.rect(background, BLACK, self.back_panel)
        pg.draw.rect(background, PANEL, self.inner_panel)
        pg.draw.rect(background, PANEL, self.title_rect)
        for i in range(0, len(self.tile_rects)):
            pg.draw.rect(background, self.color, self.tile_rects[i])

        background.blit(self.font, self.title_rect)
        pg.display.flip()

    def get_piece(self, piece_type):
        """
        Retrieve an available piece of the specified type

        :param piece_type: Type of piece to retrieve (str)
        :return: Piece if available, None otherwise
        """
        # Check if any pieces of this type are available
        if self.available_pieces.get(piece_type.__name__, 0) > 0:
            # Find the first inventory tile with a matching piece type
            for tile in self.tiles:
                if tile.has_pieces() and isinstance(tile.pieces[-1], piece_type):
                    # Reduce available piece count
                    self.available_pieces[piece_type.__name__] -= 1
                    # Return and remove the piece from the tile
                    return tile.remove_piece()
        return None

    def has_pieces(self):
        """
        Check if the inventory has any pieces available

        :return: Boolean indicating if pieces are available
        """
        return any(count > 0 for count in self.available_pieces.values())

    def get_available_piece_types(self):
        """
        Get a list of piece types still available in the inventory

        :return: List of piece types with remaining pieces
        """
        available_types = []
        piece_map = {
            "Queen": Queen,
            "Beetle": Beetle,
            "Spider": Spider,
            "Grasshopper": Grasshopper,
            "Ant": Ant,
        }

        for piece_name, count in self.available_pieces.items():
            if count > 0:
                available_types.append(piece_map[piece_name])

        return available_types
