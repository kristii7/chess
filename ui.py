import pygame
import chess
from settings import *
import os

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("arial", 22)
        self.big_font = pygame.font.SysFont("arial", 36)
        self.images = {}
        self.load_images()

    def load_images(self):
        pieces = ['p','r','n','b','q','k']
        colors = ['w','b']
        for c in colors:
            for p in pieces:
                img = pygame.image.load(
                    os.path.join("assets", "pieces", f"{c}{p}.png")
                )
                self.images[c+p] = pygame.transform.scale(img, (SQ_SIZE, SQ_SIZE))

    def draw_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                color = WHITE if (row + col) % 2 == 0 else PINK
                pygame.draw.rect(
                    self.screen,
                    color,
                    (col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE)
                )

    def draw_pieces(self, board):
        for sq in chess.SQUARES:
            piece = board.piece_at(sq)
            if piece:
                col = chess.square_file(sq)
                row = 7 - chess.square_rank(sq)
                key = ('w' if piece.color else 'b') + piece.symbol().lower()
                self.screen.blit(self.images[key], (col*SQ_SIZE, row*SQ_SIZE))

    def highlight_moves(self, moves):
        for move in moves:
            col = chess.square_file(move.to_square)
            row = 7 - chess.square_rank(move.to_square)
            pygame.draw.rect(
                self.screen, BLUE,
                (col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE),
                4
            )

    def draw_move_history(self, game):
        start_x = BOARD_SIZE + 20
        start_y = 10

        line_height = 25


        # background panel
        pygame.draw.rect(
            self.screen,
            (134, 136, 138),
            (BOARD_SIZE, 0, PANEL_WIDTH, BOARD_SIZE)
        )

        #move history and capture divider
        divider_x = BOARD_SIZE + 260  # adjust this if needed

        pygame.draw.line(
            self.screen,
            (80, 80, 80),
            (divider_x, 0),
            (divider_x, BOARD_SIZE),
            2
        )


        for i, text in enumerate(game.move_descriptions):
            y = start_y + i * line_height - game.scroll_offset

            # only draw visible area
            if 0 <= y <= BOARD_SIZE - 20:
                label = self.font.render(f"{i + 1}. {text}", True, WHITE)
                self.screen.blit(label, (start_x, y))

    def draw_promotion_popup(self):
        pygame.draw.rect(self.screen, (200, 200, 200), (160, 200, 320, 80))
        pieces = ['q', 'r', 'b', 'n']
        for i, p in enumerate(pieces):
            img = self.images['w' + p]
            self.screen.blit(img, (180 + i * 70, 210))

    def show_message(self, text, color=RED):
        # clear message area first
        pygame.draw.rect(self.screen, BLACK, (0, HEIGHT - 60, WIDTH, 60))

        label = self.big_font.render(text, True, color)
        self.screen.blit(label, (WIDTH // 2 - label.get_width() // 2, HEIGHT - 45))

    def highlight_check(self, board):
        if not board.is_check():
            return

        # find the king of the side to move (the one in check)
        king_square = board.king(board.turn)

        if king_square is not None:
            col = chess.square_file(king_square)
            row = 7 - chess.square_rank(king_square)

            pygame.draw.rect(
                self.screen,
                RED,
                (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE),
                5
            )

    def draw_coordinates(self):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        # Bottom letters (a–h)
        for col in range(8):
            label = self.font.render(letters[col], True, GREEN)
            self.screen.blit(
                label,
                (col * SQ_SIZE + SQ_SIZE - 15, 8 * SQ_SIZE - 20)
            )

        # Left numbers (1–8)
        for row in range(8):
            number = str(8 - row)
            label = self.font.render(number, True, GREEN)
            self.screen.blit(
                label,
                (3, row * SQ_SIZE + 3)
            )

    def draw_captured_pieces(self, board):
        # starting counts
        start_counts = {
            chess.PAWN: 8,
            chess.KNIGHT: 2,
            chess.BISHOP: 2,
            chess.ROOK: 2,
            chess.QUEEN: 1
        }

        captured_white = []
        captured_black = []

        for piece_type, count in start_counts.items():
            white_left = len(board.pieces(piece_type, chess.WHITE))
            black_left = len(board.pieces(piece_type, chess.BLACK))

            captured_white += [piece_type] * (count - white_left)
            captured_black += [piece_type] * (count - black_left)

        start_x = BOARD_SIZE + 280
        y_white = 10
        y_black = 360

        white_label = self.font.render("White Captured", True, WHITE)
        black_label = self.font.render("Black Captured", True, WHITE)

        self.screen.blit(white_label, (start_x, y_white))
        self.screen.blit(black_label, (start_x, y_black))

        #captured white pieces
        for i, piece in enumerate(captured_white):
            key = 'w' + chess.piece_symbol(piece)
            img = self.images[key]
            self.screen.blit(img, (start_x + (i % 4) * 40, y_white + 30 + (i // 4) * 40))

        #captured black pieces
        for i, piece in enumerate(captured_black):
            key = 'b' + chess.piece_symbol(piece)
            img = self.images[key]
            self.screen.blit(img, (start_x + (i % 4) * 40, y_black + 30 + (i // 4) * 40))