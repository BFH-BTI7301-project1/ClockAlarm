from PyQt5.QtGui import QColor, QFont
from PyQt5.QtMultimedia import QSound


class Notification:

    def __init__(self, message):
        self._color = QColor(80, 80, 200)
        self._font = QFont("Helvetica")
        self._sound = QSound("resources/sounds/floop.wav")
        self._message = message

    def display(self):
        """display QWidget"""
        print("display notification:\n" + self._message)
