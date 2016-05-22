import sys
from PyQt4 import QtGui, QtCore
import random


# window initial values
WINDOW_W = 500
WINDOW_H = 500


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

    timer = None

    # list contains available keys in the game and its press states
    pressed_keys = {
        QtCore.Qt.Key_Z: KEY_NOT_PRESSED,
    }

    key_actions = {}

    def __init__(self):
        super(Panikoton, self).__init__()

        # initialize internal values
        self.init_key_actions()

        # initialize player and stage
        self.player = Player
        self.stage = Stage()

        self.init_ui()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.key_action)
        self.timer.start(self.TIMER_TICK)

    # prepare and display main window
    def init_ui(self):
        self.setFixedWidth(WINDOW_W)
        self.setFixedHeight(WINDOW_H)

        self.show()

    # initializes key actions
    def init_key_actions(self):
        self.key_actions = {
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

    # adds pressed key to the set
    def keyPressEvent(self, e):
        key = e.key()

        # check allowed keys (for now it's only Z)
        if key != QtCore.Qt.Key_Z:
            return

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

    def player_jump(self):
        return self.player.jump()


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
    def draw(cls, painter):
        pixmap = QtGui.QPixmap(cls.player_img)
        painter.drawPixmap(cls.x, cls.y, pixmap)

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
    ground_h = 50
    ground_x = 0
    ground_y = WINDOW_W - ground_h  # h of the stage minus ground h
    ground_pattern_w = 50
    ground_pattern = "./assets/platform-bg.png"

    move_size = 10
    move_index = 0
    move_intervals = [-25, 0, 25]

    landscape = []

    enemies = []

    def __init__(self):
        self.draw_landscape()
        t = 0

    @classmethod
    def draw(cls, painter):
        cls.move()

        # ground drawing
        bg_pixmap = QtGui.QPixmap(cls.ground_pattern)
        for i in range(0, int(WINDOW_W / cls.ground_pattern_w) + 1):
            painter.drawPixmap(cls.ground_x + i * 50, cls.ground_y, bg_pixmap)

        for element in cls.landscape:
            pixmap = QtGui.QPixmap(element["src"])
            painter.drawPixmap(element["x"], element["y"], pixmap)

        for enemy in cls.enemies:
            pixmap = QtGui.QPixmap(enemy["src"])
            painter.drawPixmap(enemy["x"], enemy["y"], pixmap)

    @classmethod
    def draw_landscape(cls):
        for i in range(0, 5):
            cls.landscape.append(Landscape.get_cloud())

        for i in range(0, 5):
            cls.landscape.append(Landscape.get_tree())

    @classmethod
    def move(cls):
        cls.move_index += 1
        cls.ground_x -= cls.move_intervals[cls.move_index % len(cls.move_intervals)]

        missing_elements = []
        for i, element in enumerate(cls.landscape):
            element["x"] -= element["v"]

            if element["x"] + element["w"] <= 0:
                del cls.landscape[i]

                # don't add missing element with probability = 20%
                if 2 > random.randint(0, 10):
                    missing_elements.append(element["type"])

        for element in missing_elements:
            if element == "cloud":
                cls.landscape.append(Landscape.add_cloud())
            elif element == "tree":
                cls.landscape.append(Landscape.add_tree())

        # randomly create new landscape element with specific chances if there is less than 150% initial elements in landscape
        if 15 > len(cls.landscape):
            if 1 > random.randint(0, 10):
                cls.landscape.append(Landscape.add_cloud())
            if 1 > random.randint(0, 10):
                cls.landscape.append(Landscape.add_tree())

        # enemies
        for i, enemy in enumerate(cls.enemies):
            enemy["x"] -= enemy["v"]

            if enemy["x"] + enemy["w"] <= 0:
                del cls.enemies[i]

        # randomly create enemy but no more than 2 are allowed at the time!
        if 2 > len(cls.enemies):
            if 2 > random.randint(0, 10):
                cls.enemies.append(Enemy.add_hankey())


class Landscape(object):
    cloud = {
        "type": "cloud",
        "w": 50,
        "h": 50,
        "src": "./assets/cloud.png",
        "y": 0,
        "x": 0,
        "max_y": WINDOW_H - 200,
        "max_x": WINDOW_W - 100,
        "max_v": 4,
        "v": 0
    }

    tree = {
        "type": "tree",
        "w": 50,
        "h": 100,
        "src": "./assets/tree.png",
        "y": WINDOW_H - 150,
        "x": 0,
        "max_x": WINDOW_W - 50,
        "max_v": 10,
        "v": 0
    }

    @classmethod
    def get_cloud(cls):
        cloud = cls.cloud.copy()
        cloud["y"] = random.randint(0, cloud["max_y"])
        cloud["x"] = random.randint(0, cloud["max_x"])
        cloud["v"] = random.randint(1, cloud["max_v"])

        return cloud

    @classmethod
    def add_cloud(cls):
        cloud = cls.cloud.copy()
        cloud["y"] = random.randint(0, cloud["max_y"])
        cloud["x"] = WINDOW_W
        cloud["v"] = random.randint(1, cloud["max_v"])

        return cloud

    @classmethod
    def get_tree(cls):
        tree = cls.tree.copy()
        tree["x"] = random.randint(0, tree["max_x"])
        tree["v"] = random.randint(tree["max_v"] - 2, tree["max_v"])

        return tree

    @classmethod
    def add_tree(cls):
        tree = cls.tree.copy()
        tree["x"] = WINDOW_W
        tree["v"] = random.randint(tree["max_v"] - 2, tree["max_v"])

        return tree


class Enemy(object):
    hankey = {
        "type": "hankey",
        "w": 30,
        "h": 30,
        "src": "./assets/hankey.png",
        "y": WINDOW_H - 80,
        "x": WINDOW_W,
        "min_v": 15,
        "max_v": 20,
        "v": 0
    }

    @classmethod
    def add_hankey(cls):
        hankey = cls.hankey.copy()
        hankey["v"] = random.randint(hankey["min_v"], hankey["max_v"])

        return hankey


def main():
    app = QtGui.QApplication([])
    panikoton = Panikoton()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
