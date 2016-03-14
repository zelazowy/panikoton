import sys
from PyQt4 import QtGui, QtCore


class Panikoton(QtGui.QMainWindow):
    # player initial values
    pos_x = 230
    pos_y = 230
    player_h = 40
    player_w = 40
    is_centered = True

    # move initial values
    move_size = 10

    # window initial values
    window_w = 500
    window_h = 500

    # stage initial values
    background = './assets/stage1_bg.png'
    background_pos_x = 0
    stage_w = 1000  # width of the bg
    stage_h = 500   # height of the bg

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
        painter = QtGui.QPainter(self)

        pixmap = QtGui.QPixmap(self.background)
        painter.drawPixmap(self.background_pos_x, 0, pixmap)

        painter.setBrush(QtGui.QColor(255, 0, 0))
        painter.drawRect(self.pos_x, self.pos_y, self.player_w, self.player_h)

        # is player centered?
        self.is_centered = False
        if 225 == self.pos_x:
            self.is_centered = True

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

        # update stage state (dispatches paintEvent)
        self.update()

    def move_occurred(self):
        print(self.pos_x, self.pos_y, 'bg_x:', self.background_pos_x)

    def player_move_right(self):
        if self.pos_x + self.player_w >= self.window_w:
            return

        # if player is centered then:
        #   if background_pos_x

        # if True == self.is_centered:
            #  its end of the stage
        if self.window_w - self.stage_w == self.background_pos_x:
            self.pos_x += self.move_size
        else:
            self.background_pos_x -= self.move_size
        # else:
        #     #  its end of the stage
        #     if self.window_w - self.stage_w == self.background_pos_x:
        #         self.pos_x += self.move_size
        #     else:


    def player_move_left(self):
        if self.pos_x <= 0:
            return

        # its left end of the stage
        if 0 == self.background_pos_x:
            self.pos_x -= self.move_size
        else:
            self.background_pos_x += self.move_size



    def player_move_up(self):
        if self.pos_y <= 0:
            return

        self.pos_y -= self.move_size

    def player_move_down(self):
        if self.pos_y + self.player_h >= self.window_h:
            return

        self.pos_y += self.move_size

    def background_move_right(self):
        if self.stage_w - self.window_w == self.background_pos_x:
            return

        self.background_pos_x += self.move_size

    def background_move_left(self):
        if 0 == self.pos_x:
            return

        self.background_pos_x -= self.move_size


def main():

    app = QtGui.QApplication([])
    panikoton = Panikoton()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
