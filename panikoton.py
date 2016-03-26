import sys
from PyQt4 import QtGui, QtCore


# Panikoton class with the game ;)
class Panikoton(QtGui.QMainWindow):
    # player initial values
    player = None

    # stage initial values
    stage = None

    # window initial values
    window_w = 500
    window_h = 500

    def __init__(self):
        super(Panikoton, self).__init__()

        # initialize player and stage
        self.player = Player
        self.stage = Stage

        self.init_ui()

    # prepare and display main window
    def init_ui(self):
        self.setFixedWidth(self.window_w)
        self.setFixedHeight(self.window_h)

        self.show()

    # event dispatched after `self.update()` call
    def paintEvent(self, QPaintEvent):
        self.draw_scene()

    # draws scene: stage + player
    def draw_scene(self):
        painter = QtGui.QPainter(self)

        self.stage.draw(painter)
        self.player.draw(painter)

        self.player.after_move()

    # player controls
    def keyPressEvent(self, e):
        key = e.key()

        if key == QtCore.Qt.Key_Left:
            self.player_move_backward()

            self.move_occurred()
        elif key == QtCore.Qt.Key_Right:
            self.player_move_forward()

            self.move_occurred()

        # update stage state (dispatches paintEvent)
        self.update()

    # debug
    def move_occurred(self):
        print(self.player.x, self.player.y, 'bg_x:', self.stage.background_x)

    # moves player forward
    def player_move_forward(self):
        if self.player.can_move_forward():
            return

        if self.stage.is_right_end(self.window_w):
            self.player.move_forward()
            return

        if self.player.is_centered:
            self.stage.move_forward()
            return

        self.player.move_forward()

    # moves player backward
    def player_move_backward(self):
        if self.player.can_move_backward():
            return

        self.player.move_backward()


# Player class with player attributes and controls
class Player(object):
    x = 230
    y = 230
    h = 40
    w = 40
    is_centered = True

    move_size = 10

    def __init__(self):
        self.move_size = 10

    @classmethod
    def move_forward(cls):
        cls.x += cls.move_size

    @classmethod
    def move_backward(cls):
        cls.x -= cls.move_size

    @classmethod
    def after_move(cls):
        # is player centered?
        cls.is_centered = False
        if 230 == cls.x:
            cls.is_centered = True

    @classmethod
    def draw(cls, painter):
        painter.setBrush(QtGui.QColor(255, 0, 0))
        painter.drawRect(cls.x, cls.y, cls.w, cls.h)

    @classmethod
    def is_centered(cls):
        return cls.is_centered

    @classmethod
    def can_move_forward(cls, window_w):
        return cls.x + cls.w >= window_w

    @classmethod
    def can_move_backward(cls):
        return cls.x <= 0


# Stage class with stage attributes and controls
class Stage(object):
    background = './assets/stage1_bg.png'
    background_x = 0
    w = 1000  # width of the bg
    h = 500   # height of the bg

    move_size = 10

    def __init__(self):
        self.move_size = 10

    @classmethod
    def move_forward(cls):
        cls.background_x -= cls.move_size

    @classmethod
    def draw(cls, painter):
        pixmap = QtGui.QPixmap(cls.background)
        painter.drawPixmap(cls.background_x, 0, pixmap)

    @classmethod
    def is_right_end(cls, window_w):
        return window_w - cls.w == cls.background_x

    @classmethod
    def is_left_end(cls):
        return 0 == cls.background_x


def main():

    app = QtGui.QApplication([])
    panikoton = Panikoton()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
