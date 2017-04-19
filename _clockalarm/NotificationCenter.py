import threading

from PyQt5.QtCore import QRect

from _clockalarm.UI import NotificationWidget

WIDGET_SIZE = (380, 180)


class NotificationCenter(object):
    _popup_queue = []
    _lock = threading.RLock()

    def __init__(self, screen_geometry):
        super(NotificationCenter, self).__init__()
        self._screen_geometry = screen_geometry

    def display(self, notification):
        """display QWidget"""
        ax = self._screen_geometry.width() - WIDGET_SIZE[0] - 20
        ay = round(self._screen_geometry.height() * 0.1)

        notification.sound.play()

        self._lock.acquire()
        padding = len(self._popup_queue) * (WIDGET_SIZE[1] + 10)
        popup = NotificationWidget(QRect(ax, ay + padding, WIDGET_SIZE[0], WIDGET_SIZE[1]), notification)
        self._popup_queue.insert(0, popup)
        self._popup_queue[0].show()
        self._lock.release()
