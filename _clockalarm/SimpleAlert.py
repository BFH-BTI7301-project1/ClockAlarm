from _clockalarm.Alert import Alert
from _clockalarm.Notification import Notification


class SimpleAlert(Alert):

    def __init__(self, time, message):
        super(SimpleAlert, self).__init__(time)
        self._notification = Notification(message)

    def triggered(self):
        self._notification.display()
