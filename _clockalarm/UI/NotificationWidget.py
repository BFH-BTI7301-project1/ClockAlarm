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

import os

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel


class NotificationWidget(QWidget):
    popup_close = pyqtSignal('PyQt_PyObject')

    def __init__(self, geometry, notification):
        super(NotificationWidget, self).__init__(flags=Qt.Tool | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.notification = notification
        self.init_ui(geometry)

    def init_ui(self, geom):
        self.setGeometry(geom)
        self.setAutoFillBackground(True)
        self.setWindowOpacity(0.8)
        self.setAttribute(Qt.WA_ShowWithoutActivating)

        """Notification message"""
        color = self.notification.get_color()
        alpha = 140
        rgba = "{r}, {g}, {b}, {a}".format(r=color.red(), g=color.green(), b=color.blue(), a=alpha)
        lbl = QLabel(self.notification.message, self)
        lbl.setFont(self.notification.get_font())
        lbl.setStyleSheet(
            "QLabel { color : rgba(" + rgba + ")}")

        """Clock Image"""
        im_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources\\images\\notification_clock.png')
        lbl_im = QLabel(self)
        lbl_im.setPixmap(QPixmap(im_path))

    def mousePressEvent(self, event):
        if self.underMouse():
            self.close()
            self.popup_close.emit(self)
