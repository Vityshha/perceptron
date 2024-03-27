import sys
from PyQt6 import QtWidgets
from view import View
from worker import Worker
from worker_predict import WorkerPredict
from PyQt6.QtCore import QObject, QThread


class Controller(QObject):
    def __init__(self):
        super().__init__()
        self.view = View()
        self.worker = Worker()
        self.worker_predict = WorkerPredict()
        self.init_threads()
        self.init_connects()


    def init_threads(self):
        self.thWorker = QThread()
        self.thWorkerPredict = QThread()

        self.worker.moveToThread(self.thWorker)
        self.thWorker.start()

        self.worker_predict.moveToThread(self.thWorkerPredict)
        self.thWorkerPredict.start()

    def init_connects(self):
        self.view.ui.ch_default.toggled.connect(self.worker.switch_model)
        self.view.ui.btn_start_train.clicked.connect(self.view.clear_logg_train)
        self.view.ui.btn_start_train.clicked.connect(self.worker.start_training)
        self.view.ui.tabWidget.currentChanged.connect(self.worker_predict.reload_model)

        self.worker.signal_progress.connect(self.view.progress_bar)
        self.worker.signal_logs.connect(self.view.show_logg_train)

        self.view.ui.graphicsView.signal_end_paint.connect(self.view.image_preprocess)
        self.view.signal_image.connect(self.worker_predict.predict_load_model)
        self.worker_predict.signal_send_predict.connect(self.view.set_number)
        self.worker_predict.signal_send_probability.connect(self.view.set_probability)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.view.show()
    sys.exit(app.exec())

