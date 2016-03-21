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

    # debug
    def move_occurred(self):
        print(self.player.x, self.player.y, 'bg_x:', self.stage.background_x)

    # moves player right
    def player_move_right(self):
        if self.player.x + self.player.w >= self.window_w:
            return

        # if player is centered then:
        #   if background_pos_x

        # if True == self.is_centered:
            #  its end of the stage
        if self.window_w - self.stage.w == self.stage.background_x:
            self.player.move_right()
        else:
            self.stage.move_right()
        # else:
        #     #  its end of the stage
        #     if self.window_w - self.stage_w == self.background_pos_x:
        #         self.pos_x += self.move_size
        #     else:

    # moves player left
    def player_move_left(self):
        if self.player.x <= 0:
            return

        # its left end of the stage
        if 0 == self.stage.background_x:
            self.player.move_left()
        else:
            self.stage.move_left()

    # moves player up (should be changed by jump)
    def player_move_up(self):
        if self.player.y <= 0:
            return

        self.player.y -= self.player.move_size

    # moves player down (to remove)
    def player_move_down(self):
        if self.player.y + self.player.h >= self.window_h:
            return

        self.player.y += self.player.move_size


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
    def move_right(cls):
        cls.x += cls.move_size

    @classmethod
    def move_left(cls):
        cls.x -= cls.move_size

    @classmethod
    def after_move(cls):
        # is player centered?
        cls.is_centered = False
        if 225 == cls.x:
            cls.is_centered = True

    @classmethod
    def draw(cls, painter):
        painter.setBrush(QtGui.QColor(255, 0, 0))
        painter.drawRect(cls.x, cls.y, cls.w, cls.h)


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
    def move_right(cls):
        cls.background_x -= cls.move_size

    @classmethod
    def move_left(cls):
        cls.background_x += cls.move_size

    @classmethod
    def draw(cls, painter):
        pixmap = QtGui.QPixmap(cls.background)
        painter.drawPixmap(cls.background_x, 0, pixmap)


def main():

    app = QtGui.QApplication([])
    panikoton = Panikoton()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
