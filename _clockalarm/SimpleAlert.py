from _clockalarm.Alert import Alert
from _clockalarm.Notification import Notification


class SimpleAlert(Alert):
    def __init__(self, trigger_time, message, notification_center):
        super(SimpleAlert, self).__init__(trigger_time)
        self._notification = Notification(message)
        self.timeout.connect(notification_center.display)

    def triggered(self):
        self.timeout.emit(self._notification)
