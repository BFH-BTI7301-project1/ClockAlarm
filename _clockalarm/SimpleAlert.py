from _clockalarm.Alert import Alert
from _clockalarm.Notification import Notification


class SimpleAlert(Alert):

    def __init__(self, trigger_time, message, notification_center):
        super(SimpleAlert, self).__init__(trigger_time)
        self._notification = Notification(message)
        self._notification_center = notification_center

    def triggered(self):
        self._notification_center.display(self._notification)
