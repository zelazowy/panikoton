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
    score = 0

    # list contains available keys in the game and its press states
    pressed_keys = {
        QtCore.Qt.Key_Z: KEY_NOT_PRESSED,
    }

    key_actions = {}

    def __init__(self):
        super(Panikoton, self).__init__()

        self.create_game()

    def create_game(self):
        # initialize internal values
        self.init_key_actions()

        # initialize player and stage
        self.player = Player()
        self.stage = Stage(self.player, self)

        self.init_ui()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.tick)
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
        self.draw_score(painter)

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
    def tick(self):
        if self.stage.game_over:
            self.game_over()
            return

        self.score += 5

        for key, is_pressed in self.pressed_keys.items():
            if self.KEY_PRESSED == is_pressed:
                action = self.key_actions[key]
                action()

        # if player is in jump "state" then continue it independent from current action
        if self.player.jump_started:
            self.player_jump()

        self.update()

    def draw_score(self, painter):
        painter.setPen(QtGui.QColor(0, 0, 0))
        painter.setFont(QtGui.QFont("Arial", 20))
        painter.drawText(0, 0, WINDOW_W, WINDOW_H, QtCore.Qt.AlignRight + QtCore.Qt.AlignTop, str(self.score))

    def player_jump(self):
        return self.player.jump()

    def game_over(self):
        self.timer.stop()
        self.update()


# Player class with player attributes and controls
class Player(object):
    h = 80
    w = 80
    x = 50
    y = 450 - h  # stage_h - player h

    img_pattern = "./assets/player/cat{0}.png"
    player_img = "./assets/player/cat0.png"
    player_imgs = [0, 1, 2, 2, 3, 4, 4, 5, 5, 6, 7, 8]

    jump_index = 0
    jump_started = False
    jump_run = [-20, -15, -10, -5, -2, 0, 2, 5, 10, 15, 20]

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

    player = None

    panikoton = None

    game_over = False

    @classmethod
    def __init__(cls, player, panikoton):
        cls.draw_landscape()
        cls.player = player
        cls.panikoton = panikoton

    @classmethod
    def draw(cls, painter):
        if cls.game_over:
            painter.setPen(QtGui.QColor(255, 0, 0))
            painter.setFont(QtGui.QFont("Arial", 20))
            painter.drawText(0, 0, WINDOW_W, WINDOW_H, QtCore.Qt.AlignCenter, "Game over!")
        else:
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

        for i in range(0, 5):
            cls.landscape.append(Landscape.get_far_tree())

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
            elif element == "far_tree":
                cls.landscape.append(Landscape.add_far_tree())

        # randomly create new landscape element with specific chances if there is less than 150% initial elements in landscape
        if 15 > len(cls.landscape):
            if 1 > random.randint(0, 10):
                cls.landscape.append(Landscape.add_cloud())
            elif 1 > random.randint(0, 10):
                cls.landscape.append(Landscape.add_tree())
            elif 1 > random.randint(0, 10):
                cls.landscape.append(Landscape.add_far_tree())

        # enemies
        for i, enemy in enumerate(cls.enemies):
            enemy["x"] -= enemy["v"]

            if enemy["x"] + enemy["w"] <= 0:
                del cls.enemies[i]

            cls.check_enemy_hit(enemy)

        # randomly create enemy but no more than n are allowed at the time!
        if 1 > len(cls.enemies):
            if 2 > random.randint(0, 10):
                cls.enemies.append(Enemy.add_hankey())
            elif 2 > random.randint(0, 10):
                cls.enemies.append(Enemy.add_shoe())

    @classmethod
    def check_enemy_hit(cls, enemy):
        hit_from_above = cls.player.y + cls.player.h >= enemy["y"]

        hit_from_front = cls.player.x + cls.player.w >= enemy["x"]

        is_behind = cls.player.x > enemy["x"]

        if hit_from_above and hit_from_front and not is_behind:
            cls.game_over = True


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

    far_tree = {
        "type": "far_tree",
        "w": 43,
        "h": 85,
        "src": "./assets/far_tree.png",
        "y": WINDOW_H - 135,
        "x": 0,
        "max_x": WINDOW_W - 43,
        "max_v": 6,
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

    @classmethod
    def get_far_tree(cls):
        far_tree = cls.far_tree.copy()
        far_tree["x"] = random.randint(0, far_tree["max_x"])
        far_tree["v"] = random.randint(far_tree["max_v"] - 2, far_tree["max_v"])

        return far_tree

    @classmethod
    def add_far_tree(cls):
        far_tree = cls.far_tree.copy()
        far_tree["x"] = WINDOW_W
        far_tree["v"] = random.randint(far_tree["max_v"] - 2, far_tree["max_v"])

        return far_tree


class Enemy(object):
    hankey = {
        "type": "hankey",
        "w": 30,
        "h": 30,
        "src": "./assets/hankey.png",
        "y": WINDOW_H - 80,
        "x": WINDOW_W,
        "min_v": 15,
        "max_v": 25,
        "v": 0
    }

    shoe = {
        "type": "shoe",
        "w": 40,
        "h": 40,
        "src": "./assets/shoe.png",
        "y": WINDOW_H - 90,
        "x": WINDOW_W,
        "min_v": 20,
        "max_v": 25,
        "v": 0
    }

    @classmethod
    def add_hankey(cls):
        hankey = cls.hankey.copy()
        hankey["v"] = random.randint(hankey["min_v"], hankey["max_v"])

        return hankey

    @classmethod
    def add_shoe(cls):
        shoe = cls.shoe.copy()
        shoe["v"] = random.randint(shoe["min_v"], shoe["max_v"])

        return shoe


def main():
    app = QtGui.QApplication([])
    panikoton = Panikoton()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
