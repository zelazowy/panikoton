import sys
from PyQt4 import QtGui, QtCore


# Panikoton class with the game ;)
class Panikoton(QtGui.QMainWindow):
    TIMER_TICK = 100

    KEY_PRESSED = True
    KEY_NOT_PRESSED = False

    # player initial values
    player = None

    # stage initial values
    stage = None

    tick_action = None

    # window initial values
    window_w = 500
    window_h = 500

    timer = None

    # list contains available keys in the game and its press states
    pressed_keys = {
        QtCore.Qt.Key_Left: KEY_NOT_PRESSED,
        QtCore.Qt.Key_Right: KEY_NOT_PRESSED,
        QtCore.Qt.Key_Z: KEY_NOT_PRESSED,
    }

    key_actions = {}

    def __init__(self):
        super(Panikoton, self).__init__()

        # initialize internal values
        self.init_key_actions()

        # initialize player and stage
        self.player = Player
        self.stage = Stage

        self.init_ui()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.key_action)
        self.timer.start(self.TIMER_TICK)

    # prepare and display main window
    def init_ui(self):
        self.setFixedWidth(self.window_w)
        self.setFixedHeight(self.window_h)

        self.show()

    # initializes key actions
    def init_key_actions(self):
        self.key_actions = {
            QtCore.Qt.Key_Left: self.player_move_backward,
            QtCore.Qt.Key_Right: self.player_move_forward,
            QtCore.Qt.Key_Z: self.player_jump,
        }

    # event dispatched after `self.update()` call
    def paintEvent(self, QPaintEvent):
        self.draw_scene()

    # draws scene: stage + player
    def draw_scene(self):
        painter = QtGui.QPainter(self)

        self.stage.draw(painter)
        self.player.draw(painter)

        self.player.after_move()

    # adds pressed key to the set
    def keyPressEvent(self, e):
        key = e.key()

        # sets state of the key to PRESSED
        self.pressed_keys[key] = self.KEY_PRESSED

    # removes released key from the pressed_keys set
    def keyReleaseEvent(self, e):
        key = e.key()

        # sets state of the key to NOT_PRESSED
        self.pressed_keys[key] = self.KEY_NOT_PRESSED

    # method called in every Timer tick
    # calls methods for keys pressed at the moment
    def key_action(self):
        for key, is_pressed in self.pressed_keys.items():
            if self.KEY_PRESSED == is_pressed:
                action = self.key_actions[key]
                action()

        # if player is in jump "state" then continue it independent from current action
        if self.player.jump_started:
            self.player_jump()

        self.update()

    # debug
    def move_occurred(self):
        pass
        # print(self.player.x, self.player.y, 'bg_x:', self.stage.background_x)
        # print(self.pressed_keys)

    # moves player forward
    def player_move_forward(self):
        if self.player.can_move_forward(self.window_w):
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

    def player_jump(self):
        return self.player.jump()


# Player class with player attributes and controls
class Player(object):
    JUMP_DIR_UP = -1
    JUMP_DIR_DOWN = 1

    x = 230
    y = 460
    h = 40
    w = 40
    is_centered = True

    move_size = 10
    jump_index = 0
    jump_dir = JUMP_DIR_UP
    jump_started = False
    jump_run = [20, 15, 10, 5, 2, 0]

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

    @classmethod
    def jump(cls):
        # todo: przerobić, jest sprasznie nieczytelnie
        if not cls.jump_started:
            cls.jump_started = True

        cls.y += cls.jump_dir * cls.jump_run[cls.jump_index]

        if cls.jump_index == len(cls.jump_run) - 1:
            cls.jump_dir = cls.JUMP_DIR_DOWN
        elif cls.jump_index == 0 and cls.JUMP_DIR_DOWN == cls.jump_dir:
            cls.jump_dir = cls.JUMP_DIR_UP
            cls.jump_started = False

            return False

        cls.jump_index -= cls.jump_dir

        # print(z)

        return cls.jump_started


# Stage class with stage attributes and controls
class Stage(object):
    background = './assets/stage1_bg.png'
    background_x = 0
    w = 1000  # width of the bg
    h = 500  # height of the bg

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
