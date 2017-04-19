import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel


class NotificationWidget(QWidget):
    def __init__(self, geometry, notification):
        super(NotificationWidget, self).__init__(flags=Qt.Popup)
        self.notification = notification
        self.init_ui(geometry)

    def init_ui(self, geom):
        self.setGeometry(geom)
        self.setAutoFillBackground(True)
        self.setWindowOpacity(0.8)

        '''Notification message'''
        color = self.notification.color
        alpha = 140
        rgba = "{r}, {g}, {b}, {a}".format(r=color.red(), g=color.green(), b=color.blue(), a=alpha)
        lbl = QLabel(self.notification.message, self)
        lbl.setFont(self.notification.font)
        lbl.setStyleSheet(
            "QLabel { color : rgba(" + rgba + ")}")

        '''Clock Image'''
        im_path = os.path.join(os.path.dirname(__file__), '..\\resources\\images\\notification_clock.png')
        lbl_im = QLabel(self)
        lbl_im.setPixmap(QPixmap(im_path))

    def mousePressEvent(self, event):
        self.close()
