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
        start_x = 660
        start_y = 50

        line_height = 25

        # background panel
        pygame.draw.rect(self.screen, (30, 30, 30), (640, 0, 260, 720))

        for i, text in enumerate(game.move_descriptions):
            y = start_y + i * line_height - game.scroll_offset

            # only draw visible area (prevents ghost overlap)
            if 0 <= y <= 700:
                label = self.font.render(f"{i + 1}. {text}", True, WHITE)
                self.screen.blit(label, (start_x, y))






    def draw_promotion_popup(self):
        pygame.draw.rect(self.screen, (200, 200, 200), (160, 200, 320, 80))
        pieces = ['q', 'r', 'b', 'n']
        for i, p in enumerate(pieces):
            img = self.images['w' + p]
            self.screen.blit(img, (180 + i * 70, 210))


    def show_message(self, text, color=RED):
        label = self.big_font.render(text, True, color)
        self.screen.blit(label, (WIDTH//2 - label.get_width()//2, HEIGHT-45))
