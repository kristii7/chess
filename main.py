import pygame
import chess
from game import Game
from ui import UI
from ai import AI
from settings import *

# ------------------- INIT -------------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Complete Chess")

clock = pygame.time.Clock()
game = Game()
ui = UI(screen)
ai = AI(depth=4)

running = True

# ------------------- MAIN LOOP -------------------
while running:
    clock.tick(60)

    # ------------------- EVENTS -------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #  KEYBOARD
        if event.type == pygame.KEYDOWN:
            # Undo last two moves (player + AI)
            if event.key == pygame.K_u:
                for _ in range(2):
                    if len(game.board.move_stack) > 0:
                        game.board.pop()

            # Restart game
            if event.key == pygame.K_r:
                game = Game()

        #  MOUSE
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            #  Promotion popup handling
            if game.awaiting_promotion:
                if 200 <= y <= 280:
                    index = (x - 180) // 70
                    if 0 <= index <= 3:
                        promo = [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT][index]
                        game.promotion_move.promotion = promo
                        game.board.push(game.promotion_move)
                        game.awaiting_promotion = False
                        game.promotion_move = None
                continue  # Skip normal click if promotion popup is active

            #  Normal piece selection / move
            if game.board.turn and y < WIDTH:
                col = x // SQ_SIZE
                row = y // SQ_SIZE
                square = chess.square(col, 7 - row)
                game.select(square)

    # ------------------- AI MOVE -------------------
    if not game.board.turn and not game.board.is_game_over():
        move = ai.choose_move(game.board)
        if move:
            game.board.push(move)

    # ------------------- DRAWING -------------------
    ui.draw_board()
    ui.highlight_moves(game.valid_moves)
    ui.draw_pieces(game.board)

    #  selected square highlight garne
    if game.selected is not None:
        col = chess.square_file(game.selected)
        row = 7 - chess.square_rank(game.selected)
        pygame.draw.rect(screen, GREEN,
                         (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE), 4)


    ui.draw_move_history(game.board)

    # Promotion popup
    if game.awaiting_promotion:
        ui.draw_promotion_popup()

    # Turn display
    turn_text = "White" if game.board.turn else "Black"
    label = ui.font.render(turn_text, True, BLACK)
    screen.blit(label, (650, 50))

    #  check or checkmate message
    if game.board.is_checkmate():
        ui.show_message("CHECKMATE")
    elif game.board.is_check():
        ui.show_message("CHECK")

    pygame.display.flip()

# ------------------- QUIT -------------------
pygame.quit()