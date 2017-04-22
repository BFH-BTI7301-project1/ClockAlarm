from _clockalarm import Alert
from _clockalarm import Notification


class SimpleAlert(Alert):
    """Simple Alert implementation with text message

    Attributes:
        trigger_time: The time at which the alert is triggered.
        message: The text message to display when the alert is triggered.
    """

    def __init__(self, trigger_time, message):
        """Default constructor for the SimpleAlert class."""
        super(SimpleAlert, self).__init__(trigger_time)
        self._notification = Notification(message)

    def triggered(self):
        """This method does the same as
        :func:`~_clockalarm.Alert.triggered`
        """
        self.timeout.emit(self._notification)

    def get_identifier(self):
        """This method does the same as
        :func:`~_clockalarm.Alert.get_identifier`
        """
        return self._notification.message
