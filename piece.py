from dataclasses import dataclass
from position import Position
from move import Move


def create_piece(code, ep=None, can_ep=None, can_castle=None):
    if code == 'r':
        return Rook(code, './chess_icons/dr.png', False, can_castle)
    elif code == 'n':
        return Knight(code, './chess_icons/dkn.png', False)
    elif code == 'b':
        return Bishop(code, './chess_icons/db.png', False)
    elif code == 'q':
        return Queen(code, './chess_icons/dq.png', False)
    elif code == 'k':
        return King(code, './chess_icons/dk.png', False)
    elif code == 'p':
        return Pawn(code, './chess_icons/dp.png', False, ep, can_ep)
    elif code == 'R':
        return Rook(code, './chess_icons/lr.png', True, can_castle)
    elif code == 'N':
        return Knight(code, './chess_icons/lkn.png', True)
    elif code == 'B':
        return Bishop(code, './chess_icons/lb.png', True)
    elif code == 'Q':
        return Queen(code, './chess_icons/lq.png', True)
    elif code == 'K':
        return King(code, './chess_icons/lk.png', True)
    elif code == 'P':
        return Pawn(code, './chess_icons/lp.png', True, ep, can_ep)


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
    can_castle: bool

    def __init__(self, code, image, isLight, canCaste):
        super(Rook, self).__init__(code, image, isLight)
        self.can_castle = canCaste

    def generate_moves(self, board, begin, isLight):
        """Generates all of the moves possible for the current piece given that it is a rook"""
        moves = []

        # determine the distance to the edge of the board in each direction
        r_range = range(0 - begin.r, 7 - begin.r)
        c_range = range(0 - begin.c, 7 - begin.c)

        # find the minimum and maximum of each range
        min_rval = min(r_range)
        max_rval = max(r_range)
        min_cval = min(c_range)
        max_cval = min(c_range)

        # find the limits of where the rook can travel along the rows
        dist = 1
        while True:
            break

            
        # find the limits of where the rook can travel along the columns
        dist = 1
        while True:
            break

        return moves

class Knight(Piece):
    def generate_moves(self, board, begin, isLight):
        return []

class Bishop(Piece):
    def generate_moves(self, board, begin, isLight):
        return []

class Queen(Piece):
    def generate_moves(self, board, begin, isLight):
        return []

class King(Piece):
    def generate_moves(self, board, begin, isLight):
        return []

class Pawn(Piece):
    en_passant: bool
    can_ep_cap: bool

    def __init__(self, code, image, isLight, ep, can_ep):
        super(Pawn, self).__init__(code, image, isLight)
        self.en_passant = ep
        self.can_ep_cap = can_ep
    
    def generate_moves(self, board, begin, isLight):
        """Generates all of the moves possible for the current piece given that it is a pawn"""
        moves = []

        # pawn move direction is determined by color
        if self.isLight:
            # range is negative for light since it moves up the board
            max_range = [-1 * n for n in range(1, 2 + (begin.r == 6))]
        else:
            # range is positive for dark since it moves down the board
            max_range = list(range(1, 2 + (begin.r == 1)))

        # check for en passant
        moves.extend(self.check_en_passant(begin, board, isLight))

        # iterate down the range of the pawn
        for n in max_range:
            # stop the search if the pawn would move off the edge of the board
            if begin.r + n < 0 or begin.r + n > 7:
                break

            # calculate potential attacks
            if abs(n) == 1:
                # account for the west boundary of the board
                if begin.c > 0:
                    west = Position(begin.r + n, begin.c - 1)
                    if west.contains_enemy_piece(board, isLight):
                        moves.append(Move(begin, west))
                # account for the east boundary of the board
                if begin.c < 7:
                    east = Position(begin.r + n, begin.c + 1)
                    if east.contains_enemy_piece(board, isLight):
                        moves.append(Move(begin, east))

            # calculate the position of the landing tile
            target = Position(begin.r + n, begin.c)
            # if the current tile does not contain an allied piece, it is a valid move
            if not target.contains_piece(board):
                moves.append(Move(begin, target))
            # an allied piece cannot be jumped over, so stop searching
            else:
                break

        return moves

    def check_en_passant(self, begin, board, isLight):
        moves = []

        # calculate the en passant offset
        if isLight:
            offset = -1
        else:
            offset = 1

        # check for en passant, accounting for boundaries of the board
        if begin.c > 0:
            west = Position(begin.r, begin.c - 1)
            # check if there is a pawn directly next to the current pawn
            if west.contains_enemy_piece(board, isLight) and isinstance(board.board[west.r, west.c], Pawn):
                # check if the pawn can be captured with en passant and the current pawn can capture with en passant
                if self.can_ep_cap and board.board[west.r, west.c].en_passant:
                    moves.append(Move(begin, Position(west.r + offset, west.c), True))
        # account for east side of the board
        if begin.c < 7:
            east = Position(begin.r, begin.c + 1)
            # check if there is an enemy pawn directly to the east of the current pawn
            if east.contains_enemy_piece(board, isLight) and isinstance(board.board[east.r, east.c], Pawn):
                # check if the pawn can be captured with en-passant
                if self.can_ep_cap and board.board[east.r, east.c].en_passant:
                    moves.append(Move(begin, Position(east.r + offset, east.c), True))

        return moves
