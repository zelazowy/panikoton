import sys
from PyQt4 import QtGui, QtCore


# Panikoton class with the game ;)
class Panikoton(QtGui.QMainWindow):
    TIMER_TICK = 80

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

        if self.is_level_completed():
            self.level_completed()
        elif self.is_game_over():
            self.game_over()

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
        # print(self.player.x, self.player.y, "bg_x:", self.stage.background_x)
        # print(self.pressed_keys)

    # moves player forward
    def player_move_forward(self):
        if not self.player.can_move_forward(self.window_w):
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

    def is_level_completed(self):
        return not self.player.can_move_forward(self.window_w)

    def level_completed(self):
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QColor(0, 255, 0))
        painter.setFont(QtGui.QFont("Arial", 20))
        painter.drawText(0, 0, self.window_w, self.window_h, QtCore.Qt.AlignCenter, "You win!")
        self.timer.stop()
        self.update()

    def is_game_over(self):
        return self.stage.is_enemy_hit(self.player.x + self.player.w, self.player.x, self.player.y + self.player.h)

    def is_obstacle_hit(self):
        return self.stage.is_obstacle_hit(self.player.x + self.player.w, self.player.x, self.player.y + self.player.h)

    def obstacle_hit(self):
        self.player.y = self.stage.obstacle_y

    def obstacle_not_hit(self):
        self.player.y = 450

    def game_over(self):
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QColor(255, 0, 0))
        painter.setFont(QtGui.QFont("Arial", 20))
        painter.drawText(0, 0, self.window_w, self.window_h, QtCore.Qt.AlignCenter, "Game over!")
        self.timer.stop()
        self.update()


# Player class with player attributes and controls
class Player(object):
    h = 80
    w = 80
    x = 50
    y = 450 - h  # stage_h - player h
    is_centered = True

    img_pattern = "./assets/player/cat{0}.png"
    player_img = "./assets/player/cat0.png"
    player_imgs = [0, 1, 2, 2, 3, 4, 4, 5, 5, 6, 7, 8]

    move_size = 20
    jump_index = 0
    jump_started = False
    jump_run = [-20, -15, -10, -5, -2, 0, 2, 5, 10, 15, 20]

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
        pixmap = QtGui.QPixmap(cls.player_img)
        painter.drawPixmap(cls.x, cls.y, pixmap)

    @classmethod
    def is_centered(cls):
        return cls.is_centered

    @classmethod
    def can_move_forward(cls, window_w):
        return cls.x + cls.w < window_w

    @classmethod
    def can_move_backward(cls):
        return cls.x <= 0

    @classmethod
    def jump(cls):
        if not cls.jump_started:
            cls.jump_started = True

        # change player position
        cls.y += cls.jump_run[cls.jump_index]

        # if move ends reset values
        if cls.jump_index == len(cls.jump_run) - 1:
            cls.jump_started = False
            cls.jump_index = 0
        else:
            cls.jump_index += 1

        # update player image
        cls.update_player_img(cls.jump_index)

        return cls.jump_started

    @classmethod
    def update_player_img(cls, index):
        cls.player_img = cls.img_pattern.replace("{0}", str(cls.player_imgs[index]))


# Stage class with stage attributes and controls
class Stage(object):
    background = "./assets/stage1_bg.png"
    x = 0
    y = 0
    w = 1000  # width of the bg
    h = 500  # height of the bg

    ground_w = w
    ground_h = 50
    ground_x = x
    ground_y = h - ground_h  # h of the stage minus ground h
    ground_pattern_w = 50
    ground_pattern = "./assets/platform-bg.png"

    enemy_w = 25
    enemy_h = 25
    enemy_x = 410
    enemy_y = h - ground_h - enemy_h
    enemy_pattern = "./assets/enemy.png"

    obstacle_w = 50
    obstacle_h = 50
    obstacle_x = 200
    obstacle_y = h - ground_h - obstacle_h
    obstacle_pattern = "./assets/obstacle.png"

    move_size = 20

    def __init__(self):
        self.move_size = 10

    @classmethod
    def move_forward(cls):
        # adjust background and all elements on the stage
        cls.x -= cls.move_size
        cls.enemy_x -= cls.move_size
        cls.ground_x -= cls.move_size
        cls.obstacle_x -= cls.move_size

    @classmethod
    def draw(cls, painter):
        pixmap = QtGui.QPixmap(cls.background)
        painter.drawPixmap(cls.x, cls.y, pixmap)

        # ground drawing
        painter.setBrush(QtGui.QColor(255, 0, 0))
        bg_pixmap = QtGui.QPixmap(cls.ground_pattern)
        for i in range(0, int(cls.ground_w / cls.ground_pattern_w)):
            painter.drawPixmap(cls.ground_x + i * 50, cls.ground_y, bg_pixmap)

        # enemy drawing
        enemy_pixmap = QtGui.QPixmap(cls.enemy_pattern)
        painter.drawPixmap(cls.enemy_x, cls.enemy_y, enemy_pixmap)

        # obstacle drawing
        # obstacle_pixmap = QtGui.QPixmap(cls.obstacle_pattern)
        # painter.drawPixmap(cls.obstacle_x, cls.obstacle_y, obstacle_pixmap)

    @classmethod
    def is_right_end(cls, window_w):
        return window_w - cls.w == cls.x

    @classmethod
    def is_left_end(cls):
        return 0 == cls.x

    @classmethod
    def is_enemy_hit(cls, player_x1, player_x2, player_y):
        # is possibly hit from above?
        hit_from_above = player_y >= cls.enemy_y

        if not hit_from_above:
            return

        return player_x1 >= cls.enemy_x >= player_x2

    @classmethod
    def is_obstacle_hit(cls, player_x1, player_x2, player_y):
        # is possibly hit from above?
        hit_from_above = player_y >= cls.enemy_y

        if not hit_from_above:
            return

        return player_x1 >= cls.obstacle_x >= player_x2


def main():
    app = QtGui.QApplication([])
    panikoton = Panikoton()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
