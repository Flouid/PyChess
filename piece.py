import numpy as np

class Piece:
    # piece data
    name  = None
    image = None
    role  = None

    # state data
    is_active = False

    def __init__(self, name):
        self.name = name

        if name == 'r':
            self.image = './chess_icons/dr.png'
            self.role = 'rook'
        elif name == 'n':
            self.image = './chess_icons/dkn.png'
            self.role = 'knight'
        elif name == 'b':
            self.image = './chess_icons/db.png'
            self.role = 'bishop'
        elif name == 'q':
            self.image = './chess_icons/dq.png'
            self.role = 'queen'
        elif name == 'k':
            self.image = './chess_icons/dk.png'
            self.role = 'king'
        elif name == 'p':
            self.image = './chess_icons/dp.png'
            self.role = 'pawn'
        elif name == 'R':
            self.image = './chess_icons/lr.png'
            self.role = 'rook'
        elif name == 'N':
            self.image = './chess_icons/lkn.png'
            self.role = 'knight'
        elif name == 'B':
            self.image = './chess_icons/lb.png'
            self.role = 'bishop'
        elif name == 'Q':
            self.image = './chess_icons/lq.png'
            self.role = 'queen'
        elif name == 'K':
            self.image = './chess_icons/lk.png'
            self.role = 'king'
        elif name == 'P':
            self.image = './chess_icons/lp.png'
            self.role = 'pawn'

    def __str__(self):
        return self.name


class Board:
    default_board = 'rnbqkbnrppppppppeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeePPPPPPPPRNBQKBNR11110'
    empty_board   = 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee11110'

    lkc   = 1
    lqc   = 1
    dkc   = 1
    dqc   = 1
    move  = 0

    def __init__(self, board=default_board):
        if board is None:
            self.board = self.init_board()
        elif board == 'empty':
            self.board = self.read_board(self.empty_board)
        else:
            self.board = self.read_board(board)

            self.lkc    = int(board[64])
            self.lqc    = int(board[65])
            self.dkc    = int(board[66])
            self.dqc    = int(board[67])
            self.move   = int(board[68:])

    def read_board(self, board):
        """Read a board encoded as a string"""
        # create an empty board of type piece
        pieces = np.zeros((8, 8), dtype=Piece)

        # for each character in the board range of the encoding, map 'e' to none and everything else to a piece
        for i in range(64):
            if board[i] == 'e':
                pieces[i // 8, i % 8] = None
            else:
                pieces[i // 8, i % 8] = Piece(board[i])

        return pieces

    def __str__(self):
        """Encode the board state as a string"""
        out = ''
        # for every place on the board, write it as a single character
        for r in range(8):
            for c in range(8):
                if self.board[r, c] is None:
                    out += 'e'
                else:
                    out += str(self.board[r, c])
        # use four bits for the states of castling in each corner, and store the move number
        return out + str(self.lkc) + str(self.lqc) + str(self.dkc) + str(self.dqc) + str(self.move)

    def init_board(self):
        board = np.zeros((8, 8), dtype=str)
        for r in range(8):
            for c in range(8):
                board[r, c] = 'e'
        return board
