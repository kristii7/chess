import chess
class Game:
    def __init__(self):
        self.board = chess.Board()
        self.selected = None
        self.valid_moves = []
        self.promotion_move = None
        self.awaiting_promotion = False

    def select(self, square):
        if self.awaiting_promotion:
            return

        if self.selected is None:
            piece = self.board.piece_at(square)
            if piece and piece.color == self.board.turn:
                self.selected = square
                self.valid_moves = [
                    m for m in self.board.legal_moves if m.from_square == square
                ]
        else:
            for move in self.valid_moves:
                if move.to_square == square:
                    if self.is_promotion(move):
                        self.promotion_move = move
                        self.awaiting_promotion = True
                        return
                    self.board.push(move)
            self.selected = None
            self.valid_moves = []

    def is_promotion(self, move):
        piece = self.board.piece_at(move.from_square)
        return piece and piece.piece_type == chess.PAWN and (
            chess.square_rank(move.to_square) in [0,7]
        )
