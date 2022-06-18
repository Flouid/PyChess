from dataclasses import dataclass


@dataclass
class Position:
    """A class for representing a single position as a set of coordinates.
    Coordinates are encoded (r, c) where r is the row and c is the column, 
    with the origin being in the top left"""
    r: int
    c: int

    def __eq__(self, __o):
        return __o.r == self.r and __o.c == self.c

    def __add__(self, __o):
        return Position(self.r + __o.r, self.c + __o.c)

    def __sub__(self, __o):
        return Position(self.r - __o.r, self.c - __o.c)

    def __str__(self):
        return f'({self.r}, {self.c})'

    def __repr__(self):
        return self.__str__()

    def is_on_board(self):
        """Checks if a given position is on the board"""
        return (0 <= self.r <= 7) and (0 <= self.c <= 7)

    def contains_piece(self, board):
        """Checks if a tile on a given board contains any piece"""
        return board.board[self.r, self.c] is not None

    def contains_enemy_piece(self, board, isLight):
        """Checks if a tile on a given board contains an enemy piece"""
        return board.board[self.r, self.c] is not None and board.board[self.r, self.c].isLight != isLight

    def contains_allied_piece(self, board, isLight):
        """Checks if a tile on a given board contains an allied piece"""
        return board.board[self.r, self.c] is not None and board.board[self.r, self.c].isLight == isLight
