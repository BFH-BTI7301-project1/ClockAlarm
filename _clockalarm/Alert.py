import abc
from abc import abstractmethod

from PyQt5.QtCore import pyqtSignal, QObject


class Alert(QObject):
    __metaclass__ = abc.ABCMeta

    timeout = pyqtSignal('PyQt_PyObject')

    def __init__(self, trigger_time):
        super(Alert, self).__init__()
        """Constructor"""
        self.trigger_time = trigger_time

    def kill(self):
        self.setParent(None)

    @abstractmethod
    def triggered(self):
        """Triggers action"""
        return

    @abstractmethod
    def get_identifier(self):
        """Return an identifier"""
        return str
