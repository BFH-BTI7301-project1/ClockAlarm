import abc
from abc import abstractmethod

from PyQt5.QtCore import pyqtSignal, QObject


class Alert(QObject):
    """Abstract Alert class representing alerts.
    
    Attributes:
        trigger_time: The trigger time of the alert.
        id: The identification number of the alert in the alert. Set up when added to the database.
    """
    __metaclass__ = abc.ABCMeta

    timeout = pyqtSignal('PyQt_PyObject')

    def __init__(self, trigger_time):
        """Inits Alert class with the trigger time given in arguments."""
        super(Alert, self).__init__()
        self.trigger_time = trigger_time
        self.id = None

    def kill(self):
        """Kills the Alert.

        Removes the parent of the alert.
        """
        self.setParent(None)

    @abstractmethod
    def triggered(self):
        """Triggers the alert action."""
        return

    @abstractmethod
    def get_identifier(self):
        """Get the alert identifier.
        
        Returns:
            The identifier of the alert.
        """
        return str
