from abc import ABC, abstractmethod
import time
import threading

PERIODICITY = 1  # frequency of time checks

lock = threading.RLock()  # unused for the moment


class Alert(ABC):

    def __init__(self, trigger_time):
        """Constructor"""
        self._trigger_time = trigger_time
        self._periodic_time_check()

    @abstractmethod
    def triggered(self):
        """Triggers action"""

    def _periodic_time_check(self):
        """Periodically checks if alert must be triggered"""
        if time.time() < self._trigger_time:
            threading.Timer(PERIODICITY, self._periodic_time_check).start()
        else:
            self.triggered()
