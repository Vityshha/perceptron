import sys

from PyQt6 import QtWidgets
from PyQt6.QtGui import QPixmap, QImage, QColor
import numpy as np
import pandas as pd
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import pyqtSlot as Slot, Qt, QRect, QRectF
from PyQt6.QtGui import QIntValidator
import cv2
from PyQt6.QtCore import pyqtSignal as Signal
from matplotlib import pyplot as plt

from gui.perceptron_gui import Ui_MainWindow



class View(QMainWindow, Ui_MainWindow):

    '''
    Класс отвечающий за GUI
    '''

    signal_image = Signal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_connect()
        self.init_image()
        self.set_number()
        self.progress_bar()
        self.validator()


    def init_connect(self):
        self.ui.ch_default.clicked.connect(self.switch_settings)
        self.ui.cb_sigmoid.clicked.connect(lambda: self.ui.cb_th.setChecked(False))
        self.ui.cb_sigmoid.clicked.connect(lambda: self.ui.cb_relu.setChecked(False))
        self.ui.cb_th.clicked.connect(lambda: self.ui.cb_sigmoid.setChecked(False))
        self.ui.cb_th.clicked.connect(lambda: self.ui.cb_relu.setChecked(False))
        self.ui.cb_relu.clicked.connect(lambda: self.ui.cb_sigmoid.setChecked(False))
        self.ui.cb_relu.clicked.connect(lambda: self.ui.cb_th.setChecked(False))
        self.ui.btn_clear.clicked.connect(self.ui.graphicsView.clear)
        self.ui.btn_clear.clicked.connect(self.set_number)

    def init_image(self):
        path = ['./gui/sigmoid.png', './gui/relu.png', './gui/th.png']

        sigmoid_img = QPixmap(path[0])
        relu_img = QPixmap(path[1])
        th_img = QPixmap(path[2])

        self.ui.sigmoid.setPixmap(sigmoid_img)
        self.ui.relu.setPixmap(relu_img)
        self.ui.th.setPixmap(th_img)
        self.ui.sigmoid.setScaledContents(True)
        self.ui.relu.setScaledContents(True)
        self.ui.th.setScaledContents(True)


    def switch_settings(self):
        if self.ui.ch_default.isChecked():
            self.ui.cb_relu.setEnabled(False)
            self.ui.cb_th.setEnabled(False)
            self.ui.cb_sigmoid.setEnabled(False)
            self.ui.model_name.setEnabled(False)
            self.ui.num_layers.setEnabled(False)
            self.ui.num_neuron.setEnabled(False)
            self.ui.num_epochs.setEnabled(False)
            self.ui.model_name.setText('Default')

            self.ui.cb_sigmoid.setChecked(True)
            self.ui.cb_th.setChecked(False)
            self.ui.cb_relu.setChecked(False)

            self.ui.num_layers.setText('3')
            self.ui.num_neuron.setText("1:256, 2:128, 3:10")
            self.ui.num_epochs.setText('10')

            self.ui.progress.setMaximum(9)
        else:
            self.ui.cb_relu.setEnabled(True)
            self.ui.cb_th.setEnabled(True)
            self.ui.cb_sigmoid.setEnabled(True)
            self.ui.model_name.setEnabled(True)
            self.ui.num_layers.setEnabled(True)
            self.ui.num_neuron.setEnabled(True)
            self.ui.num_epochs.setEnabled(True)

            self.ui.model_name.clear()
            self.ui.num_layers.clear()
            self.ui.num_neuron.clear()
            self.ui.num_epochs.clear()

    def validator(self):
        onlyInt = QIntValidator()
        # onlyInt.setRange(0, 1000)
        # self.ui.num_layers.setValidator(onlyInt)
        # self.ui.num_neuron.setValidator(onlyInt)

    def set_number(self, number=0):
        self.ui.predict_number.display(number)

    @Slot(int)
    def progress_bar(self, progress=0):
        self.ui.progress.setValue(progress)

    def show_logg_train(self, logs):
        old_text = self.ui.logs.text()
        new_text = old_text + '\n' + logs
        self.ui.logs.setText(new_text)

    def clear_logg_train(self):
        self.ui.progress.setValue(0)
        self.ui.logs.clear()

    def set_probability(self, list_prob):
        self.ui.prob_0.setText(str(list_prob[0][0]))
        self.ui.prob_1.setText(str(list_prob[0][1]))
        self.ui.prob_2.setText(str(list_prob[0][2]))
        self.ui.prob_3.setText(str(list_prob[0][3]))
        self.ui.prob_4.setText(str(list_prob[0][4]))
        self.ui.prob_5.setText(str(list_prob[0][5]))
        self.ui.prob_6.setText(str(list_prob[0][6]))
        self.ui.prob_7.setText(str(list_prob[0][7]))
        self.ui.prob_8.setText(str(list_prob[0][8]))
        self.ui.prob_9.setText(str(list_prob[0][9]))

    @Slot()
    def image_preprocess(self):
        image = QImage(self.ui.graphicsView.grab().toImage())
        width = image.width()
        height = image.height()

        if width > height:
            scaled_image = image.scaledToWidth(28)
        else:
            scaled_image = image.scaledToHeight(28)

        array = np.zeros((28, 28), dtype=int)

        for y in range(28):
            for x in range(28):
                pixel_color = scaled_image.pixelColor(x, y)

                if pixel_color.black().real == 255:
                    array[y, x] = 1

        # Нормализация данных
        fig, ax = plt.subplots()
        ax.imshow(array, aspect='auto')
        plt.show()
        normalized_image = array.astype(np.float32)
        normalized_image = np.expand_dims(normalized_image, axis=0)

        df = pd.DataFrame(normalized_image[0])
        df.to_excel(excel_writer='predict.xlsx', index=False)
        self.signal_image.emit(normalized_image)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = View()
    win.show()
    sys.exit(app.exec())