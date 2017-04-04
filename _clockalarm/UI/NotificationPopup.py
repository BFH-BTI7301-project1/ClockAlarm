from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt


class NotificationPopup(QWidget):

    def __init__(self,  notification):

        super(NotificationPopup, self).__init__(flags=Qt.Window)  # Qt.Popup
        self.notification = notification
        self.init_ui()

    def init_ui(self):

        self.setGeometry(100, 100, 300, 40)

        color = self.notification.color
        alpha = 140
        rgba = "{r}, {g}, {b}, {a}".format(r=color.red(), g=color.green(), b=color.blue(), a=alpha)
        lbl = QLabel(self.notification.message, self)
        lbl.setFont(self.notification.font)
        lbl.setStyleSheet("QLabel { color : rgba(" + rgba + "); }")

    def mousePressEvent(self, event):

        self.close()
