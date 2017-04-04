from _clockalarm.UI import NotificationPopup
from PyQt5.QtWidgets import QWidget


class NotificationCenter:

    def __init__(self):
        super(NotificationCenter, self).__init__()
        self.popup_queue = []
        self.w = QWidget()
        self.w.show()

    def display(self, notification):
        """display QWidget"""
        print(notification.message)

        popup = NotificationPopup(notification)
        self.popup_queue.append(popup)
        self.popup_queue[0].show()
