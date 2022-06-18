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

    def march(self, pos, offset, board, direction=None, unblocked_directions=None):
        """A method to allow a piece to march in a provided direction provided it is not blocked.
        Wraps a number of common function calls together to make move calculation much more simple.
        Returns a move to a position at a given offset if possible, otherwise none."""            
        # calculate the position of the target
        target = pos + offset

        # case for tracking directions
        if unblocked_directions is not None and direction is not None:
            # if the direction is blocked or the target isn't on the board then stop now
            if not unblocked_directions[direction] or not target.is_on_board():
                return unblocked_directions, None
            # if the tile is empty, a move is possible
            if board.board[target.r, target.c] is None:
                return unblocked_directions, Move(pos, target)
            # if a tile contains an enemy piece, a move is possible but the direction is blocked
            if target.contains_enemy_piece(board, self.isLight):
                unblocked_directions[direction] = False
                return unblocked_directions, Move(pos, target)
            # if the tile contains an allied piece, the a move is impossible and the direction is blocked
            if target.contains_allied_piece(board, self.isLight):
                unblocked_directions[direction] = False
                return unblocked_directions, None
                
        # a move is possible so long as the target tile is on the board and doesn't contain an allied piece
        if target.is_on_board() and not target.contains_allied_piece(board, self.isLight):
            return Move(pos, target)
    
        # no move was possible
        return None


class Rook(Piece):
    can_castle: bool

    def __init__(self, code, image, isLight, canCaste):
        super(Rook, self).__init__(code, image, isLight)
        self.can_castle = canCaste

    def generate_moves(self, board, pos, isLight):
        """Generates all of the moves possible for the current piece given that it is a rook"""
        moves = []

        # named booleans for whether each direction is blocked and a list of names
        unblocked_directions = {'N': True, 'E': True, 'S': True, 'W': True}
        directions = ['N', 'E', 'S', 'W']

        # traverse the maximum range in each direction
        for d in range(1, 8):
            # all of the posible offsets for a rook
            offsets = [Position(-d, 0), Position(0, d), Position(d, 0), Position(0, -d)]
            # for each offset/direction, attempt to march d tiles and track if an obstruction is found
            for i, offset in enumerate(offsets):
                # attempt to march
                unblocked_directions, move = self.march(pos, offset, board, directions[i], unblocked_directions)

                # if a valid move was found then add it
                if move is not None:
                    moves.append(move)

        return moves

class Knight(Piece):
    def generate_moves(self, board, pos, isLight):
        """Generates all of the moves possible for the current piece given that it is a rook"""
        moves = []

        # offsets representing the eight places a knight can attack
        offsets = [Position(-2, 1), Position(-1, 2), Position(1, 2), Position(2, 1), 
                   Position(2, -1), Position(1, -2), Position(-1, -2), Position(-2, -1)]

        for offset in offsets:
            # attempt to march by jumping to the offset
            move = self.march(pos, offset, board)

            if move is not None:
                moves.append(move)

        return moves

class Bishop(Piece):
    def generate_moves(self, board, pos, isLight):
        """Generates all of the moves possible for the current piece given that it is a bishop"""
        moves = []

        # named booleans for whether each direction is blocked and a list of names
        unblocked_directions = {'NE': True, 'SE': True, 'SW': True, 'NW': True}
        directions = ['NE', 'SE', 'SW', 'NW']

        # traverse the maximum range in each direction
        for d in range(1, 8):
            # all of the posible offsets for a bishop
            offsets = [Position(-d, d), Position(d, d), Position(d, -d), Position(-d, -d)]
            # for each offset/direction, attempt to march d tiles and track if an obstruction is found
            for i, offset in enumerate(offsets):
                # attempt to march
                unblocked_directions, move = self.march(pos, offset, board, directions[i], unblocked_directions)

                # if a valid move was found then add it
                if move is not None:
                    moves.append(move)

        return moves

class Queen(Piece):
    def generate_moves(self, board, pos, isLight):
        """Generates all of the moves possible for the current piece given that it is a queen"""
        moves = []

        # named booleans for whether each direction is blocked and a list of names
        unblocked_directions = {'N': True, 'NE': True, 'E': True, 'SE': True, 'S': True, 'SW': True, 'W': True, 'NW': True}
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

        # traverse the maximum range in each direction
        for d in range(1, 8):
            # all of the posible offsets for a queen
            offsets = [Position(-d, 0), Position(-d, d), Position(0, d), Position(d, d), 
                       Position(d, 0), Position(d, -d), Position(0, -d), Position(-d, -d)]
            # for each offset/direction, attempt to march d tiles and track if an obstruction is found
            for i, offset in enumerate(offsets):
                # attempt to march
                unblocked_directions, move = self.march(pos, offset, board, directions[i], unblocked_directions)

                # if a valid move was found then add it
                if move is not None:
                    moves.append(move)

        return moves

class King(Piece):
    def generate_moves(self, board, pos, isLight):
        """Generates all of the moves possible for the current piece given that it is a queen"""
        moves = []

        # all of the posible offsets for a king
        offsets = [Position(-1, 0), Position(-1, 1), Position(0, 1), Position(1, 1), 
                    Position(1, 0), Position(1, -1), Position(0, -1), Position(-1, -1)]
        # for each offset/direction, attempt to march d tiles and track if an obstruction is found
        for offset in offsets:
            # attempt to march
            move = self.march(pos, offset, board)

            # if a valid move was found then add it
            if move is not None:
                moves.append(move)

        return moves

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
