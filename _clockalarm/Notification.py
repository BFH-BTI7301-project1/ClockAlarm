import os

from PyQt5 import QtMultimedia
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import QUrl


class Notification(object):
    def __init__(self, message):
        self.color = QColor(255, 0, 0)
        self.font = QFont("lucida", 12, QFont.Bold, True)
        _sound_path = "C:/Users/Loic/Documents/BFH/BA4_Project1/ClockAlarm/_clockalarm/resources/sounds/floop.wav"
        print(os.path.dirname(os.path.abspath(__file__)))
        self.sound = QtMultimedia.QMediaContent(QUrl(_sound_path))
        self.message = message
