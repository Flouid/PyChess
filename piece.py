

class Piece:
    """A class for representing a single piece on the board. 
    Constructor takes a single unique character code for a piece and constructs the piece accordingly"""
    # piece data
    name: str = None
    image: str = None
    role: str = None
    light: bool = False
    en_passant: bool = False

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
            self.light = True
        elif name == 'N':
            self.image = './chess_icons/lkn.png'
            self.role = 'knight'
            self.light = True
        elif name == 'B':
            self.image = './chess_icons/lb.png'
            self.role = 'bishop'
            self.light = True
        elif name == 'Q':
            self.image = './chess_icons/lq.png'
            self.role = 'queen'
            self.light = True
        elif name == 'K':
            self.image = './chess_icons/lk.png'
            self.role = 'king'
            self.light = True
        elif name == 'P':
            self.image = './chess_icons/lp.png'
            self.role = 'pawn'
            self.light = True

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()
