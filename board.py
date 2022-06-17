import numpy as np
from piece import create_piece, Piece, Rook, Pawn


class Board:
    """A class for representing an entire board state. Constructed from and capable of constructing
    unique string encodings. Stores a board as a 2D numpy array of pieces."""

    # string encodings
    default_board: str = 'r1nbqkbnr1p01p01p01p01p01p01p01p01eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeP01P01P01P01P01P01P01P01R1NBQKBNR1'
    empty_board: str = 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'

    def __init__(self, board=default_board):
        if board is None:
            self.board = self.init_board()
        elif board == 'empty':
            self.board = self.read_board(self.empty_board)
        else:
            self.board = self.read_board(board)

    def read_board(self, board):
        """Read a board encoded as a string"""
        # create an empty board of type piece
        pieces = np.zeros((8, 8), dtype=Piece)

        pieces_idx = 0
        board_idx = 0
        while True:
            curr = board[board_idx]
            if curr == 'r' or curr == 'R':
                pieces[pieces_idx // 8, pieces_idx % 8] = create_piece(curr, \
                                                          can_castle=(board[board_idx+1] == '1'))
                pieces_idx += 1
                board_idx += 2
            elif board[board_idx] == 'p' or board[board_idx] == 'P':
                pieces[pieces_idx // 8, pieces_idx % 8] = create_piece(curr, \
                                                          ep=(board[board_idx+1] == '1'),  \
                                                          can_ep=(board[board_idx + 2] == '1'))
                pieces_idx += 1
                board_idx += 3
            else:
                pieces[pieces_idx // 8, pieces_idx % 8] = create_piece(curr)
                pieces_idx += 1
                board_idx += 1
            if pieces_idx == 64:
                break
    
        return pieces

    def __str__(self):
        """Encode the board state as a string"""
        out = ''
        # for every place on the board, write it as a single character
        for r in range(8):
            for c in range(8):
                # write an empty space
                if self.board[r, c] is None:
                    out += 'e'
                # write a rook and whether or not it can castle
                elif isinstance(self.board[r, c], Rook):
                    out += str(self.board[r, c])
                    if self.board[r, c].can_castle:
                        out += '1'
                    else:
                        out += '0'
                # write a pawn and it's en passant information
                elif isinstance(self.board[r, c], Pawn):
                    out += str(self.board[r, c])
                    if self.board[r, c].en_passant:
                        out += '1'
                    else:
                        out += '0'
                    if self.board[r, c].can_ep_cap:
                        out += '1'
                    else:
                        out += '0'
                # write any other piece
                else:
                    out += (str(self.board[r, c]))
        # use four bits for the states of castling in each corner, and store the move number
        return out

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def init_board():
        board = np.zeros((8, 8), dtype=str)
        for r in range(8):
            for c in range(8):
                board[r, c] = 'e'
        return board
