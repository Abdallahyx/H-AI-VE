import time
from move_checker import is_valid_move, game_is_over
from pieces import Queen, Beetle, Spider, Ant, Grasshopper
from settings import PIECE_WHITE
from tile import Start_Tile


class AIPlayer:
    def __init__(self, color, difficulty=2):
        self.color = color
        self.difficulty = max(1, min(difficulty, 4))
        self.queen_placed = False
        self.time_limit = 5 if self.difficulty == 4 else 2
        self.max_depth = self.difficulty * 2

        # Strategic piece values
        self.piece_values = {
            Queen: 1000,
            Beetle: 80,  # Important for attacking and covering
            Spider: 40,  # Good for pinning pieces
            Ant: 60,  # Excellent mobility for surrounding
            Grasshopper: 30,
        }

    def _get_valid_moves(self, state):
        """Get all valid moves for the current state"""
        valid_moves = []

        # Special case for first move (turn 1)
        if state.turn == 1:
            # Find the start tile and first piece to place
            start_tile = next(
                tile for tile in state.board_tiles if type(tile) is Start_Tile
            )
            inventory = (
                state.white_inventory
                if self.color == PIECE_WHITE
                else state.black_inventory
            )
            first_piece_tile = next(
                tile for tile in inventory.tiles if tile.has_pieces()
            )

            if first_piece_tile and start_tile:
                state.moving_piece = first_piece_tile.pieces[-1]
                if is_valid_move(state, first_piece_tile, start_tile):
                    return [(first_piece_tile, start_tile)]
            return []

        # Special case for second move (turn 2)
        if state.turn == 2:
            inventory = (
                state.white_inventory
                if self.color == PIECE_WHITE
                else state.black_inventory
            )
            piece_tile = next(tile for tile in inventory.tiles if tile.has_pieces())
            if piece_tile:
                state.moving_piece = piece_tile.pieces[-1]
                for board_tile in state.board_tiles:
                    if is_valid_move(state, piece_tile, board_tile):
                        valid_moves.append((piece_tile, board_tile))
            return valid_moves

        # Normal move generation for later turns
        movable_tiles = [
            tile
            for tile in state.get_tiles_with_pieces(include_inventory=True)
            if tile.has_pieces() and tile.pieces[-1].color == self.color
        ]

        # Get all potential destination tiles
        all_occupied_tiles = state.get_tiles_with_pieces()
        potential_destinations = set()

        # Add tiles adjacent to the hive
        for tile in all_occupied_tiles:
            for adj in tile.adjacent_tiles:
                if not adj.has_pieces() or isinstance(tile.pieces[-1], Beetle):
                    potential_destinations.add(adj)

        # Check moves for each piece
        for current_tile in movable_tiles:
            piece = current_tile.pieces[-1]
            state.moving_piece = piece

            for dest in potential_destinations:
                if is_valid_move(state, current_tile, dest):
                    valid_moves.append((current_tile, dest))

        return valid_moves

    def _calculate_distance(self, tile1, tile2):
        """Calculate hexagonal distance between two tiles"""
        q1, r1 = tile1.axial_coords
        q2, r2 = tile2.axial_coords
        return (abs(q1 - q2) + abs(r1 - r2) + abs(-q1 - r1 + q2 + r2)) // 2

    def _evaluate_position(self, state):
        """Evaluate the current board position"""
        score = 0
        friendly_queen = None
        enemy_queen = None
        friendly_pieces = []
        enemy_pieces = []

        # Find queens and categorize pieces
        for tile in state.get_tiles_with_pieces():
            piece = tile.pieces[-1]
            if isinstance(piece, Queen):
                if piece.color == self.color:
                    friendly_queen = tile
                else:
                    enemy_queen = tile

            if piece.color == self.color:
                friendly_pieces.append((tile, piece))
                score += self.piece_values[type(piece)]
            else:
                enemy_pieces.append((tile, piece))
                score -= self.piece_values[type(piece)]

        # Game ending conditions take highest priority
        if self._is_queen_surrounded(enemy_queen):
            return float("inf")
        if self._is_queen_surrounded(friendly_queen):
            return float("-inf")

        # Queen safety evaluation
        if friendly_queen:
            score += self._evaluate_queen_safety(friendly_queen, True)
        if enemy_queen:
            score += self._evaluate_attack_potential(enemy_queen, friendly_pieces)
            score -= (
                self._evaluate_queen_safety(enemy_queen, False) * 0.5
            )  # Reduced defensive weight

        # Early game evaluation
        if state.turn <= 6:
            if not friendly_queen and state.turn >= 4:
                score -= 500  # Penalize not placing queen early
            score += len(friendly_pieces) * 20  # Encourage piece development

        # Position evaluation
        score += self._evaluate_piece_positions(
            friendly_pieces, enemy_pieces, enemy_queen
        )

        return score

    def _evaluate_queen_safety(self, queen_tile, is_friendly):
        """Evaluate queen's safety"""
        if not queen_tile:
            return -1000 if is_friendly else 1000

        score = 0
        surrounding_pieces = [t for t in queen_tile.adjacent_tiles if t.has_pieces()]
        empty_spaces = [t for t in queen_tile.adjacent_tiles if not t.has_pieces()]

        num_surrounding = len(surrounding_pieces)
        friendly_surrounding = sum(
            1 for t in surrounding_pieces if t.pieces[-1].color == self.color
        )

        # Safety scoring based on surrounding pieces
        if is_friendly:
            if num_surrounding <= 1:
                score -= 200  # Very exposed
            elif num_surrounding == 2:
                score += 50  # Good mobility
            elif num_surrounding == 3:
                score += friendly_surrounding * 40  # Reward friendly protection
            elif num_surrounding >= 4:
                score -= 150 * (
                    num_surrounding - 3
                )  # Heavily penalize being surrounded
        else:
            score += num_surrounding * 80  # Reward surrounding enemy queen

        # Mobility consideration
        score += len(empty_spaces) * (20 if is_friendly else -20)

        return score

    def _evaluate_attack_potential(self, enemy_queen, friendly_pieces):
        """Evaluate potential for attacking enemy queen"""
        if not enemy_queen:
            return 0

        score = 0
        queen_adjacents = enemy_queen.adjacent_tiles

        # Count pieces that could potentially move to surround the queen
        for tile, piece in friendly_pieces:
            if isinstance(piece, Beetle):
                # Beetles can climb, so they're especially valuable near enemy queen
                distance = self._calculate_distance(tile, enemy_queen)
                if distance <= 2:
                    score += 200 / (distance + 1)
            elif isinstance(piece, Ant):
                # Ants are highly mobile, reward them for being in play
                score += 50
            elif isinstance(piece, Spider):
                # Spiders are good for pinning pieces
                distance = self._calculate_distance(tile, enemy_queen)
                if distance <= 3:
                    score += 100 / (distance + 1)

        # Extra points for controlling spaces adjacent to enemy queen
        our_adjacent_pieces = sum(
            1
            for t in queen_adjacents
            if t.has_pieces() and t.pieces[-1].color == self.color
        )
        score += our_adjacent_pieces * 100

        return score

    def _evaluate_piece_positions(self, friendly_pieces, enemy_pieces, enemy_queen):
        """Evaluate the strategic positioning of pieces"""
        score = 0

        if not enemy_queen:
            return score

        # Reward pieces positioned between enemy pieces and their queen
        for tile, piece in friendly_pieces:
            if isinstance(piece, (Beetle, Spider)):
                blocking_score = 0
                for enemy_tile, _ in enemy_pieces:
                    if self._is_between(tile, enemy_tile, enemy_queen):
                        blocking_score += 50
                score += blocking_score

        # Reward control of key spaces
        for tile, piece in friendly_pieces:
            if len([t for t in tile.adjacent_tiles if t.has_pieces()]) >= 3:
                score += 30  # Reward pieces that help control multiple spaces

        return score

    def _is_between(self, piece_tile, enemy_tile, queen_tile):
        """Check if a piece is positioned between an enemy piece and their queen"""
        dist_total = self._calculate_distance(enemy_tile, queen_tile)
        dist_to_piece = self._calculate_distance(enemy_tile, piece_tile)
        dist_piece_to_queen = self._calculate_distance(piece_tile, queen_tile)
        return abs(dist_to_piece + dist_piece_to_queen - dist_total) <= 1

    def _is_queen_surrounded(self, queen_tile):
        """Check if a queen is surrounded"""
        if not queen_tile:
            return False
        return len([t for t in queen_tile.adjacent_tiles if t.has_pieces()]) == 6

    def _minimax(self, state, depth, alpha, beta, maximizing_player, start_time):
        """Minimax algorithm with alpha-beta pruning"""
        if time.time() - start_time > self.time_limit:
            return None, self._evaluate_position(state)

        if depth == 0 or game_is_over(state):
            return None, self._evaluate_position(state)

        valid_moves = self._get_valid_moves(state)
        if not valid_moves:
            return None, self._evaluate_position(state)

        best_move = None
        if maximizing_player:
            max_eval = float("-inf")
            for move in valid_moves:
                old_tile, new_tile = move
                # Make move
                piece = old_tile.pieces[-1]
                old_tile.remove_piece()
                new_tile.add_piece(piece)

                # Recursive evaluation
                _, eval = self._minimax(
                    state, depth - 1, alpha, beta, False, start_time
                )

                # Undo move
                piece = new_tile.remove_piece()
                old_tile.add_piece(piece)

                if eval > max_eval:
                    max_eval = eval
                    best_move = move

                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            return best_move, max_eval
        else:
            min_eval = float("inf")
            for move in valid_moves:
                old_tile, new_tile = move
                # Make move
                piece = old_tile.pieces[-1]
                old_tile.remove_piece()
                new_tile.add_piece(piece)

                # Recursive evaluation
                _, eval = self._minimax(state, depth - 1, alpha, beta, True, start_time)

                # Undo move
                piece = new_tile.remove_piece()
                old_tile.add_piece(piece)

                if eval < min_eval:
                    min_eval = eval
                    best_move = move

                beta = min(beta, eval)
                if beta <= alpha:
                    break

            return best_move, min_eval

    def get_best_move(self, state):
        """Get best move using iterative deepening"""
        start_time = time.time()
        valid_moves = self._get_valid_moves(state)

        if not valid_moves:
            return None, None

        # For first few turns, just pick the first valid move
        if state.turn <= 2:
            if valid_moves:
                old_tile, new_tile = valid_moves[0]
                state.moving_piece = old_tile.pieces[-1]
                return old_tile, new_tile
            return None, None

        overall_best_move = valid_moves[0]

        # Iterative deepening for later turns
        for depth in range(1, self.max_depth + 1):
            if time.time() - start_time > self.time_limit:
                break

            best_move, eval = self._minimax(
                state, depth, float("-inf"), float("inf"), True, start_time
            )

            if best_move is not None:
                overall_best_move = best_move

        if overall_best_move:
            state.moving_piece = overall_best_move[0].pieces[-1]
            return overall_best_move

        return None, None

    def _find_queen_piece(self, state):
        """Find queen piece in inventory or on board"""
        inventory = (
            state.white_inventory
            if self.color == PIECE_WHITE
            else state.black_inventory
        )

        # Check inventory first
        for tile in inventory.tiles:
            if (
                tile.has_pieces()
                and isinstance(tile.pieces[-1], Queen)
                and tile.pieces[-1].color == self.color
            ):
                return tile

        # Check board
        for tile in state.board_tiles:
            if tile.has_pieces():
                piece = tile.pieces[-1]
                if isinstance(piece, Queen) and piece.color == self.color:
                    return tile
        return None

    def place_queen(self, state):
        """Place queen using position evaluation"""
        queen_tile = self._find_queen_piece(state)
        if not queen_tile:
            return None, None

        valid_moves = []
        state.moving_piece = queen_tile.pieces[-1]

        for new_tile in state.board_tiles:
            if is_valid_move(state, queen_tile, new_tile):
                valid_moves.append((queen_tile, new_tile))

        if not valid_moves:
            return None, None

        best_move = valid_moves[0]
        best_score = float("-inf")

        for move in valid_moves:
            old_tile, new_tile = move
            # Make move
            piece = old_tile.pieces[-1]
            old_tile.remove_piece()
            new_tile.add_piece(piece)

            # Evaluate position
            score = self._evaluate_position(state)

            # Undo move
            piece = new_tile.remove_piece()
            old_tile.add_piece(piece)

            if score > best_score:
                best_score = score
                best_move = move

        return best_move
