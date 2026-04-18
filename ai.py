import chess

class AI:
    def __init__(self, depth=2):
        self.depth = depth

    def evaluate(self, board):
        #Game-ending states FIRST
        if board.is_checkmate():
            if board.turn:  # side to move is checkmated
                return -9999
            else:
                return 9999

        if board.is_stalemate() or board.is_insufficient_material():
            return 0
        values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
        }
        score = 0
        for piece,val in values.items():
            score += len(board.pieces(piece, chess.WHITE)) * val
            score -= len(board.pieces(piece, chess.BLACK)) * val

        return score

    def minimax(self, board, depth, alpha, beta, maximizing):
        if depth == 0 or board.is_game_over():
            return self.evaluate(board), None

        best_move = None


        # Move ordering
        moves = list(board.legal_moves)
        moves.sort(key=lambda move: board.is_capture(move), reverse=True)

        if maximizing:
            max_eval = -9999

            for move in moves:
                board.push(move)
                eval, _ = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
#higher score= best move
                if eval > max_eval:
                    max_eval = eval
                    best_move = move

                alpha = max(alpha, eval)

                # Alpha-Beta pruning
                if beta <= alpha:
                    break

            return max_eval, best_move

        else:
            min_eval = 9999

            for move in moves:
                board.push(move)
                eval, _ = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()

                if eval < min_eval:
                    min_eval = eval
                    best_move = move

                beta = min(beta, eval)

                #  Alpha-Beta pruning
                if beta <= alpha:
                    break

            return min_eval, best_move

    def choose_move(self, board):
        if board.is_game_over():
            return None
        _, move = self.minimax(board, self.depth, -9999, 9999, False)
        return move