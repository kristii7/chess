import chess

class AI:
    def __init__(self, depth=2):
        self.depth = depth

    def evaluate(self, board):
        values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9
        }
        score = 0
        for piece,val in values.items():
            score += len(board.pieces(piece, chess.WHITE)) * val
            score -= len(board.pieces(piece, chess.BLACK)) * val
        return score

    def minimax(self, board, depth, maximizing):
        if depth == 0 or board.is_game_over():
            return self.evaluate(board), None

        best_move = None
        if maximizing:
            max_eval = -9999
            for move in board.legal_moves:
                board.push(move)
                eval,_ = self.minimax(board, depth-1, False)
                board.pop()
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = 9999
            for move in board.legal_moves:
                board.push(move)
                eval,_ = self.minimax(board, depth-1, True)
                board.pop()
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return min_eval, best_move

    def choose_move(self, board):
        _, move = self.minimax(board, self.depth, False)
        return move
