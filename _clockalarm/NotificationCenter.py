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

import pygame
from PyQt5.QtCore import QRect

from _clockalarm.UI.NotificationWidget import NotificationWidget

WIDGET_SIZE = (350, 215)  # dimensions of the notification widgets in pixels
PADDING = 10  # space between the widgets in pixels


class NotificationCenter(object):
    """Class handling the display of the Notification Widgets

    Receives the notifications to display and add it to a queue.
    If there is free slot on the UI display area, pop the queue and display the notification.
    If the user clicks on the widget, closes it and compacts the remaining widgets.

    """

    def __init__(self, screen_geometry, parent=None):
        """Default NotificationCenter constructor

        Initialize the waiting queue and the list of displayed popups.
        Compute the maximum number of popup one can display on the screen.

        Attributes:
            screen_geometry: dimensions of the screen displaying the app
            parent: parent class for NotificationCenter (usually main.App object)

        """
        super(NotificationCenter, self).__init__()
        self.parent = parent
        self._screen_geometry = screen_geometry
        self._max_popups = math.floor((screen_geometry.height() * 0.9) / (
            WIDGET_SIZE[1] + PADDING))  # number of widget one can display with the given screen geometry

        self._popup_queue = deque([])  # list as a queue
        self._displayed_popups = []
        self._lock = threading.RLock()  # lock to protect the queue

        self.ax = self._screen_geometry.width() - WIDGET_SIZE[0] - 20  # x coordinate of the notification zone in pixels
        self.ay = round(self._screen_geometry.height() * 0.1)  # y coordinate of the notification zone in pixels

    def add_to_queue(self, notification):
        """Add a new notification to the queue

        The notification will wait till there is a free sport in the display zone

        Attributes:
            notification (Notification): The notification to add to enqueue

        """
        self._lock.acquire()
        self._popup_queue.append(notification)
        self._lock.release()
        self.refresh()  # check if it's possible to directly display the notification

    def refresh(self):
        """Refresh the display off notifications in the display zone

        Compact the remaining notifications in the display zone, if there is free slots, pop the notification queue and
        display the popup.

        """
        if len(self._displayed_popups) >= self._max_popups:  # display zone is full
            return

        i = 0  # position of the popup in the display zone
        """Compact the remaining popups"""
        for popup in self._displayed_popups:
            popup.setGeometry(QRect(self.ax,
                                    self.ay + i * (WIDGET_SIZE[1] + PADDING),
                                    WIDGET_SIZE[0], WIDGET_SIZE[1]))
            i += 1

        """Add new popups"""
        self._lock.acquire()
        if len(self._popup_queue) == 0:  # empty queue
            self._lock.release()
        else:  # notification waiting in queue
            new_notification = self._popup_queue.popleft()
            self._lock.release()
            self.display_popup(QRect(self.ax,
                                     self.ay + i * (WIDGET_SIZE[1] + PADDING),
                                     WIDGET_SIZE[0], WIDGET_SIZE[1]),
                               new_notification)

    def display_popup(self, geom: QRect, notification):
        """Display a QWidget popup

        Play a sound if the program isn't muted

        Attributes:
            geom(QRect): position and size of the widget on the screen
            notification (Notification): the notification to display

        """
        if not self.parent.MUTE:
            try:
                notification.get_sound().play()
            except pygame.error:
                logging.log(1, "unavailable audio device")  # no audio device found by pygame on the computer

        popup = NotificationWidget(geom, notification)

        self._displayed_popups.append(popup)
        popup.popup_close.connect(
            self.close_popup)  # to be able to update the NotificationCenter when the popup is closed
        popup.show()

    def close_popup(self, popup: NotificationWidget):
        """Triggered by a NotificationWidget when closed

        Remove the popup from the list and refresh the display zone.

        Attributes:
            popup: The NotificationWidget to remove from the display zone

        """
        self._displayed_popups.remove(popup)
        self.refresh()
