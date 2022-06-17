
from dataclasses import dataclass


def create_piece(code):
    if code == 'r':
        return Rook(code, './chess_icons/dr.png', False)
    elif code == 'n':
        return Knight(code, './chess_icons/dkn.png', False)
    elif code == 'b':
        return Bishop(code, './chess_icons/db.png', False)
    elif code == 'q':
        return Queen(code, './chess_icons/dq.png', False)
    elif code == 'k':
        return King(code, './chess_icons/dk.png', False)
    elif code == 'p':
        return Pawn(code, './chess_icons/dp.png', False)
    elif code == 'R':
        return Rook(code, './chess_icons/lr.png', True)
    elif code == 'N':
        return Knight(code, './chess_icons/lkn.png', True)
    elif code == 'B':
        return Bishop(code, './chess_icons/lb.png', True)
    elif code == 'Q':
        return Queen(code, './chess_icons/lq.png', True)
    elif code == 'K':
        return King(code, './chess_icons/lk.png', True)
    elif code == 'P':
        return Pawn(code, './chess_icons/lp.png', True)


@dataclass
class Piece:
    """A class for representing a single piece on the board. 
    Constructor takes a single unique character code for a piece and constructs the piece accordingly"""
    # piece data
    code: str
    image: str
    isLight: bool

    def __str__(self):
        return self.code

    def __repr__(self):
        return self.__str__()

class Rook(Piece):
    pass

class Knight(Piece):
    pass

class Bishop(Piece):
    pass

class Queen(Piece):
    pass

class King(Piece):
    pass

class Pawn(Piece):
    en_passant: bool = False
    can_ep_cap: bool = True