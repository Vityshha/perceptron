from PyQt6.QtCore import QObject


class PerceptronCusromModel(QObject):

    def train_model(self):
        print('Training Custom Perceptron')