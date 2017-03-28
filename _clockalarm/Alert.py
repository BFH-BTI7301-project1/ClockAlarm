from abc import ABC, abstractmethod

class Alert(ABC):

    def __init__(self, time):
        '''constructor'''
        self._time = time

    @abstractmethod
    def triggered(self):
        """Triggers action"""