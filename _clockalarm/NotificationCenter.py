# ClockAlarm is a cross-platform alarm manager
# Copyright (C) 2017  Loïc Charrière, Samuel Gauthier
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import math
import threading
from collections import deque
from os.path import dirname, abspath

import pygame
from PyQt5 import QtMultimedia
from PyQt5.QtCore import QRect

from _clockalarm.UI.NotificationWidget import NotificationWidget

WIDGET_SIZE = (380, 180)
PADDING = 10

base_path = dirname(dirname(abspath(__file__)))


class NotificationCenter(object):
    def __init__(self, screen_geometry, parent=None):
        super(NotificationCenter, self).__init__()
        self.parent = parent
        self._screen_geometry = screen_geometry
        self._max_popups = math.floor((screen_geometry.height() * 0.9) /
                                      (WIDGET_SIZE[1] + PADDING))

        self._popup_queue = deque([])
        self._displayed_popups = []
        self._lock = threading.RLock()

        self.ax = self._screen_geometry.width() - WIDGET_SIZE[0] - 20
        self.ay = round(self._screen_geometry.height() * 0.1)

        self.player = QtMultimedia.QMediaPlayer()

    def add_to_queue(self, notification):
        self._lock.acquire()
        self._popup_queue.append(notification)
        self._lock.release()
        self.refresh()

    def refresh(self):
        if len(self._displayed_popups) >= self._max_popups:
            return

        i = 0
        for popup in self._displayed_popups:
            popup.setGeometry(QRect(self.ax,
                                    self.ay + i * (WIDGET_SIZE[1] + PADDING),
                                    WIDGET_SIZE[0], WIDGET_SIZE[1]))
            i += 1

        self._lock.acquire()
        if len(self._popup_queue) == 0:
            self._lock.release()
        else:
            new_notification = self._popup_queue.popleft()
            self._lock.release()
            self.display_popup(QRect(self.ax,
                                     self.ay + i * (WIDGET_SIZE[1] + PADDING),
                                     WIDGET_SIZE[0], WIDGET_SIZE[1]),
                               new_notification)

    def display_popup(self, geom: QRect, notification):
        if not self.parent.MUTE:
            try:
                notification.get_sound().play()
            except pygame.error:
                logging.log(1, "unavailable audio device")

        popup = NotificationWidget(geom, notification)

        self._displayed_popups.append(popup)
        popup.popup_close.connect(self.close_popup)
        popup.show()

    def close_popup(self, popup: NotificationWidget):
        self._displayed_popups.remove(popup)
        self.refresh()
