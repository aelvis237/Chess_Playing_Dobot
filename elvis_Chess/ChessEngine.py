# Storing the information about the current state of a chess game
# Determining the valid moves at the current state
# Storing the move log
import chess
from stockfish import Stockfish

STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
# STARTING_FEN = "1n1qkb1r/P1p2ppp/3r1n2/1p1ppb2/P1BPP3/5N2/2P2PPP/RNBQK2R w KQk - 0 1"
# STARTING_FEN = "4R3/7k/3QR3/8/8/8/8/4K3 w - - 0 1"
PATH_TO_STOCKFISH = ""


def _fen_to_2d_board(fen):
    res = []
    # split the fen string
    fen_split = fen.split(" ")
    fen_split = fen_split[0].split("/")
    # convert the fen string to a 2d board
    for row in fen_split:
        row_list = []
        for char in row:
            if char.isdigit():
                row_list.extend(["--"] * int(char))
            else:
                # check if char is upper case
                if char.isupper():
                    row_list.append("w" + char)
                else:
                    row_list.append("b" + char)
        res.append(row_list)

    return res


def coordinates_to_chess_notation(col, row):
    return chr(col + 97) + str(8 - row)


# wrapper for python-chess library
class GameState:

    def __init__(self):
        self.board_2d_representation = _fen_to_2d_board(STARTING_FEN)
        self.board = chess.Board(STARTING_FEN)
        self.stockfish = Stockfish(PATH_TO_STOCKFISH)
        self.stockfish.set_fen_position(STARTING_FEN)
        self.stockfish.set_skill_level(5)

    """
    makes a move on the board
    if pawn promotion, then promote to queen
    updates the board_2d_representation
    """
    def make_move(self, from_square, to_square):
        from_move = coordinates_to_chess_notation(*from_square)
        to_move = coordinates_to_chess_notation(*to_square)
        move = from_move + to_move
        # check for pawn promotion
        moving_piece = self.board_2d_representation[from_square[1]][from_square[0]]
        # check if moving piece has a p in it
        if (moving_piece == "wP" or moving_piece == "bp") and (to_square[1] == 0 or to_square[1] == 7):
            print("promoted pawn to queen")
            move += "q"

        self.board.push_san(move)
        # convert the new board to board_2d
        # refresh the fen position for stockfish
        self.stockfish.set_fen_position(self.board.fen())
        self.board_2d_representation = _fen_to_2d_board(self.board.fen())

        return move

    # check if there is a piece on the square
    def square_has_piece(self, col, row):
        return self.board_2d_representation[row][col] != "--"

    # check if the game is over
    def game_over(self):
        return self.board.is_game_over()

    def stockfish_move(self):
        best_move = self.stockfish.get_best_move()
        self.board.push_san(best_move)
        # update stockfish fen position
        self.stockfish.set_fen_position(self.board.fen())
        self.board_2d_representation = _fen_to_2d_board(self.board.fen())
        return best_move

    def print_board(self):
        for row in self.board_2d_representation:
            print(row)

    def get_game_result(self):
        return self.board.result()

    def undo_move(self):
        move = self.board.pop()
        self.stockfish.set_fen_position(self.board.fen())
        self.board_2d_representation = _fen_to_2d_board(self.board.fen())
        return move

    # reset board to STARTING_FEN
    def reset_game(self):
        self.board_2d_representation = _fen_to_2d_board(STARTING_FEN)
        self.board = chess.Board(STARTING_FEN)
        self.stockfish.set_fen_position(STARTING_FEN)

    def whites_turn(self):
        return self.board.turn