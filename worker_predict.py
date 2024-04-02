from PyQt6.QtCore import QObject, pyqtSlot as Slot, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap
from tensorflow.keras.models import load_model
from keras.preprocessing import image
import numpy as np
import os
from keras.models import load_model
from PIL import Image
import cv2

class WorkerPredict(QObject):

    '''
    Класс который подгружает модели и делает предикты в потоке
    '''

    signal_send_predict = pyqtSignal(str)
    signal_send_probability = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.model = None
        self.load()

    def load(self, model_name='Default'):
        folder_path = './models'
        files_in_folder = os.listdir(folder_path)
        keras_files = [file for file in files_in_folder if file.endswith('.keras')]
        if keras_files:
            keras_files = keras_files[0]
            self.model = load_model(f'../perceptron/models/{keras_files}')
        else:
            print('No keras model')

    def reload_model(self):
        print('При выборе новой модели')
        folder_path = './models'
        files_in_folder = os.listdir(folder_path)
        keras_files = [file for file in files_in_folder if file.endswith('.keras')]
        if keras_files:
            keras_files = keras_files[0]
            self.model = load_model(f'../perceptron/models/{keras_files}')
        else:
            print('No keras model')

    @Slot(np.ndarray)
    def predict_load_model(self, img):
        prediction = self.model.predict(img)
        print(prediction)

        threshold = 0.0001
        min_value = np.min(prediction)
        max_value = np.max(prediction)
        normalized_prediction = (prediction - min_value) / (max_value - min_value)
        normalized_prediction[np.abs(prediction) < threshold] = 0

        self.signal_send_probability.emit(normalized_prediction)
        predict_number = str(prediction.argmax())
        print(predict_number)
        self.signal_send_predict.emit(predict_number)