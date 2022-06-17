import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtGui import QPainter, QPixmap, QColor
from PyQt5.QtCore import QRect, QPoint
from piece import Board


class ChessUI(QWidget):
    # sets the default color scheme for the app
    background_color    = '#dddddd'
    light_color         = '#a0a0a0'
    dark_color          = '#353535'

    # size paramters for the app
    height          = 600
    width           = 600
    box_size        = 60
    height_offset   = (height - box_size * 8) // 2
    width_offset    = (width - box_size * 8) // 2

    # tracks game parameters
    board = Board()

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

    def paintEvent(self, event):
        # initialize the painter and draw the background
        painter = QPainter(self)
        painter.drawPixmap(QPoint(), self.pix)

        # draw the board to the screen
        self.drawBoard(painter)
        # draw the pieces to the screen
        self.drawPieces(painter)

    def mousePressEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        
        # if the click is outside the board, do nothing
        if x < self.width_offset or x > self.width - self.width_offset:
            return
        elif y < self.height_offset or y > self.height - self.height_offset:
            return
        else:
            # calculate which square the user clicked on
            c = (x - self.width_offset) // self.box_size
            r = (y - self.height_offset) // self.box_size

            self.board.board[r, c].is_active = True

            # print(f'clicked on square ({c}, {r})')
            # print(f'located at ({x}, {y})')
            # x1, y1 = self.rowcol_to_pixels(r, c)
            # print(f'box origin: ({x1}, {y1})')
        
        self.update()


    def mouseReleaseEvent(self, event):
        for r in range(8):
            for c in range(8):
                if self.board.board[r, c] is not None:
                    self.board.board[r, c].is_active = False
        self.update()

    def drawBoard(self, painter):
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

    def drawPieces(self, painter):
        """Draw the pieces on the chessboard using the painter"""
        for r in range(8):
            for c in range(8):
                # only consider pieces that exist
                if self.board.board[r, c] is not None and not self.board.board[r, c].is_active:
                    # get the origin for the box the piece is in
                    x, y = self.rowcol_to_pixels(r, c)
                    # draw the image for the piece at the calculated coordinates
                    painter.drawPixmap(QPoint(x, y), QPixmap(self.board.board[r, c].image))

    def rowcol_to_pixels(self, r, c):
        """Gets the pixel values of the origin on the box that a set of row-column indices points to"""
        x = c * self.box_size + self.width_offset
        y = r * self.box_size + self.width_offset
        return x, y
          

def main():
    app = QApplication(sys.argv)
    ui = ChessUI()
    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
