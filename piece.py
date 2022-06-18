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

    def generate_moves(self, board, pos, isLight):
        """Generates all of the moves possible for the current piece given that it is a rook"""
        moves = []
        unblocked_directions = {'N': True, 'E': True, 'S': True, 'W': True}

        def march(direction, r_offset, c_offset):
            target = pos + Position(r_offset, c_offset)
            # only proceed if the target is actually on the board and the direction is unblocked
            if target.is_on_board() and unblocked_directions[direction]:
                # if the tile is empty, add a move
                if board.board[target.r, target.c] is None:
                    moves.append(Move(pos, target))
                # if the tile contains an enemy piece, add a move and mark the direction as blocked
                elif target.contains_enemy_piece(board, isLight):
                    moves.append(Move(pos, target))
                    unblocked_directions[direction] = False
                # if the tile contains an allied piece, mark the direction as blocked
                elif target.contains_allied_piece(board, isLight):
                    unblocked_directions[direction] = False

        # try to march up to 7 tiles in each direction
        for d in range(1, 8):
            march('N', -d, 0)   # north
            march('E', 0, d)    # east
            march('S', d, 0)    # south
            march('W', 0, -d)   # west

        return moves

class Knight(Piece):
    def generate_moves(self, board, pos, isLight):
        """Generates all of the moves possible for the current piece given that it is a rook"""
        moves = []

        def lance(r_offset, c_offset):
            target = pos + Position(r_offset, c_offset)
            # only proceed if the target is actually on the board
            if target.is_on_board():
                # if the target tile is empty or contains an enemy piece then it is a valid move
                if board.board[target.r, target.c] is None or board.board[target.r, target.c].isLight != isLight:
                    moves.append(Move(pos, target))

        lance(-2, 1)    # 1 o'clock
        lance(-1, 2)    # 2 o'clock
        lance(1, 2)     # 4 o'clock
        lance(2, 1)     # 5 o'clock    
        lance(2, -1)    # 7 o'clock
        lance(1, -2)    # 8 o'clock
        lance(-1, -2)   # 10 o'clock
        lance(-2, -1)   # 11 o'clock

        return moves

class Bishop(Piece):
    def generate_moves(self, board, pos, isLight):
        return []

class Queen(Piece):
    def generate_moves(self, board, pos, isLight):
        return []

class King(Piece):
    def generate_moves(self, board, pos, isLight):
        return []

class Pawn(Piece):
    en_passant: bool
    can_ep_cap: bool

    def __init__(self, code, image, isLight, ep, can_ep):
        super(Pawn, self).__init__(code, image, isLight)
        self.en_passant = ep
        self.can_ep_cap = can_ep
    
    def generate_moves(self, board, pos, isLight):
        """Generates all of the moves possible for the current piece given that it is a pawn"""
        moves = []

        # pawn move direction is determined by color
        if self.isLight:
            # range is negative for light since it moves up the board
            max_range = [-1 * n for n in range(1, 2 + (pos.r == 6))]
        else:
            # range is positive for dark since it moves down the board
            max_range = list(range(1, 2 + (pos.r == 1)))

        # check for en passant
        moves.extend(self.check_en_passant(pos, board, isLight))

        # iterate down the range of the pawn
        for n in max_range:
            # stop the search if the pawn would move off the edge of the board
            if pos.r + n < 0 or pos.r + n > 7:
                break

            # calculate potential attacks
            if abs(n) == 1:
                # account for the west boundary of the board
                if pos.c > 0:
                    west = Position(pos.r + n, pos.c - 1)
                    if west.contains_enemy_piece(board, isLight):
                        moves.append(Move(pos, west))
                # account for the east boundary of the board
                if pos.c < 7:
                    east = Position(pos.r + n, pos.c + 1)
                    if east.contains_enemy_piece(board, isLight):
                        moves.append(Move(pos, east))

            # calculate the position of the landing tile
            target = Position(pos.r + n, pos.c)
            # if the current tile does not contain an allied piece, it is a valid move
            if not target.contains_piece(board):
                moves.append(Move(pos, target))
            # an allied piece cannot be jumped over, so stop searching
            else:
                break

        return moves

    def check_en_passant(self, pos, board, isLight):
        moves = []

        # calculate the en passant offset
        if isLight:
            offset = -1
        else:
            offset = 1

        # check for en passant, accounting for boundaries of the board
        if pos.c > 0:
            west = Position(pos.r, pos.c - 1)
            # check if there is a pawn directly next to the current pawn
            if west.contains_enemy_piece(board, isLight) and isinstance(board.board[west.r, west.c], Pawn):
                # check if the pawn can be captured with en passant and the current pawn can capture with en passant
                if self.can_ep_cap and board.board[west.r, west.c].en_passant:
                    moves.append(Move(pos, Position(west.r + offset, west.c), True))
        # account for east side of the board
        if pos.c < 7:
            east = Position(pos.r, pos.c + 1)
            # check if there is an enemy pawn directly to the east of the current pawn
            if east.contains_enemy_piece(board, isLight) and isinstance(board.board[east.r, east.c], Pawn):
                # check if the pawn can be captured with en-passant
                if self.can_ep_cap and board.board[east.r, east.c].en_passant:
                    moves.append(Move(pos, Position(east.r + offset, east.c), True))

        return moves
