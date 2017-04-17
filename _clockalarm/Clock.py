import time

from PyQt5.QtCore import pyqtSignal, QThread


class Clock(QThread):
    tick = pyqtSignal('PyQt_PyObject')
    running = True

    def __init__(self, periodicity, parent=None):
        super(self.__class__, self).__init__(parent)
        self._periodicity = periodicity

    def run(self):
        while self.running:
            self.sleep(self._periodicity)
            self.tick.emit(time.time())
            print("ClockTread: tick(P=" + str(self._periodicity) + "s)")

    def stop(self):
        self.running = False
