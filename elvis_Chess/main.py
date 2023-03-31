import easygui
import pygame
import pygame as pg
from easygui import enterbox, msgbox
from pygame import mixer
from elvis_Chess import ChessOpeningDatabaseConnector

from elvis_Chess import ChessEngine


WIDTH = HEIGHT = 545
BOARD_WIDTH = BOARD_HEIGHT = 512
DIMENSION = 8  # 8x8 chess board
SQ_SIZE = BOARD_HEIGHT // DIMENSION  # --> Square sizes
FPS = 10
IMAGES = {}
TITLE = "Chess v3"
COLORS = {'dark': '#769656', 'light': '#eeeed2', 'background': '#2E282A', 'font': '#cecdcd'}

screen = pg.display.set_mode((WIDTH, HEIGHT))


def load_images():
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bp", "br", "bn", "bb", "bq", "bk"]
    for piece in pieces:
        IMAGES[piece] = pg.image.load("./my_chess/chess_pieces/" + piece + ".png")


def draw_coordinates(screen):
    font = pg.font.SysFont("Arial", 15)
    sq_offset = SQ_SIZE // 2 - 5
    for r in range(DIMENSION):
        # draw a to h on the bottom
        text = font.render(chr(r + 97), True, pg.Color(COLORS['font']))
        screen.blit(text, (r * SQ_SIZE + sq_offset, BOARD_HEIGHT + 10))
        # draw 1 to 8 on the right
        text = font.render(str(8 - r), True, pg.Color(COLORS['font']))
        screen.blit(text, (BOARD_WIDTH + 10, r * SQ_SIZE + sq_offset))


def draw_board(screen):
    # top left square is always light
    colors = [COLORS['light'], COLORS['dark']]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            pg.draw.rect(screen, color, pg.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    draw_coordinates(screen)


def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], pg.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_game_state(screen, gs):
    draw_board(screen)
    # add in piece highlighting or move suggestions (later)
    draw_pieces(screen, gs.board_2d_representation)  # draw pieces on top of squares


def print_ascii_pompt():
    with open('ascii_prompt.txt', 'r') as file:
        print(file.read())


# handle user input and updating the graphics
def main():
    pg.init()
    pg.display.set_caption(TITLE)
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color(COLORS['background']))


    # change param to false to play against ChessAI algorithm
    gamestate = ChessEngine.GameState(False)

    load_images()  # only do this once

    continue_game = True

    print_ascii_pompt()

    selected_square = ()  # no square is selected, keep track of last click of user (tuple: (col, row))
    player_clicks = []  # keep track of player clicks (two tuples: [(6, 4), (4, 4)])
    players_turn = True  # player is white, stockfish is black
    recording_state = False

    while continue_game:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                continue_game = False
            # mouse handler
            elif event.type == pg.MOUSEBUTTONDOWN:
                location = pg.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                selected_square = (col, row)
                # check if there is a piece on the first square
                if len(player_clicks) == 0 and not gamestate.square_has_piece(col, row):
                    selected_square = ()
                    player_clicks = []
                    print("No piece on selected square. Try again.")

                elif players_turn:
                    player_clicks.append(selected_square)  # append for both 1st and 2nd
                    pg.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

                if len(player_clicks) == 2 and players_turn:  # after 2nd click
                    try:
                        former_fen = gamestate.board.board_fen()
                        move = gamestate.make_move(player_clicks[0], player_clicks[1])
                        mixer.music.play()
                        players_turn = False
                        print("Player move: " + str(player_clicks[0]) + str(player_clicks[1]))
                        print("Your move: ", move)
                        print("-----------------------")
                        if (recording_state == True):
                            players_turn = True
                            ChessOpeningDatabaseConnector.insert_opening_moves(former_fen, move)
                        else:
                            print("TURN: BLACK \nPress Space to generate a move for black.")
                    except ValueError:
                        print("Invalid move. Try again.")

                    pg.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    selected_square = ()  # reset user clicks
                    player_clicks = []
                    continue_game = not gamestate.game_over()
            # key handler
            elif event.type == pg.KEYDOWN:
                # check if user wants to record opening
                if event.key == pg.K_o:
                    if (recording_state == True):
                        opening_stop = easygui.ynbox('Do you want to reset the game and stop the opening recording?',
                                                     'Opening stop', ('Yes', 'No'))
                        if (opening_stop):
                            recording_state = False
                            gamestate.reset_game();
                    else:
                        # check if User wants to record an Opening
                        opening_question = easygui.ynbox('Do you want to reset the game and record an opening?',
                                                         'Opening Question', ('Yes', 'No'))
                        if (opening_question == True):
                            text = "Enter name of Opening"
                            title = "Opening"
                            # creating a enter box
                            output = enterbox(text, title)
                            ChessOpeningDatabaseConnector.insert_opening_name(output)
                            gamestate.reset_game()
                            recording_start = easygui.msgbox(
                                'Start recording your opening, end recording by pressing o', 'Recording start')
                        if (recording_start == 'OK'):
                            recording_state = True

                # get turn from AI
                if event.key == pg.K_SPACE and not players_turn:
                    try:
                        print("Generating move for black...")
                        move_of_stockfish = gamestate.ai_make_move()
                        print("Move: ", move_of_stockfish)
                        mixer.music.play()
                        players_turn = True
                        print("-----------------------")
                        print("TURN: WHITE")
                    except ValueError:
                        print(ValueError)
                        print("Error: AI move failed.")
                        continue_game = False
                # undo move
                if event.key == pg.K_u:
                    try:
                        print("Undo last move...")
                        move = gamestate.undo_move()
                        print("Move undone: ", move)
                        players_turn = not players_turn
                    except IndexError:
                        print("No move to undo.")
                # reset game
                if event.key == pg.K_r:
                    print("Reset game to starting position...")
                    gamestate.reset_game()
                    players_turn = gamestate.whites_turn()
                    print("Game reset.")

        draw_game_state(screen, gamestate)
        clock.tick(FPS)
        pg.display.flip()

    pg.quit()
    print("Game Over")
    res = gamestate.get_game_result()
    print(res)


if __name__ == '__main__':
    main()
