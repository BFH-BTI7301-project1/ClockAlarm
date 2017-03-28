from abc import ABC, abstractmethod
from threading import Thread


class Alert(ABC):

    def __init__(self, time):
        '''constructor'''
        self._time = time
        self._thread = Thread()

    @abstractmethod
    def triggered(self):
        """Triggers action"""
