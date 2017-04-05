from PyQt5.QtGui import QColor, QFont
from PyQt5.QtMultimedia import QSound


class Notification:
    def __init__(self, message):
        self.color = QColor(255, 0, 0)
        self.font = QFont("lucida", 12, QFont.Bold, True)
        self.sound = QSound("resources/sounds/floop.wav")
        self.message = message
