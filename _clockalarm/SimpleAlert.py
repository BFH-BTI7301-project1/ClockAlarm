from _clockalarm import Alert
from _clockalarm import Notification


class SimpleAlert(Alert):
    def __init__(self, trigger_time, message):
        super(SimpleAlert, self).__init__(trigger_time)
        self._notification = Notification(message)

    def triggered(self):
        self.timeout.emit(self._notification)

    def get_identifier(self):
        return self._notification.message
