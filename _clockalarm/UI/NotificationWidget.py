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

from os.path import join, abspath, dirname

from PyQt5.QtCore import Qt, pyqtSignal, QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel

from _clockalarm.utils.importExportUtils import get_default_config


class NotificationWidget(QWidget):
    """Notification widget

    Attributes:
        geometry: The position and size of the widget on the screen
        notification: The notification
    """
    popup_close = pyqtSignal('PyQt_PyObject')

    def __init__(self, geometry, notification, parent=None):
        """Inits the NotificationWidget with a position and a notification.

        Note:
            By default, the NotificationWidget has no parent
        """
        super(NotificationWidget, self).__init__(parent=parent,
                                                 flags=Qt.Tool | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.parent = parent
        self.notification = notification
        self.init_ui(geometry)

    def init_ui(self, geom):
        """Helper method that sets the style of the NotificationWidget.
        
        Attributes:
            geom: The position and size of the widget on the screen
        """
        self.setGeometry(geom)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)

        """Background Image"""
        im_name = get_default_config("WIDGET_FILE_NAME")
        im_path = join(dirname(dirname(abspath(__file__))), 'resources', 'images',
                       im_name)
        lbl_im = QLabel(self)
        lbl_im.setPixmap(QPixmap(im_path))

        """Notification message"""
        color = self.notification.get_color()
        alpha = get_default_config("WIDGET_TRANSPARENCY", "int")
        rgba = "{r}, {g}, {b}, {a}".format(r=color.red(), g=color.green(), b=color.blue(), a=alpha)
        lbl = QLabel(self.notification.message, self)
        lbl.setAlignment(Qt.AlignVCenter)
        lbl.setWordWrap(True)
        padding_top = get_default_config("WIDGET_TEXT_PADDING_TOP", "int")
        padding_left = get_default_config("WIDGET_TEXT_PADDING_LEFT", "int")
        text_width = get_default_config("WIDGET_TEXT_WIDTH", "int")
        text_height = get_default_config("WIDGET_TEXT_HEIGHT", "int")
        lbl.setGeometry(QRect(padding_left, padding_top, text_width, text_height))
        lbl.setFont(self.notification.get_font())
        lbl.setStyleSheet(
            "QLabel { color : rgba(" + rgba + ")}")

    def mousePressEvent(self, event):
        """Override of :class:~PyQt5.QtWidgets.QWidget.mousePressEvent method"""
        if self.underMouse():
            self.close()
            self.popup_close.emit(self)
