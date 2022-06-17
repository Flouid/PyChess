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
