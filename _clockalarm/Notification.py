from PyQt5.QtGui import QColor, QFont
from PyQt5.QtMultimedia import QSound


class Notification:

    def __init__(self, message):
        self.color = QColor(80, 80, 200)
        self.font = QFont("Helvetica")
        self.sound = QSound("resources/sounds/floop.wav")
        self.message = message
