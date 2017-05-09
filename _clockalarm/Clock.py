import logging
import time

from PyQt5.QtCore import pyqtSignal, QThread


class Clock(QThread):
    """Clock emitting ticks with a given periodicity.

    The class extends QThread to allow threading.

    Attributes:
        frequency: The frequency at which the clock emits a tick.
        parent: The parent. Default value is None.
    """
    tick = pyqtSignal('PyQt_PyObject')

    def __init__(self, frequency, parent=None):
        """Default constructor for the Clock class."""
        super(self.__class__, self).__init__(parent)
        self._frequency = frequency
        self.running = True

    def run(self):
        """Start the clock."""
        while self.running:
            self.sleep(self._frequency)
            self.tick.emit(time.time())
            logging.log(1, "clocktread tick(P=" + str(self._frequency) + "s)")

    def stop(self):
        """Stop the clock."""
        self.running = False
