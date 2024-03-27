from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import pyqtSignal as Signal, Qt, QPoint
import sys
from PyQt6 import QtWidgets

class Paint(QMainWindow):

    '''
    Класс отвечающий за отрисовку
    '''

    signal_end_paint = Signal()

    def __init__(self, parent=None):
        super().__init__()
        self.image = QImage(self.size(), QImage.Format.Format_RGB32)
        self.image.fill(Qt.GlobalColor.white)
        self.scale_grid(width=int(self.image.width()), height=int(self.image.height()))
        self.drawing = False
        self.brushSize = 30
        self.brushColor = Qt.GlobalColor.black
        self.lastPointPressed = QPoint()
        self.lastPointMoved = QPoint()


        # def paintEvent(self, event):
    #     painter = QPainter(self)
    #     painter.drawImage(0, 0, self.image)

    def scale_grid(self, width, height):
        rows = 28
        cols = 28
        cell_width = width // cols
        cell_height = height // rows

        grid = QPainter(self.image)
        pen = QPen(Qt.GlobalColor.gray, 1, Qt.PenStyle.SolidLine)

        for i in range(1, rows):
            y = i * cell_height
            grid.setPen(pen)
            grid.drawLine(0, y, width, y)

        for i in range(1, cols):
            x = i * cell_width
            grid.setPen(pen)
            grid.drawLine(x, 0, x, height)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.lastPointPressed = event.pos()
            self.lastPointMoved = event.pos()

    def mouseMoveEvent(self, event):
        if self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap,
                                Qt.PenJoinStyle.RoundJoin))
            painter.drawLine(self.lastPointMoved, event.pos())
            self.lastPointMoved = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = False
            self.signal_end_paint.emit()

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.image.rect(), self.image, self.image.rect())


    def clear(self):
        self.image.fill(Qt.GlobalColor.white)
        self.scale_grid(width=int(self.image.width()), height=int(self.image.height()))
        self.update()


if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Paint()
    window.show()
    sys.exit(App.exec())
