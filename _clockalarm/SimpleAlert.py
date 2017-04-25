from _clockalarm import Alert
from _clockalarm import Notification, main


class SimpleAlert(Alert):
    """Simple Alert implementation with text message

    Attributes:
        trigger_time: The time at which the alert is triggered.
        message: The text message to display when the alert is triggered.
        periodicity: frequency in which the alert is displayed, in seconds.
    """

    def __init__(self, trigger_time, message, periodicity=None):
        """Default constructor for the SimpleAlert class."""
        super(SimpleAlert, self).__init__(trigger_time)
        self._notification = Notification(message)
        self.periodicity = periodicity

    def triggered(self):
        """This method does the same as
        :func:`~_clockalarm.Alert.triggered`
        """
        self.timeout.emit(self._notification)

        if not self.periodicity:
            main.app.alert_collection.delete(self.id)
        else:
            main.app.alert_collection.edit(Notification(self.get_identifier()), self.trigger_time + self.periodicity,
                                           self.id, self.periodicity)

    def get_identifier(self):
        """This method does the same as
        :func:`~_clockalarm.Alert.get_identifier`
        """
        return self._notification.message
