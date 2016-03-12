import sys
from PyQt4 import QtGui, QtCore


class Panikoton(QtGui.QMainWindow):
    # player initial values
    pos_x = 0
    pos_y = 0
    player_h = 50
    player_w = 50

    # move initial values
    move_size = 10

    # window initial values
    window_w = 500
    window_h = 500

    def __init__(self):
        super(Panikoton, self).__init__()

        self.initUI()

    def initUI(self):
        self.setFixedWidth(self.window_w)
        self.setFixedHeight(self.window_h)

        self.show()

    def paintEvent(self, QPaintEvent):
        self.drawPlayer()

    def drawPlayer(self):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setBrush(QtGui.QColor(255, 0, 0))
        painter.drawRect(self.pos_x, self.pos_y, self.player_w, self.player_h)
        painter.end()

    def keyPressEvent(self, e):
        key = e.key()

        if key == QtCore.Qt.Key_Left:
            self.player_move_left()

            self.move_occurred()
        elif key == QtCore.Qt.Key_Right:
            self.player_move_right()

            self.move_occurred()
        elif key == QtCore.Qt.Key_Up:
            self.player_move_up()

            self.move_occurred()
        elif key == QtCore.Qt.Key_Down:
            self.player_move_down()

            self.move_occurred()

    def move_occurred(self):
        print(self.pos_x, self.pos_y)

    def player_move_right(self):
        if self.pos_x + self.player_w >= self.window_w:
            return

        self.pos_x += self.move_size
        self.update()

    def player_move_left(self):
        if self.pos_x <= 0:
            return

        self.pos_x -= self.move_size
        self.update()

    def player_move_up(self):
        if self.pos_y <= 0:
            return

        self.pos_y -= self.move_size
        self.update()

    def player_move_down(self):
        if self.pos_y + self.player_h >= self.window_h:
            return

        self.pos_y += self.move_size
        self.update()


def main():

    app = QtGui.QApplication([])
    panikoton = Panikoton()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
