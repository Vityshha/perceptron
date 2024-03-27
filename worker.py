from PyQt6.QtCore import QObject, pyqtSlot as Slot, pyqtSignal as Signal
from default_perceptron_model import PerceptronDefaultModel
from custom_perceptron_model import PerceptronCusromModel


class Worker(QObject):

    '''
    Класс который запускает обучение персептронов в потоке
    '''

    signal_finished = Signal()
    signal_progress = Signal(int)
    signal_logs = Signal(str)

    def __init__(self):
        super().__init__()
        self.workerDefaultTh = None
        self.workerCustomTh = None
        self.default_model = None
        self.custom_model = None
        self.signal = True

    def WorkerPerceptronDefaultModel(self):
        self.default_model = PerceptronDefaultModel()
        self.default_model.signal_progress.connect(self.epochs)
        self.default_model.signal_loggs.connect(self.logs)

    def WorkerPerseptronCustomModel(self):
        self.custom_model = PerceptronCusromModel()

    def switch_model(self, signal):
        self.signal = signal
        if signal:
            self.WorkerPerceptronDefaultModel()
        else:
            self.WorkerPerseptronCustomModel()

    def start_training(self):
        if self.signal:
            self.default_model.train_model()
        else:
            self.custom_model.train_model()

    @Slot(int)
    def epochs(self, epochs):
        self.signal_progress.emit(epochs)

    @Slot(str)
    def logs(self, logs):
        self.signal_logs.emit(logs)
