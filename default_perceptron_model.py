import os

import numpy as np
import pandas as pd
import tensorflow as tf
from matplotlib import pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Activation
from tensorflow.keras.callbacks import LambdaCallback
from PyQt6.QtCore import pyqtSignal as Signal, QObject


class PerceptronDefaultModel(QObject):

    '''
    Класс с реализацией персетрона из библиотеки tensorflow
    '''

    signal_loggs = Signal(str)
    signal_progress = Signal(int)

    def __init__(self):
        super().__init__()
        self.init_data()
        self.init_model()


    def init_data(self):
        self.x_train = None
        self.x_test = None
        self.gray_scale = 255
        (self.x_train, self.y_train), (self.x_test, self.y_test) = tf.keras.datasets.mnist.load_data()
        # Cast the records into float values
        self.x_train = self.x_train.astype('float32')
        self.x_test = self.x_test.astype('float32')

        # normalize image pixel values by dividing
        # by 255
        # self.x_train /= self.gray_scale
        # self.x_test /= self.gray_scale

        # Нам не нужна градация))
        self.x_test[self.x_test != 0] = 1
        self.x_train[self.x_train != 0] = 1
        self.y_train[self.y_train != 0] = 1
        self.y_test[self.y_test != 0] = 1

    def init_model(self):
        self.model = Sequential([

            # reshape 28 row * 28 column data to 28*28 rows
            Flatten(input_shape=(28, 28, 1)),
            # dense layer 1
            Dense(512, activation='relu'),
            # dense layer 2
            Dense(128, activation='relu'),

            Dense(64, activation='relu'),

            Dense(32, activation='relu'),

            Dense(16, activation='relu'),
            # output layer
            Dense(10, activation='softmax'),
        ])

        self.model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    def train_model(self, epochs=20, batch_size=2000, validation_split=0.2):
        epoch_end_callback = LambdaCallback(on_epoch_end=self.print_epoch_end)
        self.model.fit(self.x_train, self.y_train, epochs=epochs, batch_size=batch_size, validation_split=validation_split, callbacks=[epoch_end_callback])
        self.save_model(model_name='Default')

    def print_epoch_end(self, epoch, logs):
        rounded_logs = {metric: round(value, 4) for metric, value in logs.items()}
        self.signal_progress.emit(int(epoch))
        self.signal_loggs.emit(str(rounded_logs))

    def save_model(self, model_name):
        directory = os.path.abspath("../perceptron/models/")
        if not os.path.exists(directory):
            os.makedirs(directory)
        filepath = os.path.join(directory, model_name + ".keras")
        self.model.save(filepath)

