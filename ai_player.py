import time

class MinimaxAlphaBeta:
    def __init__(self, max_depth, time_limit):
        self.max_depth = max_depth
        self.time_limit = time_limit

    def minimax(self, state, depth, alpha, beta, maximizing_player, start_time, get_valid_moves, make_move, undo_move, evaluate, is_terminal):
        """
        Minimax algorithm with alpha-beta pruning.

        Args:
            state: The current game state.
            depth: Remaining depth to explore.
            alpha: The best score for the maximizing player.
            beta: The best score for the minimizing player.
            maximizing_player: Boolean, True if it's the maximizing player's turn.
            start_time: Start time for time limit enforcement.
            get_valid_moves: Function to get valid moves for a state.
            make_move: Function to apply a move to the state.
            undo_move: Function to undo a move on the state.
            evaluate: Function to evaluate a terminal or depth-limited state.
            is_terminal: Function to check if the game is over.

        Returns:
            (best_move, best_score): Tuple of the best move and its evaluation score.
        """
        if time.time() - start_time > self.time_limit:
            return None, evaluate(state)

        if depth == 0 or is_terminal(state):
            return None, evaluate(state)

        valid_moves = get_valid_moves(state)
        if not valid_moves:
            return None, evaluate(state)

        best_move = None

        if maximizing_player:
            max_eval = float("-inf")
            for move in valid_moves:
                make_move(state, move)
                _, eval = self.minimax(state, depth - 1, alpha, beta, False, start_time, get_valid_moves, make_move, undo_move, evaluate, is_terminal)
                undo_move(state, move)

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
                make_move(state, move)
                _, eval = self.minimax(state, depth - 1, alpha, beta, True, start_time, get_valid_moves, make_move, undo_move, evaluate, is_terminal)
                undo_move(state, move)

                if eval < min_eval:
                    min_eval = eval
                    best_move = move

                beta = min(beta, eval)
                if beta <= alpha:
                    break

            return best_move, min_eval

    def get_best_move(self, state, get_valid_moves, make_move, undo_move, evaluate, is_terminal):
        """
        Find the best move using iterative deepening.

        Args:
            state: The current game state.
            get_valid_moves: Function to get valid moves for a state.
            make_move: Function to apply a move to the state.
            undo_move: Function to undo a move on the state.
            evaluate: Function to evaluate a terminal or depth-limited state.
            is_terminal: Function to check if the game is over.

        Returns:
            The best move found.
        """
        start_time = time.time()
        valid_moves = get_valid_moves(state)

        if not valid_moves:
            return None

        overall_best_move = valid_moves[0]

        for depth in range(1, self.max_depth + 1):
            if time.time() - start_time > self.time_limit:
                break

            best_move, _ = self.minimax(
                state, depth, float("-inf"), float("inf"), True, start_time,
                get_valid_moves, make_move, undo_move, evaluate, is_terminal
            )

            if best_move is not None:
                overall_best_move = best_move

        return overall_best_move
