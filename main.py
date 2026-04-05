import pygame
import chess
from game import Game
from ui import UI
from ai import AI
from settings import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Complete Chess")

clock = pygame.time.Clock()
game = Game()
ui = UI(screen)
ai = AI()

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and game.board.turn:
            x, y = pygame.mouse.get_pos()
            if y < WIDTH:
                col = x // SQ_SIZE
                row = y // SQ_SIZE
                square = chess.square(col, 7-row)
                game.select(square)

    # AI move
    if not game.board.turn and not game.board.is_game_over():
        move = ai.choose_move(game.board)
        game.board.push(move)

    ui.draw_board()
    ui.highlight_moves(game.valid_moves)
    ui.draw_pieces(game.board)
    ui.draw_move_history(game.board)

    if game.board.is_checkmate():
        ui.show_message("CHECKMATE")
    elif game.board.is_check():
        ui.show_message("CHECK")

    if game.awaiting_promotion and event.type == pygame.MOUSEBUTTONDOWN:
        x, y = pygame.mouse.get_pos()
        if 200 <= y <= 280:
            index = (x - 180) // 70
            if 0 <= index <= 3:
                promo = [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT][index]
                game.promotion_move.promotion = promo
                game.board.push(game.promotion_move)
                game.awaiting_promotion = False
                game.promotion_move = None

    pygame.display.flip()

pygame.quit()
