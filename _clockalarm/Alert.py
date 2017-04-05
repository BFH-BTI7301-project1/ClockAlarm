import abc
import threading
import time
from abc import abstractmethod

from PyQt5.QtCore import pyqtSignal, QObject

PERIODICITY = 1  # frequency of time checks


class Alert(QObject):
    __metaclass__ = abc.ABCMeta

    timeout = pyqtSignal('PyQt_PyObject')

    def __init__(self, trigger_time):
        super(Alert, self).__init__()
        """Constructor"""
        self._trigger_time = trigger_time
        self._periodic_time_check()

    @abstractmethod
    def triggered(self):
        """Triggers action"""
        return

    def _periodic_time_check(self):
        """Periodically checks if alert must be triggered"""
        if time.time() < self._trigger_time:
            threading.Timer(PERIODICITY, self._periodic_time_check).start()
        else:
            self.triggered()
