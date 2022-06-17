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

    def __str__(self):
        return f'({self.r}, {self.c})'

    def __repr__(self):
        return self.__str__()

    def contains_enemy_piece(self, board, isLight):
        """Checks if a tile on a given board contains an enemy piece to a given color"""
        return board.board[self.r, self.c] is not None and board.board[self.r, self.c].isLight != isLight

    def does_share_color(self, board, isLight):
        """Checks if a tile on a given board contains a piece of a given color"""
        return board.board[self.r, self.c] is not None and board.board[self.r, self.c].isLight == isLight
