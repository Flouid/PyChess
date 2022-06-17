import numpy as np
from piece import Piece


class Board:
    """A class for representing an entire board state. Constructed from and capable of constructing
    unique string encodings. Stores a board as a 2D numpy array of pieces."""

    # string encodings
    default_board: str = 'rnbqkbnrppppppppeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeePPPPPPPPRNBQKBNR11110'
    empty_board: str = 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee11110'

    # state data
    lkc: int = 1
    lqc: int = 1
    dkc: int = 1
    dqc: int = 1
    move: int = 0

    def __init__(self, board=default_board):
        if board is None:
            self.board = self.init_board()
        elif board == 'empty':
            self.board = self.read_board(self.empty_board)
        else:
            self.board = self.read_board(board)

            self.lkc = int(board[64])
            self.lqc = int(board[65])
            self.dkc = int(board[66])
            self.dqc = int(board[67])
            self.move = int(board[68:])

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

    def __repr__(self):
        return self.str()

    @staticmethod
    def init_board():
        board = np.zeros((8, 8), dtype=str)
        for r in range(8):
            for c in range(8):
                board[r, c] = 'e'
        return board
