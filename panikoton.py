import sys
from PyQt4 import QtGui, QtCore


class Panikoton(QtGui.QMainWindow):
    def __init__(self):
        super(Panikoton, self).__init__()

        self.initUI()

    def initUI(self):
        self.setFixedWidth(500)
        self.setFixedHeight(500)

        self.show()

    def paintEvent(self, QPaintEvent):
        self.drawPlayer()

    def drawPlayer(self):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setBrush(QtGui.QColor(255, 0, 0))
        painter.drawRect(0, 0, 50, 50)
        painter.end()

def main():

    app = QtGui.QApplication([])
    panikoton = Panikoton()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
