import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtGui import QPainter, QPixmap, QColor
from PyQt5.QtCore import QRect, QPoint
from position import Position
from move import Move
from board import Board


class ChessUI(QWidget):
    # sets the default color scheme for the app
    background_color = '#cccccc'
    light_color = '#a0a0a0'
    dark_color = '#353535'

    # load the icon for a targetable tile
    target_icon: str = './chess_icons/green_circle.png'

    # size parameters for the app
    height = 600
    width = 600
    box_size = 60
    height_offset = (height - box_size * 8) // 2
    width_offset = (width - box_size * 8) // 2

    # tracks game parameters
    board = Board()             # the current board state
    pickup: Position = None     # the coordinates to the held piece
    ghosts = Board('empty')     # an empty board for tracking ghosts
    isLightTurn: bool = True    # tracks if it is the light player's turn

    # a variable for tracking all of the possible moves
    moves: list = []

    def __init__(self):
        # call the parent constructor for a qwidget
        super(ChessUI, self).__init__()
        # lock in a size for the window and give it a nice name
        self.resize(self.height, self.width)
        self.setWindowTitle('PyChess')

        # create an empty layout and set it as the default
        layout = QVBoxLayout()
        self.setLayout(layout)

        # create the background 
        self.pix = QPixmap(self.rect().size())
        self.pix.fill(QColor(self.background_color))

        # generate all of the first possible moves
        self.generate_moves()

    def paintEvent(self, event):
        """Draws each layer of the board one after another every update"""
        # initialize the painter and draw the background
        painter = QPainter(self)
        painter.drawPixmap(QPoint(), self.pix)

        # draw the board to the screen
        self.draw_board(painter)
        # draw the pieces to the screen
        self.draw_pieces(painter)
        # draw piece ghosts to the screen
        self.draw_ghosts(painter)
        # draw target icons to the screen
        self.draw_targets(painter)

    def mousePressEvent(self, event):
        """When the user clicks the mouse, the game checks if the user can pick up a piece and does so"""
        # get the pixel position of the click
        x, y = event.pos().x(), event.pos().y()
        
        # if the click is outside the board, do nothing
        if x < self.width_offset or x > self.width - self.width_offset:
            return
        elif y < self.height_offset or y > self.height - self.height_offset:
            return
        else:
            # calculate which square the user clicked on
            pos = self.pixels_to_rowcol(x, y)

            # do nothing if the user clicked on empty space or a piece of the wrong color
            if self.board.board[pos.r, pos.c] is None or self.board.board[pos.r, pos.c].light != self.isLightTurn:
                return

            # store the position of the picked up piece
            self.pickup = pos
        
        self.update()

    def mouseReleaseEvent(self, event):
        """When the user releases the mouse, the game clears any existing ghosts,
        drops any held pieces, and makes a move if possible"""
        # traverse all of the tiles
        for r in range(8):
            for c in range(8):
                # clear any existing ghosts
                self.ghosts.board[r, c] = None

        # if the user is holding a piece
        if self.pickup is not None:
            # get the pixel position of the dropped piece
            x, y = event.pos().x(), event.pos().y()

            # only drop the piece if the target location is on the board
            if (self.width_offset < x <= self.width - self.width_offset) and \
               (self.height_offset < y <= self.height - self.height_offset):
                pos = self.pixels_to_rowcol(x, y)

                # if the user dropped the piece where they picked it up then do nothing
                if pos == self.pickup:
                    return

                # put the held piece in the dropped position
                self.board.board[pos.r, pos.c] = self.board.board[self.pickup.r, self.pickup.c]
                # empty the space that the held piece came from
                self.board.board[self.pickup.r, self.pickup.c] = None

                # add a move to the board and change the color
                self.board.move += 1
                self.isLightTurn = not self.isLightTurn

        # clear the picked up piece
        self.pickup = None
        # generate a new set of moves
        self.generate_moves()

        self.update()

    def mouseMoveEvent(self, event):
        """When the user moves the mouse, checks if they are holding a piece.
        If so, place a ghost on the tile that the player is mousing over."""
        if self.pickup is not None:
            # reset all of the ghosts
            self.ghosts = Board('empty')

            # get the pixel position of the click
            x, y = event.pos().x(), event.pos().y()

            # don't do anything if mousing outside the board
            if x < self.width_offset or x > self.width - self.width_offset:
                return
            if y < self.height_offset or y > self.height - self.height_offset:
                return

            # calculate the coordinates of the current tile
            pos = self.pixels_to_rowcol(x, y)
            # mark the current tile with a ghost of the held piece
            self.ghosts.board[pos.r, pos.c] = self.board.board[self.pickup.r, self.pickup.c]

            # update the render to show the piece
            self.update()

    def draw_board(self, painter):
        """Draw the chessboard using the painter"""
        for r in range(8):
            x = self.height_offset + self.box_size * r      # height offset
            for c in range(8):
                y = self.width_offset + self.box_size * c   # width offset
                rect = QRect(x, y, self.box_size, self.box_size)

                # the coloring of the square can be determined using the parity of the sum of the indices
                if (r + c) & 1:
                    color = QColor(self.dark_color)
                else:
                    color = QColor(self.light_color)

                painter.fillRect(rect.normalized(), color)

    def draw_pieces(self, painter):
        """Draw the pieces on the chessboard using the painter"""
        for r in range(8):
            for c in range(8):
                # only consider pieces that exist
                if self.board.board[r, c] is not None:
                    # if a piece is held, don't draw it either
                    if self.pickup is not None and self.pickup == Position(r, c):
                        continue
                    # get the origin for the box the piece is in
                    x, y = self.rowcol_to_pixels(r, c)
                    # draw the image for the piece at the calculated coordinates
                    painter.drawPixmap(QPoint(x, y), QPixmap(self.board.board[r, c].image))

    def draw_ghosts(self, painter):
        """Draw any ghosts created by the player dragging a piece using the painter"""
        # lower the opacity since ghosts shouldn't look like real pieces
        painter.setOpacity(0.5)

        # iterate over every tile
        for r in range(8):
            for c in range(8):
                # if the tile contains a ghost, then draw it to the screen
                if self.ghosts.board[r, c] is not None:
                    x, y = self.rowcol_to_pixels(r, c)
                    painter.drawPixmap(QPoint(x, y), QPixmap(self.ghosts.board[r, c].image))

    def draw_targets(self, painter):
        """Draw a distinctive highlight on every tile that the held piece can move to"""
        # lower the opacity since highlights should be subtle
        painter.setOpacity(0.5)

        # if nothing is currently held, don't draw anything
        if self.pickup is None:
            return

        # iterate over every move that was calculated
        for move in self.moves:
            # only consider moves that belong to the held piece
            if move.begin != self.pickup:
                continue

            # calculate the pixel coordinates of the target
            x, y = self.rowcol_to_pixels(move.target.r, move.target.c)
            # rescale the icon to take up a portion of the tile
            scaledSize = (self.box_size * 3) // 5
            scaledPadding = self.box_size // 5
            # draw the target icon on the potential landing space
            painter.drawPixmap(QPoint(x + scaledPadding, y + scaledPadding), QPixmap(self.target_icon).scaledToWidth(scaledSize))

    def pixels_to_rowcol(self, x, y):
        """Gets the row and column values for the indices correlated to the pixel values x and y"""
        c = (x - self.width_offset) // self.box_size
        r = (y - self.height_offset) // self.box_size
        return Position(r, c)

    def rowcol_to_pixels(self, r, c):
        """Gets the pixel values of the origin on the box that a set of row-column indices points to"""
        x = c * self.box_size + self.width_offset
        y = r * self.box_size + self.width_offset
        return x, y     
          
    def generate_moves(self):
        """Generates all of the possible moves for the current player. Uses this to populate the moves list"""
        # clear the moves list
        moves = []

        # iterate over every tile
        for r in range(8):
            for c in range(8):
                piece = self.board.board[r, c]
                # only consider pieces that belong to the current player
                if piece is not None and piece.light == self.isLightTurn:
                    # track the position the piece would move from
                    begin = Position(r, c)

                    # generate pawn moves
                    if piece.role == 'pawn':
                        moves.extend(self.generate_pawn_moves(begin, piece))

        self.moves = moves

    def generate_pawn_moves(self, begin, piece):
        """Generates all of the moves possible for the current piece given that it is a pawn"""
        moves = []

        # pawn move direction is determined by color
        if piece.light:
            # range is negative for light since it moves up the board
            max_range = [-1 * n for n in range(1, 2 + (begin.r == 6))]
        else:
            # range is positive for dark since it moves down the board
            max_range = list(range(1, 2 + (begin.r == 1)))

        # iterate down the range of the pawn
        for n in max_range:

            # calculate potential attacks
            if abs(n) == 1:
                # account for the west boundary of the board
                if begin.c > 0:
                    west = Position(begin.r + n, begin.c - 1)
                    if west.contains_enemy_piece(self.board, self.isLightTurn):
                        moves.append(Move(begin, west))
                # account for the east boundary of the board
                if begin.c < 7:
                    east = Position(begin.r + n, begin.c + 1)
                    if east.contains_enemy_piece(self.board, self.isLightTurn):
                        moves.append(Move(begin, east))

            # calculate the position of the landing tile
            target = Position(begin.r + n, begin.c)
            # if the current tile does not contain an allied piece, it is a valid move
            if not target.does_share_color(self.board, self.isLightTurn):
                moves.append(Move(begin, target))
            # an allied piece cannot be jumped over, so stop searching
            else:
                break

        return moves

def main():
    app = QApplication(sys.argv)
    ui = ChessUI()
    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
