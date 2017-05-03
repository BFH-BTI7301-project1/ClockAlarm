import time
import logging

from PyQt5.QtCore import pyqtSignal, QThread


class Clock(QThread):
    tick = pyqtSignal('PyQt_PyObject')

    def __init__(self, periodicity, parent=None):
        super(self.__class__, self).__init__(parent)
        self._periodicity = periodicity
        self.running = True

    def run(self):
        while self.running:
            self.sleep(self._periodicity)
            self.tick.emit(time.time())
            logging.log(1, "clocktread tick(P=" + str(self._periodicity) + "s)")

    def stop(self):
        self.running = False
